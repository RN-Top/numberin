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
    KARMIC,
    KARMIC_NOTE,
    LATIN_CIPHERS,
    angel_read,
    depth_lines,
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

st.set_page_config(page_title="NUMBERIN", page_icon="✦", layout="wide")

st.markdown(
    """
<style>
html, body, {
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
} {
  background: #0a0a0c;
  border-right: 1px solid #c9a22755;
} {background: rgba(0,0,0,.85);}
textarea {
  background: #0b0b0d !important;
  color: #f5d76e !important;
  border: 1px solid #c9a227 !important;
  box-shadow: 0 0 16px rgba(0,229,255,.15);
}
 {color: #f5d76e;}
div[data-baseweb="tab-list"] {border-bottom: 1px solid #c9a22744;}
</style>
""",
    unsafe_allow_html=True,
)

BIBLE_RE = re.compile(
    r"\b(?:(?P<book>(?:[1-3]\s*)?  +(?:\s+ +)?))\s+"
    r"(?P<ch>\d{1,3})\s*:\s*(?P<vs>\d{1,3})",
    re.I,
)
DATE_ISO = re.compile(r"\b(\d{4})[-/. -/.](\d{1,2})\b")
DATE_US = re.compile(r"\b(\d{1,2})[-/. -/.](\d{2,4})\b")
TIME_RE = re.compile(
    r"\b([01 0-3])[:.;]([0-5]\d)(?:\s*( \.? \.?))?\b"
)
COORD_RE = re.compile(r"(-?\d{1,3}\.\d+)\s*[,/ ]\s*(-?\d{1,3}\.\d+)")
PLACE_HINT = re.compile(
    r"\b(  +(?:\s+  +)*)\s*,?\s*(FL|Florida|TX|Texas|CA|NY|OH|GA|NC|SC|MI|Michigan)\b",
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
        "th": "θ", "ph": "φ", "ch": "χ",
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_dates(text: str) -> list :
    found: list = []
    for m in DATE_ISO.finditer(text):
        try:
            found.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    for m in DATE_US.finditer(text):
        try:
            mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if y < 100:
                y += 2000 if y < 50 else 1900
            found.append(date(y, mo, d))
        except ValueError:
            pass
    return found


def parse_times(text: str) -> list :
    out: list = []
    for m in TIME_RE.finditer(text):
        h = int(m.group(1))
        mi = int(m.group(2))
        ap = (m.group(3) or "").lower()
        if ap.startswith("p") and h < 12:
            h += 12
        if ap.startswith("a") and h == 12:
            h = 0
        try:
            out.append(time(h, mi))
        except ValueError:
            pass
    return out


def parse_coords(text: str) -> list :
    out: list = []
    for m in COORD_RE.finditer(text):
        try:
            lat, lon = float(m.group(1)), float(m.group(2))
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                out.append((lat, lon, f"{lat}, {lon}"))
        except ValueError:
            pass
    low = text.lower()
    for key, (lat, lon, label) in KNOWN_COORDS.items():
        if key in low:
            out.append((lat, lon, label))
    return out


def parse_places(text: str) -> list :
    return [m.group(0) for m in PLACE_HINT.finditer(text)]


def detect_bible(text: str) -> str | None:
    m = BIBLE_RE.search(text)
    if not m:
        return None
    return f"{m.group('book')} {m.group('ch')}:{m.group('vs')}"


def fetch_number_fact(n: int) -> str | None:
    try:
        r = requests.get(f"http://numbersapi.com/{n}", timeout=6)
        if r.status_code == 200 and r.text and "oops" not in r.text.lower():
            return r.text
    except Exception:
        pass
    return None


def fetch_bible(ref: str) -> dict | None:
    try:
        r = requests.get(
            f"https://bible-api.com/{quote(ref)}?translation=web",
            timeout=8,
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("text"):
                return {
                    "ref": data.get("reference", ref),
                    "text": data .strip(),
                    "translation": data.get("translation_name", "WEB"),
                }
    except Exception:
        pass
    return None


def render_depth(n: int, key: str):
    red, steps = reduce_trace(n, True)
    if len(steps) <= 1:
        return
    st.caption(" → ".join(str(s) for s in steps))
    for i, s in enumerate(steps[1:], 1):
        st.markdown(f"**{s}** — {meaning(s) }")


def render_profile(label: str, prof: dict, d: date | None):
    st.markdown(f"### {label}")
    if d:
        lp = life_path(d)
        st.metric("Life Path", lp [1], lp [0 1]) )
        if lp [1 1 1]:
            st.metric("Maturity", lp [1])
    c1, c2, c3 = st.columns(3)
    c1.metric("Destiny", prof [1])
    c1.caption(meaning(prof [1 1])
    c2.caption(meaning(prof [1 "personality"][1 1]) )
    if prof :
        st.warning("Karmic debt: " + ", ".join(str(k) for k in prof["karmic"]))
        st.caption(KARMIC_NOTE)
    with st.expander("Depth lines"):
        for line in depth_lines(prof):
            st.write(line)
    with st.expander("Script readings"):
        for name, val in script_readings(prof ).items():
            st.markdown(f"**{name}:** {val}")


def render_moon(d: date):
    phase = moon_phase(d)
    st.markdown(f"### Moon — {d.isoformat()}")
    st.metric("Illumination", f"{phase *100:.0f}%", phase )
    st.markdown(moon_svg(phase ), unsafe_allow_html=True)
    st.caption(phase )


def render_cycles(d: date):
    cyc = personal_cycles(d)
    st.markdown("### Personal cycles")
    for k, v in cyc.items():
        st.metric(k.replace("_", " ").title(), v)
    st.caption("Pinnacles, challenges, personal year — the moving numbers.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

st.title("NUMBERIN")
st.caption("A counting machine and a correspondence board. Not a priesthood.")

with st.sidebar:
    st.markdown("### Input")
    text = st.text_area(
        "Paste anything",
        height=220,
        placeholder="Names, dates, places, a verse, a feeling…",
    )
    live = st.checkbox("Live lookups (numbers + bible)", value=False)
    st.markdown("---")
    st.markdown("### Moon of Eden")
    st.caption("God's calendar is the moon. 5,500 lunar years ≈ 5,336 solar years.")
    lunar_years = st.number_input(
        "Lunar years from creation",
        min_value=0,
        max_value=20000,
        value=5500,
        step=100,
    )
    solar_eq = lunar_years * 354.367 / 365.25
    creation_bc = round(solar_eq)
    st.metric("Solar equivalent", f"{solar_eq:,.0f} yrs")
    st.metric("Creation lands at", f"~{creation_bc:,} BC")
    if st.button("Read the lunar era"):
        st.session_state = lunar_years

dates = parse_dates(text)
times = parse_times(text)
coords = parse_coords(text)
places = parse_places(text)
bible_ref = detect_bible(text)

default_a = text.splitlines()[0] if text.strip() else "Erin"
default_b = text.splitlines()[1] if len(text.splitlines()) > 1 else "Drew"
birth_default = dates[0] if dates else date(1990, 1, 1)

tab_main, tab_pair, tab_moon, tab_look = st.tabs(
    ["Chart", "Pair", "Moon", "Lookups"]
)

with tab_main:
    if not text.strip():
        st.info("Paste a name or a date to begin.")
    else:
        names = [n.strip() for n in text.splitlines() if n.strip() :6]):
            prof = name_profile(name)
            d = dates if i < len(dates) else None
            render_profile(name, prof, d)
            st.markdown("---")
        if dates:
            st.markdown("### Dates found")
            for d in dates:
                st.write(d.isoformat())
                render_moon(d)
                render_cycles(d)
        if "lunar_read" in st.session_state:
            ly = st.session_state st.markdown("### 🌙 Moon of Eden reading")
            st.metric("Lunar years", ly)
            st.metric("Solar equivalent", f"{ly * 354.367 / 365.25:,.0f}")
            st.metric("Creation", f"~{round(ly * 354.367 / 365.25):,} BC")
            prof = name_profile(str(ly))
            render_profile(f"Lunar era {ly}", prof, None)

with tab_pair:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### A")
        a_txt = st.text_input("A — name", value=default_a, key="pair_a_name")
        a_date = st.date_input(
            "A — birth",
            value=dates[0] if dates else birth_default,
            min_value=date(1, 1, 1),
            max_value=date.today(),
            key="pa",
        )
    with c2:
        st.markdown("##### B")
        b_txt = st.text_input("B — name", value=default_b, key="pair_b_name")
        b_date = st.date_input(
            "B — birth",
            value=dates[1] if len(dates) > 1 else date.today(),
            min_value=date(1, 1, 1),
            max_value=date.today(),
            key="pb",
        )

    if not a_txt.strip() or not b_txt.strip():
        st.info("Type a name in both A and B. Or put two names on two lines in the main box.")
    else:
        A = name_profile(a_txt)
        B = name_profile(b_txt)
        alp = life_path(a_date) [1 "life_path"][1 ("Life Path", alp, blp, "The road."),
            ("Destiny", A["destiny"][1 1 1], B [1 1 1], "Consonants. The face the room meets."),
        ]
        for lab, av, bv, hint in