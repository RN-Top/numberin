import streamlit as st
import datetime
import math
from PIL import Image

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
# CIPHERS, ASTRONOMICAL & NUMEROLOGY ENGINES
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

def get_julian_date(year: int, month: int, day: int, hour: float = 12.0) -> float:
    """Calculates astronomical Julian Day Number for historical BCE/CE dates with fractional hours."""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    day_fraction = day + (hour / 24.0)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day_fraction + b - 1524.5
    return jd

def get_lunar_phase_details(year: int, month: int, day: int, hour: float = 12.0) -> dict:
    """Computes moon age, illumination, and synodic phase name."""
    jd = get_julian_date(year, month, day, hour)
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

def get_approx_sun_sign(month: int, day: int) -> str:
    dates = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 20, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 22, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 21, "Sagittarius"),
        (12, 31, "Capricorn")
    ]
    for m, d, sign in dates:
        if (month, day) <= (m, d):
            return sign
    return "Capricorn"

def calculate_vibrational_root(date_str: str) -> int:
    digits = [int(c) for c in date_str if c.isdigit()]
    return reduce_number(sum(digits))

def evaluate_compatibility(root1: int, root2: int) -> dict:
    diff = abs(root1 - root2)
    if diff == 0:
        score = 98
        desc = "Harmonic Mirror: Identical vibrational rhythm; mutual reflection."
    elif diff in [2, 4, 6]:
        score = 88
        desc = "Sympathetic Resonance: Complementary flow with shared affinities."
    elif root1 in [11, 22, 33] or root2 in [11, 22, 33]:
        score = 85
        desc = "Master Octave Spark: High potential intensity requiring grounded focus."
    else:
        score = 65
        desc = "Catalytic Polarity: Constructive tension driving mutual growth."
    return {"score": score, "description": desc}

# ---------------------------------------------------------
# DATA REPOSITORIES: DECANS, MILESTONES & ANCIENT BOOKS
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
        "astronomy": "Equinoctial conjunction matching Archbishop Ussher's canonical chronology.",
        "details": "Zero-point marker encoding foundational creation mathematics across classical traditions."
    },
    "WW1 Outbreak (1914 Epoch)": {
        "date_str": "1914-07-28", "year": 1914, "month": 7, "day": 28,
        "category": "Modern Eschatology",
        "astronomy": "Waxing Crescent Moon transiting into Libra; major solar eclipse followed on August 21, 1914.",
        "details": "Viewed in historic biblical scholarship as the close of the 'Times of the Gentiles' and the onset of global systemic warfare."
    },
    "Planetary Hexagon & Inauguration Alignment": {
        "date_str": "2017-01-20", "year": 2017, "month": 1, "day": 20,
        "category": "Political Astrometry",
        "astronomy": "Last Quarter Moon in Scorpio with wide dispersion across Mercury, Venus, Mars, and Jupiter.",
        "details": "Marked by astrological study as an initiation of severe systemic disruption."
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
    "1": {"archetype": "The Primal Initiator", "element": "Fire", "keyword": "Independence, Will, Leadership", "reading": "You are a self-generating force designed to break new ground and lead with pioneering energy."},
    "2": {"archetype": "The Reflective Vessel", "element": "Water", "keyword": "Duality, Receptivity, Harmony", "reading": "Your frequency navigates the subtle tides of diplomacy, intuitive observation, and quiet mediation."},
    "3": {"archetype": "The Radiant Expression", "element": "Air", "keyword": "Creativity, Synthesis, Voice", "reading": "A channel of synthesis and communication, turning raw concepts into vivid artistic expression."},
    "4": {"archetype": "The Sacred Builder", "element": "Earth", "keyword": "Structure, Foundation, Order", "reading": "The anchor of tangible reality. You manifest stability, discipline, and endurance out of chaos."},
    "5": {"archetype": "The Dynamic Catalyst", "element": "Ether / Air", "keyword": "Change, Freedom, Motion", "reading": "An agent of kinetic evolution, dismantling static constructs to invite expansive freedom."},
    "6": {"archetype": "The Cosmic Caretaker", "element": "Earth / Water", "keyword": "Balance, Protection, Duty", "reading": "Harmonizer of communal and personal spheres, driven to restore equilibrium and sanctity."},
    "7": {"archetype": "The Esoteric Seeker", "element": "Water / Ether", "keyword": "Mystery, Analysis, Wisdom", "reading": "Investigator of deeper mechanics. You look past surface noise into root principles."},
    "8": {"archetype": "The Master of Manifestation", "element": "Earth", "keyword": "Power, Balance, Realization", "reading": "Wields the mathematics of cause and effect, materializing vision into durable authority."},
    "9": {"archetype": "The Universal Completer", "element": "Fire / Ether", "keyword": "Culmination, Compassion, Synthesis", "reading": "The cycle's end and transition point, embodying universal perspectives and detachment."},
    "11": {"archetype": "The Illuminator (Master)", "element": "Light", "keyword": "Intuition, Visionary Revelation", "reading": "Conduit of high-frequency intuition, acting as a bridge between unseen insights and the world."},
    "22": {"archetype": "The Master Architect (Master)", "element": "Form", "keyword": "Large-Scale Creation, Reality", "reading": "Possesses the ability to anchor ambitious, timeless ideas into structural reality."},
    "33": {"archetype": "The Avatar of Compassion (Master)", "element": "Love", "keyword": "Universal Upliftment, Service", "reading": "Devoted to elevating consciousness through dedicated service and heart-centered guidance."}
}

PRELOADED_TEXTS = {
    "The Book of Enoch (The Luminaries - Chapter 72)": """
1. The book of the courses of the luminaries of the heaven, the relations of each, according to their classes, their dominion and their seasons, according to their names and places of origin, and according to their months.
2. First there goes forth the great luminary, named the Sun, and his circumference is like the circumference of the heaven, and he is quite filled with illuminating and heating fire.
3. The chariot on which he mounts, the wind drives, and the sun goes down from the heaven as he returns through the north in order to reach the east, and is so led that he comes to the appropriate portal and shines in the face of the heaven.
4. In this manner he rises in the first month in the great portal, which is the fourth portal of the six portals in the cast.
5. And in that fourth portal from which the sun rises in the first month are twelve window-openings, from which proceed a flame when they are opened in their season.
    """,
    "Pistis Sophia (Book of the Saviors)": """
1. And Jesus continued again in the discourse and said unto his disciples: It came to pass, when I had come to the sphere of Fate, that I changed their paths and their courses according as they were appointed.
2. And Pistis Sophia cried out exceedingly; she sang praises to the Light of the Treasury which she had seen, for she was surrounded by the archons and the rulers of the darkness.
3. And the first power of the Treasury of Light shone down through the realms, purifying the twelve aeons, so that the light spark should be extracted from the matter of chaos.
4. He who hath ears to hear, let him hear what the Spirit saith unto the powers of the emanations: the light shall overcome the mixture, and Sophia shall return unto her place.
    """,
    "Nag Hammadi (Gospel of Thomas - Selections)": """
Logion 1: Whoever discovers the interpretation of these sayings will not taste death.
Logion 2: Let him who seeks continue seeking until he finds. When he finds, he will become troubled. When he becomes troubled, he will be astonished, and he will rule over the All.
Logion 3: If your leaders say to you, 'Look, the Kingdom is in the sky,' then the birds of the sky will precede you. Rather, the Kingdom is inside of you, and it is outside of you.
Logion 22: When you make the two into one, and when you make the inner like the outer and the outer like the inner, and the upper like the lower, then you will enter the kingdom.
Logion 77: I am the light that is over all things. I am all: from me all came forth, and to me all attained. Split a piece of wood; I am there. Lift up the stone, and you will find me there.
    """,
    "The Bible (Genesis 1 & Revelation 12 Celestial Alignment)": """
Genesis 1:1 In the beginning God created the heaven and the earth.
Genesis 1:14 And God said, Let there be lights in the firmament of the heaven to divide the day from the night; and let them be for signs, and for seasons, and for days, and years.
Genesis 1:16 And God made two great lights; the greater light to rule the day, and the lesser light to rule the night: he made the stars also.
Revelation 12:1 And there appeared a great wonder in heaven; a woman clothed with the sun, and the moon under her feet, and upon her head a crown of twelve stars.
Revelation 12:2 And she being with child cried, travailing in birth, and pained to be delivered.
    """,
    "I Ching (The Book of Changes - Hexagrams 1 & 2)": """
Hexagram 1: QIAN - The Creative (Heaven over Heaven)
The Creative works sublime success, furthering through perseverance. Six unbroken light lines symbolize pure primal power, unceasing vitality, and the celestial father archetype.
Action: Persevere in virtue. The dragon rises from the depths to soar across the heavens.

Hexagram 2: KUN - The Receptive (Earth over Earth)
The Receptive brings about sublime success, furthering through the perseverance of a mare. Six divided Yin lines represent infinite receptivity, quiet devotion, and spatial foundation.
Action: Do not seek to lead; find guidance in following the celestial rhythm.
    """
}

# ---------------------------------------------------------
# SIDEBAR: HARMONIC AUDIO & NEUTRAL OBSERVER INPUTS
# ---------------------------------------------------------

with st.sidebar:
    st.title("💥 Numberin")
    st.caption("Cosmic Frequency & Resonance Suite")
    st.write("---")

    # 1. Harmonic Audio Atmosphere
    st.subheader("🎵 Harmonic Atmosphere")
    audio_source = st.selectbox(
        "Ambient Frequency Track",
        ["432 Hz Pure Sine (Deep Resonance)", "528 Hz DNA / Transformation Tone", "Custom Audio URL / File Upload"]
    )
    
    if audio_source == "432 Hz Pure Sine (Deep Resonance)":
        st.audio("https://ia800108.us.archive.org/11/items/432HzTone/432Hz_2min.mp3")
    elif audio_source == "528 Hz DNA / Transformation Tone":
        st.audio("https://ia801503.us.archive.org/15/items/528HzTone/528Hz_Tone.mp3")
    else:
        uploaded_audio = st.file_uploader("Upload Audio (.mp3, .wav)", type=["mp3", "wav"])
        if uploaded_audio:
            st.audio(uploaded_audio)
        else:
            custom_url = st.text_input("Audio URL:")
            if custom_url:
                st.audio(custom_url)

    st.write("---")

    # 2. General Observer Inputs (Blank / User Controlled)
    st.subheader("👤 Observer Natal Anchor")
    user_name = st.text_input("Your Name / Handle", value="", placeholder="Enter your name...")
    user_birth_date = st.date_input("Your Birth Date", value=datetime.date(2000, 1, 1))
    user_birth_time = st.time_input("Your Birth Time", value=datetime.time(12, 0))
    user_birth_place = st.text_input("Birthplace (City, State/Country)", value="", placeholder="e.g. Naples, FL")

    decimal_hour = user_birth_time.hour + (user_birth_time.minute / 60.0)
    user_lp = calculate_vibrational_root(user_birth_date.strftime("%Y%m%d"))
    user_name_val = calculate_name_vibration(user_name) if user_name else 0
    user_sun_sign = get_approx_sun_sign(user_birth_date.month, user_birth_date.day)
    user_moon = get_lunar_phase_details(user_birth_date.year, user_birth_date.month, user_birth_date.day, decimal_hour)

    if user_name:
        st.markdown(f"**Observer:** `{user_name}`")
    st.markdown(f"**Life Path Number:** `{user_lp}`")
    if user_name_val > 0:
        st.markdown(f"**Name Number:** `{user_name_val}`")
    st.markdown(f"**Sun Sign:** `{user_sun_sign}`")
    st.markdown(f"**Moon Phase:** `{user_moon['phase']}` ({user_moon['illumination']}%)")
    st.write("---")

# ---------------------------------------------------------
# INTUITIVE UNIVERSAL SEARCH BAR & DOSSIER ENGINE
# ---------------------------------------------------------

st.title("💥 Numberin")
st.write("Instant numbers, archetypes, and readings for any name, word, or date.")

search_query = st.text_input(
    "🔍 Enter any name, word, or date:",
    value="",
    placeholder="Type a name like 'Sarah' or a date like '1990-05-15'...",
    help="Type any word or date to immediately calculate its numbers and meaning."
)

if search_query.strip():
    query = search_query.strip()
    digits = [int(c) for c in query if c.isdigit()]
    letters = [c for c in query if c.isalpha()]

    # Case A: Date Search
    if len(digits) >= 4 and len(letters) == 0:
        root_val = reduce_number(sum(digits))
        entry = KNOWLEDGE_BASE.get(str(root_val), KNOWLEDGE_BASE["1"])
        
        astro_notes = ""
        if len(digits) == 8:
            try:
                y = int("".join(str(d) for d in digits[0:4]))
                m = int("".join(str(d) for d in digits[4:6]))
                d = int("".join(str(d) for d in digits[6:8]))
                sun = get_approx_sun_sign(m, d)
                lunar = get_lunar_phase_details(y, m, d)
                astro_notes = f"\n* **Sun Sign:** {sun}\n* **Moon Phase:** {lunar['phase']} ({lunar['illumination']}% illuminated)"
            except Exception:
                pass

        st.success(f"### 🗓️ Date Analysis: Root Number {root_val}")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Life Path Root", f"{root_val}")
        col_m2.metric("Archetype", entry['archetype'])

        st.markdown(f"**Core Archetype:** **{entry['archetype']}** ({entry['element']})")
        st.markdown(f"**Key Traits:** {entry['keyword']}{astro_notes}")
        st.info(f"**Reading Insight:**\n\n{entry['reading']}")

        card_text = f"NUMBERIN READING CARD\nDate: {query}\nRoot: {root_val}\nArchetype: {entry['archetype']}\nTraits: {entry['keyword']}\nReading: {entry['reading']}"
        
        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.download_button(
                "📥 Download Reading Card (.txt)",
                data=card_text,
                file_name=f"numberin_date_{query.replace('-', '_')}.txt"
            )
        with col_b2:
            if st.button("🖨️ Open Print View"):
                st.markdown(
                    f"""
                    <div style="border: 2px solid #888; border-radius: 8px; padding: 20px; background-color: #fcfcfc; color: #111; font-family: monospace;">
                        <h2 style="margin: 0; color: #111;">💥 NUMBERIN DOSSIER CARD</h2>
                        <hr/>
                        <p><b>Target Date:</b> {query}</p>
                        <p><b>Life Path Root:</b> {root_val}</p>
                        <p><b>Archetype:</b> {entry['archetype']} ({entry['element']})</p>
                        <p><b>Traits:</b> {entry['keyword']}</p>
                        <p><b>Reading:</b> {entry['reading']}</p>
                    </div>
                    <script>window.print();</script>
                    """,
                    unsafe_allow_html=True
                )

    # Case B: Name or Word Search
    else:
        pyth_val = calculate_name_vibration(query, "Pythagorean")
        chald_val = calculate_name_vibration(query, "Chaldean")
        entry = KNOWLEDGE_BASE.get(str(pyth_val), KNOWLEDGE_BASE["1"])

        st.success(f"### ✨ Reading for: {query.title()}")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Primary Number", f"{pyth_val}")
        col_m2.metric("Chaldean Vibration", f"{chald_val}")
        col_m3.metric("Archetype", entry['archetype'])

        st.markdown(f"**Your Archetype:** **{entry['archetype']}** (Element: `{entry['element']}`)")
        st.markdown(f"**Traits & Energy:** {entry['keyword']}")
        st.info(f"**Personal Meaning:**\n\n{entry['reading']}")

        card_text = f"NUMBERIN READING CARD\nName/Word: {query}\nPrimary Number: {pyth_val}\nChaldean Number: {chald_val}\nArchetype: {entry['archetype']}\nTraits: {entry['keyword']}\nReading: {entry['reading']}"
        
        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            st.download_button(
                "📥 Download Reading Card (.txt)",
                data=card_text,
                file_name=f"numberin_reading_{query.lower().replace(' ', '_')}.txt"
            )
        with col_b2:
            if st.button("🖨️ Open Print View"):
                st.markdown(
                    f"""
                    <div style="border: 2px solid #888; border-radius: 8px; padding: 20px; background-color: #fcfcfc; color: #111; font-family: monospace;">
                        <h2 style="margin: 0; color: #111;">💥 NUMBERIN DOSSIER CARD</h2>
                        <hr/>
                        <p><b>Target:</b> {query}</p>
                        <p><b>Primary Number:</b> {pyth_val} | <b>Chaldean:</b> {chald_val}</p>
                        <p><b>Archetype:</b> {entry['archetype']} ({entry['element']})</p>
                        <p><b>Traits:</b> {entry['keyword']}</p>
                        <p><b>Reading:</b> {entry['reading']}</p>
                    </div>
                    <script>window.print();</script>
                    """,
                    unsafe_allow_html=True
                )

st.write("---")

# ---------------------------------------------------------
# WORKBENCH MODULE TABS
# ---------------------------------------------------------

tab_milestones, tab_oracle, tab_compat, tab_patterns, tab_knowledge = st.tabs([
    "🌌 Milestone Timeline Lens",
    "♈ Decan Oracle",
    "💫 Compatibility Matrix",
    "🔍 Pattern & Frequency Engine",
    "📖 Book of Knowledge & Sacred Texts"
])

# TAB 1: MILESTONE TIMELINE LENS & READINGS (CUSTOM & PRE-SET)
with tab_milestones:
    st.header("Chronos & Cosmos: Milestone Timeline")
    st.caption("Cross-reference historical dates against celestial events, eclipses, and personal resonance.")

    timeline_mode = st.radio(
        "Timeline Selection Mode:",
        ["Choose Pre-Set Turning Point", "Enter Any Custom Date"],
        horizontal=True
    )

    if timeline_mode == "Choose Pre-Set Turning Point":
        selected_milestone = st.selectbox(
            "Select Historical or Cosmic Turning Point:",
            list(MILESTONES.keys()),
            index=0
        )
        m_info = MILESTONES[selected_milestone]
        target_year = m_info["year"]
        target_month = m_info["month"]
        target_day = m_info["day"]
        date_display = m_info["date_str"]
        category_display = m_info["category"]
        astro_display = m_info["astronomy"]
        details_display = m_info["details"]
    else:
        custom_input_date = st.date_input("Pick or Type Any Milestone Date:", value=datetime.date.today())
        target_year = custom_input_date.year
        target_month = custom_input_date.month
        target_day = custom_input_date.day
        date_display = custom_input_date.strftime("%Y-%m-%d")
        category_display = "Custom Inquired Timeline"
        astro_display = "Dynamic calculated astronomical phase for selected date."
        details_display = f"Custom timeline probe for {date_display}."

    m_lunar = get_lunar_phase_details(target_year, target_month, target_day)
    m_root = calculate_vibrational_root(date_display)
    m_compat = evaluate_compatibility(user_lp, m_root)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Date", date_display)
    c2.metric("Lunar Phase", m_lunar["phase"])
    c3.metric("Illumination", f"{m_lunar['illumination']}%")
    c4.metric("Milestone Root", f"Root {m_root}")

    st.markdown("---")
    col_hist, col_read = st.columns([1.2, 1])

    with col_hist:
        st.subheader("📜 Historical & Celestial Chronicle")
        st.markdown(f"**Category:** *{category_display}*")
        st.info(f"**Astronomical Occurrence:**\n\n{astro_display}")
        st.write(details_display)

    with col_read:
        st.subheader("⚡ Synchronicity Reading")
        display_label = user_name if user_name else "Observer"
        st.markdown(f"**{display_label}** | Life Path `{user_lp}`  ↔  Milestone `{m_root}`")
        st.metric("Resonance Index", f"{m_compat['score']}%")
        st.success(m_compat['description'])
        st.markdown(f"""
        * **Lunar Dynamics:** Observer phase: **{user_moon['phase']}** ({user_moon['illumination']}%), Milestone phase: **{m_lunar['phase']}** ({m_lunar['illumination']}%).
        * **Solar Anchor:** {user_sun_sign} alignment across historic coordinates.
        """)

# TAB 2: DECAN ORACLE & RADIAL SPOKES
with tab_oracle:
    st.header("Decan Oracle & Zodiac Coordinates")
    st.caption("Ptolemaic decans and planetary rulers mapped across 30° radial increments.")

    default_sign_index = list(ZODIAC_DECANS.keys()).index(user_sun_sign) if user_sun_sign in ZODIAC_DECANS else 0
    sign = st.selectbox("Explore Zodiac Sector:", list(ZODIAC_DECANS.keys()), index=default_sign_index)
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

# TAB 3: COMPATIBILITY / SYNASTRY MATRIX
with tab_compat:
    st.header("Synastry & Resonant Compatibility")
    st.caption("Compare your vibrational anchor with a partner, collaborator, or specific calendar date.")

    comp_type = st.radio("Comparison Mode", ["Compare with another Person", "Compare with an Event / Date"], horizontal=True)

    if comp_type == "Compare with another Person":
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            p_name = st.text_input("Partner / Peer Name", value="", placeholder="Enter companion name...")
            p_date = st.date_input("Partner Natal Date", value=datetime.date(1995, 1, 1))
        with col_p2:
            p_time = st.time_input("Partner Birth Time", value=datetime.time(12, 0))
            p_place = st.text_input("Partner Birthplace", value="", placeholder="City, Country...")

        p_dec_hour = p_time.hour + (p_time.minute / 60.0)
        p_root = calculate_vibrational_root(p_date.strftime("%Y%m%d"))
        p_moon = get_lunar_phase_details(p_date.year, p_date.month, p_date.day, p_dec_hour)
        p_sun = get_approx_sun_sign(p_date.month, p_date.day)
        
        result = evaluate_compatibility(user_lp, p_root)
        
        c_a, c_b, c_c = st.columns(3)
        c_a.metric("Observer Life Path", user_lp)
        c_b.metric("Partner Life Path", p_root)
        c_c.metric("Compatibility Index", f"{result['score']}%")

        st.info(f"**Synastry Dynamic:** {result['description']}")
        st.write(f"* **Interaction Matrix:** Observer ({user_sun_sign} / {user_moon['phase']}) transiting with Companion ({p_sun} / {p_moon['phase']}).")

    else:
        target_date = st.date_input("Target Date for Assessment", value=datetime.date.today())
        t_root = calculate_vibrational_root(target_date.strftime("%Y%m%d"))
        t_moon = get_lunar_phase_details(target_date.year, target_date.month, target_date.day)
        
        result = evaluate_compatibility(user_lp, t_root)
        
        c_a, c_b = st.columns(2)
        c_a.metric("Target Date Vibration", f"Root {t_root}")
        c_b.metric("Day Alignment Index", f"{result['score']}%")
        st.info(f"**Day Resonance:** {result['description']}")

# TAB 4: PATTERN & FREQUENCY ENGINE
with tab_patterns:
    st.header("Pattern & Frequency Analysis")
    st.caption("Translate arbitrary sequences, words, or custom names into distribution patterns.")

    user_text = st.text_input("Input Word, Cipher Phrase, or Sequence:", value="As Above So Below")
    
    pyth_val = calculate_name_vibration(user_text, "Pythagorean")
    chald_val = calculate_name_vibration(user_text, "Chaldean")

    k1, k2 = st.columns(2)
    k1.metric("Pythagorean Root", pyth_val)
    k2.metric("Chaldean Root", chald_val)

    cleaned_text = [c.upper() for c in user_text if c.isalpha()]
    char_freq = {}
    for c in cleaned_text:
        char_freq[c] = char_freq.get(c, 0) + 1

    st.subheader("Vibrational Distribution")
    st.bar_chart(char_freq)

# TAB 5: BOOK OF KNOWLEDGE & SACRED TEXTS
with tab_knowledge:
    st.header("📖 The Book of Knowledge & Sacred Oracle Library")
    st.caption("Canonical wisdom texts, Gnostic treatises, cosmological revelations, and document image scanner.")

    know_section = st.radio(
        "Knowledge Navigation",
        ["📜 Sacred Texts & Oracle Workbench", "🔢 Vibrational Root Definitions", "🖼️ Scan & Analyze Manuscript Page (JPEG)"],
        horizontal=True
    )

    if know_section == "📜 Sacred Texts & Oracle Workbench":
        st.subheader("Oracle Reading & Hidden Pattern Finder")
        st.write("Select a pre-loaded sacred text to decipher its verses, calculate root numerical frequencies, and reveal hidden synchronicities.")

        chosen_book = st.selectbox("Select Canonical Sacred Text:", list(PRELOADED_TEXTS.keys()))
        book_content = PRELOADED_TEXTS[chosen_book]

        st.text_area("Original Text Excerpt", book_content.strip(), height=200)

        st.markdown("#### 🔍 Oracle Pattern & Hidden Meaning Extraction")
        search_kw = st.text_input("Filter for Word, Symbol, or Verse Number in Text:", value="light")
        
        matching_lines = [line.strip() for line in book_content.split('\n') if search_kw.lower() in line.lower() and line.strip()]

        if matching_lines:
            st.success(f"Found {len(matching_lines)} resonant passages containing '{search_kw}':")
            for idx, passage in enumerate(matching_lines):
                line_pyth = calculate_name_vibration(passage, "Pythagorean")
                line_chald = calculate_name_vibration(passage, "Chaldean")
                with st.expander(f"Passage {idx + 1} | Pyth Root {line_pyth} | Chald Root {line_chald}"):
                    st.write(f"> *{passage}*")
                    passage_compat = evaluate_compatibility(user_lp, line_pyth)
                    st.info(f"**Observer Resonance with Verse:** {passage_compat['description']} (Index: {passage_compat['score']}%)")
        else:
            st.warning(f"No direct lines found containing '{search_kw}'. Try terms like 'heaven', 'moon', 'one', or 'sun'.")

    elif know_section == "🔢 Vibrational Root Definitions":
        st.subheader("Canonical Archetypes & Geometric Roots")
        selected_number = st.selectbox("Consult Number Root:", list(KNOWLEDGE_BASE.keys()))
        entry = KNOWLEDGE_BASE[selected_number]

        b1, b2 = st.columns(2)
        with b1:
            st.markdown(f"### Root {selected_number}: {entry['archetype']}")
            st.markdown(f"**Elemental Current:** `{entry['element']}`")
            st.markdown(f"**Key Vibrations:** `{entry['keyword']}`")
            st.write(f"**Full Reading Matrix:** {entry['reading']}")

        with b2:
            st.markdown("### Lunar Phase Esotericism")
            st.write("""
            * **New Moon (Conjunction):** Seed point of pure intent, unmanifest potential, and initiation.
            * **Crescent & Quarter:** Momentum building, navigating resistance, anchoring structure.
            * **Full Moon (Opposition):** Total illumination, confrontation of polarities, and revelations.
            * **Waning Phases:** Synthesis, harvesting wisdom, releasing outworn cycles.
            """)

    else:
        st.subheader("🖼️ Manuscript & Page Image Scanner")
        st.caption("Upload JPEG / PNG images of ancient book folios, manuscripts, or diagrams for visual inspection and oracle notations.")

        uploaded_img = st.file_uploader("Upload Image File (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])
        if uploaded_img is not None:
            image = Image.open(uploaded_img)
            col_img1, col_img2 = st.columns([1.5, 1])
            with col_img1:
                st.image(image, caption=f"Uploaded Folio / Page: {uploaded_img.name}", use_container_width=True)
            with col_img2:
                st.markdown("### 📝 Folio Analysis & Cipher Notes")
                folio_label = st.text_input("Folio / Spoke Coordinate Label:", value="Folio-Alpha")
                notes = st.text_area("Decipherment & Symbol Observations:", height=150, placeholder="Record astronomical glyphs, decan spokes, or marginalia cipher values...")
                if st.button("Save Notations to Memory"):
                    label_root = calculate_name_vibration(folio_label, "Pythagorean")
                    st.success(f"Logged {folio_label} (Vibrational Root: {label_root}) into workbench context.")
