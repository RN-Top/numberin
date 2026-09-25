import streamlit as st
import datetime
import math

# ---------------------------------------------------------
# APPLICATION CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Numberin 💥",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ASTRONOMICAL, JULIAN & NUMEROLOGY ENGINES
# ---------------------------------------------------------

def get_julian_date(year: int, month: int, day: int) -> float:
    """Calculates the Julian Day Number for historical BCE/CE dates."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return jd

def get_lunar_phase_details(year: int, month: int, day: int) -> dict:
    """Computes moon age, illumination, and traditional phase name."""
    jd = get_julian_date(year, month, day)
    synodic_month = 29.53058867
    days_since_new = (jd - 2451549.5) % synodic_month
    phase_ratio = days_since_new / synodic_month
    illumination = round((1 - math.cos(phase_ratio * 2 * math.pi)) / 2 * 100, 1)

    if phase_ratio < 0.03 or phase_ratio > 0.97:
        phase_name = "New Moon 🌑"
    elif phase_ratio < 0.22:
        phase_name = "Waxing Crescent 🌒"
    elif phase_ratio < 0.28:
        phase_name = "First Quarter 🌓"
    elif phase_ratio < 0.47:
        phase_name = "Waxing Gibbous 🌔"
    elif phase_ratio < 0.53:
        phase_name = "Full Moon 🌕"
    elif phase_ratio < 0.72:
        phase_name = "Waning Gibbous 🌖"
    elif phase_ratio < 0.78:
        phase_name = "Last Quarter 🌗"
    else:
        phase_name = "Waning Crescent 🌘"

    return {
        "moon_age_days": round(days_since_new, 1),
        "illumination": illumination,
        "phase": phase_name,
        "phase_ratio": round(phase_ratio, 3)
    }

def calculate_vibrational_root(date_str: str) -> int:
    """Reduces any date string to single-digit or master number root."""
    digits = [int(c) for c in date_str if c.isdigit()]
    total = sum(digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

def calculate_resonance(user_root: int, target_root: int) -> str:
    """Evaluates the harmonic relationship between two vibrational numbers."""
    diff = abs(user_root - target_root)
    if diff == 0:
        return "Direct Harmonic Mirror (100% Alignment)"
    elif diff in [2, 4, 6]:
        return "Sympathetic Octave Resonance (High Compatibility)"
    else:
        return "Polar Catalyst Dynamic (Transformative Tension)"

# ---------------------------------------------------------
# DATA: DECANS & ZODIAC ALIGNMENTS
# ---------------------------------------------------------

ZODIAC_DECANS = {
    "Aries": [("Decan 1 (0°-10°)", "Mars"), ("Decan 2 (10°-20°)", "Sun"), ("Decan 3 (20°-30°)", "Venus")],
    "Taurus": [("Decan 1 (0°-10°)", "Mercury"), ("Decan 2 (10°-20°)", "Moon"), ("Decan 3 (20°-30°)", "Saturn")],
    "Gemini": [("Decan 1 (0°-10°)", "Jupiter"), ("Decan 2 (10°-20°)", "Mars"), ("Decan 3 (20°-30°)", "Sun")],
    "Cancer": [("Decan 1 (0°-10°)", "Venus"), ("Decan 2 (10°-20°)", "Mercury"), ("Decan 3 (20°-30°)", "Moon")],
    "Leo": [("Decan 1 (0°-10°)", "Saturn"), ("Decan 2 (10°-20°)", "Jupiter"), ("Decan 3 (20°-30°)", "Mars")],
    "Virgo": [("Decan 1 (0°-10°)", "Sun"), ("Decan 2 (10°-20°)", "Venus"), ("Decan 3 (20°-30°)", "Mercury")],
    "Libra": [("Decan 1 (0°-10°)", "Moon"), ("Decan 2 (10°-20°)", "Saturn"), ("Decan 3 (20°-30°)", "Jupiter")],
    "Scorpio": [("Decan 1 (0°-10°)", "Mars"), ("Decan 2 (10°-20°)", "Sun"), ("Decan 3 (20°-30°)", "Venus")],
    "Sagittarius": [("Decan 1 (0°-10°)", "Mercury"), ("Decan 2 (10°-20°)", "Moon"), ("Decan 3 (20°-30°)", "Saturn")],
    "Capricorn": [("Decan 1 (0°-10°)", "Jupiter"), ("Decan 2 (10°-20°)", "Mars"), ("Decan 3 (20°-30°)", "Sun")],
    "Aquarius": [("Decan 1 (0°-10°)", "Venus"), ("Decan 2 (10°-20°)", "Mercury"), ("Decan 3 (20°-30°)", "Moon")],
    "Pisces": [("Decan 1 (0°-10°)", "Saturn"), ("Decan 2 (10°-20°)", "Jupiter"), ("Decan 3 (20°-30°)", "Mars")]
}

# ---------------------------------------------------------
# DATA: HISTORICAL & CELESTIAL MILESTONES
# ---------------------------------------------------------

MILESTONES = {
    "Crucifixion Blood Moon (Passover)": {
        "date_str": "0033-04-03", "year": 33, "month": 4, "day": 3,
        "category": "Sacred History",
        "astronomy": "Partial/Total Lunar Eclipse at moonrise over Jerusalem during Passover (14 Nisan).",
        "details": "Fulfills scriptural depictions of celestial darkening; astronomical models verify an eclipse in the constellation Virgo."
    },
    "Annus Lucis / Traditional Epoch of Creation": {
        "date_str": "-4004-10-23", "year": -4004, "month": 10, "day": 23,
        "category": "Biblical & Hermetic",
        "astronomy": "Conjunction marking the traditional creation timeline established in classical chronologies.",
        "details": "Point zero for classical theological timelines, corresponding to the foundational genesis matrix."
    },
    "The Outbreak of WW1 (1914 Milestone)": {
        "date_str": "1914-07-28", "year": 1914, "month": 7, "day": 28,
        "category": "Modern Eschatology",
        "astronomy": "Waxing Crescent Moon moving from Virgo into Libra; total solar eclipse followed on August 21, 1914.",
        "details": "Viewed in historic eschatological studies as the conclusion of the 'Times of the Gentiles' and the onset of global systemic shifts."
    },
    "Inauguration & Planetary Alignment": {
        "date_str": "2017-01-20", "year": 2017, "month": 1, "day": 20,
        "category": "Political Astrometry",
        "astronomy": "Last Quarter Moon in Scorpio with wide planetary distribution across Mercury, Venus, Mars, and Jupiter.",
        "details": "Marked by heightened astrological debate regarding structural shifts and systemic transformation."
    },
    "The Great Reset Declaration": {
        "date_str": "2020-06-03", "year": 2020, "month": 6, "day": 3,
        "category": "Global Transition",
        "astronomy": "Waxing Gibbous Moon in Scorpio square Neptune/Mars; Venus retrograde inferior conjunction.",
        "details": "Public launch of comprehensive restructuring initiatives amid global disruption."
    },
    "The Great Year Equinoctial Precession": {
        "date_str": "2012-12-21", "year": 2012, "month": 12, "day": 21,
        "category": "Cosmic Precession",
        "astronomy": "Winter Solstice Sun conjunction with Galactic Equator, closing the ~25,772-year cycle.",
        "details": "Marks the transition into a new precessional age recorded across multiple ancient calendrical traditions."
    }
}

# ---------------------------------------------------------
# SIDEBAR: OBSERVER COORDINATES
# ---------------------------------------------------------

with st.sidebar:
    st.title("Numberin 💥")
    st.header("👤 Observer Anchor")
    user_birth_date = st.date_input("Natal / Inquiry Date", value=datetime.date(1990, 1, 1))
    user_root = calculate_vibrational_root(user_birth_date.strftime("%Y%m%d"))
    user_moon = get_lunar_phase_details(user_birth_date.year, user_birth_date.month, user_birth_date.day)

    st.markdown(f"**Life Path / Root Value:** `{user_root}`")
    st.markdown(f"**Natal Phase:** `{user_moon['phase']}`")
    st.markdown(f"**Illumination:** `{user_moon['illumination']}%`")
    st.markdown("---")
    st.caption("Active observer coordinates applied across all Numberin modules.")

# ---------------------------------------------------------
# MAIN INTERFACE & WORKBENCH TABS
# ---------------------------------------------------------

st.title("💥 Numberin")
st.caption("Celestial cycles, astronomical phases, and numerical resonance engine.")

tab1, tab2, tab3 = st.tabs([
    "🌌 Timeline Lens & Milestones",
    "♈ Decan Oracle & Radial Spokes",
    "🔢 Numerology & Phase Calculator"
])

# TAB 1: HISTORICAL MILESTONES & ECLIPSES
with tab1:
    st.header("Chronos & Cosmos: Milestone Timeline")
    st.caption("Cross-reference historical dates against celestial events, eclipses, and personal resonance.")

    selected_event_name = st.selectbox("Select Historical / Cosmic Milestone:", list(MILESTONES.keys()))
    event_data = MILESTONES[selected_event_name]

    m_lunar = get_lunar_phase_details(event_data["year"], event_data["month"], event_data["day"])
    m_root = calculate_vibrational_root(event_data["date_str"])
    res = calculate_resonance(user_root, m_root)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Date", event_data["date_str"])
    c2.metric("Lunar Phase", m_lunar["phase"])
    c3.metric("Illumination", f"{m_lunar['illumination']}%")
    c4.metric("Vibrational Root", f"Root {m_root}")

    st.markdown("---")
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("📜 Historical & Celestial Record")
        st.markdown(f"**Category:** *{event_data['category']}*")
        st.info(f"**Celestial Event:**\n\n{event_data['astronomy']}")
        st.write(event_data["details"])

    with col_right:
        st.subheader("⚡ Personal Synchronicity")
        st.markdown(f"**Your Root:** `{user_root}` ↔ **Event Root:** `{m_root}`")
        st.success(f"**Resonance Dynamic:**\n\n{res}")
        st.markdown(f"""
        - **Natal Anchor:** {user_moon['phase']} ({user_moon['illumination']}%)
        - **Milestone Phase:** {m_lunar['phase']} ({m_lunar['illumination']}%)
        """)

# TAB 2: ZODIAC SPOKES & DECAN ORACLE
with tab2:
    st.header("Decan Oracle & Zodiac Coordinates")
    st.caption("Analyze 30-degree radial segments and their traditional planetary rulers.")

    selected_sign = st.selectbox("Select Zodiac Sign:", list(ZODIAC_DECANS.keys()))
    decans = ZODIAC_DECANS[selected_sign]

    cols = st.columns(3)
    for idx, (decan_range, ruler) in enumerate(decans):
        with cols[idx]:
            st.markdown(f"### {decan_range}")
            st.markdown(f"**Ruler:** `{ruler}`")
            if ruler == "Moon":
                st.info("🌙 Lunar-ruled decan: associated with shifts, reflection, and cycles.")
            else:
                st.write(f"Governed by the energetic sphere of {ruler}.")

# TAB 3: CUSTOM CALCULATOR
with tab3:
    st.header("Custom Date & Phase Calculator")
    calc_date = st.date_input("Lookup Any Calendar Date", value=datetime.date.today())
    calc_lunar = get_lunar_phase_details(calc_date.year, calc_date.month, calc_date.day)
    calc_root = calculate_vibrational_root(calc_date.strftime("%Y%m%d"))

    q1, q2, q3 = st.columns(3)
    q1.metric("Selected Date", str(calc_date))
    q2.metric("Moon Phase", calc_lunar["phase"])
    q3.metric("Root Vibration", f"Root {calc_root}")
