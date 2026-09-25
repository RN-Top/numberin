import streamlit as st
import datetime
import math

# ---------------------------------------------------------
# 1. CORE ASTRONOMICAL & NUMEROLOGICAL ENGINES
# ---------------------------------------------------------

def get_julian_date(year, month, day):
    """Calculates Julian Day Number for historical BCE/CE dates."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return jd

def get_lunar_phase_details(year, month, day):
    """Computes moon age, illumination, and traditional phase name."""
    jd = get_julian_date(year, month, day)
    # Reference new moon: Jan 6, 2000 (JD 2451549.5)
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
        "phase": phase_name
    }

def calculate_vibrational_root(date_str):
    """Reduces any date to its core single-digit or master number root."""
    digits = [int(c) for c in date_str if c.isdigit()]
    total = sum(digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

def calculate_resonance(user_root, milestone_root):
    """Calculates harmonic resonance between user and milestone."""
    diff = abs(user_root - milestone_root)
    if diff == 0:
        return "Direct Harmonic Mirror (100% Alignment)"
    elif diff in [2, 4, 6]:
        return "Sympathetic Octave Resonance (High Compatibility)"
    else:
        return "Polar Catalyst Dynamic (Transformative Tension)"

# ---------------------------------------------------------
# 2. MILESTONES DATABASE
# ---------------------------------------------------------

MILESTONES = {
    "Crucifixion Blood Moon (Passover)": {
        "date_str": "0033-04-03",
        "year": 33, "month": 4, "day": 3,
        "category": "Sacred History",
        "astronomy": "Partial/Total Blood Red Lunar Eclipse at moonrise over Jerusalem (Passover 14 Nisan).",
        "history": "According to astronomical records and biblical accounts, the moon rose eclipsed in the sign of Virgo, fulfilling ancient prophecies of the moon turning to blood during the passion."
    },
    "The Great Year Equinoctial Shift": {
        "date_str": "2012-12-21",
        "year": 2012, "month": 12, "day": 21,
        "category": "Cosmic Precession",
        "astronomy": "Winter Solstice Sun aligns with the Galactic Equator, closing the ~25,772-year Precession Cycle.",
        "history": "Marks the end of a grand cosmic cycle recorded across Mayan, Egyptian, and Vedic calendars, initiating a realignment into the next World Age."
    },
    "Annus Lucis / Traditional Epoch of Creation": {
        "date_str": "-4004-10-23",
        "year": -4004, "month": 10, "day": 23,
        "category": "Biblical & Hermetic",
        "astronomy": "Autumnal Equinox New Moon conjunction as calculated by Archbishop Ussher and Hermetic chronologies.",
        "history": "The theological point zero representing Adam and the breath of Genesis, frequently encoded as Year of Light (AL)."
    },
    "The Fall / Cast to Earth (WW1 Outbreak)": {
        "date_str": "1914-07-28",
        "year": 1914, "month": 7, "day": 28,
        "category": "Apocalyptic Prophecy",
        "astronomy": "Waxing Crescent Moon in Virgo entering Libra; major solar eclipse followed on August 21, 1914.",
        "history": "Highlighted in early 20th-century eschatological scholarship as the closure of the 'Times of the Gentiles' and the symbolic casting down of adversary forces into worldly warfare."
    },
    "The Great Reset Declaration": {
        "date_str": "2020-06-03",
        "year": 2020, "month": 6, "day": 3,
        "category": "Modern Transition",
        "astronomy": "Waxing Gibbous Moon square Mars and Neptune; Venus retrograde inferior conjunction.",
        "history": "Official public launch of the global restructuring initiative during global lockdowns, symbolizing the initiation of technocratic and financial realignment."
    },
    "Inauguration & Planetary Hexagon Alignment": {
        "date_str": "2017-01-20",
        "year": 2017, "month": 1, "day": 20,
        "category": "Political Astrometry",
        "astronomy": "Last Quarter Moon in Scorpio; rare alignment and geometric distribution of Mercury, Venus, Mars, and Jupiter.",
        "history": "The 58th Presidential Inauguration, accompanied by marked celestial alignments that triggered extensive astrological discussion regarding systemic disruption."
    }
}

# ---------------------------------------------------------
# 3. STREAMLIT INTERFACE
# ---------------------------------------------------------

st.set_page_config(page_title="Chronos & Cosmos Lens", layout="wide")

st.title("🌌 Chronos & Cosmos: Milestone Alignment Engine")
st.caption("Inspect astronomical phases, celestial eclipses, and cipher resonance across time.")

with st.sidebar:
    st.header("👤 Observer Coordinates")
    user_bday = st.date_input("Your Birth Date", value=datetime.date(1990, 1, 1))
    user_root = calculate_vibrational_root(user_bday.strftime("%Y%m%d"))
    user_moon = get_lunar_phase_details(user_bday.year, user_bday.month, user_bday.day)

    st.markdown(f"**Life Path / Root Value:** `{user_root}`")
    st.markdown(f"**Natal Phase:** `{user_moon['phase']}`")
    st.markdown("---")
    st.write("Select a milestone to calculate alignment and historical astronomy.")

# Milestone Selector
event_key = st.selectbox("Choose a Significant Historical or Cosmic Milestone:", list(MILESTONES.keys()))
event = MILESTONES[event_key]

# Milestone Astronomical & Numerology Calculations
m_lunar = get_lunar_phase_details(event["year"], event["month"], event["day"])
m_root = calculate_vibrational_root(event["date_str"])
resonance = calculate_resonance(user_root, m_root)

# Layout Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Event Date", event["date_str"])
col2.metric("Lunar Phase", m_lunar["phase"])
col3.metric("Lunar Illumination", f"{m_lunar['illumination']}%")
col4.metric("Vibrational Root", f"Root {m_root}")

st.markdown("---")

# Presentation Columns
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("📜 Historical & Celestial Record")
    st.markdown(f"**Classification:** *{event['category']}*")
    st.info(f"**Astronomical Signature:**\n\n{event['astronomy']}")
    st.write(event["history"])

with right_col:
    st.subheader("⚡ Personal Synchronicity & Reading")
    st.markdown(f"**Your Root:** `{user_root}`  ↔  **Event Root:** `{m_root}`")
    st.success(f"**Resonance Harmonic:**\n\n{resonance}")
    st.markdown(f"""
    * **Moon Phase Dynamics:** You were born under a **{user_moon['phase']}**, whereas this event manifested under a **{m_lunar['phase']}** with **{m_lunar['illumination']}%** illumination.
    * **Cycle Integration:** This alignment reveals how your innate vibration acts as an echo or counterweight to this historic turning point.
    """)
