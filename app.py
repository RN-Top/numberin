import streamlit as st
import datetime
import math

# ---------------------------------------------------------
# APPLICATION SETUP & CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Numberin 💥",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# MATHEMATICAL, ASTRONOMICAL & NUMEROLOGY ENGINES
# ---------------------------------------------------------

CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

def reduce_number(n: int, keep_master: bool = True) -> int:
    """Reduces an integer to a single digit or master number (11, 22, 33)."""
    while n > 9:
        if keep_master and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

def calculate_name_vibration(name: str, cipher: str = "Pythagorean") -> int:
    mapping = PYTHAGOREAN_MAP if cipher == "Pythagorean" else CHALDEAN_MAP
    total = sum(mapping.get(char.upper(), 0) for char in name if char.isalpha())
    return reduce_number(total)

def get_julian_date(year: int, month: int, day: int) -> float:
    """Calculates the astronomical Julian Day Number for historical BCE/CE dates."""
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
    digits = [int(c) for c in date_str if c.isdigit()]
    return reduce_number(sum(digits))

def evaluate_compatibility(root1: int, root2: int) -> dict:
    """Calculates compatibility harmonics between two vibrational profiles."""
    harmonic_families = {
        "Physical / Pragmatic": [1, 4, 7],
        "Emotional / Instinctive": [2, 5, 8],
        "Mental / Visionary": [3, 6, 9],
        "Master Axis": [11, 22, 33]
    }
    
    score = 70
    desc = "Dynamic balance with polarity."
    diff = abs(root1 - root2)
    
    if diff == 0:
        score = 98
        desc = "Harmonic Mirror: Identical vibrational rhythm; mutual reflection."
    elif diff in [2, 4, 6]:
        score = 88
        desc = "Sympathetic Resonance: Complementary flow with shared affinities."
    elif root1 in [11, 22, 33] or root2 in [11, 22, 33]:
        score = 85
        desc = "Master Octave Spark: High potential intensity requiring active grounding."
    else:
        score = 65
        desc = "Catalytic Polarity: Constructive tension driving mutual growth."

    return {"score": score, "description": desc}

# ---------------------------------------------------------
# DATA REPOSITORIES: DECANS, MILESTONES & KNOWLEDGE
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

MILESTONES = {
    "Crucifixion Blood Moon (Passover)": {
        "date_str": "0033-04-03", "year": 33, "month": 4, "day": 3,
        "category": "Sacred History",
        "astronomy": "Partial/Total Blood Red Lunar Eclipse at moonrise over Jerusalem during Passover (14 Nisan).",
        "details": "Concurs with scriptural records of darkening skies. Astronomical back-calculations verify the moon rising in eclipse in the constellation Virgo."
    },
    "Annus Lucis / Traditional Creation Epoch": {
        "date_str": "-4004-10-23", "year": -4004, "month": 10, "day": 23,
        "category": "Biblical & Hermetic",
        "astronomy": "Equinoctial conjunction matching Archbishop Ussher's canonical biblical chronology.",
        "details": "Zero-point marker encoding foundational creation mathematics across classical Hermetic traditions."
    },
    "WW1 Outbreak (1914 Epoch)": {
        "date_str": "1914-07-28", "year": 1914, "month": 7, "day": 28,
        "category": "Modern Eschatology",
        "astronomy": "Waxing Crescent Moon transiting into Libra; major solar eclipse followed within 24 days on August 21, 1914.",
        "details": "Viewed in historic biblical scholarship as the close of the 'Times of the Gentiles' and the descent of systemic warfare."
    },
    "Planetary Hexagon & Inauguration Alignment": {
        "date_str": "2017-01-20", "year": 2017, "month": 1, "day": 20,
        "category": "Political Astrometry",
        "astronomy": "Last Quarter Moon in Scorpio with wide dispersion across Mercury, Venus, Mars, and Jupiter.",
        "details": "Marked by astrological study as an initiation of severe systemic and administrative disruption."
    },
    "Great Reset Launch": {
        "date_str": "2020-06-03", "year": 2020, "month": 6, "day": 3,
        "category": "Global Transition",
        "astronomy": "Waxing Gibbous Moon square Mars and Neptune; Venus inferior conjunction.",
        "details": "Public unveiling of global institutional resets during worldwide societal suspension."
    },
    "The Great Year Solstice Precession": {
        "date_str": "2012-12-21", "year": 2012, "month": 12, "day": 21,
        "category": "Cosmic Precession",
        "astronomy": "Solstice Sun aligned with the Galactic Equator, closing the ~25,772-year Precession Cycle.",
        "details": "Culmination of long-count calendrical mathematics signaling entrance into a fresh precessional age."
    }
}

KNOWLEDGE_BASE = {
    "1": {"archetype": "The Primal Initiator", "element": "Fire", "keyword": "Independence, Will, Origin"},
    "2": {"archetype": "The Reflective Vessel", "element": "Water", "keyword": "Duality, Receptivity, Harmony"},
    "3": {"archetype": "The Radiant Expression", "element": "Air", "keyword": "Creativity, Synthesis, Voice"},
    "4": {"archetype": "The Sacred Builder", "element": "Earth", "keyword": "Structure, Foundation, Order"},
    "5": {"archetype": "The Dynamic Catalyst", "element": "Ether / Air", "keyword": "Change, Freedom, Motion"},
    "6": {"archetype": "The Cosmic Caretaker", "element": "Earth / Water", "keyword": "Balance, Protection, Duty"},
    "7": {"archetype": "The Esoteric Seeker", "element": "Water / Ether", "keyword": "Mystery, Analysis, Inner Solitude"},
    "8": {"archetype": "The Master of Manifestation", "element": "Earth", "keyword": "Power, Equilibrium, Karmic Return"},
    "9": {"archetype": "The Universal Completer", "element": "Fire / Ether", "keyword": "Culmination, Compassion, Wisdom"},
    "11": {"archetype": "The Illuminator (Master)", "element": "Light", "keyword": "Intuition, Visionary Revelation, Lightning"},
    "22": {"archetype": "The Master Architect (Master)", "element": "Form", "keyword": "Large-Scale Creation, Systemic Manifestation"},
    "33": {"archetype": "The Avatar of Compassion (Master)", "element": "Love", "keyword": "Universal Upliftment, Dedicated Service"}
}

# ---------------------------------------------------------
# SIDEBAR: OBSERVER ANCHOR
# ---------------------------------------------------------

with st.sidebar:
    st.title("💥 Numberin")
    st.markdown("**Unified Frequency & Celestial Engine**")
    st.write("---")

    user_name = st.text_input("Observer Name / Identifier", value="Seeker")
    user_birth_date = st.date_input("Natal Date", value=datetime.date(1990, 1, 1))

    user_lp = calculate_vibrational_root(user_birth_date.strftime("%Y%m%d"))
    user_name_val = calculate_name_vibration(user_name)
    user_moon = get_lunar_phase_details(user_birth_date.year, user_birth_date.month, user_birth_date.day)

    st.markdown(f"**Life Path:** `{user_lp}`")
    st.markdown(f"**Expression Vibration:** `{user_name_val}`")
    st.markdown(f"**Natal Moon:** `{user_moon['phase']}` ({user_moon['illumination']}%)")
    st.write("---")

# ---------------------------------------------------------
# MAIN WORKBENCH INTERFACE: 5 COMPREHENSIVE TABS
# ---------------------------------------------------------

st.title("💥 Numberin: Cosmic & Numerical Workbench")

tab_milestones, tab_oracle, tab_compat, tab_patterns, tab_knowledge = st.tabs([
    "🌌 Milestone Timeline Lens",
    "♈ Decan Oracle",
    "💫 Compatibility Matrix",
    "🔍 Pattern & Frequency Engine",
    "📖 Book of Knowledge"
])

# ---------------------------------------------------------
# TAB 1: MILESTONE TIMELINE LENS & HISTORICAL READINGS
# ---------------------------------------------------------
with tab_milestones:
    st.header("Chronos & Cosmos: Milestone Lens")
    st.caption("Inspect astronomical phases, ancient eclipses, and vibrational resonance with history.")

    selected_milestone = st.selectbox("Select Historical or Cosmic Turning Point:", list(MILESTONES.keys()))
    m_info = MILESTONES[selected_milestone]

    m_lunar = get_lunar_phase_details(m_info["year"], m_info["month"], m_info["day"])
    m_root = calculate_vibrational_root(m_info["date_str"])
    m_compat = evaluate_compatibility(user_lp, m_root)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Date", m_info["date_str"])
    c2.metric("Lunar Phase", m_lunar["phase"])
    c3.metric("Illumination", f"{m_lunar['illumination']}%")
    c4.metric("Milestone Root", f"Root {m_root}")

    st.markdown("---")
    col_hist, col_read = st.columns([1.2, 1])

    with col_hist:
        st.subheader("📜 Historical & Celestial Chronicle")
        st.markdown(f"**Category:** *{m_info['category']}*")
        st.info(f"**Astronomical Occurrence:**\n\n{m_info['astronomy']}")
        st.write(m_info["details"])

    with col_read:
        st.subheader("⚡ Personal Synchronicity Reading")
        st.markdown(f"**Your Life Path:** `{user_lp}`  ↔  **Milestone Vibration:** `{m_root}`")
        st.metric("Resonance Score", f"{m_compat['score']}%")
        st.success(m_compat['description'])
        st.markdown(f"""
        * **Lunar Counterpart:** You entered under a **{user_moon['phase']}**, encountering an event sealed under a **{m_lunar['phase']}**.
        * **Energetic Reading:** Reflects the balance between your innate purpose and this historic turning point.
        """)

# ---------------------------------------------------------
# TAB 2: DECAN ORACLE & RADIAL SPOKES
# ---------------------------------------------------------
with tab_oracle:
    st.header("Decan Oracle & Zodiac Coordinates")
    st.caption("Ptolemaic decans and planetary rulers mapped across 30° radial increments.")

    sign = st.selectbox("Explore Zodiac Sector:", list(ZODIAC_DECANS.keys()))
    cols = st.columns(3)

    for i, (decan_deg, ruler) in enumerate(ZODIAC_DECANS[sign]):
        with cols[i]:
            st.markdown(f"### {decan_deg}")
            st.markdown(f"**Planetary Ruler:** `{ruler}`")
            if ruler == "Moon":
                st.info("🌙 **Lunar Decan**: Associated with tides, reflections, transitions, and intuition.")
            elif ruler in ["Mars", "Saturn"]:
                st.warning(f"⚡ **Intensive Force**: Governed by the sphere of {ruler}.")
            else:
                st.write(f"Governed by the harmonious currents of {ruler}.")

# ---------------------------------------------------------
# TAB 3: COMPATIBILITY / SYNASTRY MATRIX
# ---------------------------------------------------------
with tab_compat:
    st.header("Synastry & Resonant Compatibility")
    st.caption("Compare your vibrational anchor with a partner, collaborator, or specific calendar date.")

    comp_type = st.radio("Comparison Mode", ["Compare with another Person", "Compare with an Event / Date"], horizontal=True)

    if comp_type == "Compare with another Person":
        p_name = st.text_input("Partner / Collaborator Name", value="Companion")
        p_date = st.date_input("Partner Natal Date", value=datetime.date(1992, 5, 15))
        p_root = calculate_vibrational_root(p_date.strftime("%Y%m%d"))
        p_moon = get_lunar_phase_details(p_date.year, p_date.month, p_date.day)
        
        result = evaluate_compatibility(user_lp, p_root)
        
        c_a, c_b, c_c = st.columns(3)
        c_a.metric(f"{user_name}'s Life Path", user_lp)
        c_b.metric(f"{p_name}'s Life Path", p_root)
        c_c.metric("Compatibility Index", f"{result['score']}%")

        st.info(f"**Synastry Dynamic:** {result['description']}")
        st.write(f"* **Moon Phase Interaction:** {user_name} ({user_moon['phase']}) transiting alongside {p_name} ({p_moon['phase']}).")

    else:
        target_date = st.date_input("Target Date for Assessment", value=datetime.date.today())
        t_root = calculate_vibrational_root(target_date.strftime("%Y%m%d"))
        t_moon = get_lunar_phase_details(target_date.year, target_date.month, target_date.day)
        
        result = evaluate_compatibility(user_lp, t_root)
        
        c_a, c_b = st.columns(2)
        c_a.metric("Target Date Vibration", f"Root {t_root}")
        c_b.metric("Day Alignment Index", f"{result['score']}%")
        st.info(f"**Day Resonance:** {result['description']}")

# ---------------------------------------------------------
# TAB 4: PATTERN & FREQUENCY ENGINE
# ---------------------------------------------------------
with tab_patterns:
    st.header("Pattern & Frequency Analysis")
    st.caption("Translate arbitrary sequences, words, phrases, or custom dates into numerical patterns.")

    user_text = st.text_input("Input Word, Cipher Phrase, or Sequence:", value="As Above So Below")
    cipher_type = st.selectbox("Select Numerical Cipher:", ["Pythagorean", "Chaldean"])

    pyth_val = calculate_name_vibration(user_text, "Pythagorean")
    chald_val = calculate_name_vibration(user_text, "Chaldean")

    k1, k2 = st.columns(2)
    k1.metric("Pythagorean Root", pyth_val)
    k2.metric("Chaldean Root", chald_val)

    # Character frequency breakdown
    cleaned_text = [c.upper() for c in user_text if c.isalpha()]
    char_freq = {}
    for c in cleaned_text:
        char_freq[c] = char_freq.get(c, 0) + 1

    st.subheader("Vibrational Distribution")
    st.bar_chart(char_freq)

# ---------------------------------------------------------
# TAB 5: BOOK OF KNOWLEDGE
# ---------------------------------------------------------
with tab_knowledge:
    st.header("📖 The Book of Knowledge")
    st.caption("Canonical reference definitions for vibrational roots, celestial phases, and sacred geometries.")

    selected_number = st.selectbox("Consult Number Root:", list(KNOWLEDGE_BASE.keys()))
    entry = KNOWLEDGE_BASE[selected_number]

    b1, b2 = st.columns(2)
    with b1:
        st.markdown(f"### Root {selected_number}: {entry['archetype']}")
        st.markdown(f"**Elemental Current:** `{entry['element']}`")
        st.markdown(f"**Key Vibrations:** `{entry['keyword']}`")

    with b2:
        st.markdown("### Lunar Phase Esotericism")
        st.write("""
        * **New Moon (Conjunction):** The seed point of pure intent, unmanifest potential, and initiation.
        * **Crescent & Quarter:** Momentum building, navigating resistance, anchoring structure.
        * **Full Moon (Opposition):** Total illumination, confrontation of polarities, and revelations.
        * **Waning Phases:** Synthesis, harvesting wisdom, releasing outworn cycles.
        """)
