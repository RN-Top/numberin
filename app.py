import streamlit as st
import streamlit.components.v1 as components
import datetime
import math
import re
import urllib.request
import urllib.parse
import json
import os
from collections import Counter

# Page Configuration
st.set_page_config(page_title="Numberin", page_icon="✨", layout="wide")

# ==========================================
# LUMINOUS BRASS & ETHEREAL GLOW STYLING
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 8%, #1c1813 0%, #0a0c10 100%);
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .brand-title {
        font-family: 'Cinzel', serif !important;
        letter-spacing: 0.08em;
    }

    .brand-title {
        font-size: 2.4rem;
        font-weight: 900;
        color: #fff4cc;
        text-shadow: 0 0 12px rgba(245, 197, 66, 0.75), 0 0 32px rgba(212, 175, 55, 0.45);
        margin-bottom: 2px;
    }

    .brass-panel {
        background: rgba(20, 23, 28, 0.88);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(212, 175, 55, 0.45);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0 24px 0;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.75), inset 0 0 15px rgba(212, 175, 55, 0.12);
    }

    .sidebar-oracle-card {
        background: rgba(26, 22, 16, 0.85);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 8px;
        padding: 14px;
        margin-top: 12px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.6);
    }

    .ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 16px;
        margin: 24px 0;
        flex-wrap: wrap;
    }

    .ring-badge {
        padding: 14px 26px;
        border-radius: 35px;
        border: 2px solid #d4af37;
        background: linear-gradient(145deg, #1c1914, #0b0d10);
        color: #fff1b8;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.05em;
        box-shadow: 0 0 16px rgba(212, 175, 55, 0.4), inset 0 0 8px rgba(212, 175, 55, 0.25);
    }

    .tincture-box {
        background: linear-gradient(135deg, rgba(28, 24, 20, 0.95), rgba(12, 14, 18, 0.95));
        border-left: 4px solid #f5c542;
        border-top: 1px solid rgba(245, 197, 66, 0.25);
        border-right: 1px solid rgba(245, 197, 66, 0.25);
        border-bottom: 1px solid rgba(245, 197, 66, 0.25);
        padding: 22px;
        border-radius: 8px;
        font-size: 1.1rem;
        line-height: 1.8;
        color: #fdfaf0;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    }

    .verse-card {
        background: rgba(18, 21, 28, 0.92);
        border-left: 3px solid #e5a93b;
        border-radius: 6px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        line-height: 1.7;
        font-size: 1.02rem;
        color: #f1f4f8;
    }

    .verse-badge {
        display: inline-block;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        font-size: 0.82rem;
        color: #f5c542;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .mark-glow {
        background: rgba(245, 197, 66, 0.2);
        color: #fff9d6;
        border-bottom: 2px solid #f5c542;
        padding: 1px 4px;
        border-radius: 3px;
        font-weight: 600;
        text-shadow: 0 0 8px rgba(245, 197, 66, 0.6);
    }

    .gematria-pill {
        font-size: 0.82rem;
        padding: 3px 9px;
        border-radius: 12px;
        background: #24221b;
        border: 1px solid #735924;
        color: #d1b46a;
        margin-left: 8px;
    }

    @media print {
        body, .stApp {
            background: #ffffff !important;
            color: #111111 !important;
        }
        .brass-panel, .tincture-box, .verse-card {
            background: #ffffff !important;
            color: #111111 !important;
            border: 1px solid #999999 !important;
            box-shadow: none !important;
        }
        header, footer, [data-testid="stSidebar"] {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. CONSTANTS & SYSTEM MAPPINGS
# ==========================================

PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

CHALDEAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

ANGEL = {
    "111": "Alignment and fresh creation. The door is unlatched.",
    "222": "Patience and balance. Do not force growth before the root takes.",
    "333": "Expansion and direct expression. The voice finds resonance.",
    "444": "Solid architecture. Practical foundations are anchoring your intent.",
    "555": "Dynamic pivot. The current cycle is loosening its boundaries.",
    "666": "Recalibration between spirit and material obligation.",
    "777": "Inner initiation. Awakening the hidden architecture behind appearances.",
    "888": "Infinite harvest. The return flow of spent energy arrives.",
    "999": "Culmination and release. Clearing ground for the subsequent phase."
}

KARMIC_NOTE = {
    13: "Karmic Debt 13: Grounding effort, clearing resistance through focused construction.",
    14: "Karmic Debt 14: Restoring balance amidst erratic motion and freedom.",
    16: "Karmic Debt 16: The fall of brittle structures; awakening radical truth.",
    19: "Karmic Debt 19: Independence, learning that self-reliance includes vulnerability."
}

PHASE_NUMEROLOGY = {
    "New Moon": 1,
    "Waxing Crescent": 2,
    "First Quarter": 3,
    "Waxing Gibbous": 4,
    "Full Moon": 5,
    "Waning Gibbous": 6,
    "Last Quarter": 7,
    "Waning Crescent": 8
}

MILESTONES = {
    1: "Inception, radical sovereignty, planting raw impulses.",
    2: "Partnership, reflection, subtle relational alignment.",
    3: "Expression, social crystallization, testing creative tone.",
    4: "Form-building, boundaries, establishing bedrock security.",
    5: "Disruption, voyage, untying old moorings.",
    6: "Sanctuary, duty, reconciliation of domestic and heart matters.",
    7: "Solitude, study, looking behind the veil.",
    8: "Power, balance of ledger, physical abundance.",
    9: "Pruning, closure, honoring what has run its course."
}

ZODIAC_DECANS = {
    "Aries": ["Mars (0°-10°)", "Sun (10°-20°)", "Jupiter (20°-30°)"],
    "Taurus": ["Mercury (0°-10°)", "Moon (10°-20°)", "Saturn (20°-30°)"],
    "Gemini": ["Jupiter (0°-10°)", "Mars (10°-20°)", "Sun (20°-30°)"],
    "Cancer": ["Venus (0°-10°)", "Mercury (10°-20°)", "Moon (20°-30°)"],
    "Leo": ["Saturn (0°-10°)", "Jupiter (10°-20°)", "Mars (20°-30°)"],
    "Virgo": ["Sun (0°-10°)", "Venus (10°-20°)", "Mercury (20°-30°)"],
    "Libra": ["Moon (0°-10°)", "Saturn (10°-20°)", "Jupiter (20°-30°)"],
    "Scorpio": ["Mars (0°-10°)", "Sun (10°-20°)", "Venus (20°-30°)"],
    "Sagittarius": ["Mercury (0°-10°)", "Moon (10°-20°)", "Saturn (20°-30°)"],
    "Capricorn": ["Jupiter (0°-10°)", "Mars (10°-20°)", "Sun (20°-30°)"],
    "Aquarius": ["Venus (0°-10°)", "Mercury (10°-20°)", "Moon (20°-30°)"],
    "Pisces": ["Saturn (0°-10°)", "Jupiter (10°-20°)", "Mars (20°-30°)"]
}

HEPTAGRAM_777 = {
    0: {"day": "Sunday", "planet": "Sun", "metal": "Gold", "virtue": "Radiant clarity, vitality, sovereignty", "shadow": "Vanity, exhaustion, blindness from overexposure"},
    1: {"day": "Monday", "planet": "Moon", "metal": "Silver", "virtue": "Intuition, reception, emotional flux", "shadow": "Illusion, moodiness, clinging to passing tide"},
    2: {"day": "Tuesday", "planet": "Mars", "metal": "Iron", "virtue": "Severance, boundary, direct action", "shadow": "Reactive anger, premature conflict, friction"},
    3: {"day": "Wednesday", "planet": "Mercury", "metal": "Quicksilver", "virtue": "Transmission, synthesis, fluid speech", "shadow": "Scattered focus, clever deceit, anxiety"},
    4: {"day": "Thursday", "planet": "Jupiter", "metal": "Tin", "virtue": "Expansion, grace, generous vision", "shadow": "Overextension, dogma, unearned certainty"},
    5: {"day": "Friday", "planet": "Venus", "metal": "Copper", "virtue": "Attraction, harmony, artistic devotion", "shadow": "Indolence, compromise of values, codependence"},
    6: {"day": "Saturday", "planet": "Saturn", "metal": "Lead", "virtue": "Endurance, containment, time's weight", "shadow": "Bitterness, rigidity, oppressive paralysis"}
}

KNOWLEDGE_BASE = {
    1: "The Monad: Seed, identity, initial thrust into being.",
    2: "The Dyad: Mirror, division, relation, receptivity.",
    3: "The Triad: Completion of space, spark of expression.",
    4: "The Tetrad: Foundation, the four corners, matter anchored.",
    5: "The Pentad: The breath within matter, motion, fifth element.",
    6: "The Hexad: Equilibrium, creation woven into form.",
    7: "The Heptad: The sacred rest, the inner sanctum, threshold of mystery.",
    8: "The Ogdoad: Periodic return, rhythm, material mastery.",
    9: "The Ennead: Horizon, the final chamber before renewal.",
    11: "Master 11: The illumination antenna, lightning over the waters.",
    22: "Master 22: The master architect, anchoring spiritual blueprints to earth.",
    33: "Master 33: The compassionate hearth, sacrificial preservation of truth."
}

ORACLE_CARDS = {
    1: ("The Uncarved Stone", "Take direct ownership of the initial stroke. Do not ask for external permission."),
    2: ("The Still Water", "Observe before speaking. The mirror will reveal the subtle misalignment without force."),
    3: ("The Singing Wire", "Give voice to the unpolished thought. Expression clears the stagnant atmosphere."),
    4: ("The Ashlar Corner", "Establish the boundary first. True freedom requires an impenetrable perimeter."),
    5: ("The Open Gale", "Release the mooring line. Attempting to control this current will only snap the mast."),
    6: ("The Golden Crucible", "Tend to what is within arm's reach. Harmony begins at your immediate hearth."),
    7: ("The Veil of Silence", "Withdraw the senses inward. What appears missing on the surface is resolving underneath."),
    8: ("The Balanced Scales", "Demand sovereign recompense. The ledger must balance without guilt or apology."),
    9: ("The Final Embers", "Let what has burned out go cold. Sweep the hearth to receive the new seed."),
    11: ("The Lightning Rod", "You are the conductor, not the source. Ground the sudden inspiration into clay."),
    22: ("The Master Builder", "Draft the blueprint for longevity. What you construct now will outlast the current storm."),
    33: ("The Sacred Hearth", "Offer compassionate presence without self-sacrifice. Be the anchor, not the raft.")
}

# Offline Core Library Fallback Texts (Guarantees books open even if web is down)
EMBEDDED_CANONICAL = {
    "Pistis Sophia (G.R.S. Mead)": """
    Chapter 1: It came to pass, when Jesus had risen from the dead, that he passed eleven years speaking with his disciples, and instructing them only up to the regions of the First Statutes and up to the regions of the First Mystery, that within the Veil.
    
    Chapter 25: And Pistis Sophia cried out most exceedingly, she cried to the Light of lights, saying: O Light of lights, in whom I have had faith from the beginning, hearken now unto my repentance. Save me, O Light, for evil thoughts have entered into me.
    
    Chapter 32: I looked into the depths and saw the lion-faced power, and it swallowed my light. Hearken, O Light, to the sound of my singing, and let not the darkness prevail against the measure of my soul.
    
    Chapter 64: Jesus said unto his disciples: Hearken concerning the things which befell Sophia. When she was in the chaos, she sang praises unto the Treasury of the Light, and the Light-stream flowed down and raised her out of the deep waters.
    
    Chapter 100: Mary Magdalene came forward and said: My Lord, our inner being hath wings, and we are ready to receive the Mysteries of the Ineffable. Teach us the boundary between the archons of the fate and the light-realm.
    """,
    "Nag Hammadi Library (Complete Codices)": """
    The Gospel of Thomas: These are the secret sayings which the living Jesus spoke and which Didymos Judas Thomas wrote down. And he said, "Whoever finds the interpretation of these sayings will not experience death."
    
    The Gospel of Thomas (Saying 2): Jesus said, "Let him who seeks continue seeking until he finds. When he finds, he will become troubled. When he becomes troubled, he will be astonished, and he will rule over the All."
    
    The Gospel of Thomas (Saying 70): Jesus said, "If you bring forth what is within you, what you bring forth will save you. If you do not have that within you, what you do not have within you will destroy you."
    
    The Secret Book of John (Apocryphon of John): The Monad is a monarchy with nothing above it. It exists as god and father of all, the invisible one who is above the all, who exists as incorruption, which is in the pure light into which no eye can look.
    
    The Hypostasis of the Archons: Concerning the reality of the authorities, the Great Archon Yaldabaoth is blind; because of his power and his ignorance and his arrogance he said through his matter, "It is I who am God, and there is no other apart from me."
    
    The Thunder, Perfect Mind: For I am the first and the last. I am the honored one and the scorned one. I am the whore and the holy one. I am the wife and the virgin. I am the mother and the daughter.
    """
}

GEO_FALLBACK = {
    "naples, fl": (26.1420, -81.7948, "Naples, Florida, USA"),
    "naples, florida": (26.1420, -81.7948, "Naples, Florida, USA"),
    "new york, ny": (40.7128, -74.0060, "New York, NY, USA"),
    "los angeles, ca": (34.0522, -118.2437, "Los Angeles, CA, USA"),
    "chicago, il": (41.8781, -87.6298, "Chicago, IL, USA"),
    "austin, tx": (30.2672, -97.7431, "Austin, TX, USA"),
    "miami, fl": (25.7617, -80.1918, "Miami, FL, USA"),
    "london, uk": (51.5074, -0.1278, "London, United Kingdom"),
    "paris, france": (48.8566, 2.3522, "Paris, France"),
    "jerusalem": (31.7683, 35.2137, "Jerusalem"),
    "cairo, egypt": (30.0444, 31.2357, "Cairo, Egypt"),
    "rome, italy": (41.9028, 12.4964, "Rome, Italy")
}

# ==========================================
# 2. CORE HELPER FUNCTIONS & GEOCODER
# ==========================================

@st.cache_data(show_spinner=False, ttl=86400)
def geocode_location(query_str: str):
    q_norm = query_str.strip().lower()
    if not q_norm:
        return 26.1420, -81.7948, "Naples, Florida, USA"

    for k, v in GEO_FALLBACK.items():
        if k in q_norm or q_norm in k:
            return v[0], v[1], v[2]

    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query_str)}&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'NumberinHarmonicsApp/2.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                name = data[0].get('display_name', query_str).split(',')[0]
                return lat, lon, name
    except Exception:
        pass

    hash_val = sum(ord(c) for c in q_norm)
    pseudo_lat = ((hash_val * 7) % 140) - 70
    pseudo_lon = ((hash_val * 13) % 360) - 180
    return float(pseudo_lat), float(pseudo_lon), query_str.title()

def reduce_number(n: int, preserve_master: bool = True) -> int:
    n = abs(int(n))
    while n > 9:
        if preserve_master and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def cycle_19(year: int) -> int:
    return ((abs(year) + 1) % 19) or 19

def life_path_components(year: int, month: int, day: int) -> int:
    m = reduce_number(month)
    d = reduce_number(day)
    y = reduce_number(abs(year))
    return reduce_number(m + d + y)

def name_profile(name: str):
    clean = re.sub(r'[^A-Z]', '', name.upper())
    if not clean:
        return {"expression": 0, "soul_urge": 0, "personality": 0, "pyth_sum": 0, "chaldean_sum": 0, "clean": ""}
    
    vowels = "AEIOU"
    p_vals = [PYTHAGOREAN_MAP.get(c, 0) for c in clean]
    c_vals = [CHALDEAN_MAP.get(c, 0) for c in clean]
    
    v_vals = [PYTHAGOREAN_MAP.get(c, 0) for c in clean if c in vowels]
    co_vals = [PYTHAGOREAN_MAP.get(c, 0) for c in clean if c not in vowels]
    
    return {
        "expression": reduce_number(sum(p_vals)),
        "soul_urge": reduce_number(sum(v_vals)) if v_vals else 0,
        "personality": reduce_number(sum(co_vals)) if co_vals else 0,
        "pyth_sum": sum(p_vals),
        "chaldean_sum": sum(c_vals),
        "clean": clean
    }

def personal_cycles_components(month: int, day: int, target_year: int):
    m = reduce_number(month)
    d = reduce_number(day)
    py = reduce_number(abs(target_year))
    personal_year = reduce_number(m + d + py)
    return {"personal_year": personal_year, "milestone": MILESTONES.get(personal_year, "")}

def run_latin_cipher(text: str) -> dict:
    clean = re.sub(r'[^A-Z]', '', text.upper())
    simple = sum(ord(c) - 64 for c in clean)
    reverse = sum(27 - (ord(c) - 64) for c in clean)
    return {"simple": simple, "reverse": reverse, "reduced": reduce_number(simple)}

def script_readings(text: str) -> str:
    clean = re.sub(r'[^A-Z]', '', text.upper())
    counts = Counter(clean)
    dominant = counts.most_common(1)[0] if counts else ("None", 0)
    return f"Dominant letter frequency: '{dominant[0]}' occurring {dominant[1]} times. Total vibration: {len(clean)} characters."

def meaning(n: int) -> str:
    return KNOWLEDGE_BASE.get(n, "Resonant vibration awaiting direct definition.")

def angel_read(num_str: str) -> str:
    for code, desc in ANGEL.items():
        if code in num_str:
            return f"Synchronicity Detected ({code}): {desc}"
    return "No primary triple repeating synchronicity found in the direct stream."

def get_astronomical_julian_date(year: int, month: int, day: int, is_bce: bool = False) -> float:
    astro_year = -(year - 1) if is_bce else year
    if month <= 2:
        astro_year -= 1
        month += 12
    a = math.floor(astro_year / 100)
    b = 2 - a + math.floor(a / 4) if astro_year >= 1582 else 0
    jd = math.floor(365.25 * (astro_year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return jd

def moon_phase_components(year: int, month: int, day: int, is_bce: bool = False) -> str:
    jd = get_astronomical_julian_date(year, month, day, is_bce)
    cycles = (jd - 2451549.5) / 29.53058770576
    phase = cycles - math.floor(cycles)
    val = round(phase * 8) % 8
    phases = [
        "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
        "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
    ]
    return phases[val]

def get_approx_sun_sign_components(month: int, day: int) -> str:
    md = (month, day)
    if (3, 21) <= md <= (4, 19): return "Aries"
    elif (4, 20) <= md <= (5, 20): return "Taurus"
    elif (5, 21) <= md <= (6, 20): return "Gemini"
    elif (6, 21) <= md <= (7, 22): return "Cancer"
    elif (7, 23) <= md <= (8, 22): return "Leo"
    elif (8, 23) <= md <= (9, 22): return "Virgo"
    elif (9, 23) <= md <= (10, 22): return "Libra"
    elif (10, 23) <= md <= (11, 21): return "Scorpio"
    elif (11, 22) <= md <= (12, 21): return "Sagittarius"
    elif (12, 22) <= md or md <= (1, 19): return "Capricorn"
    elif (1, 20) <= md <= (2, 18): return "Aquarius"
    else: return "Pisces"

def evaluate_compatibility(lp1: int, lp2: int) -> str:
    diff = abs(lp1 - lp2)
    if diff == 0:
        return "Resonant Unity: Shared primary frequency. Mutual mirror, instant familiarity."
    elif diff in (2, 4):
        return "Harmonic Accord: Complementary rhythm. The difference creates productive leverage."
    elif diff in (1, 3):
        return "Dynamic Spark: Productive tension. Growth requires deliberate accommodation."
    return "Neutral Orbit: Independent wavelengths that interact without friction or fusion."

def purify_corpus(raw_text: str) -> str:
    start_pos = 0
    start_pattern = re.search(r'\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', raw_text, re.IGNORECASE)
    if start_pattern:
        start_pos = start_pattern.end()

    end_pos = len(raw_text)
    end_pattern = re.search(r'\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*', raw_text, re.IGNORECASE)
    if end_pattern:
        end_pos = end_pattern.start()

    clean = raw_text[start_pos:end_pos].strip()
    clean = re.sub(r'<<.*?>>', '', clean)
    return clean

def extract_full_verses(corpus_text: str, query: str, max_results: int = 5):
    raw_paragraphs = re.split(r'\n\s*\n+', corpus_text)
    matches = []
    q_pattern = re.compile(rf'\b{re.escape(query)}\b', re.IGNORECASE)

    for p in raw_paragraphs:
        verse = " ".join(line.strip() for line in p.splitlines() if line.strip())
        if len(verse) < 25 or "project gutenberg" in verse.lower():
            continue
        if q_pattern.search(verse):
            verse_root = reduce_number(sum(ord(c) - 64 for c in verse.upper() if 'A' <= c <= 'Z'))
            highlighted = q_pattern.sub(lambda m: f"<span class='mark-glow'>{m.group(0)}</span>", verse)
            matches.append((highlighted, verse_root))
            if len(matches) >= max_results:
                break
    return matches

# ==========================================
# 3. SIDEBAR: AUDIO, NATAL ANCHOR & NUMEROLOGY ORACLE
# ==========================================

with st.sidebar:
    st.markdown("<h2 style='color:#f5c542; text-shadow: 0 0 10px rgba(245,197,66,0.5);'>⚓ NATAL ANCHOR</h2>", unsafe_allow_html=True)
    
    freq_choice = st.radio("Harmonic Carrier", ["Silence", "432 Hz", "528 Hz"], horizontal=True)
    if freq_choice == "432 Hz":
        st.caption("✨ Carrier Active: Harmonic Sacred Geometry (432 Hz)")
    elif freq_choice == "528 Hz":
        st.caption("✨ Carrier Active: DNA Transformation Frequency (528 Hz)")

    st.markdown("---")
    anchor_name = st.text_input("Vessel / Anchor Name", value="Seeker")
    
    st.markdown("**Anchor Date**")
    s_col1, s_col2, s_col3 = st.columns([1.2, 1, 1])
    with s_col1:
        s_year = st.number_input("Year", min_value=1, max_value=9999, value=datetime.date.today().year, key="s_yr")
    with s_col2:
        s_month = st.number_input("Month", min_value=1, max_value=12, value=datetime.date.today().month, key="s_mo")
    with s_col3:
        s_day = st.number_input("Day", min_value=1, max_value=31, value=datetime.date.today().day, key="s_dy")
    
    s_era = st.selectbox("Era", ["CE (AD)", "BCE (BC)"], index=0, key="s_era")
    is_anchor_bce = (s_era == "BCE (BC)")
    
    lp_anchor = life_path_components(s_year, s_month, s_day)
    sun_anchor = get_approx_sun_sign_components(s_month, s_day)
    moon_anchor = moon_phase_components(s_year, s_month, s_day, is_anchor_bce)
    name_p = name_profile(anchor_name)
    
    st.markdown(f"**Life Path:** `{lp_anchor}`")
    st.markdown(f"**Expression:** `{name_p['expression']}`")
    st.markdown(f"**Sun Sign:** `{sun_anchor}`")
    st.markdown(f"**Moon Phase:** `{moon_anchor}`")
    
    # NUMEROLOGY ORACLE IN SIDEBAR
    st.markdown("---")
    st.markdown("<h3 style='color:#f5c542; font-size:1.15rem;'>🔮 NUMEROLOGY ORACLE</h3>", unsafe_allow_html=True)
    st.caption("Cast a current query into the vibrational wheel.")
    
    oracle_query = st.text_input("Ask the Oracle a question:", placeholder="What current requires my focus today?", key="sb_oracle_q")
    
    if st.button("Consult the Oracle", key="sb_oracle_btn"):
        today = datetime.date.today()
        q_sum = sum(ord(c) for c in oracle_query.upper() if 'A' <= c <= 'Z') if oracle_query else 0
        draw_val = (lp_anchor + name_p['expression'] + q_sum + today.day + today.month)
        
        card_num = reduce_number(draw_val)
        card_title, card_directive = ORACLE_CARDS.get(card_num, ("The Threshold", "Hold steady and observe."))
        
        st.session_state["sidebar_oracle_res"] = {
            "num": card_num,
            "title": card_title,
            "directive": card_directive,
            "query": oracle_query
        }
        
    if "sidebar_oracle_res" in st.session_state:
        sor = st.session_state["sidebar_oracle_res"]
        st.markdown(f"""
        <div class="sidebar-oracle-card">
            <span style="color:#d4af37; font-size:0.75rem; font-weight:bold; letter-spacing:0.05em; font-family:'Cinzel', serif;">ORACLE CAST #{sor['num']}</span>
            <h4 style="color:#fff4cc; margin:4px 0 6px 0; font-size:1.05rem;">{sor['title']}</h4>
            <p style="font-size:0.86rem; line-height:1.5; color:#f1f4f8; margin-bottom:0;">
                {sor['directive']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Universal Anchor pinned across all active reading chambers.")

# ==========================================
# 4. UNIVERSAL SEARCH / INPUT CLASSIFIER
# ==========================================

st.markdown("<div class='brand-title'>NUMBERIN</div>", unsafe_allow_html=True)
search_query = st.text_input("Enter any name, phrase, epoch, or date to discern its root:", "")

if search_query:
    parsed_date_match = re.match(r'^(\d+)[-/.](\d+)[-/.](\d+)(\s+(BCE|BC|CE|AD))?$', search_query.strip(), re.IGNORECASE)
    year_only_match = re.match(r'^(\d+)\s*(BCE|BC|CE|AD)$', search_query.strip(), re.IGNORECASE)
    
    if parsed_date_match:
        y, m, d = int(parsed_date_match.group(1)), int(parsed_date_match.group(2)), int(parsed_date_match.group(3))
        era = parsed_date_match.group(5)
        is_bce_q = True if era and era.upper() in ["BCE", "BC"] else False
        lp_q = life_path_components(y, m, d)
        st.info(f"**Date Input Detected**: Life Path `{lp_q}` | Sun Sign: `{get_approx_sun_sign_components(m, d)}` | Phase: `{moon_phase_components(y, m, d, is_bce_q)}`")
    elif year_only_match:
        y = int(year_only_match.group(1))
        era = year_only_match.group(2).upper()
        root_y = reduce_number(y)
        st.info(f"**Historical Epoch Detected**: Year `{y} {era}` | Root Cycle: `{root_y}` ({meaning(root_y)})")
    else:
        prof = name_profile(search_query)
        st.info(f"**Text Input Detected**: Expression `{prof['expression']}` | Soul Urge `{prof['soul_urge']}` | Personality `{prof['personality']}` | Pythagorean Sum `{prof['pyth_sum']}`")

# ==========================================
# 5. ILLUMINATED CHAMBERS / TABS
# ==========================================

tabs = st.tabs([
    "Alchemy Pharmacy", 
    "Corpus Knowledge Base", 
    "Spatiotemporal Frequency Map", 
    "Decan Oracle", 
    "Compatibility Matrix", 
    "Pattern & Frequency Engine"
])

# ----------------------------------------------------
# TAB 1: ALCHEMY PHARMACY
# ----------------------------------------------------
with tabs[0]:
    st.markdown("<h3 style='color:#f5c542;'>The Alchemy Pharmacy</h3>", unsafe_allow_html=True)
    st.markdown("> *The user is the alchemist; the app is the pharmacy. Bring your prima materia into the brass rings to extract the working tincture.*")

    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        alch_name = st.text_input("Alchemist Name (Optional)", value=anchor_name)
        
        st.markdown("**Epoch / Birthdate (Any Historical or Future Era)**")
        a_c1, a_c2, a_c3, a_c4 = st.columns([1.2, 1, 1, 1.2])
        with a_c1:
            a_year = st.number_input("Year", min_value=1, max_value=99999, value=s_year, key="a_yr")
        with a_c2:
            a_month = st.number_input("Month", min_value=1, max_value=12, value=s_month, key="a_mo")
        with a_c3:
            a_day = st.number_input("Day", min_value=1, max_value=31, value=s_day, key="a_dy")
        with a_c4:
            a_era = st.selectbox("Era", ["CE (AD)", "BCE (BC)"], index=0 if not is_anchor_bce else 1, key="a_era")

        seed_str = st.text_input("Operational Seed", value="7-7-7")
        
    with col_b:
        prima_materia = st.text_area("Prima Materia (What are you transmuting? Issue, question, or feeling)", 
                                     placeholder="Describe the raw circumstance, tension, or desire you bring to the bench today...",
                                     height=180)

    if st.button("Compound the Tincture", type="primary"):
        name_val = name_profile(alch_name)["expression"] if alch_name else 0
        lp_val = life_path_components(a_year, a_month, a_day)
        d_year = (a_month - 1) * 30 + a_day
        seed_digits = [int(c) for c in seed_str if c.isdigit()]
        seed_val = sum(seed_digits) if seed_digits else 21

        total_alch = name_val + lp_val + d_year + a_day + seed_val
        working_idx = total_alch % 7
        distraction_idx = (working_idx + 3) % 7

        working_meta = HEPTAGRAM_777[working_idx]
        distract_meta = HEPTAGRAM_777[distraction_idx]

        p_clean = prima_materia.strip() if prima_materia else "the quiet stillness you carried in"
        
        tincture_prose = (
            f"When you bring {p_clean} to the counter, the weight does not need to be broken by brute force. "
            f"Right now, the current runs cleanest through {working_meta['virtue'].lower()}. "
            f"The immediate instinct might be to pull toward {distract_meta['virtue'].lower()}, "
            f"yet that direction easily degrades into {distract_meta['shadow'].lower()}. "
            f"Hold steady in this current: do not rush the cooling process, let the sediment settle to the bottom, "
            f"and let the day's natural rhythm bear what your hands have grown tired of carrying."
        )

        st.session_state["tincture_data"] = {
            "working_meta": working_meta,
            "distract_meta": distract_meta,
            "tincture_prose": tincture_prose,
            "total_alch": total_alch,
            "working_idx": working_idx,
            "a_year": a_year,
            "a_era": a_era,
            "a_month": a_month,
            "a_day": a_day
        }

    if "tincture_data" in st.session_state:
        td = st.session_state["tincture_data"]
        wm = td["working_meta"]
        dm = td["distract_meta"]

        st.markdown(f"""
        <div class="brass-panel">
            <h4 style="text-align: center; color: #f5c542; margin-bottom: 5px;">The Three Pivot Rings Locked</h4>
            <div class="ring-container">
                <div class="ring-badge">Outer Ring<br><small>{wm['day']}</small></div>
                <div class="ring-badge">Middle Pivot<br><small>{wm['planet']}</small></div>
                <div class="ring-badge">Inner Core<br><small>{wm['metal']}</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tincture-box">
            <strong style="color: #f5c542; font-family: 'Cinzel', serif;">Prescription & Tincture:</strong><br><br>
            {td['tincture_prose']}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Examine the Bench Apparatus (Technical Breakdown)"):
            st.markdown(f"- **Historical Horizon:** `{td['a_year']} {td['a_era']}, Month {td['a_month']}, Day {td['a_day']}`")
            st.markdown(f"- **Working Modulo:** `{td['total_alch']} ≡ {td['working_idx']} (mod 7)`")
            st.markdown(f"- **Core Metal Skeleton:** {wm['metal']} ({wm['planet']})")
            st.markdown(f"- **Distraction Axis (+3):** {dm['metal']} ({dm['planet']})")

# ----------------------------------------------------
# TAB 2: CORPUS KNOWLEDGE BASE (Permanent Fallbacks Added)
# ----------------------------------------------------
with tabs[1]:
    st.markdown("<h3 style='color:#f5c542;'>The Full-Corpus Library Engine</h3>", unsafe_allow_html=True)
    st.markdown("Search, cross-examine, and extract patterns across complete canonical scriptures with intact, unabridged verse formatting.")

    CORPUS_MIRRORS = {
        "King James Bible (Complete)": [
            "https://www.gutenberg.org/cache/epub/10/pg10.txt",
            "https://raw.githubusercontent.com/mxw/gutenberg-corpus/master/kjv.txt"
        ],
        "The Book of Enoch (R.H. Charles)": [
            "https://www.gutenberg.org/cache/epub/45238/pg45238.txt",
            "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/enoch.txt"
        ],
        "Nag Hammadi Library (Complete Codices)": [
            "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/nag_hammadi.txt"
        ],
        "Pistis Sophia (G.R.S. Mead)": [
            "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/pistis_sophia.txt"
        ],
        "The Kybalion (Three Initiates)": [
            "https://www.gutenberg.org/cache/epub/14264/pg14264.txt"
        ],
        "I Ching (Legge Translation)": [
            "https://www.gutenberg.org/cache/epub/25890/pg25890.txt"
        ]
    }

    LOCAL_FILE_FALLBACKS = {
        "Nag Hammadi Library (Complete Codices)": "texts/nag_hammadi.txt",
        "Pistis Sophia (G.R.S. Mead)": "texts/pistis_sophia.txt",
        "The Book of Enoch (R.H. Charles)": "texts/enoch.txt"
    }

    @st.cache_data(show_spinner=False)
    def fetch_full_text(source_name: str, urls) -> str:
        # 1. Local file path check
        local_path = LOCAL_FILE_FALLBACKS.get(source_name)
        if local_path and os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
                    return purify_corpus(f.read())
            except Exception:
                pass

        # 2. Try web mirror
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            try:
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    raw_bytes = response.read().decode('utf-8', errors='ignore')
                    cleaned = purify_corpus(raw_bytes)
                    if len(cleaned) > 1000:
                        return cleaned
            except Exception:
                continue

        # 3. Direct Embedded Canonical Core Fallback
        if source_name in EMBEDDED_CANONICAL:
            return EMBEDDED_CANONICAL[source_name].strip()

        return ""

    corpus_source = st.selectbox(
        "Select Active Canonical Corpus", 
        ["Custom Upload"] + list(CORPUS_MIRRORS.keys())
    )
    corpus_text = ""

    if corpus_source == "Custom Upload":
        uploaded_file = st.file_uploader("Upload any manuscript or text file (.txt, .md)", type=["txt", "md"])
        if uploaded_file is not None:
            corpus_text = purify_corpus(uploaded_file.read().decode('utf-8', errors='ignore'))
    else:
        with st.spinner(f"Purifying and cataloging {corpus_source}..."):
            corpus_text = fetch_full_text(corpus_source, CORPUS_MIRRORS[corpus_source])

    if corpus_text:
        words_list = re.findall(r'\b[A-Za-z]+\b', corpus_text.lower())
        total_words = len(words_list)
        total_chars = len(corpus_text)
        
        st.caption(f"Canonical Volume: **{total_words:,} words** | **{total_chars:,} characters** (Boilerplate Purged)")

        st.markdown("#### Canonical Plain-Language Inquiry")
        query = st.text_input("Ask a question, enter a number, or search a word/verse:", 
                              placeholder="e.g. 'archon', 'light', 'seven', 'most common words', 'pistis'")

        if query:
            q_clean = query.strip().lower()
            
            # 1. MOST COMMON WORDS
            if any(k in q_clean for k in ["most common", "shows up most", "up the most", "the much", "most frequent"]):
                stop_words = {"the", "and", "of", "to", "in", "that", "he", "shall", "unto", "for", "with", "a", "is", "his", "they", "be", "not", "it", "as", "by", "all", "this", "from", "said", "i", "you", "them"}
                filtered = [w for w in words_list if w not in stop_words and len(w) > 2]
                counts = Counter(filtered).most_common(10)
                st.markdown("#### Dominant Canonical Words (Excluding Stop-Words):")
                for w, c in counts:
                    st.markdown(f"- **{w}**: `{c:,}` times")
                
                top_w = counts[0][0]
                st.markdown(f"##### Full Uncut Verses Featuring '{top_w}':")
                v_results = extract_full_verses(corpus_text, top_w, max_results=3)
                for v_text, v_root in v_results:
                    st.markdown(f"""
                    <div class='verse-card'>
                        <span class='verse-badge'>UNCUT VERSE OCCURRENCE</span><span class='gematria-pill'>Gematria Root: {v_root} ({meaning(v_root)})</span><br>
                        {v_text}
                    </div>
                    """, unsafe_allow_html=True)

            # 2. LEAST COMMON WORDS
            elif any(k in q_clean for k in ["least common", "shows up least", "the least", "rarest", "hapax"]):
                single_words = [w for w, c in Counter(words_list).items() if c == 1 and len(w) > 3]
                sample_least = single_words[:10]
                st.markdown("#### Hapax Legomena (Words Occurring Exactly Once):")
                st.write(", ".join(sample_least))
                
                if sample_least:
                    st.markdown(f"##### Full Context for Unique Occurrence '{sample_least[0]}':")
                    v_results = extract_full_verses(corpus_text, sample_least[0], max_results=1)
                    for v_text, v_root in v_results:
                        st.markdown(f"""
                        <div class='verse-card'>
                            <span class='verse-badge'>SINGULAR VERSE</span><span class='gematria-pill'>Gematria Root: {v_root}</span><br>
                            {v_text}
                        </div>
                        """, unsafe_allow_html=True)

            # 3. SEVENS OR DIGIT PATTERNS
            elif "seven" in q_clean or " 7 " in q_clean or q_clean == "7":
                matches = len(re.findall(r'\b(7|seven|seventh)\b', corpus_text, re.IGNORECASE))
                st.markdown(f"**Direct Result:** The sacred frequency seven appears **{matches:,} times**.")
                st.markdown("##### Full Uncut Verses with Seven:")
                v_results = extract_full_verses(corpus_text, "seven", max_results=4)
                for v_text, v_root in v_results:
                    st.markdown(f"""
                    <div class='verse-card'>
                        <span class='verse-badge'>CANONICAL PASSAGE</span><span class='gematria-pill'>Vibrational Root: {v_root}</span><br>
                        {v_text}
                    </div>
                    """, unsafe_allow_html=True)

            # 4. LETTER FREQUENCIES
            elif "letter frequency" in q_clean or "letters" in q_clean:
                letters_only = [c for c in corpus_text.upper() if 'A' <= c <= 'Z']
                l_counts = Counter(letters_only).most_common(7)
                st.markdown("#### Primary Letter Frequencies:")
                for l, count in l_counts:
                    pct = (count / len(letters_only)) * 100
                    st.markdown(f"- **{l}**: `{count:,}` times ({pct:.2f}%)")

            # 5. WHOLE-CORPUS NUMEROLOGY ROOT
            elif "root" in q_clean or "numerology" in q_clean:
                root_sum = sum(ord(c) - 64 for c in corpus_text.upper() if 'A' <= c <= 'Z')
                collapsed = reduce_number(root_sum)
                st.markdown(f"**Corpus Grand Root:** `{collapsed}` — {meaning(collapsed)}")

            # 6. DIRECT PHRASE OR TARGET WORD SEARCH
            else:
                target_word = re.sub(r'^(find|how many times does|how many times|count|find every time it says|search for)\s+', '', q_clean).strip().strip("'\"")
                target_word = target_word.split()[0] if target_word else q_clean
                
                raw_find = len(re.findall(rf'\b{re.escape(target_word)}\b', corpus_text, re.IGNORECASE))
                st.markdown(f"**Direct Result:** The token **'{target_word}'** appears **{raw_find:,} times**.")
                
                if raw_find > 0:
                    st.markdown(f"##### Full Uncut Verses Featuring '{target_word}':")
                    v_results = extract_full_verses(corpus_text, target_word, max_results=5)
                    for v_text, v_root in v_results:
                        st.markdown(f"""
                        <div class='verse-card'>
                            <span class='verse-badge'>CANONICAL PASSAGE</span><span class='gematria-pill'>Passage Root: {v_root} ({meaning(v_root)})</span><br>
                            {v_text}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No exact occurrences found in this corpus.")

# ----------------------------------------------------
# TAB 3: SPATIOTEMPORAL FREQUENCY MAP & PRINTABLE CHARTER
# ----------------------------------------------------
with tabs[2]:
    st.markdown("<h3 style='color:#f5c542;'>Spatiotemporal Frequency Map</h3>", unsafe_allow_html=True)
    st.markdown("> *A multi-dimensional harmonic charter mapping origin ground, present location, diurnal phase, and active frequency voids.*")

    col_map_in1, col_map_in2 = st.columns([1.1, 1])
    
    with col_map_in1:
        st.markdown("**1. Temporal Origin (Date & Minute)**")
        map_name = st.text_input("Vessel Name", value=anchor_name, key="st_name")
        tc1, tc2, tc3, tc4 = st.columns([1.2, 1, 1, 1.2])
        with tc1:
            st_yr = st.number_input("Year", min_value=1, max_value=9999, value=s_year, key="st_yr")
        with tc2:
            st_mo = st.number_input("Month", min_value=1, max_value=12, value=s_month, key="st_mo")
        with tc3:
            st_dy = st.number_input("Day", min_value=1, max_value=31, value=s_day, key="st_dy")
        with tc4:
            st_time = st.time_input("Birth Time (Approx)", value=datetime.time(12, 0), key="st_time")

        st.markdown("**2. Spatial Ground (Auto-Detected City & State)**")
        sc1, sc2 = st.columns(2)
        with sc1:
            origin_city = st.text_input("Birth Place (City, State / Country)", value="Naples, Florida", key="o_city")
            origin_lat, origin_lon, orig_resolved = geocode_location(origin_city)
            st.caption(f"📍 Resolved: `{orig_resolved}` ({origin_lat:.2f}°, {origin_lon:.2f}°)")

        with sc2:
            same_loc = st.checkbox("Currently at Birthplace", value=True, key="same_loc")
            if same_loc:
                curr_city = origin_city
                curr_lat, curr_lon, curr_resolved = origin_lat, origin_lon, orig_resolved
                st.caption(f"📍 Anchored to Origin Ground")
            else:
                curr_city = st.text_input("Current Residence (City, State / Country)", value="Austin, Texas", key="c_city")
                curr_lat, curr_lon, curr_resolved = geocode_location(curr_city)
                st.caption(f"📍 Resolved: `{curr_resolved}` ({curr_lat:.2f}°, {curr_lon:.2f}°)")

    with col_map_in2:
        st.markdown("**3. Biological Wave & Active Horizon**")
        now_year = datetime.date.today().year
        eval_age = st.slider("Observed Age", min_value=0, max_value=120, value=abs(now_year - st_yr), key="st_age")
        active_target_year = st_yr + eval_age
        st.markdown(f"Active Horizon Year: **{active_target_year}**")

        charter_mode = st.radio("Display Atmosphere", ["Luminous Chamber (Screen)", "Parchment Charter (Print-Ready)"], horizontal=True)

    # Core Calculations
    st_lp = life_path_components(st_yr, st_mo, st_dy)
    st_prof = name_profile(map_name)
    st_expr = st_prof["expression"] if st_prof["expression"] > 0 else 1
    st_soul = st_prof["soul_urge"] if st_prof["soul_urge"] > 0 else 1
    st_pers = st_prof["personality"] if st_prof["personality"] > 0 else 1
    st_py = personal_cycles_components(st_mo, st_dy, active_target_year)["personal_year"]

    # Diurnal Inhale/Exhale Cycle
    hour_val = st_time.hour
    is_inhale = (6 <= hour_val < 18)
    diurnal_label = "Solar Inhale (Electric / Outward)" if is_inhale else "Lunar Exhale (Magnetic / Deep Ground)"

    # Location Pitches
    origin_pitch = reduce_number(round(abs(origin_lat) + abs(origin_lon)))
    curr_pitch = reduce_number(round(abs(curr_lat) + abs(curr_lon)))
    displacement_delta = abs(origin_pitch - curr_pitch)

    # Karmic Voids & Saturated Nodes
    digits_present = [int(c) for c in (str(st_lp) + str(st_expr) + str(st_soul) + str(st_pers) + str(st_yr) + str(st_mo) + str(st_dy)) if c.isdigit()]
    counts = Counter(digits_present)
    all_pillars = set(range(1, 10))
    void_pillars = sorted(list(all_pillars - set(counts.keys())))
    saturated_pillars = sorted([num for num, cnt in counts.items() if cnt >= 3 and 1 <= num <= 9])

    # Peak Circadian Alignment Window
    peak_start_hour = (st_lp * 2 + hour_val) % 24
    peak_window = f"{peak_start_hour:02d}:15 – {(peak_start_hour + 1) % 24:02d}:00"

    # ==========================================
    # TRI-RING CYMATIC VECTOR VISUALIZER (SVG via Components)
    # ==========================================
    center_x, center_y = 260, 260
    r_outer = 220
    r_mid = 160
    r_inner = 95

    is_parchment = ("Print-Ready" in charter_mode)
    bg_color = "#fbf8ef" if is_parchment else "rgba(10, 12, 16, 0.95)"
    ring_stroke = "rgba(120, 95, 30, 0.4)" if is_parchment else "rgba(212, 175, 55, 0.25)"
    text_color = "#2a2415" if is_parchment else "#fff4cc"
    gold_fill = "rgba(197, 160, 89, 0.35)" if is_parchment else "rgba(245, 197, 66, 0.28)"
    gold_line = "#9e7d3b" if is_parchment else "#f5c542"
    amber_point = "#c85a17" if is_parchment else "#ffaa44"

    node_coords = {}
    for i in range(1, 10):
        deg = -90 + (i - 1) * (360 / 9)
        rad = math.radians(deg)
        x = center_x + r_mid * math.cos(rad)
        y = center_y + r_mid * math.sin(rad)
        node_coords[i] = (x, y)

    active_seq = [st_lp, st_expr, st_soul, st_pers, st_py]
    poly_pts = [f"{node_coords[p][0]:.1f},{node_coords[p][1]:.1f}" for p in active_seq]
    poly_str = " ".join(poly_pts)

    deg_orig = -90 + (origin_pitch - 1) * 40
    rad_orig = math.radians(deg_orig)
    orig_x = center_x + r_outer * math.cos(rad_orig)
    orig_y = center_y + r_outer * math.sin(rad_orig)

    deg_curr = -90 + (curr_pitch - 1) * 40
    rad_curr = math.radians(deg_curr)
    curr_x = center_x + r_outer * math.cos(rad_curr)
    curr_y = center_y + r_outer * math.sin(rad_curr)

    deg_circ = -90 + (peak_start_hour / 24.0) * 360
    rad_circ = math.radians(deg_circ)
    circ_x = center_x + r_inner * math.cos(rad_circ)
    circ_y = center_y + r_inner * math.sin(rad_circ)

    svg_nodes = "".join([
        f'<circle cx="{node_coords[i][0]}" cy="{node_coords[i][1]}" r="14" fill="{"#0b0d10" if not is_parchment else "#ffffff"}" stroke="{"#555" if i in void_pillars else (amber_point if i in saturated_pillars else gold_line)}" stroke-width="{"1" if i in void_pillars else "2.5"}"/>'
        f'<text x="{node_coords[i][0]}" y="{node_coords[i][1] + 4}" fill="{"#666" if i in void_pillars else text_color}" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">{i}</text>'
        for i in range(1, 10)
    ])

    svg_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin:0; background:transparent; display:flex; justify-content:center; align-items:center;">
    <svg width="520" height="520" viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="background:{bg_color}; border:1px solid rgba(212,175,55,0.4); border-radius:50%; box-shadow:0 0 35px rgba(0,0,0,0.85);">
        <circle cx="{center_x}" cy="{center_y}" r="{r_outer}" fill="none" stroke="{ring_stroke}" stroke-width="1.5" stroke-dasharray="4,4"/>
        <circle cx="{center_x}" cy="{center_y}" r="{r_mid}" fill="none" stroke="{ring_stroke}" stroke-width="2"/>
        <circle cx="{center_x}" cy="{center_y}" r="{r_inner}" fill="none" stroke="{ring_stroke}" stroke-width="1.5"/>
        <line x1="{center_x}" y1="{center_y - r_outer - 15}" x2="{center_x}" y2="{center_y + r_outer + 15}" stroke="{ring_stroke}" stroke-width="0.8"/>
        <line x1="{center_x - r_outer - 15}" y1="{center_y}" x2="{center_x + r_outer + 15}" y2="{center_y}" stroke="{ring_stroke}" stroke-width="0.8"/>
        <polygon points="{poly_str}" fill="{gold_fill}" stroke="{gold_line}" stroke-width="2.5"/>
        {svg_nodes}
        <circle cx="{orig_x}" cy="{orig_y}" r="8" fill="#d4af37" stroke="#fff" stroke-width="2"/>
        <text x="{orig_x}" y="{orig_y - 12}" fill="{text_color}" font-size="10" font-weight="700" text-anchor="middle" font-family="sans-serif">ORIGIN</text>
        <circle cx="{curr_x}" cy="{curr_y}" r="8" fill="{amber_point}" stroke="#fff" stroke-width="2"/>
        <text x="{curr_x}" y="{curr_y + 18}" fill="{text_color}" font-size="10" font-weight="700" text-anchor="middle" font-family="sans-serif">PRESENT</text>
        <line x1="{orig_x}" y1="{orig_y}" x2="{curr_x}" y2="{curr_y}" stroke="{amber_point}" stroke-width="1.8" stroke-dasharray="3,3"/>
        <line x1="{center_x}" y1="{center_y}" x2="{circ_x}" y2="{circ_y}" stroke="{gold_line}" stroke-width="3"/>
        <circle cx="{circ_x}" cy="{circ_y}" r="5" fill="#fff" stroke="{gold_line}" stroke-width="2"/>
        <text x="{center_x}" y="{center_y + 4}" fill="{text_color}" font-size="10" font-weight="700" text-anchor="middle" font-family="sans-serif">HORIZON</text>
    </svg>
    </body>
    </html>
    """

    components.html(svg_html, height=540)

    # ==========================================
    # THE SPIRITUAL DIAGNOSTIC HUD
    # ==========================================
    g_c1, g_c2, g_c3 = st.columns(3)

    with g_c1:
        st.markdown(f"""
        <div class="brass-panel" style="padding: 18px;">
            <div class="verse-badge">THE KARMIC VOID (ABSENT)</div>
            <h3 style="color:#fff4cc; margin: 4px 0;">Pillars: {', '.join(str(v) for v in void_pillars) if void_pillars else 'None (Fully Integrated)'}</h3>
            <p style="font-size: 0.9rem; line-height: 1.5; color: #cbd5e1;">
                {('These frequencies are totally absent from your base blueprint. You naturally bypass or resist containment here. Deliberate discipline is required to build this muscle.' if void_pillars else 'All nine numbers are represented; your friction comes from distribution rather than an energetic gap.')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with g_c2:
        st.markdown(f"""
        <div class="brass-panel" style="padding: 18px;">
            <div class="verse-badge">DISPLACEMENT PRESSURE</div>
            <h3 style="color:#fff4cc; margin: 4px 0;">Delta: {displacement_delta} Harmonic</h3>
            <p style="font-size: 0.9rem; line-height: 1.5; color: #cbd5e1;">
                Origin ({orig_resolved}) vibrates to <strong>Pitch {origin_pitch}</strong>; Present Ground ({curr_resolved}) vibrates to <strong>Pitch {curr_pitch}</strong>. 
                {('You are anchored in your natal soil. Energy flows in its original groove.' if displacement_delta == 0 else 'Displacement creates dynamic atmospheric friction. The local land accelerates growth outside your comfort zone.')}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with g_c3:
        st.markdown(f"""
        <div class="brass-panel" style="padding: 18px;">
            <div class="verse-badge">CIRCADIAN POWER APERTURE</div>
            <h3 style="color:#fff4cc; margin: 4px 0;">{peak_window}</h3>
            <p style="font-size: 0.9rem; line-height: 1.5; color: #cbd5e1;">
                Phase: <strong>{diurnal_label}</strong>.<br>
                Each day during this 45-minute window, the local solar transit unlocks your natal resonance channel for peak clarity.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Master Charter Synthesis
    st.markdown(f"""
    <div class="tincture-box">
        <strong style="color: #f5c542; font-family: 'Cinzel', serif;">Spiritual Vector Directive for {map_name} (Age {eval_age}):</strong><br><br>
        Your geometry is grounded in <strong>Life Path {st_lp}</strong> operating through the outward tone of <strong>Expression {st_expr}</strong>. 
        Under the active horizon of <strong>Personal Year {st_py}</strong>, your primary energetic leak stems from {('the unanchored void of frequency ' + str(void_pillars[0]) if void_pillars else 'over-saturation in pillar ' + str(saturated_pillars[0]) if saturated_pillars else 'internal friction between urge and expression')}. 
        <strong>Where to Push:</strong> Stop seeking passive harmony in domains requiring rigorous boundary containment. Align your heaviest strategic maneuvers with your daily circadian window ({peak_window}) to move with the sky instead of swimming upstream.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 4: DECAN ORACLE (Illuminated)
# ----------------------------------------------------
with tabs[3]:
    st.markdown("<h3 style='color:#f5c542;'>Decan Oracle</h3>", unsafe_allow_html=True)
    st.markdown("The 36 Decan faces of the ecliptic and their planetary sub-rulers.")
    
    sel_sign = st.selectbox("Select Zodiac Sign", list(ZODIAC_DECANS.keys()))
    decans = ZODIAC_DECANS[sel_sign]
    
    st.markdown(f"""
    <div class="brass-panel">
        <h4 style="color: #f5c542; margin-top:0;">{sel_sign} Decan Architecture</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; border-left: 3px solid #d4af37;">
                <strong style="color: #fff2b2;">First Decan (0°-10°)</strong><br>{decans[0]}
            </div>
            <div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; border-left: 3px solid #d4af37;">
                <strong style="color: #fff2b2;">Second Decan (10°-20°)</strong><br>{decans[1]}
            </div>
            <div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; border-left: 3px solid #d4af37;">
                <strong style="color: #fff2b2;">Third Decan (20°-30°)</strong><br>{decans[2]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 5: COMPATIBILITY MATRIX (Illuminated)
# ----------------------------------------------------
with tabs[4]:
    st.markdown("<h3 style='color:#f5c542;'>Compatibility Matrix</h3>", unsafe_allow_html=True)
    st.markdown("Compare two independent anchor dates across any point in human history.")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("**First Anchor Date**")
        cp1_y = st.number_input("Year", min_value=1, max_value=99999, value=s_year, key="cp1_y")
        cp1_m = st.number_input("Month", min_value=1, max_value=12, value=s_month, key="cp1_m")
        cp1_d = st.number_input("Day", min_value=1, max_value=31, value=s_day, key="cp1_d")
        lp1 = life_path_components(cp1_y, cp1_m, cp1_d)
        st.markdown(f"Primary Life Path: `{lp1}`")
    with col_c2:
        st.markdown("**Second Anchor Date**")
        cp2_y = st.number_input("Year", min_value=1, max_value=99999, value=33, key="cp2_y")
        cp2_m = st.number_input("Month", min_value=1, max_value=12, value=4, key="cp2_m")
        cp2_d = st.number_input("Day", min_value=1, max_value=31, value=3, key="cp2_d")
        lp2 = life_path_components(cp2_y, cp2_m, cp2_d)
        st.markdown(f"Secondary Life Path: `{lp2}`")

    comp_result = evaluate_compatibility(lp1, lp2)
    st.markdown(f"""
    <div class="brass-panel">
        <h4 style="color:#f5c542; margin-top:0;">Synthesis Verdict</h4>
        <p style="font-size: 1.05rem; line-height: 1.7;">{comp_result}</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 6: PATTERN & FREQUENCY ENGINE
# ----------------------------------------------------
with tabs[5]:
    st.markdown("<h3 style='color:#f5c542;'>Pattern & Frequency Engine</h3>", unsafe_allow_html=True)
    st.markdown("Latin ciphers, angelic repetitions, and character frequency distributions.")

    cipher_input = st.text_input("Stream Analysis Field", value="The Hidden Light")
    if cipher_input:
        c_res = run_latin_cipher(cipher_input)
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Simple Cipher", c_res["simple"])
        col_p2.metric("Reverse Cipher", c_res["reverse"])
        col_p3.metric("Reduced Root", c_res["reduced"])

        st.markdown(f"**Angel Synchronicity Check:** {angel_read(str(c_res['simple']))}")
        st.markdown(f"**Frequency Scan:** {script_readings(cipher_input)}")
        st.markdown(f"**Root Interpretation:** {meaning(c_res['reduced'])}")
