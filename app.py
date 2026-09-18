"""NUMBERIN — Streamlit UI. Math lives in engine.py."""

from __future__ import annotations

import hashlib
import io
import re
import textwrap
from datetime import date, datetime, time, timezone
from urllib.parse import quote

import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

from engine import (
    EDEN_LUNAR_YEARS,
    KARMIC,
    KARMIC_NOTE,
    LATIN_CIPHERS,
    LUNAR_YEAR_DAYS,
    SOLAR_YEAR_DAYS,
    angel_read,
    depth_lines,
    eden_span,
    extract_digits,
    letters_latin,
    life_path,
    meaning,
    moon_phase,
    moon_svg,
    name_profile,
    personal_cycles,
    reduce_number,
    reduce_trace,
    run_latin_cipher,
    script_readings,
)

# Python date floor is year 1. BC lives in Moon of Eden as a count, not a date.
DATE_FLOOR = date(1, 1, 1)
DATE_CEILING = date(9999, 12, 31)

st.set_page_config(page_title="NUMBERIN", page_icon="✦", layout="wide")

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at 18% 0%, #1a1408 0%, #050506 42%, #000 100%);
  color: #f3e6c4;
}
.block-container {padding-top: 1rem; max-width: 1180px;}
h1 {
  font-weight: 900;
  letter-spacing: .22em;
  color: #f5d76e;
  text-shadow: 0 0 6px #f5d76e, 0 0 22px #c9a227, 0 0 40px #00e5ff55;
}
.seal {
  font-size: 1.25rem;
  letter-spacing: .32rem;
  color: #00e5ff;
  text-shadow: 0 0 10px #00e5ff;
}
[data-testid="stSidebar"] {
  background: #0a0a0c;
  border-right: 1px solid #c9a22755;
}
[data-testid="stHeader"] {background: rgba(0,0,0,.85);}
textarea {
  background: #0b0b0d !important;
  color: #f5d76e !important;
  border: 1px solid #c9a227 !important;
  box-shadow: 0 0 16px rgba(0,229,255,.15);
}
[data-testid="stMetricValue"] {color: #f5d76e;}
div[data-baseweb="tab-list"] {border-bottom: 1px solid #c9a22744;}

/* Dark-mode buttons: dark fill, neon edge, no washed-out gold */
div.stButton > button,
div.stDownloadButton > button,
div.stFormSubmitButton > button,
[data-testid="stSidebar"] button,
button[kind="primary"],
button[kind="secondary"],
[data-testid="baseButton-primary"],
[data-testid="baseButton-secondary"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border: 1.5px solid #00e5ff !important;
  font-weight: 800 !important;
  letter-spacing: .04em;
  text-shadow: 0 0 8px #00e5ff88;
  box-shadow: 0 0 14px rgba(0,229,255,.28);
}
div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stFormSubmitButton > button:hover,
[data-testid="stSidebar"] button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
  background: #00222c !important;
  color: #f8f4e6 !important;
  border-color: #f5d76e !important;
  box-shadow: 0 0 18px rgba(245,215,110,.35);
}
div.stButton > button:focus,
div.stDownloadButton > button:focus {
  outline: 2px solid #00e5ff !important;
  outline-offset: 2px;
}

/* Sidebar copy: kill Streamlit's gray-on-black */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color: #ead9a4 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5 {
  color: #f5d76e !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
  color: #c9dbe3 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
  color: #7ef6ff !important;
}
.stCaption, [data-testid="stCaptionContainer"] {
  color: #d7c48a !important;
}

/* The little arrow that opens / closes the sidebar */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stBaseButton-header"],
[data-testid="stBaseButton-headerNoPadding"],
[data-testid="baseButton-header"],
[data-testid="baseButton-headerNoPadding"],
button[kind="header"],
button[kind="headerNoPadding"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border: 1.5px solid #00e5ff !important;
  box-shadow: 0 0 12px rgba(0,229,255,.35) !important;
}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stExpandSidebarButton"] svg,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stBaseButton-header"] svg,
[data-testid="stBaseButton-headerNoPadding"] svg,
button[kind="header"] svg,
button[kind="headerNoPadding"] svg {
  fill: #00e5ff !important;
  color: #00e5ff !important;
  stroke: #00e5ff !important;
}
</style>
""",
    unsafe_allow_html=True,
)

BIBLE_RE = re.compile(
    r"\b(?:(?P<book>(?:[1-3]\s*)?[A-Za-z][A-Za-z]+(?:\s+[A-Za-z]+)?))\s+"
    r"(?P<ch>\d{1,3})\s*:\s*(?P<vs>\d{1,3})",
    re.I,
)
DATE_ISO = re.compile(r"\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b")
DATE_US = re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")
TIME_RE = re.compile(
    r"\b([01]?\d|2[0-3])[:.;]([0-5]\d)(?:\s*([AaPp]\.?[Mm]\.?))?\b"
)
COORD_RE = re.compile(r"(-?\d{1,3}\.\d+)\s*[,/ ]\s*(-?\d{1,3}\.\d+)")
PLACE_HINT = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,?\s*(FL|Florida|TX|Texas|CA|NY|OH|GA|NC|SC|MI|Michigan)\b",
    re.I,
)
KNOWN_COORDS = {
    "naples fl": (26.1420, -81.7948, "Naples, Florida, US"),
    "naples florida": (26.1420, -81.7948, "Naples, Florida, US"),
    "naples": (26.1420, -81.7948, "Naples, Florida, US"),
    "cape coral": (26.5628, -81.9495, "Cape Coral, Florida, US"),
    "cape coral fl": (26.5628, -81.9495, "Cape Coral, Florida, US"),
    "mcallen": (26.2034, -98.2300, "McAllen, Texas, US"),
    "mcallen tx": (26.2034, -98.2300, "McAllen, Texas, US"),
    "canton mi": (42.3087, -83.4822, "Canton, Michigan, US"),
    "canton michigan": (42.3087, -83.4822, "Canton, Michigan, US"),
    "canton": (42.3087, -83.4822, "Canton, Michigan, US"),
}
MONTHS = {
    m.lower(): i
    for i, m in enumerate(
        "January February March April May June July August September October November December".split(),
        1,
    )
}

LANG_FILTER = {
    "Auto": None,
    "English (Latin)": "latin",
    "Sanskrit": "sanskrit",
    "Greek": "greek",
    "Coptic": "coptic",
    "Aramaic (Square)": "square",
    "Aramaic (Syriac)": "syriac",
    "Hebrew": "hebrew",
    "Arabic": "arabic",
    "Russian": "russian",
    "Ukrainian": "ukrainian",
    "Georgian": "georgian",
    "Armenian": "armenian",
}

# Longest-token-first Latin → script. Enough to make Erin / Sophia / Naples count.
LATIN_TO_SCRIPT = {
    "Russian": {
        "shch": "щ", "yo": "ё", "zh": "ж", "kh": "х", "ts": "ц", "ch": "ч",
        "sh": "ш", "yu": "ю", "ya": "я", "ye": "е",
        "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "г",
        "h": "х", "i": "и", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н",
        "o": "о", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у",
        "v": "в", "w": "в", "x": "кс", "y": "ы", "z": "з",
    },
    "Ukrainian": {
        "shch": "щ", "zh": "ж", "kh": "х", "ts": "ц", "ch": "ч", "sh": "ш",
        "yu": "ю", "ya": "я", "ye": "є", "yi": "ї",
        "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "г",
        "h": "г", "i": "і", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н",
        "o": "о", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у",
        "v": "в", "w": "в", "x": "кс", "y": "и", "z": "з",
    },
    "Greek": {
        "th": "θ", "ph": "φ", "ch": "χ", "ps": "ψ", "kh": "χ",
        "a": "α", "b": "β", "c": "κ", "d": "δ", "e": "ε", "f": "φ", "g": "γ",
        "h": "η", "i": "ι", "j": "ι", "k": "κ", "l": "λ", "m": "μ", "n": "ν",
        "o": "ο", "p": "π", "q": "κ", "r": "ρ", "s": "σ", "t": "τ", "u": "υ",
        "v": "β", "w": "ω", "x": "ξ", "y": "υ", "z": "ζ",
    },
    "Coptic": {
        "th": "ⲑ", "ph": "ⲫ", "ch": "ⲭ", "ps": "ⲯ", "sh": "ϣ",
        "a": "ⲁ", "b": "ⲃ", "c": "ⲕ", "d": "ⲇ", "e": "ⲉ", "f": "ϥ", "g": "ⲅ",
        "h": "ϩ", "i": "ⲓ", "j": "ϫ", "k": "ⲕ", "l": "ⲗ", "m": "ⲙ", "n": "ⲛ",
        "o": "ⲟ", "p": "ⲡ", "q": "ⲕ", "r": "ⲣ", "s": "ⲥ", "t": "ⲧ", "u": "ⲩ",
        "v": "ⲃ", "w": "ⲱ", "x": "ⲝ", "y": "ⲓ", "z": "ⲍ",
    },
    "Hebrew": {
        "sh": "ש", "ch": "ח", "ts": "צ", "th": "ת", "kh": "כ",
        "a": "א", "b": "ב", "c": "כ", "d": "ד", "e": "א", "f": "פ", "g": "ג",
        "h": "ה", "i": "י", "j": "י", "k": "כ", "l": "ל", "m": "מ", "n": "נ",
        "o": "ו", "p": "פ", "q": "ק", "r": "ר", "s": "ס", "t": "ט", "u": "ו",
        "v": "ו", "w": "ו", "x": "קס", "y": "י", "z": "ז",
    },
    "Aramaic (Square)": {
        "sh": "ש", "ch": "ח", "ts": "צ", "th": "ת", "kh": "כ",
        "a": "א", "b": "ב", "c": "כ", "d": "ד", "e": "א", "f": "פ", "g": "ג",
        "h": "ה", "i": "י", "j": "י", "k": "כ", "l": "ל", "m": "מ", "n": "נ",
        "o": "ו", "p": "פ", "q": "ק", "r": "ר", "s": "ס", "t": "ט", "u": "ו",
        "v": "ו", "w": "ו", "x": "קס", "y": "י", "z": "ז",
    },
    "Aramaic (Syriac)": {
        "sh": "ܫ", "ch": "ܚ", "ts": "ܨ", "th": "ܬ",
        "a": "ܐ", "b": "ܒ", "c": "ܟ", "d": "ܕ", "e": "ܐ", "f": "ܦ", "g": "ܓ",
        "h": "ܗ", "i": "ܝ", "j": "ܝ", "k": "ܟ", "l": "ܠ", "m": "ܡ", "n": "ܢ",
        "o": "ܘ", "p": "ܦ", "q": "ܩ", "r": "ܪ", "s": "ܣ", "t": "ܛ", "u": "ܘ",
        "v": "ܘ", "w": "ܘ", "x": "ܣ", "y": "ܝ", "z": "ܙ",
    },
    "Arabic": {
        "sh": "ش", "kh": "خ", "th": "ث", "dh": "ذ", "gh": "غ",
        "a": "ا", "b": "ب", "c": "ك", "d": "د", "e": "ا", "f": "ف", "g": "ج",
        "h": "ه", "i": "ي", "j": "ج", "k": "ك", "l": "ل", "m": "م", "n": "ن",
        "o": "و", "p": "ب", "q": "ق", "r": "ر", "s": "س", "t": "ت", "u": "و",
        "v": "و", "w": "و", "x": "كس", "y": "ي", "z": "ز",
    },
    "Sanskrit": {
        "kh": "ख", "gh": "घ", "ch": "च", "jh": "झ", "th": "थ", "dh": "ध",
        "ph": "फ", "bh": "भ", "sh": "श", "ss": "ष",
        "a": "अ", "b": "ब", "c": "क", "d": "द", "e": "ए", "f": "फ", "g": "ग",
        "h": "ह", "i": "इ", "j": "ज", "k": "क", "l": "ल", "m": "म", "n": "न",
        "o": "ओ", "p": "प", "q": "क", "r": "र", "s": "स", "t": "त", "u": "उ",
        "v": "व", "w": "व", "x": "क्ष", "y": "य", "z": "ज",
    },
    "Georgian": {
        "a": "ა", "b": "ბ", "c": "ც", "d": "დ", "e": "ე", "f": "ფ", "g": "გ",
        "h": "ჰ", "i": "ი", "j": "ჯ", "k": "კ", "l": "ლ", "m": "მ", "n": "ნ",
        "o": "ო", "p": "პ", "q": "ქ", "r": "რ", "s": "ს", "t": "ტ", "u": "უ",
        "v": "ვ", "w": "ვ", "x": "ხ", "y": "ი", "z": "ზ",
    },
    "Armenian": {
        "a": "ա", "b": "բ", "c": "ց", "d": "դ", "e": "ե", "f": "ֆ", "g": "գ",
        "h": "հ", "i": "ի", "j": "ջ", "k": "կ", "l": "լ", "m": "մ", "n": "ն",
        "o": "ո", "p": "պ", "q": "ք", "r": "ր", "s": "ս", "t": "տ", "u": "ու",
        "v": "վ", "w": "վ", "x": "խ", "y": "յ", "z": "զ",
    },
}

TRACKS = {
    "Genesis": "1FH-q0I1fJY",
    "So Heavy I Fell Through the Earth": "eLo1pQ45XYs",
    "Alien": "hky6cifwWyo",
    "Cellophane": "YkLjqFpBh84",
    "The First Time Ever I Saw Your Face": "VqW-eO3jTVU",
}


def reading_stamp() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "when": now,
        "iso": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "date": now.date().isoformat(),
        "clock": now.strftime("%H:%M:%S"),
    }


def seed_sigil(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    glyphs = "✦✧✺❋❖☼☾☿♀♁♂♃♄☥ॐᛟᚠ"
    return "".join(glyphs[int(h[i : i + 2], 16) % len(glyphs)] for i in range(0, 16, 2))


def detect_dates(text: str) -> list[date]:
    found: list[date] = []
    mname = re.search(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(\d{1,2})(?:st|nd|rd|th)?(?:,)?\s+(\d{4})\b",
        text,
        re.I,
    )
    if mname:
        try:
            found.append(date(int(mname.group(3)), MONTHS[mname.group(1).lower()], int(mname.group(2))))
        except ValueError:
            pass
    for y, m, d in DATE_ISO.findall(text):
        try:
            found.append(date(int(y), int(m), int(d)))
        except ValueError:
            pass
    for a, b, c in DATE_US.findall(text):
        year = int(c)
        if year < 100:
            year += 1900 if year > 30 else 2000
        try:
            found.append(date(year, int(a), int(b)))
        except ValueError:
            try:
                found.append(date(year, int(b), int(a)))
            except ValueError:
                pass
    out, seen = [], set()
    for d in found:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def detect_times(text: str) -> list[time]:
    found: list[time] = []
    seen = set()
    for hh, mm, ampm in TIME_RE.findall(text):
        hour = int(hh)
        minute = int(mm)
        if ampm:
            tag = re.sub(r"[^A-Za-z]", "", ampm).upper()
            if tag == "PM" and hour < 12:
                hour += 12
            if tag == "AM" and hour == 12:
                hour = 0
        try:
            t = time(hour, minute)
        except ValueError:
            continue
        if t not in seen:
            seen.add(t)
            found.append(t)
    return found


def detect_coords(text: str) -> tuple[float, float] | None:
    m = COORD_RE.search(text)
    if not m:
        return None
    lat, lon = float(m.group(1)), float(m.group(2))
    if abs(lat) <= 90 and abs(lon) <= 180:
        return lat, lon
    return None


def detect_place(text: str) -> str | None:
    m = PLACE_HINT.search(text)
    if m:
        return f"{m.group(1).strip()} {m.group(2).strip()}"
    low = text.lower()
    for key in KNOWN_COORDS:
        if key in low:
            return KNOWN_COORDS[key][2]
    return None


@st.cache_data(ttl=86400, show_spinner=False)
def geocode_place(place: str) -> dict | None:
    key = place.strip().lower()
    if key in KNOWN_COORDS:
        lat, lon, label = KNOWN_COORDS[key]
        return {"label": label, "lat": lat, "lon": lon, "source": "known"}
    for k, (lat, lon, label) in KNOWN_COORDS.items():
        if k in key or key in k:
            return {"label": label, "lat": lat, "lon": lon, "source": "known"}
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "json", "limit": 1},
            timeout=6,
            headers={"User-Agent": "NUMBERIN/2.0 (personal numerology lab)"},
        )
        if r.ok:
            data = r.json()
            if data:
                hit = data[0]
                return {
                    "label": hit.get("display_name", place),
                    "lat": float(hit["lat"]),
                    "lon": float(hit["lon"]),
                    "source": "nominatim",
                }
    except Exception:
        return None
    return None


def earth_profile(place: str, lat: float, lon: float) -> dict:
    prof = name_profile(place)
    lat_red, lat_steps = reduce_trace(int(abs(lat) * 10000))
    lon_red, lon_steps = reduce_trace(int(abs(lon) * 10000))
    pair_red, pair_steps = reduce_trace(int(abs(lat) * 100 + abs(lon) * 100))
    return {
        "place": place,
        "lat": lat,
        "lon": lon,
        "lat_hemi": "N" if lat >= 0 else "S",
        "lon_hemi": "E" if lon >= 0 else "W",
        "name": prof,
        "lat_num": (lat_red, lat_steps),
        "lon_num": (lon_red, lon_steps),
        "earth_num": (pair_red, pair_steps),
    }


def name_extras(prof: dict) -> dict:
    rows = prof["rows"]
    letters = [r["letter"] for r in rows]
    values = [r["value"] for r in rows]
    counts = {n: values.count(n) for n in range(1, 10)}
    hidden = max(counts, key=counts.get) if values else 0
    first = rows[0] if rows else None
    last = rows[-1] if rows else None
    vowels = [r for r in rows if r["kind"] == "vowel"]
    cons = [r for r in rows if r["kind"] == "consonant"]
    tokens: dict[str, list] = {}
    for r in rows:
        tokens.setdefault(r["token"], []).append(r)
    token_sums = {}
    for tok, rs in tokens.items():
        raw = sum(x["value"] for x in rs)
        token_sums[tok] = (raw, *reduce_trace(raw))
    return {
        "counts": counts,
        "hidden": hidden,
        "corner": first,
        "cap": last,
        "first_vowel": vowels[0] if vowels else None,
        "vowel_n": len(vowels),
        "cons_n": len(cons),
        "token_sums": token_sums,
    }


def decode_voice(prof: dict) -> str:
    d = meaning(prof["destiny"][1])
    s = meaning(prof["soul"][1])
    p = meaning(prof["personality"][1])
    extras = name_extras(prof)
    bits = [
        f"The vehicle is {prof['destiny'][1]} — {d['title']}. {d.get('current', d['light'])}",
        f"Under the tongue: {prof['soul'][1]} — {s['title']}. {s.get('current', s['light'])}",
        f"What the room meets: {prof['personality'][1]} — {p['title']}. {p.get('current', p['light'])}",
    ]
    if extras["corner"]:
        c = extras["corner"]
        bits.append(
            f"Cornerstone {c['letter']}={c['value']} ({meaning(c['value'])['title']}) "
            f"is how this name walks into a room."
        )
    if extras["cap"]:
        c = extras["cap"]
        bits.append(
            f"Capstone {c['letter']}={c['value']} ({meaning(c['value'])['title']}) "
            f"is how it finishes what it starts."
        )
    if extras["hidden"]:
        h = meaning(extras["hidden"])
        bits.append(
            f"Hidden passion {extras['hidden']} — {h['title']} — is the number that repeats. "
            f"That hunger does not clock out."
        )
    if extras["first_vowel"]:
        v = extras["first_vowel"]
        bits.append(
            f"First vowel {v['letter']}={v['value']} is the first private note. "
            f"{meaning(v['value'])['light']}"
        )
    return " ".join(bits)


def hour_profile(t: time) -> dict:
    raw_hour = t.hour or 24
    red, steps = reduce_trace(raw_hour)
    minute_red, minute_steps = reduce_trace(t.minute) if t.minute else (0, [0])
    stamp = raw_hour * 100 + t.minute
    stamp_red, stamp_steps = reduce_trace(stamp)
    return {
        "time": t,
        "hour": (raw_hour, red, steps),
        "minute": (t.minute, minute_red, minute_steps),
        "stamp": (stamp, stamp_red, stamp_steps),
    }


def filter_scripts(rows: list[dict], lang: str) -> list[dict]:
    key = LANG_FILTER.get(lang)
    if key is None or key == "latin":
        return [] if key == "latin" else rows
    return [r for r in rows if key in r.get("name", "").lower()]


def transliterate(text: str, lang: str) -> str:
    table = LATIN_TO_SCRIPT.get(lang)
    if not table:
        return text
    keys = sorted(table, key=len, reverse=True)
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if not ch.isascii() or not ch.isalpha():
            out.append(ch)
            i += 1
            continue
        hit = False
        for token in keys:
            chunk = text[i : i + len(token)]
            if chunk.lower() == token:
                mapped = table[token]
                out.append(mapped.upper() if ch.isupper() and len(mapped) == 1 else mapped)
                i += len(token)
                hit = True
                break
        if not hit:
            out.append(ch)
            i += 1
    return "".join(out)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_number_fact(n: int) -> str | None:
    try:
        r = requests.get(
            f"http://numbersapi.com/{n}/trivia?notfound=floor",
            timeout=4,
            headers={"User-Agent": "NumerologyLab/2.0"},
        )
        if r.ok and r.text:
            return r.text.strip()
    except Exception:
        return None
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_bible(ref: str) -> dict | None:
    try:
        r = requests.get(
            f"https://bible-api.com/{quote(ref)}",
            timeout=5,
            headers={"User-Agent": "NumerologyLab/2.0"},
        )
        if r.ok:
            data = r.json()
            return {
                "ref": data.get("reference", ref),
                "text": (data.get("text") or "").strip(),
                "translation": data.get("translation_name", ""),
            }
    except Exception:
        return None
    return None


def letter_chips(rows: list[dict]) -> None:
    chips = []
    for r in rows[:120]:
        gold = r["kind"] == "vowel"
        bg = "rgba(245,215,110,.16)" if gold else "rgba(0,229,255,.12)"
        border = "#f5d76e" if gold else "#00e5ff"
        fg = "#f5d76e" if gold else "#00e5ff"
        chips.append(
            f'<span style="display:inline-block;text-align:center;margin:3px;background:{bg};'
            f'border:1px solid {border};border-radius:8px;padding:5px 7px;min-width:28px;'
            f'box-shadow:0 0 10px {border}33">'
            f'<div style="font-weight:800;color:{fg}">{r["letter"]}</div>'
            f'<div style="font-size:.68rem;color:#c9a227">{r["value"]}</div></span>'
        )
    st.markdown("".join(chips) or "_No Latin letters._", unsafe_allow_html=True)
    st.caption("Gold = vowel (Soul Urge). Cyan = consonant (Personality). Y is a vowel only when the token has no A/E/I/O/U.")


def render_depth(n: int, key: str) -> None:
    info = meaning(n)
    with st.expander(f"{n} · {info['title']} — full current", expanded=False, key=key):
        st.caption(info["keywords"])
        for label, line in depth_lines(n):
            if line:
                st.markdown(f"**{label}.** {line}")


def _slug(text: str) -> str:
    first = (text.splitlines() or ["reading"])[0].strip() or "reading"
    clean = re.sub(r"[^A-Za-z0-9_\-]+", "_", first)[:40].strip("_")
    return clean or "reading"


def build_report(text: str, latin: list, scripts: list, dates: list, digits: str, birth_time: time | None = None, earth: dict | None = None, stamp: dict | None = None) -> str:
    lines = [
        "# NUMBERIN reading",
        f"Saved {(stamp or reading_stamp())['iso']}",
        "",
        f"Seal: {seed_sigil(text)}",
        "",
        f"Stamp: {(stamp or reading_stamp())['iso']}",
        "",
        "## Input",
        text,
        "",
    ]
    if latin:
        prof = name_profile(text)
        lines.append("## Name chart")
        lines.append(decode_voice(prof))
        lines.append("")
        extras = name_extras(prof)
        if extras["corner"]:
            c = extras["corner"]
            lines.append(f"- Cornerstone {c['letter']}={c['value']} ({meaning(c['value'])['title']})")
        if extras["cap"]:
            c = extras["cap"]
            lines.append(f"- Capstone {c['letter']}={c['value']} ({meaning(c['value'])['title']})")
        if extras["hidden"]:
            lines.append(f"- Hidden passion {extras['hidden']} ({meaning(extras['hidden'])['title']})")
        lines.append("- Intensity: " + ", ".join(f"{n}×{extras['counts'][n]}" for n in range(1, 10) if extras["counts"][n]))
        lines.append("")
        for label, pack in (
            ("Destiny / Expression", prof["destiny"]),
            ("Soul Urge", prof["soul"]),
            ("Personality", prof["personality"]),
        ):
            raw, red, steps = pack
            info = meaning(red)
            lines.append(f"### {label}: {red} — {info['title']}")
            lines.append(f"raw {raw} · {' → '.join(map(str, steps))}")
            for lab, line in depth_lines(red):
                if line:
                    lines.append(f"- **{lab}:** {line}")
            lines.append("")
    if digits:
        red, steps = reduce_trace(int(digits[:18]))
        lines.append("## Digit stream")
        lines.append(f"`{digits[:18]}` → {red} ({' → '.join(map(str, steps))})")
        omen = angel_read(digits) or angel_read(digits[:4])
        if omen:
            lines.append(omen)
        lines.append("")
    if dates:
        lines.append("## Dates")
        for d in dates[:8]:
            lp = life_path(d)
            info = meaning(lp["life_path"][1])
            lines.append(f"- {d.isoformat()} · Life Path {lp['life_path'][1]} — {info['title']}")
            lines.append(f"  {info.get('current', info['light'])}")
        lines.append("")
    if birth_time:
        hp = hour_profile(birth_time)
        info = meaning(hp["hour"][1])
        lines.append("## Birth time")
        lines.append(f"- Clock: {birth_time.strftime('%H:%M')}")
        lines.append(f"- Natal hour {hp['hour'][1]} — {info['title']}")
        lines.append(f"  {info.get('current', info['light'])}")
        if dates:
            when = datetime.combine(dates[0], birth_time, tzinfo=timezone.utc)
            m = moon_phase(when)
            lines.append(f"- Moon at birth (UTC clock): {m['name']} — {m['note']}")
        lines.append("")
    if earth:
        info = meaning(earth["earth_num"][0])
        lines.append("## Earth / coordinates")
        lines.append(f"- Place: {earth['place']}")
        lines.append(
            f"- Coordinates: {abs(earth['lat']):.4f}°{earth['lat_hemi']}, "
            f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}"
        )
        lines.append(
            f"- Earth number {earth['earth_num'][0]} — {info['title']}. "
            f"{info.get('current', info['light'])}"
        )
        lines.append(
            f"- Latitude number {earth['lat_num'][0]} · Longitude number {earth['lon_num'][0]}"
        )
        if earth["name"]["destiny"][1]:
            lines.append(
                f"- Place name Destiny {earth['name']['destiny'][1]} — "
                f"{meaning(earth['name']['destiny'][1])['title']}"
            )
        lines.append("")
    if scripts:
        lines.append("## Scripts")
        for r in scripts:
            info = meaning(r["reduced"])
            lines.append(f"- {r['name']}: raw {r['raw']} → {r['reduced']} — {info['title']}")
            lines.append(f"  {info.get('current', info['light'])}")
        lines.append("")
    lines.append("---")
    lines.append("Counting is local. The click you feel is the reading.")
    return "\n".join(lines)


def _font(size: int, bold: bool = False):
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for path in names:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_photo(text: str, latin: list, scripts: list, dates: list, digits: str, birth_time: time | None = None, earth: dict | None = None, stamp: dict | None = None) -> bytes:
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), "#050506")
    draw = ImageDraw.Draw(img)
    gold = "#f5d76e"
    cyan = "#00e5ff"
    cream = "#f3e6c4"
    mute = "#c9a227"

    title_f = _font(54, True)
    big_f = _font(42, True)
    body_f = _font(28)
    small_f = _font(22)

    y = 70
    draw.text((W // 2, y), "NUMBERIN", font=title_f, fill=gold, anchor="mt")
    y += 80
    draw.text((W // 2, y), seed_sigil(text), font=big_f, fill=cyan, anchor="mt")
    y += 70
    draw.line((80, y, W - 80, y), fill=mute, width=1)
    y += 36

    first = (text.splitlines() or [""])[0][:48]
    for wrapped in textwrap.wrap(first, 34)[:2]:
        draw.text((80, y), wrapped, font=big_f, fill=cream)
        y += 48
    y += 20

    blocks = []
    if latin:
        prof = name_profile(text)
        for label, pack in (
            ("DESTINY", prof["destiny"]),
            ("SOUL URGE", prof["soul"]),
            ("PERSONALITY", prof["personality"]),
        ):
            raw, red, steps = pack
            info = meaning(red)
            blocks.append((label, str(red), info["title"], info.get("current", info["light"])))
    if dates:
        d = dates[0]
        lp = life_path(d)
        info = meaning(lp["life_path"][1])
        blocks.append(
            (
                "LIFE PATH",
                str(lp["life_path"][1]),
                info["title"],
                f"{d.isoformat()} · {info.get('current', info['light'])}",
            )
        )
    if digits:
        red, _ = reduce_trace(int(digits[:18]))
        info = meaning(red)
        blocks.append(("DIGITS", str(red), info["title"], digits[:18]))
    if birth_time:
        hp = hour_profile(birth_time)
        info = meaning(hp["hour"][1])
        blocks.append(
            (
                "NATAL HOUR",
                str(hp["hour"][1]),
                info["title"],
                f"{birth_time.strftime('%H:%M')} · {info.get('current', info['light'])}",
            )
        )
    if earth:
        info = meaning(earth["earth_num"][0])
        blocks.append(
            (
                earth["place"].upper()[:22],
                str(earth["earth_num"][0]),
                info["title"],
                f"{abs(earth['lat']):.4f}°{earth['lat_hemi']}  {abs(earth['lon']):.4f}°{earth['lon_hemi']}",
            )
        )
    for r in scripts[:3]:
        info = meaning(r["reduced"])
        blocks.append((r["name"].upper()[:22], str(r["reduced"]), info["title"], info.get("current", info["light"])))

    for label, num, title, current in blocks[:6]:
        draw.text((80, y), label, font=small_f, fill=cyan)
        y += 34
        draw.text((80, y), num, font=title_f, fill=gold)
        draw.text((220, y + 14), title, font=body_f, fill=cream)
        y += 60
        for wrapped in textwrap.wrap(current, 46)[:3]:
            draw.text((80, y), wrapped, font=small_f, fill=mute)
            y += 32
        y += 28
        if y > H - 160:
            break

    stamp_line = (stamp or reading_stamp())["iso"]
    if earth:
        stamp_line += f"  {abs(earth['lat']):.2f}{earth['lat_hemi']} {abs(earth['lon']):.2f}{earth['lon_hemi']}"
    draw.line((80, H - 110, W - 80, H - 110), fill=mute, width=1)
    draw.text((W // 2, H - 78), stamp_line, font=small_f, fill=mute, anchor="mt")
    draw.text((W // 2, H - 44), "the click you feel is the reading", font=small_f, fill=cyan, anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def wipe_reading() -> None:
    st.session_state.payload = ""
    st.session_state.lang_pick = "Auto"
    st.session_state.know_time = False
    st.session_state.place_in = ""
    st.session_state.track = "Off"


if "payload" not in st.session_state:
    st.session_state.payload = ""
if "lang_pick" not in st.session_state:
    st.session_state.lang_pick = "Auto"
if "place_in" not in st.session_state:
    st.session_state.place_in = ""
if "know_time" not in st.session_state:
    st.session_state.know_time = False
if "track" not in st.session_state:
    st.session_state.track = "Off"

moon = moon_phase()
h1, h2, h3 = st.columns([3.2, 1.1, 1])
with h1:
    st.title("NUMBERIN")
    st.caption(
        "Type a letter, a name, a date, a verse, Hebrew, Greek, Coptic, Sanskrit, "
        "Arabic, Aramaic, Russian, Ukrainian, Georgian, Armenian, a phone number, or junk from your notes. "
        "Local math. Optional live lookups."
    )
with h2:
    st.write("")
    if st.button("New reading", type="primary", use_container_width=True):
        wipe_reading()
        st.rerun()
    st.caption("Clears the specimen. Starts a clean count.")
with h3:
    st.markdown(
        f'<div style="text-align:center">{moon_svg(moon["fraction"], 80)}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"{moon['name']} · {moon['illumination']*100:.0f}% · {moon['note']}")

with st.sidebar:
    if st.button("New reading", use_container_width=True, key="reset_side"):
        wipe_reading()
        st.rerun()
    st.header("Lenses")
    lang = st.selectbox(
        "Language / script",
        list(LANG_FILTER.keys()),
        key="lang_pick",
    )
    st.markdown("##### Tracks")
    track = st.selectbox("Play", ["Off"] + list(TRACKS.keys()), key="track")
    if track != "Off":
        vid = TRACKS[track]
        st.markdown(
            f'<iframe width="100%" height="160" src="https://www.youtube.com/embed/{vid}?rel=0" '
            f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
            unsafe_allow_html=True,
        )
        st.caption("Official upload. Use headphones.")
    live = st.toggle("Live lookups (Numbers API + Bible API)", value=True)
    as_of = st.date_input(
        "Personal cycles as of",
        value=date.today(),
        min_value=DATE_FLOOR,
        max_value=DATE_CEILING,
    )
    st.markdown("##### Birth (optional)")
    st.caption("Leave blank unless you want a natal chart. Nothing here is prefilled.")
    know_time = st.toggle("I know the birth time", key="know_time")
    birth_time_in = st.time_input("Birth time", value=None, disabled=not know_time)
    place_in = st.text_input("Birth place", key="place_in", placeholder="City, country")
    place_preview = geocode_place(place_in.strip()) if place_in.strip() else None
    if place_in.strip() and place_preview:
        st.caption(place_preview["label"])
        st.caption(
            f"{abs(place_preview['lat']):.4f}°{'N' if place_preview['lat'] >= 0 else 'S'}, "
            f"{abs(place_preview['lon']):.4f}°{'E' if place_preview['lon'] >= 0 else 'W'}"
        )
    elif place_in.strip():
        st.caption("Could not pin that place. Try City, State or City, Country.")
    moon_date = st.date_input(
        "Moon for date",
        value=date.today(),
        min_value=DATE_FLOOR,
        max_value=DATE_CEILING,
    )
    st.markdown("---")
    st.markdown("### Moon of Eden")
    st.caption(
        "God's calendar is the moon. "
        f"{EDEN_LUNAR_YEARS:,} lunar years from Creation to Christ "
        f"≈ {eden_span()['solar_years']:,.0f} solar years "
        f"({LUNAR_YEAR_DAYS:.3f} d / {SOLAR_YEAR_DAYS} d)."
    )
    lunar_years = st.number_input(
        "Lunar years from Creation",
        min_value=0,
        max_value=20000,
        value=int(EDEN_LUNAR_YEARS),
        step=100,
        key="eden_lunar_years",
    )
    eden = eden_span(lunar_years)
    e1, e2 = st.columns(2)
    e1.metric("Solar equivalent", f"{eden['solar_years']:,.0f} yrs")
    e2.metric("Creation lands at", f"~{eden['creation_bc']:,} BC")
    st.caption(
        f"Lunar count {eden['lunar_number'][0]} → {eden['lunar_number'][1]} "
        f"({' → '.join(map(str, eden['lunar_number'][2]))}). "
        f"Solar count {eden['solar_number'][0]} → {eden['solar_number'][1]}."
    )
    if st.button("Read the lunar era", use_container_width=True):
        st.session_state["lunar_read"] = eden
    st.markdown("---")
    st.markdown(
        "Counting is local (Pythagorean 3-cycle Life Path, master 11/22/33 kept, "
        "karmic 13/14/16/19 flagged). APIs only decorate."
    )

birth_default = date.today()

if moon_date != date.today():
    m2 = moon_phase(datetime(moon_date.year, moon_date.month, moon_date.day, 12, tzinfo=timezone.utc))
    st.sidebar.markdown(f"**Moon on {moon_date.isoformat()}:** {m2['name']} — {m2['note']}")

payload = st.text_area(
    "Drop anything",
    height=110,
    placeholder="Name\nMonth/Day/Year\nCity, Country",
    key="payload",
)

if not payload.strip():
    st.info("Waiting for a letter, a name, a date, or anything else.")
    st.stop()

text = payload.strip()
st.markdown(f'<div class="seal">{seed_sigil(text)}</div>', unsafe_allow_html=True)
st.caption("Seal of this input — same text, same seal.")

dates = detect_dates(text)
times = detect_times(text)
digits = extract_digits(text)
birth_time = birth_time_in if know_time else (times[0] if times else None)

place_guess = detect_place(text) or (place_in.strip() if place_in.strip() else None)
coords_guess = detect_coords(text)
lat = lon = None
place_label = place_guess
if coords_guess:
    lat, lon = coords_guess
geo = geocode_place(place_guess) if place_guess else None
if geo:
    place_label = geo["label"]
    if lat is None or lon is None:
        lat, lon = geo["lat"], geo["lon"]
earth = earth_profile(place_label, lat, lon) if (place_label and lat is not None and lon is not None) else None
stamp = reading_stamp()
stamp_bits = [f"Stamped {stamp['iso']}"]
if earth:
    stamp_bits.append(
        f"{earth['place']} · {abs(earth['lat']):.4f}°{earth['lat_hemi']}, "
        f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}"
    )
st.caption(" · ".join(stamp_bits))

bible_m = BIBLE_RE.search(text)
bible_ref = f"{bible_m.group('book')} {bible_m.group('ch')}:{bible_m.group('vs')}" if bible_m else None
script_text = text
if lang not in ("Auto", "English (Latin)"):
    script_text = transliterate(text, lang)
latin = letters_latin(text) if lang in ("Auto", "English (Latin)") else []
native = script_readings(text)
converted = script_readings(script_text) if script_text != text else []
scripts = filter_scripts(converted or native, lang)
if lang == "Auto":
    scripts = filter_scripts(native, lang)
if lang not in ("Auto", "English (Latin)") and script_text != text:
    st.markdown(f"**{lang}:** `{script_text}`")
    st.caption("Latin letters moved into this script so the cipher can actually count.")

save_l, save_r = st.columns(2)
with save_l:
    st.download_button(
        "Save reading as file",
        data=build_report(text, latin, scripts, dates, digits, birth_time, earth, stamp),
        file_name=f"numberin_{_slug(text)}.md",
        mime="text/markdown",
    )
with save_r:
    st.download_button(
        "Save reading as photo",
        data=build_photo(text, latin, scripts, dates, digits, birth_time, earth, stamp),
        file_name=f"numberin_{_slug(text)}.png",
        mime="image/png",
    )

tab_decode, tab_chart, tab_ciphers, tab_moon, tab_pair, tab_look = st.tabs(
    ["Decode", "Body chart", "All ciphers", "Moon", "Compare", "Lookups"]
)

with tab_decode:
    if lang not in ("Auto", "English (Latin)"):
        st.subheader(f"{lang} decode")
        if scripts:
            for r in scripts:
                info = meaning(r["reduced"])
                st.write(
                    f"**{r['name']}** — raw `{r['raw']}` → **{r['reduced']}** · {info['title']}"
                )
                st.write(info.get("current", info["light"]))
                shown = " ".join(f"{ch}={v}" for ch, v in r["pairs"][:48])
                st.caption(shown)
                render_depth(r["reduced"], f"dec_lang_{r['name']}")
        else:
            st.warning(
                f"No {lang} letters counted. Type in that script, or keep English letters — "
                "they get converted automatically (Erin → Эрин / Εριν / ארין)."
            )
    st.subheader("Letter / name decode (Pythagorean)")
    if latin:
        prof = name_profile(text)
        letter_chips(prof["rows"])
        a, b, c = st.columns(3)
        for col, label, pack, note in (
            (a, "Destiny / Expression", prof["destiny"], "Every letter — the vehicle."),
            (b, "Soul Urge", prof["soul"], "Vowels — private hunger."),
            (c, "Personality", prof["personality"], "Consonants — the face the room meets."),
        ):
            raw, red, steps = pack
            info = meaning(red)
            col.metric(label, red)
            col.caption(f"{info['title']} · raw {raw} · {' → '.join(map(str, steps))}")
            col.write(info["light"])
            col.caption(note)
            if raw in KARMIC:
                col.warning(KARMIC_NOTE[raw])
            col.caption(info.get("shadow", ""))

        extras = name_extras(prof)
        st.markdown("##### The current of this name")
        st.write(decode_voice(prof))

        g1, g2, g3, g4 = st.columns(4)
        if extras["corner"]:
            c = extras["corner"]
            g1.metric("Cornerstone", f"{c['letter']} · {c['value']}")
            g1.caption(f"{meaning(c['value'])['title']} — how it enters.")
        if extras["cap"]:
            c = extras["cap"]
            g2.metric("Capstone", f"{c['letter']} · {c['value']}")
            g2.caption(f"{meaning(c['value'])['title']} — how it closes.")
        if extras["first_vowel"]:
            v = extras["first_vowel"]
            g3.metric("First vowel", f"{v['letter']} · {v['value']}")
            g3.caption("First private note.")
        if extras["hidden"]:
            g4.metric("Hidden passion", extras["hidden"])
            g4.caption(f"{meaning(extras['hidden'])['title']} — the repeat.")

        st.markdown("##### Intensity (how often each number lives in the name)")
        icols = st.columns(9)
        for n in range(1, 10):
            icols[n - 1].metric(str(n), extras["counts"].get(n, 0))
        missing = [str(n) for n in range(1, 10) if extras["counts"].get(n, 0) == 0]
        loud = [str(n) for n in range(1, 10) if extras["counts"].get(n, 0) >= 3]
        if missing:
            st.caption("Quiet / absent: " + ", ".join(missing) + " — not a hole. A lesson that arrives from outside the name.")
        if loud:
            st.caption("Loud: " + ", ".join(loud) + " — this voltage is the habit.")

        if extras["token_sums"]:
            st.markdown("##### Each word")
            for tok, (raw, red, steps) in extras["token_sums"].items():
                info = meaning(red)
                st.write(
                    f"**{tok}** — raw `{raw}` → **{red}** {info['title']} "
                    f"({' → '.join(map(str, steps))})"
                )
                st.caption(info.get("current", info["light"]))

        with st.expander("Letter by letter", expanded=False):
            for r in prof["rows"]:
                info = meaning(r["value"])
                kind = "vowel" if r["kind"] == "vowel" else "consonant"
                st.markdown(
                    f"**{r['letter']}** = {r['value']} ({kind}, {r['token']}) — "
                    f"{info['title']}. {info['light']}"
                )

        st.markdown("##### Full current")
        render_depth(prof["destiny"][1], "dec_dest")
        render_depth(prof["soul"][1], "dec_soul")
        render_depth(prof["personality"][1], "dec_pers")
        if extras["hidden"]:
            render_depth(extras["hidden"], "dec_hidden")
        if extras["corner"]:
            render_depth(extras["corner"]["value"], "dec_corner")
    else:
        st.write("No Latin letters in this specimen. Check **All ciphers** for other scripts.")

    if digits:
        raw_n = int(digits[:18])
        red, steps = reduce_trace(raw_n)
        st.subheader("Digit stream")
        st.write(f"`{digits[:18]}` → **{red}** ({' → '.join(map(str, steps))})")
        omen = angel_read(digits) or angel_read(digits[:4])
        if omen:
            st.warning(omen)
        for k in KARMIC:
            if k in steps or raw_n == k:
                st.info(KARMIC_NOTE[k])
        render_depth(red, "dec_digits")

    if dates:
        st.caption("Dates found: " + ", ".join(d.isoformat() for d in dates[:8]))
    if times:
        st.caption("Times found: " + ", ".join(t.strftime("%H:%M") for t in times[:8]))
    if earth:
        st.markdown("##### Earth")
        e1, e2, e3 = st.columns(3)
        e1.metric("Place", earth["place"].split(",")[0])
        e2.metric("Latitude", f"{abs(earth['lat']):.4f}°{earth['lat_hemi']}")
        e3.metric("Longitude", f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}")
        e4, e5, e6 = st.columns(3)
        e4.metric("Earth number", earth["earth_num"][0])
        e4.write(meaning(earth["earth_num"][0])["light"])
        e5.metric("Lat number", earth["lat_num"][0])
        e6.metric("Lon number", earth["lon_num"][0])
        eplace = earth["name"]
        st.caption(
            f"Place-name Destiny {eplace['destiny'][1]} — {meaning(eplace['destiny'][1])['title']}. "
            f"{meaning(earth['earth_num'][0]).get('current', meaning(earth['earth_num'][0])['light'])}"
        )
        render_depth(earth["earth_num"][0], "dec_earth")
        render_depth(eplace["destiny"][1], "dec_place")

with tab_chart:
    name_line = st.text_input("Name to chart", value=text.split("\n")[0])
    use_date = st.date_input(
        "Birth date",
        value=dates[0] if dates else birth_default,
        min_value=DATE_FLOOR,
        max_value=date.today(),
        key="chart_d",
    )
    use_time = st.time_input(
        "Birth time (optional)",
        value=birth_time or time(12, 0),
        key="chart_t",
    )
    has_time = st.checkbox("Use this birth time", value=bool(birth_time), key="chart_use_t")
    if name_line.strip():
        nm = name_profile(name_line)
        letter_chips(nm["rows"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Destiny", nm["destiny"][1])
        c1.write(meaning(nm["destiny"][1])["light"])
        c2.metric("Soul Urge", nm["soul"][1])
        c2.write(meaning(nm["soul"][1])["light"])
        c3.metric("Personality", nm["personality"][1])
        c3.write(meaning(nm["personality"][1])["light"])
        render_depth(nm["destiny"][1], "ch_dest")
        render_depth(nm["soul"][1], "ch_soul")
        render_depth(nm["personality"][1], "ch_pers")

    lp = life_path(use_date)
    st.markdown("##### Date cycles (3-cycle method — month, day, year reduced separately)")
    d1, d2, d3 = st.columns(3)
    d1.metric("Life Path", lp["life_path"][1])
    d1.caption(" → ".join(map(str, lp["life_path"][2])))
    d1.write(meaning(lp["life_path"][1])["light"])
    d2.metric("Birthday", lp["birthday"][1])
    d2.write(meaning(lp["birthday"][1])["light"])
    d3.metric("Attitude (month+day)", lp["attitude"][1])
    d3.write(meaning(lp["attitude"][1])["light"])
    st.caption(
        f"{use_date.isoformat()} → month {lp['month'][1]} · day {lp['day'][1]} · year {lp['year'][1]}"
    )
    for pack in (lp["life_path"], lp["birthday"], lp["attitude"], lp["month"], lp["day"], lp["year"]):
        raw = pack[0]
        if raw in KARMIC:
            st.info(KARMIC_NOTE[raw])

    cy = personal_cycles(use_date, as_of)
    t1, t2, t3 = st.columns(3)
    t1.metric(f"Personal Year {as_of.year}", cy["year"][1])
    t1.write(meaning(cy["year"][1])["light"])
    t2.metric("Personal Month", cy["month"][1])
    t3.metric("Personal Day", cy["day"][1])
    render_depth(lp["life_path"][1], "ch_lp")
    render_depth(cy["year"][1], "ch_py")

    when_time = use_time if has_time else birth_time
    if when_time:
        hp = hour_profile(when_time)
        st.markdown("##### Natal hour")
        h1c, h2c, h3c = st.columns(3)
        h1c.metric("Clock", when_time.strftime("%H:%M"))
        h2c.metric("Hour number", hp["hour"][1])
        h2c.write(meaning(hp["hour"][1])["light"])
        h3c.metric("HHMM stamp", hp["stamp"][1])
        born_at = datetime.combine(use_date, when_time, tzinfo=timezone.utc)
        mb = moon_phase(born_at)
        st.caption(
            f"Moon at birth (using this clock as UTC): {mb['name']} · "
            f"{mb['illumination']*100:.0f}% — {mb['note']}"
        )
        render_depth(hp["hour"][1], "ch_hour")

with tab_ciphers:
    st.write("Same specimen, many temples. Disagreement is information.")
    if latin:
        cols = st.columns(3)
        for i, name in enumerate(LATIN_CIPHERS):
            res = run_latin_cipher(text, name)
            with cols[i % 3]:
                inf = meaning(res["reduced"])
                st.markdown(f"**{name}**")
                st.write(f"`{res['raw']}` → **{res['reduced']}** · {inf['title']}")
                st.caption(res["blurb"])
                st.caption(" → ".join(map(str, res["steps"])))
    if scripts:
        st.markdown("#### Detected scripts")
        for r in scripts:
            st.write(
                f"**{r['name']}** — raw `{r['raw']}` → **{r['reduced']}** "
                f"({' → '.join(map(str, r['steps']))})"
            )
            shown = " ".join(f"{ch}={v}" for ch, v in r["pairs"][:40])
            st.caption(shown)
            inf = meaning(r["reduced"])
            st.write(inf["current"] if "current" in inf else inf["light"])
            render_depth(r["reduced"], f"sc_{r['name']}")
    if not latin and not scripts:
        st.write("No mapped letters. Digit reduction lives on the Decode tab.")

with tab_moon:
    pick = st.date_input(
        "Phase for",
        value=moon_date,
        min_value=DATE_FLOOR,
        max_value=DATE_CEILING,
        key="moon_tab",
    )
    m = moon_phase(datetime(pick.year, pick.month, pick.day, 12, tzinfo=timezone.utc))
    left, right = st.columns([1, 2])
    with left:
        st.markdown(moon_svg(m["fraction"], 140), unsafe_allow_html=True)
    with right:
        st.markdown(f"### {m['name']}")
        st.write(m["note"])
        st.caption(
            f"Age in cycle: {m['age_days']} days of {29.53:.2f} · illumination {m['illumination']*100:.0f}%"
        )
        st.write(
            "Numerology tie-in: the phase is a timing weather system. "
            "Read it next to Personal Day / Personal Month — new moon likes 1-work, "
            "full moon likes 9-work (close, offer, forgive)."
        )

    st.markdown("---")
    st.markdown("### Moon of Eden")
    st.write(
        "The moon is the older clock. A lunar year is twelve synodic months "
        f"({LUNAR_YEAR_DAYS:.3f} days). A Julian solar year is {SOLAR_YEAR_DAYS} days. "
        f"The Life of Adam and Eve / Gospel of Nicodemus count "
        f"{EDEN_LUNAR_YEARS:,} years from Creation to Christ — "
        "held here as lunar years, then folded into solar so the chart can speak."
    )
    era = st.session_state.get("lunar_read") or eden_span(st.session_state.get("eden_lunar_years", EDEN_LUNAR_YEARS))
    r1, r2, r3 = st.columns(3)
    r1.metric("Lunar years", f"{era['lunar_years']:,.0f}")
    r2.metric("Solar years", f"{era['solar_years']:,.0f}")
    r3.metric("Creation", f"~{era['creation_bc']:,} BC")
    n1, n2 = st.columns(2)
    n1.metric("Lunar number", era["lunar_number"][1])
    n1.caption(" → ".join(map(str, era["lunar_number"][2])))
    n1.write(meaning(era["lunar_number"][1])["light"])
    n2.metric("Solar number", era["solar_number"][1])
    n2.caption(" → ".join(map(str, era["solar_number"][2])))
    n2.write(meaning(era["solar_number"][1])["light"])
    render_depth(era["lunar_number"][1], "eden_lunar")
    render_depth(era["solar_number"][1], "eden_solar")
    st.caption(
        "Python dates cannot go before year 1 AD. Anything earlier is a count "
        "(lunar years / solar equivalent / BC label), not a calendar widget."
    )

with tab_pair:
    st.caption("Four counts: Life Path, Destiny, Soul Urge (vowels), Personality (consonants).")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    default_a = lines[0] if lines else ""
    default_b = lines[1] if len(lines) > 1 else ""

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### A")
        a_txt = st.text_input("A — name", value=default_a, key="pair_a_name")
        a_date = st.date_input(
            "A — birth",
            value=dates[0] if dates else birth_default,
            min_value=DATE_FLOOR,
            max_value=date.today(),
            key="pa",
        )
    with c2:
        st.markdown("##### B")
        b_txt = st.text_input("B — name", value=default_b, key="pair_b_name")
        b_date = st.date_input(
            "B — birth",
            value=dates[1] if len(dates) > 1 else date.today(),
            min_value=DATE_FLOOR,
            max_value=date.today(),
            key="pb",
        )

    if not a_txt.strip() or not b_txt.strip():
        st.info("Type a name in both A and B. Or put two names on two lines in the main box.")
    else:
        A = name_profile(a_txt)
        B = name_profile(b_txt)
        alp = life_path(a_date)["life_path"][1]
        blp = life_path(b_date)["life_path"][1]
        rows = [
            ("Life Path", alp, blp, "Date. The road."),
            ("Destiny", A["destiny"][1], B["destiny"][1], "Every letter. The vehicle."),
            ("Soul Urge", A["soul"][1], B["soul"][1], "Vowels. Private hunger."),
            ("Personality", A["personality"][1], B["personality"][1], "Consonants. The face the room meets."),
        ]
        for lab, av, bv, hint in rows:
            same = av == bv
            root_same = reduce_number(av, False) == reduce_number(bv, False)
            if same:
                note = "Same number — instant recognition. Watch the echo chamber."
            elif root_same:
                note = "Same root, different octave (master vs simple)."
            else:
                note = f"{meaning(av)['title']} meeting {meaning(bv)['title']}."
            st.markdown(f"##### {lab}")
            st.caption(hint)
            left, right = st.columns(2)
            left.metric("A", av)
            left.caption(meaning(av)["title"])
            right.metric("B", bv)
            right.caption(meaning(bv)["title"])
            st.write(note)
            render_depth(av, f"pair_a_{lab}")
            render_depth(bv, f"pair_b_{lab}")
            st.markdown("---")

with tab_look:
    st.write("Optional internet. Math still works if these fail.")
    if live and latin:
        core = run_latin_cipher(text, "Pythagorean")
        fact = fetch_number_fact(int(core["reduced"]))
        if fact:
            st.success(f"Numbers API on {core['reduced']}: {fact}")
        if core["raw"] != core["reduced"]:
            fact2 = fetch_number_fact(int(core["raw"]))
            if fact2:
                st.info(f"Numbers API on raw {core['raw']}: {fact2}")
    if live and bible_ref:
        verse = fetch_bible(bible_ref)
        if verse:
            st.markdown(f"**{verse['ref']}** · {verse['translation']}")
            st.write(verse["text"])
            body = run_latin_cipher(verse["text"], "Pythagorean")
            st.caption(f"Verse body Pythagorean raw {body['raw']} → {body['reduced']}")
        else:
            st.warning(f"Could not fetch `{bible_ref}`.")
    elif bible_ref:
        st.caption(f"Detected `{bible_ref}` — turn on live lookups to pull text.")
    else:
        st.caption("No Book chapter:verse pattern. Try `John 1:1`.")

    st.markdown("---")
    st.markdown(
        "This is a counting machine plus a correspondence board. "
        "Traditional Western meanings are short-form, not a priesthood. "
        "The click you feel is the reading."
    )