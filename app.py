"""NUMBERIN — Streamlit UI. Math lives in engine.py."""

from __future__ import annotations

import hashlib
import re
from datetime import date, datetime, timezone
from urllib.parse import quote

import requests
import streamlit as st

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


def filter_scripts(rows: list[dict], lang: str) -> list[dict]:
    key = LANG_FILTER.get(lang)
    if key is None or key == "latin":
        return [] if key == "latin" else rows
    return [r for r in rows if key in r.get("name", "").lower()]


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


moon = moon_phase()
h1, h2 = st.columns([4, 1])
with h1:
    st.title("NUMBERIN")
    st.caption(
        "Type a letter, a name, a date, a verse, Hebrew, Greek, Coptic, Sanskrit, "
        "Arabic, Aramaic, Russian, Ukrainian, Georgian, Armenian, a phone number, or junk from your notes. "
        "Local math. Optional live lookups."
    )
with h2:
    st.markdown(
        f'<div style="text-align:center">{moon_svg(moon["fraction"], 80)}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"{moon['name']} · {moon['illumination']*100:.0f}% · {moon['note']}")

with st.sidebar:
    st.header("Lenses")
    lang = st.selectbox(
        "Language / script",
        list(LANG_FILTER.keys()),
    )
    live = st.toggle("Live lookups (Numbers API + Bible API)", value=True)
    as_of = st.date_input("Personal cycles as of", value=date.today())
    birth_default = st.date_input(
        "Default birth date",
        value=date(1983, 11, 19),
        min_value=date(1900, 1, 1),
        max_value=date(2026, 12, 31),
    )
    moon_date = st.date_input("Moon for date", value=date.today())
    st.markdown("---")
    st.markdown(
        "Counting is local (Pythagorean 3-cycle Life Path, master 11/22/33 kept, "
        "karmic 13/14/16/19 flagged). APIs only decorate."
    )

if moon_date != date.today():
    m2 = moon_phase(datetime(moon_date.year, moon_date.month, moon_date.day, 12, tzinfo=timezone.utc))
    st.sidebar.markdown(f"**Moon on {moon_date.isoformat()}:** {m2['name']} — {m2['note']}")

payload = st.text_area(
    "Drop anything",
    height=110,
    placeholder="Erin\nNovember 19 1983\nPistis Sophia\nJohn 1:1\nשלום\nΑγάπη\nσοφία\nज्ञान\nСофия\nСофія\nⲥⲟⲫⲓⲁ\n444",
)

if not payload.strip():
    st.info("Waiting for a letter, a name, a date, or anything else.")
    st.stop()

text = payload.strip()
st.markdown(f'<div class="seal">{seed_sigil(text)}</div>', unsafe_allow_html=True)
st.caption("Seal of this input — same text, same seal.")

dates = detect_dates(text)
digits = extract_digits(text)
bible_m = BIBLE_RE.search(text)
bible_ref = f"{bible_m.group('book')} {bible_m.group('ch')}:{bible_m.group('vs')}" if bible_m else None
latin = letters_latin(text) if lang in ("Auto", "English (Latin)") else []
scripts = filter_scripts(script_readings(text), lang)

tab_decode, tab_chart, tab_ciphers, tab_moon, tab_pair, tab_look = st.tabs(
    ["Decode", "Body chart", "All ciphers", "Moon", "Compare", "Lookups"]
)

with tab_decode:
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
        st.markdown("##### Full current")
        render_depth(prof["destiny"][1], "dec_dest")
        render_depth(prof["soul"][1], "dec_soul")
        render_depth(prof["personality"][1], "dec_pers")
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

with tab_chart:
    name_line = st.text_input("Name to chart", value=text.split("\n")[0])
    use_date = st.date_input("Birth date", value=dates[0] if dates else birth_default, key="chart_d")
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
    pick = st.date_input("Phase for", value=moon_date, key="moon_tab")
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

with tab_pair:
    c1, c2 = st.columns(2)
    with c1:
        a_txt = st.text_input("A — name", value=text.split("\n")[0])
        a_date = st.date_input("A — birth", value=dates[0] if dates else birth_default, key="pa")
    with c2:
        b_txt = st.text_input("B — name", value="")
        b_date = st.date_input("B — birth", value=date(1980, 1, 1), key="pb")
    if a_txt.strip() and b_txt.strip():
        A = name_profile(a_txt)
        B = name_profile(b_txt)
        alp = life_path(a_date)["life_path"][1]
        blp = life_path(b_date)["life_path"][1]
        rows = [
            ("Life Path", alp, blp),
            ("Destiny", A["destiny"][1], B["destiny"][1]),
            ("Soul Urge", A["soul"][1], B["soul"][1]),
            ("Personality", A["personality"][1], B["personality"][1]),
        ]
        for lab, av, bv in rows:
            same = av == bv
            root_same = reduce_number(av, False) == reduce_number(bv, False)
            if same:
                note = "Same number — instant recognition. Watch the echo chamber."
            elif root_same:
                note = "Same root, different octave (master vs simple)."
            else:
                note = f"{meaning(av)['title']} meeting {meaning(bv)['title']}."
            st.markdown(f"**{lab}** · A **{av}** / B **{bv}** — {note}")

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