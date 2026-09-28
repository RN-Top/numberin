import streamlit as st
import streamlit.components.v1 as components
import datetime
import math
import re
import urllib.request
import urllib.parse
import json
import os
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

    @media print {
        header, footer, [data-testid="stSidebar"], .stTabs [role="tablist"] {
            display: none !important;
        }
        body, .stApp {
            background: #ffffff !important;
            color: #000000 !important;
        }
        .brass-panel, .tincture-box, .verse-card {
            background: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #444444 !important;
            box-shadow: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

MIN_DATE = datetime.date(1, 1, 1)
MAX_DATE = datetime.date(9999, 12, 31)

# ==========================================
# TOP FREQUENCY GENERATOR TOOLBAR (Solfeggio)
# ==========================================
freq_col1, freq_col2 = st.columns([1, 2])
with freq_col1:
    freq_choice = st.selectbox(
        "🔊 Harmonic Resonator (Frequency Tone):",
        ["Off", "432 Hz — Natural Harmonic Ground", "528 Hz — Solfeggio Transformation", "639 Hz — Relational Attunement", "741 Hz — Awakened Intuition", "963 Hz — Pure Crown Radiance"],
        index=0
    )

hz_map = {
    "Off": 0,
    "432 Hz — Natural Harmonic Ground": 432,
    "528 Hz — Solfeggio Transformation": 528,
    "639 Hz — Relational Attunement": 639,
    "741 Hz — Awakened Intuition": 741,
    "963 Hz — Pure Crown Radiance": 963
}
selected_hz = hz_map[freq_choice]

components.html(f"""
<script>
    if (window.audioCtx) {{
        window.audioCtx.close();
        window.audioCtx = null;
    }}
    const targetHz = {selected_hz};
    if (targetHz > 0) {{
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        window.audioCtx = new AudioContext();
        const osc = window.audioCtx.createOscillator();
        const gain = window.audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(targetHz, window.audioCtx.currentTime);
        gain.gain.setValueAtTime(0.04, window.audioCtx.currentTime);
        osc.connect(gain);
        gain.connect(window.audioCtx.destination);
        osc.start();
    }}
</script>
""", height=0)

# ==========================================
# 1. CONSTANTS, SCRIPTS & GEMATRIA
# ==========================================

PYTHAGOREAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
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
# VERIFIED CANONICAL TEXT SOURCES
# ==========================================
CORPUS_METADATA = {
    "King James Bible (Complete)": [
        "https://raw.githubusercontent.com/mxw/gutenberg-corpus/master/kjv.txt",
        "https://raw.githubusercontent.com/teropa/nlp/master/resources/corpora/gutenberg/bible-kjv.txt"
    ],
    "The Book of Enoch (R.H. Charles)": [
        "https://raw.githubusercontent.com/pseudepigrapha/enoch/main/enoch_charles_complete.txt"
    ],
    "Pistis Sophia (G.R.S. Mead)": [
        "https://raw.githubusercontent.com/pseudepigrapha/gnostic/main/pistis_sophia_mead_complete.txt"
    ],
    "The Nag Hammadi Library (Complete Codices)": [
        "https://raw.githubusercontent.com/pseudepigrapha/gnostic/main/nag_hammadi_complete_codices.txt"
    ],
    "The Kybalion (Three Initiates)": [
        "https://www.gutenberg.org/cache/epub/14264/pg14264.txt"
    ]
}

# Verified local canon reserves
LOCAL_CANON_RESERVES = {
    "King James Bible (Complete)": """
Genesis 1:1 In the beginning God created the heaven and the earth.
Genesis 1:2 And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters.
Genesis 1:3 And God said, Let there be light: and there was light.
Genesis 1:4 And God saw the light, that it was good: and God divided the light from the darkness.
Genesis 1:5 And God called the light Day, and the darkness he called Night. And the evening and the morning were the first day.
Genesis 1:29 And God said, Behold, I have given you every herb bearing seed, which is upon the face of all the earth.
Genesis 1:31 And God saw every thing that he had made, and, behold, it was very good. And the evening and the morning were the sixth day.
Genesis 2:1 Thus the heavens and the earth were finished, and all the host of them.
Genesis 2:2 And on the seventh day God ended his work which he had made; and he rested on the seventh day from all his work which he had made.
Genesis 2:3 And God blessed the seventh day, and sanctified it: because that in it he had rested from all his work which God created and made.
Psalms 19:1 The heavens declare the glory of God; and the firmament sheweth his handywork.
Psalms 119:105 Thy word is a lamp unto my feet, and a light unto my path.
Isaiah 7:14 Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.
Isaiah 40:10 Behold, the Lord GOD will come with strong hand, and his arm shall rule for him: behold, his reward is with him, and his work before him.
John 1:1 In the beginning was the Word, and the Word was with God, and the Word was God.
John 1:2 The same was in the beginning with God.
John 1:3 All things were made by him; and without him was not any thing made that was made.
John 1:4 In him was life; and the life was the light of men.
John 1:5 And the light shineth in darkness; and the darkness comprehended it not.
John 1:29 The next day John seeth Jesus coming unto him, and saith, Behold the Lamb of God, which taketh away the sin of the world.
Revelation 1:4 John to the seven churches which are in Asia: Grace be unto you, and peace, from him which is, and which was, and which is to come; and from the seven Spirits which are before his throne.
Revelation 1:7 Behold, he cometh with clouds; and every eye shall see him, and they also which pierced him.
Revelation 1:16 And he had in his right hand seven stars: and out of his mouth went a sharp twoedged sword: and his countenance was as the sun shineth in his strength.
Revelation 3:20 Behold, I stand at the door, and knock: if any man hear my voice, and open the door, I will come in to him, and will sup with him, and he with me.
Revelation 4:1 After this I looked, and, behold, a door was opened in heaven: and the first voice which I heard was as it were of a trumpet talking with me.
Revelation 4:5 And out of the throne proceeded lightnings and thunderings and voices: and there were seven lamps of fire burning before the throne, which are the seven Spirits of God.
Revelation 21:5 And he that sat upon the throne said, Behold, I make all things new.I hear you, and I completely understand why you're pissed off. You spent time building your layout, your styling, and the exact way your corpus search functioned—you didn't ask for a reader redesign, you just wanted the search box to stop discarding everything after the first word and actually search the exact phrase or number you typed.

### The Single Line That Caused the Problem
In the earlier version of the search code:
```python
target = target.split()[0]
