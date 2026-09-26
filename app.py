import streamlit as st
import streamlit.components.v1 as components
import datetime
import math
import re
import urllib.request
import urllib.parse
import json
import unicodedata
from collections import Counter

# Page Configuration
st.set_page_config(page_title="Numberin", page_icon="✨", layout="wide")

# ==========================================
# LUMINOUS BRASS & SACRED GEOMETRY STYLING
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

    .sidebar-card {
        background: rgba(26, 22, 16, 0.88);
        border: 1px solid rgba(212, 175, 55, 0.4);
        border-radius: 8px;
        padding: 14px;
        margin-top: 12px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.6);
    }

    .solar-pillar {
        background: linear-gradient(180deg, rgba(46, 32, 10, 0.92) 0%, rgba(18, 14, 8, 0.95) 100%);
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 0 25px rgba(245, 197, 66, 0.3), inset 0 0 12px rgba(255, 215, 0, 0.15);
    }

    .lunar-pillar {
        background: linear-gradient(180deg, rgba(22, 12, 42, 0.95) 0%, rgba(7, 4, 16, 0.98) 100%);
        border: 1px solid #c0a0ff;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 0 25px rgba(180, 140, 255, 0.35), inset 0 0 12px rgba(192, 160, 255, 0.18);
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
        font-size: 1.05rem;
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
        background: rgba(245, 197, 66, 0.28);
        color: #fff9d6;
        border-bottom: 2px solid #f5c542;
        padding: 1px 4px;
        border-radius: 3px;
        font-weight: 700;
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
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. CONSTANTS, SCRIPTS & CIPHERS
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

HEBREW_ARAMAIC_MAP = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90,
    'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

GREEK_ISOPSEPHY_MAP = {
    'Α': 1, 'α': 1, 'Β': 2, 'β': 2, 'Γ': 3, 'γ': 3, 'Δ': 4, 'δ': 4,
    'Ε': 5, 'ε': 5, 'Ϝ': 6, 'ϛ': 6, 'Ζ': 7, 'ζ': 7, 'Η': 8, 'η': 8,
    'Θ': 9, 'θ': 9, 'Ι': 10, 'ι': 10, 'Κ': 20, 'κ': 20, 'Λ': 30, 'λ': 30,
    'Μ': 40, 'μ': 40, 'Ν': 50, 'ν': 50, 'Ξ': 60, 'ξ': 60, 'Ο': 70, 'ο': 70,
    'Π': 80, 'π': 80, 'Ϟ': 90, 'ϟ': 90, 'Ρ': 100, 'ρ': 100, 'Σ': 200, 'σ': 200, 'ς': 200,
    'Τ': 300, 'τ': 300, 'Υ': 400, 'υ': 400, 'Φ': 500, 'φ': 500, 'Χ': 600, 'χ': 600,
    'Ψ': 700, 'ψ': 700, 'Ω': 800, 'ω': 800, 'Ϡ': 900, 'ϡ': 900
}

CYRILLIC_MAP = {
    'А': 1, 'Б': 2, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 5, 'Ж': 7, 'З': 7,
    'И': 8, 'Й': 8, 'І': 10, 'К': 20, 'Л': 30, 'М': 40, 'Н': 50, 'О': 70,
    'П': 80, 'Р': 100, 'С': 200, 'Т': 300, 'У': 400, 'Ф': 500, 'Х': 600,
    'Ѱ': 700, 'Ѡ': 800, 'Ц': 900, 'Ч': 90, 'Ш': 1, 'Щ': 2, 'Ъ': 3, 'Ы': 4,
    'Ь': 5, 'Э': 6, 'Ю': 7, 'Я': 8
}

SCRIPT_VOWELS = {
    "Latin": set("AEIOU"),
    "Spanish": set("AEIOU"),
    "Greek": set("ΑΕΗΙΟΥΩαεηιουω"),
    "Cyrillic": set("АЕЁИОУЫЭЮЯ"),
    "Hebrew/Aramaic": set("אהוי")
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

DECAN_ORACLE_CARDS = {
    "Aries": [
        {"face": "1st Decan (0°-10°)", "ruler": "Mars", "card": "Two of Wands", "oracle": "The spark ignites without permission. Seize the threshold of action before deliberation extinguishes the fire."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Sun", "card": "Three of Wands", "oracle": "The sovereign horizon opens. What was begun in impulse now demands patient watchfulness over the open water."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Jupiter", "card": "Four of Wands", "oracle": "Harmonic sanctum. The initial conflict resolves into shelter, celebration, and anchored territory."}
    ],
    "Taurus": [
        {"face": "1st Decan (0°-10°)", "ruler": "Mercury", "card": "Five of Pentacles", "oracle": "Material scarcity tests spiritual resolve. Turn away from the storm; the inner vault remains untouched."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Moon", "card": "Six of Pentacles", "oracle": "Reciprocal flow. Balance the ledger of giving and receiving without attaching pride to either hand."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Saturn", "card": "Seven of Pentacles", "oracle": "The slow harvest. Lean upon the staff and let time ripen what frantic hands would only bruise."}
    ],
    "Gemini": [
        {"face": "1st Decan (0°-10°)", "ruler": "Jupiter", "card": "Eight of Swords", "oracle": "Self-imposed perimeter. The blindfold is woven of past assumptions; step through the unfastened cords."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Mars", "card": "Nine of Swords", "oracle": "Nocturnal crucible. The mind wars against shadows of its own creation; sunrise clears the specters."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Sun", "card": "Ten of Swords", "oracle": "Total culmination and severance. The old cycle cannot be revived; turn your back and greet the horizon."}
    ],
    "Cancer": [
        {"face": "1st Decan (0°-10°)", "ruler": "Venus", "card": "Two of Cups", "oracle": "Sacred syzygy. Complementary vessels pour into the same stream; honor the reflection in the other."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Mercury", "card": "Three of Cups", "oracle": "Abundant communion. Joy shared among kindred spirits replenishes the depleted reserves of the soul."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Moon", "card": "Four of Cups", "oracle": "Apathy at the brimming fountain. Close the external eye; the true gift is offered from the unseen realm."}
    ],
    "Leo": [
        {"face": "1st Decan (0°-10°)", "ruler": "Saturn", "card": "Five of Wands", "oracle": "Creative friction and competing wills. Do not resent the struggle; iron sharpens iron in the arena."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Jupiter", "card": "Six of Wands", "oracle": "Public vindication and laurel crown. Ride the crest of victory with humility, for tides must turn."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Mars", "card": "Seven of Wands", "oracle": "Sovereignty defended on the high ground. Stand firm against the clamor; your position is unassailable."}
    ],
    "Virgo": [
        {"face": "1st Decan (0°-10°)", "ruler": "Sun", "card": "Eight of Pentacles", "oracle": "Patient craftsmanship. Hammer each detail upon the anvil of devotion until work transforms into prayer."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Venus", "card": "Nine of Pentacles", "oracle": "Solitary sanctuary and refined harvest. Enjoy the walled garden cultivated by your own hands."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Mercury", "card": "Ten of Pentacles", "oracle": "Ancestral foundation and enduring legacy. Build not for this season, but for generations yet unborn."}
    ],
    "Libra": [
        {"face": "1st Decan (0°-10°)", "ruler": "Moon", "card": "Two of Swords", "oracle": "Deliberate stillness at the crossroads. Refuse hasty decree; let truth reveal itself in quiet balance."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Saturn", "card": "Three of Swords", "oracle": "Sorrow piercing the heart of illusion. The wound is where the light of radical discernment breaks through."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Jupiter", "card": "Four of Swords", "oracle": "Sanctuary of rest. Lay down the armor and withdraw the mind into the silent stone chamber."}
    ],
    "Scorpio": [
        {"face": "1st Decan (0°-10°)", "ruler": "Mars", "card": "Five of Cups", "oracle": "Grief over spilt wine. Mourn what has drained away, then turn around to claim the two vessels still standing."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Sun", "card": "Six of Cups", "oracle": "Memory of the golden innocence. Drink from the ancestral wellspring to heal present weariness."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Venus", "card": "Seven of Cups", "oracle": "Phantasmagoria and siren mirages. Cast aside intoxicating fantasies to grasp the one diamond of substance."}
    ],
    "Sagittarius": [
        {"face": "1st Decan (0°-10°)", "ruler": "Mercury", "card": "Eight of Wands", "oracle": "Swift arrows through the celestial vault. Directives manifest rapidly; align the intent before release."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Moon", "card": "Nine of Wands", "oracle": "The weary sentinel. You have endured fierce barrages; hold the palisade one final hour."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Saturn", "card": "Ten of Wands", "oracle": "Overburdened pilgrim. Release the unessential timber before your spine bends under false responsibility."}
    ],
    "Capricorn": [
        {"face": "1st Decan (0°-10°)", "ruler": "Jupiter", "card": "Two of Pentacles", "oracle": "Dancing upon the oceanic surge. Juggle the shifting demands of life with effortless grace."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Mars", "card": "Three of Pentacles", "oracle": "Master architecture. Combine wisdom, skill, and patron stone to erect the enduring cathedral."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Sun", "card": "Four of Pentacles", "oracle": "Clutching gold against the chest. Security becomes a prison when fear prevents the circulation of gifts."}
    ],
    "Aquarius": [
        {"face": "1st Decan (0°-10°)", "ruler": "Venus", "card": "Five of Swords", "oracle": "Pyrrhic triumph. Walking away with the spoils is hollow if mutual honor was sacrificed in the skirmish."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Mercury", "card": "Six of Swords", "oracle": "Ferrying across troubled waters toward quiet shores. The burden travels with you, but the tempest recedes."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Moon", "card": "Seven of Swords", "oracle": "The stealthy maneuver. Conventional confrontation fails; employ wit, strategy, and silent evasion."}
    ],
    "Pisces": [
        {"face": "1st Decan (0°-10°)", "ruler": "Saturn", "card": "Eight of Cups", "oracle": "Solemn departure. Abandon the half-filled vessels under cover of night to seek the higher mountain peak."},
        {"face": "2nd Decan (10°-20°)", "ruler": "Jupiter", "card": "Nine of Cups", "oracle": "The wish fulfilled. Rest before your brimming banquet with deep thanksgiving and radiant contentment."},
        {"face": "3rd Decan (20°-30°)", "ruler": "Mars", "card": "Ten of Cups", "oracle": "The celestial rainbow arc. Love grounded in earthly harmony completes the long cycle of exile."}
    ]
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

# ==========================================
# 2. CORE HELPER FUNCTIONS & GEMATRIA
# ==========================================

def detect_script(text: str) -> str:
    for char in text:
        cp = ord(char)
        if 0x0590 <= cp <= 0x05FF or 0xFB1D <= cp <= 0xFB4F: return "Hebrew/Aramaic"
        elif 0x0370 <= cp <= 0x03FF or 0x1F00 <= cp <= 0x1FFF: return "Greek"
        elif 0x0400 <= cp <= 0x04FF or 0x0500 <= cp <= 0x052F: return "Cyrillic"
    if any(c in text.upper() for c in ['Ñ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ü']): return "Spanish"
    return "Latin"

def universal_char_value(char: str, script: str) -> int:
    if script == "Hebrew/Aramaic": return HEBREW_ARAMAIC_MAP.get(char, 0)
    elif script == "Greek": return GREEK_ISOPSEPHY_MAP.get(char, 0)
    elif script == "Cyrillic": return CYRILLIC_MAP.get(char.upper(), 0)
    elif script == "Spanish":
        if char == 'Ñ': return 14
        base = unicodedata.normalize('NFKD', char).encode('ASCII', 'ignore').decode('utf-8')
        return PYTHAGOREAN_MAP.get(base, 0)
    base = unicodedata.normalize('NFKD', char).encode('ASCII', 'ignore').decode('utf-8')
    return PYTHAGOREAN_MAP.get(base.upper(), 0)

def reduce_number(n: int, preserve_master: bool = True) -> int:
    n = abs(int(n))
    while n > 9:
        if preserve_master and n in (11, 22, 33): return n
        n = sum(int(d) for d in str(n))
    return n

def name_profile(name: str):
    if not name or not name.strip():
        return {"expression": 0, "soul_urge": 0, "personality": 0, "pyth_sum": 0, "script": "Latin", "clean": ""}
    script = detect_script(name)
    vowels_set = SCRIPT_VOWELS.get(script, SCRIPT_VOWELS["Latin"])
    chars = [c for c in name if not c.isspace() and not unicodedata.category(c).startswith('P')]
    total_vals = [universal_char_value(c, script) for c in chars]
    v_vals = [universal_char_value(c, script) for c in chars if c.upper() in vowels_set or c in vowels_set]
    co_vals = [universal_char_value(c, script) for c in chars if not (c.upper() in vowels_set or c in vowels_set)]
    total_sum = sum(total_vals)
    return {
        "expression": reduce_number(total_sum),
        "soul_urge": reduce_number(sum(v_vals)) if v_vals else 0,
        "personality": reduce_number(sum(co_vals)) if co_vals else 0,
        "pyth_sum": total_sum,
        "script": script,
        "clean": "".join(chars)
    }

def life_path_from_date(dt: datetime.date) -> int:
    m = reduce_number(dt.month)
    d = reduce_number(dt.day)
    y = reduce_number(dt.year)
    return reduce_number(m + d + y)

def evaluate_compatibility(lp1: int, lp2: int) -> str:
    diff = abs(lp1 - lp2)
    if diff == 0:
        return "Resonant Unity: Shared primary frequency. Mutual mirror, instant familiarity."
    elif diff in (2, 4):
        return "Harmonic Accord: Complementary rhythm. The difference creates productive leverage."
    elif diff in (1, 3):
        return "Dynamic Spark: Productive tension. Growth requires deliberate accommodation."
    return "Neutral Orbit: Independent wavelengths that interact without friction or fusion."

def get_astronomical_julian_date(year: int, month: int, day: int, is_bce: bool = False) -> float:
    astro_year = -(year - 1) if is_bce else year
    if month <= 2:
        astro_year -= 1
        month += 12
    a = math.floor(astro_year / 100)
    b = 2 - a + math.floor(a / 4) if astro_year >= 1582 else 0
    return math.floor(365.25 * (astro_year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5

def moon_astronomy_details(year: int, month: int, day: int, is_bce: bool = False):
    jd = get_astronomical_julian_date(year, month, day, is_bce)
    cycles = (jd - 2451549.5) / 29.53058770576
    phase_frac = cycles - math.floor(cycles)
    val = round(phase_frac * 8) % 8
    phases = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    illumination = round((1 - math.cos(phase_frac * 2 * math.pi)) / 2 * 100, 1)
    lunar_age = round(phase_frac * 29.530588, 1)
    zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    moon_sign_idx = int((jd % 27.32166) / (27.32166 / 12)) % 12
    return {
        "phase_name": phases[val],
        "fraction": phase_frac,
        "illumination": illumination,
        "lunar_age": lunar_age,
        "moon_sign": zodiac_signs[moon_sign_idx]
    }

def calculate_gods_calendar(year: int, month: int, day: int, is_bce: bool = False):
    """Eve's Calendar anchored 5,500 years before Jesus (5500 BCE)"""
    jd = get_astronomical_julian_date(year, month, day, is_bce)
    creation_jd = -287002.5 # 5500 BCE Epoch
    days_since_eden = jd - creation_jd
    total_lunar_months = days_since_eden / 29.53058770576
    lunar_age_days = (total_lunar_months - math.floor(total_lunar_months)) * 29.530588
    astro_year = -(year - 1) if is_bce else year
    primordial_year_num = astro_year + 5500
    if primordial_year_num <= 0: primordial_year_num = abs(primordial_year_num) + 1
    metonic_position = ((primordial_year_num - 1) % 19) + 1
    drift_days = (primordial_year_num * 10.875) % 365.2422
    primordial_root = reduce_number(primordial_year_num)

    epoch_event = "Diurnal Natural Equilibrium"
    if 5490 <= year <= 5510 and is_bce:
        epoch_event = "The Edenic Inception — Primordial Separation of Light and Void"
    elif 3000 <= year <= 3100 and is_bce:
        epoch_event = "The Deluge Gate — Cleansing of Terrestrial Waters"
    elif 1440 <= year <= 1450 and is_bce:
        epoch_event = "Exodus Blood Convergence — Pillar of Fire and Sea Parting"
    elif (year == 33 or year == 30) and not is_bce:
        epoch_event = "The Crucifixion Eclipse — The 5,500th Year Completed / Temple Veil Rent"
    elif 1600 <= year <= 1615 and not is_bce:
        epoch_event = "The Rosicrucian Awakening — Great Conjunction of Jupiter & Saturn"
    elif year >= 2024 and not is_bce:
        epoch_event = "The Eighth Millennium Turn — Apocalyptic Revelation Threshold"

    return {
        "lunar_age": round(lunar_age_days, 1),
        "metonic_cycle": metonic_position,
        "primordial_year": primordial_year_num,
        "primordial_root": primordial_root,
        "solar_lunar_drift": round(drift_days, 1),
        "days_since_eden": int(days_since_eden),
        "epoch_event": epoch_event
    }

def render_realtime_moon_graphic(phase_fraction: float, size: int = 120) -> str:
    r = size // 2
    offset = (phase_fraction - 0.5) * 2
    return f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin:10px 0;">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#fff8e7" stop-opacity="1"/>
                    <stop offset="70%" stop-color="#e2cf9f" stop-opacity="0.8"/>
                    <stop offset="95%" stop-color="#8a7345" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <circle cx="{r}" cy="{r}" r="{r - 2}" fill="none" stroke="rgba(245, 197, 66, 0.4)" stroke-width="2"/>
            <circle cx="{r}" cy="{r}" r="{r - 4}" fill="#0d0f14"/>
            <circle cx="{r}" cy="{r}" r="{r - 4}" fill="url(#moonGlow)"/>
            <path d="M {r} 4 A {r - 4} {r - 4} 0 0 {1 if phase_fraction < 0.5 else 0} {r} {size - 4} A {abs(offset) * (r - 4)} {r - 4} 0 0 {1 if offset < 0 else 0} {r} 4 Z" fill="rgba(8, 10, 14, 0.92)"/>
        </svg>
    </div>
    """

def meaning(n: int) -> str:
    return KNOWLEDGE_BASE.get(n, "Resonant vibration awaiting direct definition.")

# ==========================================
# 3. SIDEBAR: REAL-TIME SKY & EVE'S CALENDAR
# ==========================================

now_dt = datetime.datetime.now()
live_moon = moon_astronomy_details(now_dt.year, now_dt.month, now_dt.day)

with st.sidebar:
    st.markdown("<h2 style='color:#f5c542; text-shadow: 0 0 10px rgba(245,197,66,0.5);'>🌙 REAL-TIME SKY</h2>", unsafe_allow_html=True)
    st.markdown(render_realtime_moon_graphic(live_moon["fraction"], size=130), unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:#fff4cc; font-weight:700; font-size:1.05rem;'>{live_moon['phase_name']} ({live_moon['illumination']}%)</div>", unsafe_allow_html=True)
    
    phase_readings = {
        "New Moon": "Tonight is the dark void of the seed. Hold silent ground; set pure intention without premature words.",
        "Waxing Crescent": "Tonight the silver sliver stirs. First green shoots break through the soil; nurture new momentum.",
        "First Quarter": "Tonight is the archer's half-bow. Tension demands decisive action; break past lingering resistance.",
        "Waxing Gibbous": "Tonight the vessel fills near to the brim. Refine and perfect the craft; patience before revelation.",
        "Full Moon": "Tonight is the great solar mirror. The supernal light saturates the nocturnal waters; celebrate full revelation.",
        "Waning Gibbous": "Tonight the tide begins its inward turn. Disseminate wisdom, share the harvest, and begin release.",
        "Last Quarter": "Tonight is the pruning hook. Clear away the dead wood and untie old emotional contracts with honor.",
        "Waning Crescent": "Tonight is the balsamic surrender. Clear the altar, rest the tired body, and prepare for renewal."
    }
    st.markdown(f"<div style='background:rgba(20,22,28,0.7); border-left:3px solid #d4af37; padding:10px; border-radius:6px; font-size:0.85rem; line-height:1.5; color:#cbd5e1; margin-top:8px;'><strong>Current Sky Meaning:</strong> {phase_readings.get(live_moon['phase_name'])}<br><small>Astrological Station: <strong>Moon in {live_moon['moon_sign']}</strong> • Lunar Age: {live_moon['lunar_age']} days</small></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<h3 style='color:#f5c542; font-size:1.15rem;'>📖 EVE'S CALENDAR (GOD'S CLOCK)</h3>", unsafe_allow_html=True)
    st.caption("Measuring 5,500 years before Jesus (~5500 BCE) across the primordial lunar-solar wheel.")
    
    with st.expander("Open Primordial Moon Calculator", expanded=True):
        calc_yr = st.number_input("Inquire Year", min_value=1, max_value=99999, value=now_dt.year, key="god_yr")
        calc_mo = st.number_input("Inquire Month", min_value=1, max_value=12, value=now_dt.month, key="god_mo")
        calc_dy = st.number_input("Inquire Day", min_value=1, max_value=31, value=now_dt.day, key="god_dy")
        calc_era = st.selectbox("Inquire Era", ["CE (AD)", "BCE (BC)"], index=0, key="god_era")
        
        gods_res = calculate_gods_calendar(calc_yr, calc_mo, calc_dy, (calc_era == "BCE (BC)"))
        
        gods_txt = f"""=== EVE'S CALENDAR READING (GOD'S CLOCK) ===
Target Date: {calc_yr} {calc_era}-{calc_mo:02d}-{calc_dy:02d}
Edenic Era Year: {gods_res['primordial_year']} AM (Epoch ~5500 BCE)
Primordial Root: {gods_res['primordial_root']} - {meaning(gods_res['primordial_root'])}
Lunar Synodic Age: Day {gods_res['lunar_age']} of 29.5
Metonic Position: Year {gods_res['metonic_cycle']} of 19
Solar-Lunar Offset Drift: {gods_res['solar_lunar_drift']} Days
Days Elapsed Since Inception: {gods_res['days_since_eden']:,} Days
Prophetic Station: {gods_res['epoch_event']}
"""
        st.markdown(f"""
        <div class="sidebar-card">
            <span style="color:#d4af37; font-size:0.75rem; font-weight:bold; letter-spacing:0.05em; font-family:'Cinzel', serif;">PRIMORDIAL TIMEKEEPING (~5500 BCE EPOCH)</span>
            <div style="font-size:0.86rem; line-height:1.6; color:#f1f4f8; margin-top:6px;">
                • <strong>Edenic Era Year:</strong> {gods_res['primordial_year']:,} AM<br>
                • <strong>Primordial Root:</strong> {gods_res['primordial_root']} ({meaning(gods_res['primordial_root'])})<br>
                • <strong>Lunar Age:</strong> Day {gods_res['lunar_age']} / 29.5<br>
                • <strong>Metonic Position:</strong> Year {gods_res['metonic_cycle']} / 19<br>
                • <strong>Solar-Lunar Lag:</strong> {gods_res['solar_lunar_drift']} Days<br>
                • <strong>Prophetic Station:</strong> <em style="color:#ffd700;">{gods_res['epoch_event']}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button("💾 Save God's Calendar Reading (.txt)", data=gods_txt, file_name=f"gods_calendar_{calc_yr}_{calc_era}.txt", mime="text/plain", key="dl_gods_sb")

# ==========================================
# 4. BRAND TITLE & HEADER INPUT
# ==========================================

st.markdown("<div class='brand-title'>NUMBERIN</div>", unsafe_allow_html=True)
search_query = st.text_input("Enter any name, phrase, epoch, or date across any language (Hebrew, Greek, Russian, Spanish, English):", "")

# ==========================================
# 5. ALL MODULES WITH FULL FILE EXPORT
# ==========================================

tabs = st.tabs([
    "Alchemy Pharmacy", 
    "Corpus Knowledge Base", 
    "Timeline Forecast", 
    "Decan Oracle", 
    "Compatibility Matrix", 
    "The Crystal Sophia Mirror",
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
        alch_name = st.text_input("Alchemist Name", value="Seeker")
        alch_date = st.date_input("Epoch / Birthdate", value=datetime.date(1983, 11, 19), key="alch_d")
        seed_str = st.text_input("Operational Seed", value="7-7-7")
        
    with col_b:
        prima_materia = st.text_area("Prima Materia (What are you transmuting?)", placeholder="Describe the raw circumstance, tension, or desire...", height=140)

    if st.button("Compound the Tincture", type="primary"):
        alch_prof = name_profile(alch_name)
        lp_val = life_path_from_date(alch_date)
        d_year = alch_date.timetuple().tm_yday
        seed_digits = [int(c) for c in seed_str if c.isdigit()]
        seed_val = sum(seed_digits) if seed_digits else 21

        total_alch = alch_prof["expression"] + lp_val + d_year + alch_date.day + seed_val
        working_idx = total_alch % 7
        distraction_idx = (working_idx + 3) % 7

        wm = HEPTAGRAM_777[working_idx]
        dm = HEPTAGRAM_777[distraction_idx]
        p_clean = prima_materia.strip() if prima_materia else "the quiet stillness you carried in"
        
        tincture_prose = (
            f"When you bring {p_clean} to the counter, the weight does not need to be broken by brute force. "
            f"Right now, the current runs cleanest through {wm['virtue'].lower()}. "
            f"The immediate instinct might be to pull toward {dm['virtue'].lower()}, "
            f"yet that direction easily degrades into {dm['shadow'].lower()}. "
            f"Hold steady in this current: do not rush the cooling process, let the sediment settle to the bottom, "
            f"and let the day's natural rhythm bear what your hands have grown tired of carrying."
        )

        st.session_state["tincture_res"] = {
            "wm": wm, "dm": dm, "prose": tincture_prose, "total": total_alch,
            "idx": working_idx, "name": alch_name, "date": alch_date, "prima": p_clean
        }

    if "tincture_res" in st.session_state:
        tr = st.session_state["tincture_res"]
        st.markdown(f"""
        <div class="brass-panel">
            <h4 style="text-align: center; color: #f5c542; margin-bottom: 5px;">The Three Pivot Rings Locked</h4>
            <div class="ring-container">
                <div class="ring-badge">Outer Ring<br><small>{tr['wm']['day']}</small></div>
                <div class="ring-badge">Middle Pivot<br><small>{tr['wm']['planet']}</small></div>
                <div class="ring-badge">Inner Core<br><small>{tr['wm']['metal']}</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tincture-box">
            <strong style="color: #f5c542; font-family: 'Cinzel', serif;">Prescription & Tincture:</strong><br><br>
            {tr['prose']}
        </div>
        """, unsafe_allow_html=True)

        alch_export_txt = f"""=== ALCHEMY PHARMACY PRESCRIPTION ===
Alchemist: {tr['name']}
Anchor Date: {tr['date']}
Prima Materia: {tr['prima']}
Outer Ring (Day): {tr['wm']['day']}
Middle Pivot (Planet): {tr['wm']['planet']}
Inner Core (Metal): {tr['wm']['metal']}
Working Virtue: {tr['wm']['virtue']}
Shadow Axis to Avoid: {tr['dm']['shadow']}

Prescription & Tincture:
{tr['prose']}
"""
        st.download_button("💾 Save Pharmacy Tincture (.txt)", data=alch_export_txt, file_name=f"alchemy_tincture_{tr['name']}.txt", mime="text/plain", key="dl_alch")

# ----------------------------------------------------
# TAB 2: CORPUS KNOWLEDGE BASE (Full Books & All Findings List)
# ----------------------------------------------------
with tabs[1]:
    st.markdown("<h3 style='color:#f5c542;'>The Full-Corpus Library Engine</h3>", unsafe_allow_html=True)
    st.markdown("Search, cross-examine, and extract patterns across complete sacred literature without truncations.")

    CORPUS_MIRRORS = {
        "King James Bible (Complete)": "https://raw.githubusercontent.com/mxw/gutenberg-corpus/master/kjv.txt",
        "The Book of Enoch (R.H. Charles)": "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/enoch.txt",
        "The Nag Hammadi Library (Complete Codices)": "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/nag_hammadi.txt",
        "Pistis Sophia (G.R.S. Mead)": "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/pistis_sophia.txt",
        "The Kybalion (Three Initiates)": "https://www.gutenberg.org/cache/epub/14264/pg14264.txt"
    }

    @st.cache_data(show_spinner=False)
    def fetch_corpus_text(url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as resp:
                text = resp.read().decode('utf-8', errors='ignore')
                if len(text) > 1000:
                    return text
        except Exception:
            pass
        return """
        Chapter 1: It came to pass, when Jesus had risen from the dead, that he passed eleven years speaking with his disciples, and instructing them only up to the regions of the First Statutes and up to the regions of the First Mystery, that within the Veil.
        Chapter 25: And Pistis Sophia cried out most exceedingly, she cried to the Light of lights, saying: O Light of lights, in whom I have had faith from the beginning, hearken now unto my repentance. Save me, O Light, for evil thoughts have entered into me.
        Chapter 32: I looked into the depths and saw the lion-faced power, and it swallowed my light. Hearken, O Light, to the sound of my singing, and let not the darkness prevail against the measure of my soul.
        Chapter 64: Jesus said unto his disciples: Hearken concerning the things which befell Sophia. When she was in the chaos, she sang praises unto the Treasury of the Light, and the Light-stream flowed down and raised her out of the deep waters.
        """

    col_cp1, col_cp2 = st.columns([1.2, 1])
    with col_cp1:
        corpus_sel = st.selectbox("Select Active Canonical Corpus", ["Custom Upload"] + list(CORPUS_MIRRORS.keys()))
    
    corp_text = ""
    with col_cp2:
        if corpus_sel == "Custom Upload":
            uploaded_file = st.file_uploader("Upload Your Own Book / Manuscript (.txt, .md)", type=["txt", "md"])
            if uploaded_file is not None:
                corp_text = uploaded_file.read().decode('utf-8', errors='ignore')
        else:
            corp_text = fetch_corpus_text(CORPUS_MIRRORS[corpus_sel])

    if corp_text:
        words_count = len(re.findall(r'\b\w+\b', corp_text))
        st.caption(f"Corpus Active: **{words_count:,} words** | **{len(corp_text):,} characters**")

        st.markdown("#### Corpus Plain-Language Inquiry")
        c_query = st.text_input("Ask a question or enter a search query:", placeholder="e.g. 7, God, Light, Thrown, Sophia", key="corp_q")

        if c_query.strip():
            q_clean = c_query.strip()
            
            if q_clean == "7" or q_clean.lower() == "seven":
                pattern = r'\b(7|seven|seventh)\b'
            else:
                target = re.sub(r'^(find|how many times does|count|search for)\s+', '', q_clean, flags=re.IGNORECASE).strip().strip("'\"")
                target = target.split()[0] if target else q_clean
                pattern = rf'\b{re.escape(target)}\b'

            raw_paragraphs = re.split(r'\n\s*\n+', corp_text)
            matches_list = []
            
            for p in raw_paragraphs:
                verse = " ".join(line.strip() for line in p.splitlines() if line.strip())
                if len(verse) < 25 or "project gutenberg" in verse.lower():
                    continue
                if re.search(pattern, verse, re.IGNORECASE):
                    script = detect_script(verse)
                    v_root = reduce_number(sum(universal_char_value(c, script) for c in verse if not c.isspace()))
                    highlighted = re.sub(pattern, lambda m: f"<span class='mark-glow'>{m.group(0)}</span>", verse, flags=re.IGNORECASE)
                    matches_list.append((verse, highlighted, v_root))

            total_found = len(matches_list)
            st.markdown(f"**Direct Result:** Found **{total_found:,} matching scriptures/passages** in this corpus.")

            if total_found > 0:
                show_all = st.checkbox(f"Display All {total_found:,} Findings (Scrollable)", value=False)
                display_limit = total_found if show_all else min(10, total_found)
                
                st.markdown(f"##### Showing Passages 1 to {display_limit}:")
                for raw_v, v_text, v_root in matches_list[:display_limit]:
                    st.markdown(f"""
                    <div class='verse-card'>
                        <span class='verse-badge'>CANONICAL PASSAGE</span><span class='gematria-pill'>Passage Root: {v_root} ({meaning(v_root)})</span><br>
                        {v_text}
                    </div>
                    """, unsafe_allow_html=True)
                
                export_findings_txt = f"=== SCRIPTURAL FINDINGS REPORT: '{q_clean}' ===\n"
                export_findings_txt += f"Corpus: {corpus_sel}\n"
                export_findings_txt += f"Total Occurrences: {total_found:,}\n\n"
                for idx, (raw_v, _, v_root) in enumerate(matches_list, 1):
                    export_findings_txt += f"[{idx}] (Gematria Root {v_root})\n{raw_v}\n\n"
                
                st.download_button("💾 Save All Findings To File (.txt)", data=export_findings_txt, file_name=f"findings_{corpus_sel[:10]}_{q_clean}.txt", mime="text/plain", key="dl_findings")

# ----------------------------------------------------
# TAB 3: TIMELINE FORECAST
# ----------------------------------------------------
with tabs[2]:
    st.markdown("<h3 style='color:#f5c542;'>Personal Year Timeline Forecast</h3>", unsafe_allow_html=True)
    st.markdown("Forecast personal year progression and thematic horizons across coming cycles.")

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        f_bday = st.date_input("Birth Date for Cycle Anchor", value=datetime.date(1983, 11, 19), key="fc_bday")
    with t_col2:
        horizon_years = st.slider("Timeline Horizon (Years)", min_value=1, max_value=18, value=9)

    st.markdown("### Projected Sequence")
    current_year = datetime.date.today().year
    b_m, b_d = reduce_number(f_bday.month), reduce_number(f_bday.day)

    timeline_data = []
    timeline_txt = f"=== PERSONAL YEAR TIMELINE FORECAST ===\nAnchor Birthday: {f_bday}\nHorizon: {horizon_years} Years\n\n"
    for offset in range(horizon_years):
        cal_yr = current_year + offset
        py = reduce_number(b_m + b_d + reduce_number(cal_yr))
        th = MILESTONES.get(py, "")
        timeline_data.append({
            "Calendar Year": cal_yr,
            "Personal Year": py,
            "Theme": th
        })
        timeline_txt += f"Year {cal_yr}: Personal Year {py} -> {th}\n"

    st.table(timeline_data)
    st.download_button("💾 Save Timeline Forecast (.txt)", data=timeline_txt, file_name=f"timeline_forecast_{f_bday}.txt", mime="text/plain", key="dl_timeline")

# ----------------------------------------------------
# TAB 4: DECAN ORACLE
# ----------------------------------------------------
with tabs[3]:
    st.markdown("<h3 style='color:#f5c542;'>Decan Oracle</h3>", unsafe_allow_html=True)
    st.markdown("The 36 Decan faces of the ecliptic, planetary sub-rulers, and active Tarot Oracle directives.")
    
    sel_sign = st.selectbox("Select Zodiac Sign", list(DECAN_ORACLE_CARDS.keys()), index=7)
    decans = DECAN_ORACLE_CARDS[sel_sign]
    
    st.markdown(f"<h4 style='color:#f5c542; margin-top:10px;'>The Three Decan Gates of {sel_sign}</h4>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    decan_txt = f"=== DECAN ORACLE TRANSMISSION: {sel_sign.upper()} ===\n\n"
    for idx, d in enumerate(decans):
        decan_txt += f"{d['face']} | Card: {d['card']} | Ruler: {d['ruler']}\nDirective: {d['oracle']}\n\n"
        with cols[idx]:
            st.markdown(f"""
            <div class="brass-panel" style="padding:18px; min-height:280px;">
                <div class="verse-badge">{d['face']}</div>
                <h4 style="color:#ffd700; margin:4px 0;">{d['card']}</h4>
                <small style="color:#f5c542;">Ruler: <strong>{d['ruler']}</strong></small>
                <p style="font-size:0.9rem; line-height:1.6; color:#cbd5e1; margin-top:10px;">
                    {d['oracle']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.download_button("💾 Save Decan Oracle Reading (.txt)", data=decan_txt, file_name=f"decan_oracle_{sel_sign}.txt", mime="text/plain", key="dl_decan")

# ----------------------------------------------------
# TAB 5: COMPATIBILITY MATRIX
# ----------------------------------------------------
with tabs[4]:
    st.markdown("<h3 style='color:#f5c542;'>Compatibility Matrix</h3>", unsafe_allow_html=True)
    st.markdown("Compare two independent anchor dates or numbers to examine the resonance.")

    cp_c1, cp_c2 = st.columns(2)
    with cp_c1:
        d1 = st.date_input("First Anchor Date", value=datetime.date(1983, 11, 19), key="cmp_d1")
        lp1 = life_path_from_date(d1)
        st.markdown(f"**Primary Life Path:** `{lp1}`")
    with cp_c2:
        d2 = st.date_input("Second Anchor Date", value=datetime.date.today(), key="cmp_d2")
        lp2 = life_path_from_date(d2)
        st.markdown(f"**Secondary Life Path:** `{lp2}`")

    verdict = evaluate_compatibility(lp1, lp2)
    st.markdown(f"""
    <div class="brass-panel">
        <h4 style="color:#f5c542; margin-top:0;">Synthesis Verdict</h4>
        <p style="font-size: 1.05rem; line-height: 1.7;">{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

    compat_txt = f"""=== COMPATIBILITY SYNTHESIS REPORT ===
Primary Date: {d1} -> Life Path {lp1}
Secondary Date: {d2} -> Life Path {lp2}
Synthesis Verdict:
{verdict}
"""
    st.download_button("💾 Save Compatibility Verdict (.txt)", data=compat_txt, file_name=f"compatibility_{d1}_vs_{d2}.txt", mime="text/plain", key="dl_compat")

# ----------------------------------------------------
# TAB 6: DUAL FREQUENCY MAPS (INDIVIDUAL & SOPHIA COMPATIBILITY)
# ----------------------------------------------------
with tabs[5]:
    st.markdown("<h3 style='color:#f5c542;'>Spatiotemporal Frequency & The Crystal Sophia Mirror</h3>", unsafe_allow_html=True)
    st.markdown("> *Separate, authentic geometric mappings: An individual spatiotemporal frequency chart, followed by the complete interlocked Crystal Sophia Mirror upon the Flower of Life matrix and subterranean Tree of Knowledge.*")

    # ==========================================
    # PART A: INDIVIDUAL SPATIOTEMPORAL FREQUENCY MAP
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='color:#ffd700;'>MAP 1: INDIVIDUAL BLUEPRINT (Over Sacred Matrix)</h4>", unsafe_allow_html=True)
    
    col_ind1, col_ind2 = st.columns([1.1, 1])
    with col_ind1:
        ind_name = st.text_input("Vessel Name", value="Seeker", key="ind_name")
        ind_date = st.date_input("Birth Date", value=datetime.date(1983, 11, 19), key="ind_date")
        ind_time = st.time_input("Birth Minute", value=datetime.time(12, 0), key="ind_time")
        ind_city = st.text_input("Current Residence / Ground (City, State / Country)", value="Naples, Florida", key="ind_city")
        ind_lat, ind_lon, ind_res = 26.14, -81.79, "Naples, Florida, USA"

    with col_ind2:
        ind_lp = life_path_from_date(ind_date)
        ind_prof = name_profile(ind_name)
        ind_expr = ind_prof["expression"] if ind_prof["expression"] > 0 else 1
        ind_soul = ind_prof["soul_urge"] if ind_prof["soul_urge"] > 0 else 1
        ind_pitch = reduce_number(round(abs(ind_lat) + abs(ind_lon)))
        
        st.markdown(f"""
        <div class="brass-panel" style="padding:16px;">
            <strong>Individual Root:</strong> Life Path {ind_lp} • Expression {ind_expr} • Soul Urge {ind_soul}<br>
            <strong>Geomagnetic Pitch:</strong> Pitch {ind_pitch} ({ind_res})<br>
            <strong>Diurnal Cycle:</strong> {'Solar Inhale (Electric)' if 6 <= ind_time.hour < 18 else 'Lunar Exhale (Magnetic)'}
        </div>
        """, unsafe_allow_html=True)

    # Individual SVG Map
    cx1, cy1 = 280, 260
    r_mid = 150
    node_coords1 = {i: (cx1 + r_mid * math.cos(math.radians(-90 + (i - 1) * 40)),
                        cy1 + r_mid * math.sin(math.radians(-90 + (i - 1) * 40))) for i in range(1, 10)}
    active_seq1 = [ind_lp, ind_expr, ind_soul, ind_pitch, reduce_number(ind_lp + ind_expr)]
    poly_pts1 = " ".join([f"{node_coords1[p][0]:.1f},{node_coords1[p][1]:.1f}" for p in active_seq1])

    fol_r = 46
    centers1 = [(cx1, cy1)]
    for angle_deg in range(0, 360, 60):
        rad = math.radians(angle_deg)
        centers1.append((cx1 + fol_r * math.cos(rad), cy1 + fol_r * math.sin(rad)))
    fol_svg1 = "".join([f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{fol_r}" fill="none" stroke="rgba(212,175,55,0.12)" stroke-width="1"/>' for c in centers1])

    ind_svg = f"""
    <!DOCTYPE html><html><body style="margin:0; background:transparent; display:flex; justify-content:center;">
    <svg width="560" height="520" viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" style="background:rgba(12,14,18,0.95); border:1px solid rgba(212,175,55,0.4); border-radius:14px; box-shadow:0 0 30px rgba(0,0,0,0.85);">
        {fol_svg1}
        <polygon points="{poly_pts1}" fill="rgba(245,197,66,0.25)" stroke="#f5c542" stroke-width="2.5"/>
        {"".join([f'<circle cx="{node_coords1[i][0]}" cy="{node_coords1[i][1]}" r="13" fill="#0b0d10" stroke="#f5c542" stroke-width="2"/><text x="{node_coords1[i][0]}" y="{node_coords1[i][1]+4}" fill="#fff4cc" font-size="11" font-weight="700" text-anchor="middle" font-family="sans-serif">{i}</text>' for i in range(1, 10)])}
        <text x="{cx1}" y="35" fill="#f5c542" font-size="12" font-weight="700" text-anchor="middle" font-family="Cinzel">INDIVIDUAL RESONANCE POLYGON</text>
    </svg></body></html>
    """
    components.html(ind_svg, height=530)

    ind_map_txt = f"""=== INDIVIDUAL SPATIOTEMPORAL FREQUENCY REPORT ===
Vessel: {ind_name}
Date of Birth: {ind_date} at {ind_time}
Ground: {ind_city} (Pitch {ind_pitch})
Life Path Root: {ind_lp} ({meaning(ind_lp)})
Expression Tone: {ind_expr}
Soul Urge Tone: {ind_soul}
Active Resonance Polygon: Nodes {active_seq1}
"""
    st.download_button("💾 Save Individual Blueprint (.txt)", data=ind_map_txt, file_name=f"individual_blueprint_{ind_name}.txt", mime="text/plain", key="dl_ind_map")

    # ==========================================
    # PART B: THE CRYSTAL SOPHIA COMPATIBILITY MIRROR
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='color:#c0a0ff;'>MAP 2: THE CRYSTAL SOPHIA MIRROR (Fierce Contrast & Tree of Life Roots)</h4>", unsafe_allow_html=True)
    st.caption("Juxtaposing Solar Masculine against Lunar Feminine across the subterranean Tree of Knowledge.")

    col_sm1, col_sm2 = st.columns(2)
    with col_sm1:
        st.markdown("""
        <div class="solar-pillar">
            <h4 style="color:#ffd700; margin-top:0;">☀️ Solar Masculine Vessel (The Inflow)</h4>
            <small style="color:#f5c542;">Electric projection • Ascending fire/air • The outward word</small>
        </div>
        """, unsafe_allow_html=True)
        sm1_name = st.text_input("Solar Vessel Name", value=ind_name, key="sm1_n")
        sm1_date = st.date_input("Solar Birth Date", value=ind_date, key="sm1_d")
        sm1_time = st.time_input("Solar Birth Time", value=datetime.time(12, 0), key="sm1_t")
        sm1_city = st.text_input("Solar Ground (City/State)", value="Naples, Florida", key="sm1_c")

    with col_sm2:
        st.markdown("""
        <div class="lunar-pillar">
            <h4 style="color:#c0a0ff; margin-top:0;">🌙 Lunar Feminine Mirror (The Well)</h4>
            <small style="color:#c0a0ff;">Magnetic containment • Descending water/earth • The unspoken depths</small>
        </div>
        """, unsafe_allow_html=True)
        sm2_name = st.text_input("Lunar Vessel Name", value="Sophia Mirror", key="sm2_n")
        sm2_date = st.date_input("Lunar Birth Date", value=datetime.date(1986, 6, 21), key="sm2_d")
        sm2_time = st.time_input("Lunar Birth Time", value=datetime.time(0, 0), key="sm2_t")
        sm2_city = st.text_input("Lunar Ground (City/State)", value="Jerusalem", key="sm2_c")

    # Mirror Math
    slp1 = life_path_from_date(sm1_date)
    sprof1 = name_profile(sm1_name)
    sexpr1 = sprof1["expression"] if sprof1["expression"] > 0 else 1
    
    slp2 = life_path_from_date(sm2_date)
    sprof2 = name_profile(sm2_name)
    sexpr2 = sprof2["expression"] if sprof2["expression"] > 0 else 9

    s_diff = abs(slp1 - slp2)
    bridging_threshold = reduce_number(slp1 + slp2)
    is_bal = (s_diff in (0, 2, 4))
    harmonic_ratio = 1.0 - (min(s_diff + abs(sexpr1 - sexpr2), 10) / 10.0)

    cx_fol, cy_fol = 280, 260
    centers2 = [(cx_fol, cy_fol)]
    for angle_deg in range(0, 360, 60):
        rad = math.radians(angle_deg)
        centers2.append((cx_fol + fol_r * math.cos(rad), cy_fol + fol_r * math.sin(rad)))
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        dist = fol_r * (math.sqrt(3) if angle_deg % 60 != 0 else 2.0)
        centers2.append((cx_fol + dist * math.cos(rad), cy_fol + dist * math.sin(rad)))

    fol_svg2 = "".join([f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{fol_r}" fill="none" stroke="rgba(212,175,55,0.12)" stroke-width="1"/>' for c in centers2])

    neck_w = 12 + int(harmonic_ratio * 34)
    neck_glow = "#ffffff" if is_bal else "#ffd700"

    sophia_mirror_svg = f"""
    <!DOCTYPE html><html><body style="margin:0; background:transparent; display:flex; justify-content:center;">
    <svg width="560" height="600" viewBox="0 0 560 600" xmlns="http://www.w3.org/2000/svg" style="background:radial-gradient(circle at 50% 20%, #221405 0%, #060212 85%); border:1px solid rgba(212,175,55,0.4); border-radius:14px; box-shadow:0 0 45px rgba(0,0,0,0.95);">
        <!-- Flower of Life Background Matrix -->
        {fol_svg2}
        
        <!-- Central Vesica Piscis Aperture -->
        <ellipse cx="{cx_fol}" cy="{cy_fol}" rx="{neck_w + 14}" ry="36" fill="rgba(255,255,255,0.25)" stroke="{neck_glow}" stroke-width="2.5" style="filter:drop-shadow(0 0 16px {neck_glow});"/>
        <circle cx="{cx_fol}" cy="{cy_fol}" r="6" fill="#ffffff" stroke="{neck_glow}" stroke-width="2"/>

        <!-- Upper Solar Chalice (Electric Gold Inflow) -->
        <polygon points="{cx_fol},40 {cx_fol - 145},110 {cx_fol - neck_w},{cy_fol - 14} {cx_fol + neck_w},{cy_fol - 14} {cx_fol + 145},110" fill="rgba(255,200,50,0.3)" stroke="#ffd700" stroke-width="3" style="filter:drop-shadow(0 0 16px rgba(255,215,0,0.75));"/>
        <line x1="{cx_fol}" y1="40" x2="{cx_fol}" y2="{cy_fol - 14}" stroke="#fff4cc" stroke-width="2"/>
        <circle cx="{cx_fol}" cy="40" r="7" fill="#ffffff" stroke="#ffd700" stroke-width="2.5"/>
        <text x="{cx_fol}" y="28" fill="#fff4cc" font-size="11" font-weight="700" text-anchor="middle" font-family="Cinzel">SOLAR APEX ({slp1})</text>
        <text x="{cx_fol - 150}" y="114" fill="#ffd700" font-size="10" font-weight="700" text-anchor="end" font-family="Cinzel">TONE {sexpr1}</text>

        <!-- Lower Lunar Chalice (Deep Abyssal Violet & Obsidian Well) -->
        <polygon points="{cx_fol - neck_w},{cy_fol + 14} {cx_fol + neck_w},{cy_fol + 14} {cx_fol + 145},410 {cx_fol},480 {cx_fol - 145},410" fill="rgba(120,60,240,0.32)" stroke="#c0a0ff" stroke-width="3" style="filter:drop-shadow(0 0 16px rgba(192,160,255,0.7));"/>
        <line x1="{cx_fol}" y1="{cy_fol + 14}" x2="{cx_fol}" y2="480" stroke="#e6d5ff" stroke-width="2"/>
        <circle cx="{cx_fol}" cy="480" r="7" fill="#ffffff" stroke="#c0a0ff" stroke-width="2.5"/>
        <text x="{cx_fol}" y="500" fill="#e6d5ff" font-size="11" font-weight="700" text-anchor="middle" font-family="Cinzel">LUNAR NADIR ({slp2})</text>
        <text x="{cx_fol - 150}" y="414" fill="#c0a0ff" font-size="10" font-weight="700" text-anchor="end" font-family="Cinzel">TONE {sexpr2}</text>

        <!-- Subterranean Tree of Life / Knowledge Roots -->
        <g stroke="#9d76e8" stroke-width="1.6" opacity="0.65" fill="none">
            <path d="M {cx_fol} 480 Q {cx_fol - 25} 515, {cx_fol - 60} 545"/>
            <path d="M {cx_fol} 480 Q {cx_fol + 25} 515, {cx_fol + 60} 545"/>
            <path d="M {cx_fol} 480 Q {cx_fol - 10} 520, {cx_fol - 20} 575"/>
            <path d="M {cx_fol} 480 Q {cx_fol + 10} 520, {cx_fol + 20} 575"/>
            <circle cx="{cx_fol - 60}" cy="545" r="4" fill="#8a60cc"/>
            <circle cx="{cx_fol + 60}" cy="545" r="4" fill="#8a60cc"/>
            <circle cx="{cx_fol - 20}" cy="575" r="4" fill="#8a60cc"/>
            <circle cx="{cx_fol + 20}" cy="575" r="4" fill="#8a60cc"/>
        </g>
        <text x="{cx_fol}" y="595" fill="#c0a0ff" font-size="9" font-weight="700" text-anchor="middle" font-family="Cinzel">TREE OF KNOWLEDGE ROOTS</text>
        <text x="{cx_fol}" y="{cy_fol + 4}" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle" font-family="Cinzel">BINDU</text>
    </svg></body></html>
    """
    components.html(sophia_mirror_svg, height=620)

    if s_diff == 0:
        synastry_reading = f"Identical Root {slp1}. You share an identical optical wavelength. Communication is instantaneous, yet because you share identical blind spots, neither entity naturally offers the brakes when the vehicle speeds toward an edge."
    elif s_diff in (1, 3, 5):
        synastry_reading = f"Dynamic Shear (Delta {s_diff}). The Solar engine pushes toward outward speed and manifest structure, while the Lunar well demands introversion and silent incubation. This tension is not broken; it is the exact kinetic torque needed to build."
    else:
        synastry_reading = f"Harmonic Accord (Delta {s_diff}). Symmetrical lock across the cardinal axis. What one vessel exhausts, the opposite reservoir replenishes."

    verdict_text = f"""The Sophia Mirror Verdict for {sm1_name} & {sm2_name}:

1. Polarity Dynamics:
{synastry_reading}

2. The Eye of the Needle (Aperture Threshold {bridging_threshold}):
The bindu point at the neck between the two cones opens at Frequency {bridging_threshold} ({meaning(bridging_threshold)}). This is the only ground where arguments dissolve—when disputes arise, center decisions around this exact frequency.

3. Crystalline Torque:
{sm1_name} projects outward through Tone {sexpr1}, while {sm2_name} contains and distills through Tone {sexpr2}. Respect the stark contrast: the upper cone cannot exist without the weight of the subterranean roots.
"""

    st.markdown(f"""
    <div class="tincture-box">
        <strong style="color: #f5c542; font-family: 'Cinzel', serif;">The Sophia Mirror Verdict for {sm1_name} & {sm2_name}:</strong><br><br>
        <strong>1. Polarity Dynamics:</strong> {synastry_reading}<br>
        <strong>2. The Eye of the Needle (Aperture Threshold {bridging_threshold}):</strong> The bindu point at the neck between the two cones opens at Frequency {bridging_threshold} ({meaning(bridging_threshold)}). This is the only ground where arguments dissolve—when disputes arise, center decisions around this exact frequency.<br>
        <strong>3. Crystalline Torque:</strong> {sm1_name} projects outward through Tone {sexpr1}, while {sm2_name} contains and distills through Tone {sexpr2}. Respect the stark contrast: the upper cone cannot exist without the weight of the subterranean roots.
    </div>
    """, unsafe_allow_html=True)

    st.download_button("💾 Save Sophia Mirror Synthesis (.txt)", data=verdict_text, file_name=f"sophia_mirror_{sm1_name}_and_{sm2_name}.txt", mime="text/plain", key="dl_sophia")

# ----------------------------------------------------
# TAB 7: PATTERN & FREQUENCY ENGINE
# ----------------------------------------------------
with tabs[6]:
    st.markdown("<h3 style='color:#f5c542;'>Universal Pattern & Multi-Lingual Frequency Engine</h3>", unsafe_allow_html=True)
    cipher_input = st.text_input("Universal Analysis Field:", value="The Hidden Light")
    if cipher_input:
        prof = name_profile(cipher_input)
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric(f"Tradition Sum ({prof['script']})", prof["pyth_sum"])
        col_p2.metric("Script Lineage", prof["script"])
        col_p3.metric("Reduced Root", prof["expression"])
        st.markdown(f"**Root Interpretation:** {meaning(prof['expression'])}")

        ciph_txt = f"""=== PATTERN & FREQUENCY ENGINE REPORT ===
Input Text: {cipher_input}
Detected Script Lineage: {prof['script']}
Total Tradition Gematria Sum: {prof['pyth_sum']}
Reduced Monad Root: {prof['expression']}
Root Meaning: {meaning(prof['expression'])}
"""
        st.download_button("💾 Save Frequency Engine Reading (.txt)", data=ciph_txt, file_name="frequency_engine_reading.txt", mime="text/plain", key="dl_freq")
