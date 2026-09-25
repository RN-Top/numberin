import streamlit as st
import datetime
import math
import re
from collections import Counter
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
# MATHEMATICAL, CIPHER & ASTRONOMICAL ENGINES
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
    while n > 9:
        if keep_master and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

def calculate_name_vibration(name: str, cipher: str = "Pythagorean") -> int:
    mapping = PYTHAGOREAN_MAP if cipher == "Pythagorean" else CHALDEAN_MAP
    total = sum(mapping.get(char.upper(), 0) for char in name if char.isalpha())
    return reduce_number(total) if total > 0 else 0

def get_julian_date(year: int, month: int, day: int, hour: float = 12.0) -> float:
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    day_fraction = day + (hour / 24.0)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day_fraction + b - 1524.5

def get_lunar_phase_details(year: int, month: int, day: int, hour: float = 12.0) -> dict:
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
    digits = [int(c) for c in str(date_str) if c.isdigit()]
    return reduce_number(sum(digits)) if digits else 1

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
# CONSTANTS & REPOSITORIES
# ---------------------------------------------------------

HEPTAGRAM_777 = {
    0: {"day": "Monday", "planet": "Moon ☽", "metal": "Silver", "essence": "Fluidity, Memory, Subconscious", "tincture": "The White Elixir (Albedo)"},
    1: {"day": "Tuesday", "planet": "Mars ♂", "metal": "Iron", "essence": "Kinetic Drive, Severing, Heat", "tincture": "The Martial Tincture"},
    2: {"day": "Wednesday", "planet": "Mercury ☿", "metal": "Quicksilver", "essence": "Volatile Synthesis, Transmutation", "tincture": "The Philosophic Mercury"},
    3: {"day": "Thursday", "planet": "Jupiter ♃", "metal": "Tin", "essence": "Expansion, Cohesion, Royalty", "tincture": "The Tincture of Saffron"},
    4: {"day": "Friday", "planet": "Venus ♀", "metal": "Copper", "essence": "Harmonic Affinity, Binding Love", "tincture": "The Emerald Tincture"},
    5: {"day": "Saturday", "planet": "Saturn ♄", "metal": "Lead", "essence": "Nigredo, Structure, Fixation", "tincture": "The Black Stone of Saturn"},
    6: {"day": "Sunday", "planet": "Sun ☉", "metal": "Gold", "essence": "Pure Spirit, Rubedo, Solar Will", "tincture": "The Aurum Potabile (Gold Elixir)"}
}

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
    "American Declaration of Independence": {
        "date_str": "1776-07-04", "year": 1776, "month": 7, "day": 4,
        "category": "Historical Foundation",
        "astronomy": "Waning Gibbous Moon transiting Aquarius into Pisces.",
        "details": "Foundational charter signed under Cancer Sun with high retrograde planetary dispersion."
    },
    "Crucifixion Blood Moon (Passover)": {
        "date_str": "0033-04-03", "year": 33, "month": 4, "day": 3,
        "category": "Sacred History",
        "astronomy": "Blood Red Lunar Eclipse at moonrise over Jerusalem during Passover (14 Nisan).",
        "details": "Concurs with scriptural records of darkening skies. Astronomical back-calculations verify lunar eclipse in Virgo."
    },
    "Annus Lucis / Creation Epoch": {
        "date_str": "-4004-10-23", "year": -4004, "month": 10, "day": 23,
        "category": "Biblical & Hermetic",
        "astronomy": "Equinoctial conjunction matching Archbishop Ussher's canonical chronology.",
        "details": "Zero-point marker encoding foundational creation mathematics across classical traditions."
    },
    "WW1 Outbreak (1914 Epoch)": {
        "date_str": "1914-07-28", "year": 1914, "month": 7, "day": 28,
        "category": "Modern Eschatology",
        "astronomy": "Waxing Crescent Moon transiting into Libra; solar eclipse followed on August 21, 1914.",
        "details": "Historic biblical scholarship epoch signaling systemic global transition."
    },
    "The Great Year Solstice Precession": {
        "date_str": "2012-12-21", "year": 2012, "month": 12, "day": 21,
        "category": "Cosmic Precession",
        "astronomy": "Solstice Sun aligned with the Galactic Equator, closing the ~25,772-year cycle.",
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

PRELOADED_LIBRARIES = {
    "The Book of Enoch (Full Luminaries - Ch. 72-74)": """
1. The book of the courses of the luminaries of the heaven, the relations of each, according to their classes, their dominion and their seasons, according to their names and places of origin, and according to their months.
2. First there goes forth the great luminary, named the Sun, and his circumference is like the circumference of the heaven, and he is quite filled with illuminating and heating fire.
3. The chariot on which he mounts, the wind drives, and the sun goes down from the heaven as he returns through the north in order to reach the east, and is so led that he comes to the appropriate portal and shines in the face of the heaven.
4. In this manner he rises in the first month in the great portal, which is the fourth portal of the six portals in the cast.
5. And in that fourth portal from which the sun rises in the first month are twelve window-openings, from which proceed a flame when they are opened in their season.
6. When the sun rises in the heaven, he comes forth through that fourth portal thirty mornings in succession, and sets accurately in the fourth portal in the west of the heaven.
7. And during this period the day becomes daily longer and the night nightly shorter to the thirtieth morning.
8. On that day the day is longer than the night by a ninth part, and the day amounts exactly to ten parts and the night to eight parts.
9. And the sun rises from that fourth portal, and sets in the fourth, and returns to the fifth portal of the east thirty mornings, and rises from it and sets in the fifth portal.
10. And then the day becomes longer by two parts and amounts to eleven parts, and the night becomes shorter and amounts to seven parts.
11. And the sun returns to the east and enters into the sixth portal, and rises and sets in the sixth portal one-and-thirty mornings on account of its sign.
12. On that day the day becomes longer than the night, and the day becomes double the night, and the day becomes twelve parts, and the night is shortened and becomes six parts.
    """,
    "Nag Hammadi: The Gospel of Thomas (Complete Core Logia)": """
Logion 1: Whoever discovers the interpretation of these sayings will not taste death.
Logion 2: Let him who seeks continue seeking until he finds. When he finds, he will become troubled. When he becomes troubled, he will be astonished, and he will rule over the All.
Logion 3: If your leaders say to you, 'Look, the Kingdom is in the sky,' then the birds of the sky will precede you. Rather, the Kingdom is inside of you, and it is outside of you.
Logion 4: The man old in days will not hesitate to ask a small child seven days old about the place of life, and he will live. For many who are first will become last, and they will become one and the same.
Logion 5: Recognize what is before your face, and that which is hidden from you will be revealed to you. For there is nothing hidden that will not be made manifest.
Logion 22: When you make the two into one, and when you make the inner like the outer and the outer like the inner, and the upper like the lower, then you will enter the kingdom.
Logion 77: I am the light that is over all things. I am all: from me all came forth, and to me all attained. Split a piece of wood; I am there. Lift up the stone, and you will find me there.
Logion 113: His disciples said to him, 'When will the Kingdom come?' Jesus said, 'It will not come by waiting for it. Rather, the Kingdom of the Father is spread out upon the earth, and men do not see it.'
    """,
    "Pistis Sophia: The Ascent & Treasury of Light": """
1. And Jesus continued again in the discourse and said unto his disciples: It came to pass, when I had come to the sphere of Fate, that I changed their paths and their courses according as they were appointed.
2. And Pistis Sophia cried out exceedingly; she sang praises to the Light of the Treasury which she had seen, for she was surrounded by the archons and the rulers of the darkness.
3. And the first power of the Treasury of Light shone down through the realms, purifying the twelve aeons, so that the light spark should be extracted from the matter of chaos.
4. The Lion-faced power, which is the half-light, had swallowed all the light-powers in Sophia and purged her strength into the deep matter.
5. And Sophia cried: O Light of Lights, in whom I have had faith from the beginning, hearken now unto my repentance; deliver my light from the emanations of Self-willed.
6. Then the Mystery commanded a great light-stream to descend from the first commandment, shining with twelve seals of light to liberate her soul into the thirteenth aeon.
    """,
    "Biblical Revelation & Genesis Alignment": """
Genesis 1:1 In the beginning God created the heaven and the earth.
Genesis 1:14 And God said, Let there be lights in the firmament of the heaven to divide the day from the night; and let them be for signs, and for seasons, and for days, and years.
Genesis 1:16 And God made two great lights; the greater light to rule the day, and the lesser light to rule the night: he made the stars also.
Revelation 12:1 And there appeared a great wonder in heaven; a woman clothed with the sun, and the moon under her feet, and upon her head a crown of twelve stars.
Revelation 12:2 And she being with child cried, travailing in birth, and pained to be delivered.
Revelation 21:1 And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away; and there was no more sea.
Revelation 22:13 I am Alpha and Omega, the beginning and the end, the first and the last.
    """,
    "I Ching (Hexagrams 1 & 2 Canonical Excerpt)": """
Hexagram 1: QIAN - The Creative (Heaven over Heaven). The Creative works sublime success, furthering through perseverance.
Six unbroken light lines symbolize pure primal power, unceasing vitality, and the celestial father archetype.
Action: Persevere in virtue. The dragon rises from the depths to soar across the heavens.
Hexagram 2: KUN - The Receptive (Earth over Earth). The Receptive brings about sublime success, furthering through the perseverance of a mare.
Six divided Yin lines represent infinite receptivity, quiet devotion, and spatial foundation.
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

    # Harmonic Audio Controls
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

    # Observer Anchors (Using clean number inputs to avoid mobile picker validation crashes)
    st.subheader("👤 Observer Natal Anchor")
    user_name = st.text_input("Your Name / Handle", value="", placeholder="Enter name...")

    c_by, c_bm, c_bd = st.columns([1.2, 1, 1])
    with c_by:
        user_year = st.number_input("Year", min_value=-5000, max_value=2100, value=1983, step=1)
    with c_bm:
        user_month = st.number_input("Month", min_value=1, max_value=12, value=11, step=1)
    with c_bd:
        user_day = st.number_input("Day", min_value=1, max_value=31, value=19, step=1)

    user_time_str = st.text_input("Birth Time (HH:MM 24hr)", value="12:00")
    try:
        th, tm = [int(p) for p in user_time_str.split(":")[:2]]
    except Exception:
        th, tm = 12, 0
    decimal_hour = th + (tm / 60.0)

    user_birth_place = st.text_input("Birthplace", value="", placeholder="e.g. Naples, FL")

    user_date_str = f"{abs(user_year):04d}{user_month:02d}{user_day:02d}"
    user_lp = calculate_vibrational_root(user_date_str)
    user_name_val = calculate_name_vibration(user_name) if user_name else 0
    user_sun_sign = get_approx_sun_sign(user_month, user_day)
    user_moon = get_lunar_phase_details(user_year, user_month, user_day, decimal_hour)

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
    placeholder="Type a name like 'Sarah' or a date like '1776-07-04'...",
    help="Type any word or date to immediately calculate its numbers and meaning."
)

if search_query.strip():
    query = search_query.strip()
    digits = [int(c) for c in query if c.isdigit()]
    letters = [c for c in query if c.isalpha()]

    # Case A: Date Analysis
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
    # Case B: Name or Word Analysis
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

tab_milestones, tab_oracle, tab_alembic, tab_compat, tab_patterns, tab_knowledge = st.tabs([
    "🌌 Milestone Timeline Lens",
    "♈ Decan Oracle",
    "⚗️ 7-7-7 Alchemical Lens",
    "💫 Compatibility Matrix",
    "🔍 Pattern & Frequency Engine",
    "📖 Books of Knowledge & Deep Corpus Engine"
])

# TAB 1: MILESTONE TIMELINE LENS
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
        st.write("**Enter Custom Date (BCE/CE):**")
        col_cy, col_cm, col_cd = st.columns([1.5, 1, 1])
        with col_cy:
            target_year = st.number_input("Year (e.g. 1776, -4004)", min_value=-10000, max_value=10000, value=1776, step=1, key="m_cust_yr")
        with col_cm:
            target_month = st.number_input("Month (1-12)", min_value=1, max_value=12, value=7, step=1, key="m_cust_mo")
        with col_cd:
            target_day = st.number_input("Day (1-31)", min_value=1, max_value=31, value=4, step=1, key="m_cust_dy")

        date_display = f"{target_year:04d}-{target_month:02d}-{target_day:02d}"
        category_display = "Custom Timeline Probe"
        astro_display = "Calculated synodic position and lunar phase for queried date."
        details_display = f"Custom historical calculation for {date_display}."

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

# TAB 3: 7-7-7 ALCHEMICAL LENS (ALEMBIC & CUCURBIT)
with tab_alembic:
    st.header("⚗️ The 7-7-7 Alchemical Lens")
    st.caption("Distillation of raw matter through the 7 Planets, 7 Metals, and 7 Days of the Week.")

    col_alembic_in1, col_alembic_in2 = st.columns([1.5, 1])

    with col_alembic_in1:
        st.subheader("1. The Cucurbit (Prima Materia / Raw Vessel)")
        prima_text = st.text_input(
            "Input Subject / Cipher to Distill:",
            value=user_name if user_name else "Philosopher Stone"
        )
        st.write("**Distillation Epoch Coordinates:**")
        c_ay, c_am, c_ad = st.columns(3)
        with c_ay:
            a_year = st.number_input("Operation Year", min_value=-5000, max_value=5000, value=2026, step=1, key="alch_yr")
        with c_am:
            a_month = st.number_input("Operation Month", min_value=1, max_value=12, value=9, step=1, key="alch_mo")
        with c_ad:
            a_day = st.number_input("Operation Day", min_value=1, max_value=31, value=25, step=1, key="alch_dy")

    try:
        op_date = datetime.date(abs(a_year), a_month, a_day)
        day_idx = op_date.weekday()
    except Exception:
        day_idx = 0

    hept = HEPTAGRAM_777[day_idx]
    prima_pyth = calculate_name_vibration(prima_text, "Pythagorean")
    date_root = calculate_vibrational_root(f"{abs(a_year):04d}{a_month:02d}{a_day:02d}")

    spirit_val = prima_pyth
    salt_val = date_root
    sulfur_val = (day_idx + 1)
    magnum_root = reduce_number(spirit_val + salt_val + sulfur_val)

    with col_alembic_in2:
        st.subheader("2. The Alembic Beak (Planetary Alignment)")
        st.info(f"""
        * **Operational Day:** **{hept['day']}**
        * **Governing Sphere:** **{hept['planet']}**
        * **Alchemical Metal:** **{hept['metal']}**
        * **Principle:** *{hept['essence']}*
        """)

    st.markdown("---")
    st.subheader("3. The Receiver (The Distilled Elixir)")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Spirit (Volatile)", f"Root {spirit_val}")
    r2.metric("Salt (Fixed Body)", f"Root {salt_val}")
    r3.metric("Sulfur (Governing Metal)", f"{hept['metal']}")
    r4.metric("Distillate Nexus", f"Root {magnum_root}")

    if magnum_root in [1, 5, 9]:
        alch_stage = "Nigredo (Calcination & Blackening)"
        stage_desc = "Breaking down rigid constructs to purify the root essence."
    elif magnum_root in [2, 6]:
        alch_stage = "Albedo (The White Work / Washing)"
        stage_desc = "Lunar purification, clarity, and crystallization of inner stillness."
    elif magnum_root in [3, 7]:
        alch_stage = "Citrinitas (The Yellow Dawn / Awakening)"
        stage_desc = "Solar illumination awakening theoretical symbols into living understanding."
    else:
        alch_stage = "Rubedo (The Red Work / Consummation)"
        stage_desc = "Full manifestation and complete alignment between the volatile spirit and fixed vessel."

    st.markdown(f"### Distillation Phase: **{alch_stage}**")
    st.markdown(f"**Resulting Tincture:** `{hept['tincture']}`")
    st.success(f"**Alchemical Reading:** {stage_desc}")

    alembic_card = f"NUMBERIN 7-7-7 ALCHEMICAL DOSSIER\nSubject: {prima_text}\nDate: {a_year:04d}-{a_month:02d}-{a_day:02d} ({hept['day']})\nPlanet: {hept['planet']}\nMetal: {hept['metal']}\nNexus: Root {magnum_root}\nStage: {alch_stage}\nTincture: {hept['tincture']}"
    st.download_button(
        "📥 Download Alchemical Dossier (.txt)",
        data=alembic_card,
        file_name=f"alchemical_distill_{prima_text.lower().replace(' ', '_')}.txt"
    )

# TAB 4: COMPATIBILITY / SYNASTRY MATRIX
with tab_compat:
    st.header("Synastry & Resonant Compatibility")
    st.caption("Compare your vibrational anchor with a partner, collaborator, or specific calendar date.")

    comp_type = st.radio("Comparison Mode", ["Compare with another Person", "Compare with an Event / Date"], horizontal=True)

    if comp_type == "Compare with another Person":
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            p_name = st.text_input("Partner / Peer Name", value="", placeholder="Enter companion name...")
            col_py, col_pm, col_pd = st.columns(3)
            with col_py:
                p_year = st.number_input("Year ", min_value=1900, max_value=2100, value=1995, step=1, key="p_yr")
            with col_pm:
                p_month = st.number_input("Month ", min_value=1, max_value=12, value=1, step=1, key="p_mo")
            with col_pd:
                p_day = st.number_input("Day ", min_value=1, max_value=31, value=1, step=1, key="p_dy")
        with col_p2:
            p_time_str = st.text_input("Partner Birth Time (HH:MM)", value="12:00", key="p_tm")
            try:
                pth, ptm = [int(p) for p in p_time_str.split(":")[:2]]
            except Exception:
                pth, ptm = 12, 0
            p_place = st.text_input("Partner Birthplace", value="", placeholder="City, Country...", key="p_plc")

        p_dec_hour = pth + (ptm / 60.0)
        p_date_str = f"{p_year:04d}{p_month:02d}{p_day:02d}"
        p_root = calculate_vibrational_root(p_date_str)
        p_moon = get_lunar_phase_details(p_year, p_month, p_day, p_dec_hour)
        p_sun = get_approx_sun_sign(p_month, p_day)
        
        result = evaluate_compatibility(user_lp, p_root)
        
        c_a, c_b, c_c = st.columns(3)
        c_a.metric("Observer Life Path", user_lp)
        c_b.metric("Partner Life Path", p_root)
        c_c.metric("Compatibility Index", f"{result['score']}%")

        st.info(f"**Synastry Dynamic:** {result['description']}")
        st.write(f"* **Interaction Matrix:** Observer ({user_sun_sign} / {user_moon['phase']}) transiting with Companion ({p_sun} / {p_moon['phase']}).")

    else:
        col_ty, col_tm, col_td = st.columns(3)
        with col_ty:
            t_year = st.number_input("Target Year", min_value=-5000, max_value=5000, value=2026, step=1, key="t_yr")
        with col_tm:
            t_month = st.number_input("Target Month", min_value=1, max_value=12, value=9, step=1, key="t_mo")
        with col_td:
            t_day = st.number_input("Target Day", min_value=1, max_value=31, value=25, step=1, key="t_dy")

        t_date_str = f"{t_year:04d}{t_month:02d}{t_day:02d}"
        t_root = calculate_vibrational_root(t_date_str)
        t_moon = get_lunar_phase_details(t_year, t_month, t_day)
        
        result = evaluate_compatibility(user_lp, t_root)
        
        c_a, c_b = st.columns(2)
        c_a.metric("Target Date Vibration", f"Root {t_root}")
        c_b.metric("Day Alignment Index", f"{result['score']}%")
        st.info(f"**Day Resonance:** {result['description']}")

# TAB 5: PATTERN & FREQUENCY ENGINE
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

# TAB 6: BOOKS OF KNOWLEDGE & DEEP CORPUS ENGINE
with tab_knowledge:
    st.header("📖 Books of Knowledge & Deep Corpus Engine")
    st.caption("Analyze full pre-loaded books or upload custom treatises to detect patterns, anomalies, and generate readings on raw data.")

    source_type = st.radio(
        "Corpus Source:",
        ["Select Pre-Loaded Canonical Book", "Upload Custom Book / Manuscript (.txt)", "Scan Manuscript Page Image (JPEG/PNG)"],
        horizontal=True
    )

    corpus_text = ""
    active_book_title = ""

    if source_type == "Select Pre-Loaded Canonical Book":
        active_book_title = st.selectbox("Select Canonical Work:", list(PRELOADED_LIBRARIES.keys()))
        corpus_text = PRELOADED_LIBRARIES[active_book_title].strip()
    elif source_type == "Upload Custom Book / Manuscript (.txt)":
        uploaded_doc = st.file_uploader("Upload Text Document (.txt)", type=["txt"])
        if uploaded_doc:
            corpus_text = uploaded_doc.read().decode("utf-8", errors="ignore")
            active_book_title = uploaded_doc.name
            st.success(f"Loaded '{active_book_title}' ({len(corpus_text):,} characters).")
        else:
            corpus_text = PRELOADED_LIBRARIES["The Book of Enoch (Full Luminaries - Ch. 72-74)"].strip()
            active_book_title = "The Book of Enoch (Default)"
    else:
        st.subheader("🖼️ Visual Manuscript Page Inspector")
        uploaded_img = st.file_uploader("Upload Page/Folio (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])
        if uploaded_img is not None:
            image = Image.open(uploaded_img)
            col_img1, col_img2 = st.columns([1.5, 1])
            with col_img1:
                st.image(image, caption=f"Loaded Folio: {uploaded_img.name}", use_container_width=True)
            with col_img2:
                folio_label = st.text_input("Folio Coordinate / Identification:", value="Folio-Alpha")
                notes = st.text_area("Decipherment & Symbol Observations:", height=150, placeholder="Transcribe words, glyphs, or structural anomalies...")
                if st.button("Log Folio to Reading Engine"):
                    l_root = calculate_name_vibration(folio_label, "Pythagorean")
                    st.success(f"Logged {folio_label} (Vibrational Root: {l_root}) into workbench context.")

    if corpus_text:
        st.markdown("---")
        # Text Metrics & Anomaly Engine
        words = re.findall(r'\b[A-Za-z]+\b', corpus_text)
        word_counts = Counter([w.lower() for w in words])
        total_words = len(words)
        unique_words = len(word_counts)
        hapax_legomena = [w for w, c in word_counts.items() if c == 1]
        
        # Calculate root vibration of the entire text
        corpus_root = calculate_name_vibration(corpus_text, "Pythagorean")
        reading_entry = KNOWLEDGE_BASE.get(str(corpus_root), KNOWLEDGE_BASE["1"])

        st.subheader(f"📊 Corpus Diagnostics: {active_book_title}")
        c_c1, c_c2, c_c3, c_c4 = st.columns(4)
        c_c1.metric("Total Words", f"{total_words:,}")
        c_c2.metric("Unique Vocabulary", f"{unique_words:,}")
        c_c3.metric("Oddities (1-time words)", f"{len(hapax_legomena):,}")
        c_c4.metric("Corpus Root", f"Root {corpus_root}")

        # Data-Supplied Reading Section
        st.markdown("### 🔮 Data-Supplied Reading on Loaded Book")
        compat_with_user = evaluate_compatibility(user_lp, corpus_root)
        
        col_read1, col_read2 = st.columns([1.2, 1])
        with col_read1:
            st.info(f"""
            **Corpus Archetype:** **{reading_entry['archetype']}** (Element: `{reading_entry['element']}`)  
            **Guiding Principle:** {reading_entry['keyword']}  
            **Synthesis:** {reading_entry['reading']}
            """)
        with col_read2:
            display_user = user_name if user_name else "Observer"
            st.success(f"""
            **Resonance with {display_user}:**  
            Observer Life Path `{user_lp}`  ↔  Book Root `{corpus_root}`  
            **Index:** `{compat_with_user['score']}%`  
            *{compat_with_user['description']}*
            """)

        # Search, Pattern & Oddity Discovery
        st.markdown("---")
        st.subheader("🔍 Pattern, Word & Anomaly Filter")
        
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            query_word = st.text_input("Find Patterns for Word, Symbol or Phrase:", value="Sun")
        with col_s2:
            filter_mode = st.selectbox("Search Lens:", ["Case-Insensitive Match", "Exact Word Boundary", "Search Hapax / Oddities"])

        if filter_mode == "Search Hapax / Oddities":
            st.markdown(f"**Singular Anomalies (Words appearing only once in the entire book):**")
            st.write(", ".join(hapax_legomena[:100]) + ("..." if len(hapax_legomena) > 100 else ""))
        else:
            if query_word.strip():
                clean_q = query_word.strip()
                pattern = r'\b' + re.escape(clean_q) + r'\b' if filter_mode == "Exact Word Boundary" else re.escape(clean_q)
                
                # Split text into sentences / passages for fine-grained scanning
                sentences = re.split(r'(?<=[.!?\n]) +', corpus_text)
                matches = [s.strip() for s in sentences if re.search(pattern, s, re.IGNORECASE) and s.strip()]

                if matches:
                    st.success(f"Discovered **{len(matches)}** resonant occurrences for '{query_word}':")
                    for i, m in enumerate(matches[:25]):
                        m_pyth = calculate_name_vibration(m, "Pythagorean")
                        m_chald = calculate_name_vibration(m, "Chaldean")
                        with st.expander(f"Match #{i + 1} | Pyth Root {m_pyth} | Chald Root {m_chald}"):
                            st.write(f"> *{m}*")
                            p_eval = evaluate_compatibility(user_lp, m_pyth)
                            st.caption(f"Resonance with Observer: {p_eval['score']}% — {p_eval['description']}")
                    if len(matches) > 25:
                        st.caption(f"*Displaying first 25 of {len(matches)} occurrences.*")
                else:
                    st.warning(f"No direct passages found containing '{query_word}'.")

        # Visual Word Frequency Distribution
        with st.expander("📈 View Top 20 Most Frequent Words"):
            common_words = dict(word_counts.most_common(20))
            st.bar_chart(common_words)
