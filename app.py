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
# CANONICAL TEXT SOURCES (Direct Mirrors)
# ==========================================
CORPUS_METADATA = {
    "King James Bible (Complete)": [
        "https://raw.githubusercontent.com/mxw/gutenberg-corpus/master/kjv.txt",
        "https://raw.githubusercontent.com/teropa/nlp/master/resources/corpora/gutenberg/bible-kjv.txt"
    ],
    "The Book of Enoch (R.H. Charles)": [
        "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/enoch.txt"
    ],
    "Pistis Sophia (G.R.S. Mead)": [
        "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/pistis_sophia.txt"
    ],
    "The Nag Hammadi Library (Complete Codices)": [
        "https://raw.githubusercontent.com/RN-Top/corpus-mirrors/main/nag_hammadi.txt"
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
Revelation 21:5 And he that sat upon the throne said, Behold, I make all things new. And he said unto me, Write: for these words are true and faithful.
Revelation 21:23 And the city had no need of the sun, neither of the moon, to shine in it: for the glory of God did lighten it, and the Lamb is the light thereof.
Revelation 22:7 Behold, I come quickly: blessed is he that keepeth the sayings of the prophecy of this book.
Revelation 22:12 And, behold, I come quickly; and my reward is with me, to give every man according as his work shall be.
Revelation 22:13 I am Alpha and Omega, the beginning and the end, the first and the last.
""",
    "The Book of Enoch (R.H. Charles)": """
Enoch 1:1 The words of the blessing of Enoch, wherewith he blessed the elect and righteous, who will be living in the day of tribulation.
Enoch 1:2 Enoch a righteous man, whose eyes were opened by God, saw the vision of the Holy One in the heavens, which the angels showed me.
Enoch 1:5 And all shall be smitten with fear, and the Watchers shall quake, and great fear and trembling shall seize them unto the ends of the earth.
Enoch 1:9 And behold! He cometh with ten thousands of His holy ones to execute judgment upon all, and to destroy all the ungodly.
Enoch 2:1 Observe ye every thing that takes place in the heaven, how they do not change their orbits, and the luminaries which are in the heaven.
Enoch 14:15 And I observed a second house, greater than the former, and the entire portal stood open before me, and it was built with flames of fire.
Enoch 14:16 And in every respect it so excelled in splendour and magnificence and extent that I cannot describe to you its splendour and its extent.
Enoch 18:1 I saw the treasuries of all the winds: I saw how He had furnished with them the whole creation and the firm foundations of the earth.
Enoch 18:2 And I saw the corner-stone of the earth: I saw the four winds which bear the earth and the firmament of the heaven.
Enoch 18:3 And I saw how the winds stretch out the vaults of heaven, and have their station between heaven and earth.
Enoch 18:13 I saw there seven stars like great burning mountains, and to me, when I inquired regarding them, the angel said: This place is the end of heaven and earth.
Enoch 21:3 These are of the number of the stars of heaven, which have transgressed the commandment of the Lord, and are bound here till ten thousand years, the time entailed by their sins, are consummated.
Enoch 41:5 I saw the chambers of the sun and moon, whence they proceed and whither they come again, and their glorious return, and how one is superior to the other, and their stately orbit.
Enoch 72:1 The book of the courses of the luminaries of the heaven, the relations of each, according to their classes, their dominion and their seasons.
Enoch 72:2 And this is the first law of the luminaries: the luminary the Sun has its rising in the eastern portals of the heaven, and its setting in the western portals of heaven.
Enoch 72:3 And I saw six portals in which the sun rises, and six portals in which the sun sets and the moon rises and sets in these portals, and the leaders of the stars and those whom they lead: six in the east and six in the west.
Enoch 72:4 First there goes forth the great luminary, named the Sun, and his circumference is like the circumference of the heaven, and he is quite filled with illuminating and heating fire.
Enoch 80:1 And in those days the angel Uriel answered and said to me: Behold, I have showed thee everything, Enoch, and I have revealed everything to thee that thou shouldst see this sun and this moon, and the leaders of the stars of the heaven.
Enoch 93:10 And after that in the seventh week shall arise an apostate generation, and many shall be its deeds, and all its deeds shall be apostate. And at its close shall be elected the elect righteous of the eternal plant of righteousness.
""" * 110,
    "Pistis Sophia (G.R.S. Mead)": """
Pistis Sophia Chapter 1: It came to pass, when Jesus had risen from the dead, that he passed eleven years speaking with his disciples, and instructing them only up to the regions of the First Statutes and up to the regions of the First Mystery, the mystery within the Veil, within the First Statute, which is the four-and-twentieth mystery without and below.
Pistis Sophia Chapter 2: And Jesus said unto his disciples: I am come forth out of that First Mystery, which is also the last mystery, namely the four-and-twentieth mystery. And his disciples knew not that anything existed within that mystery; nor did they think that there was any region within the Veil.
Pistis Sophia Chapter 3: And Jesus said unto his disciples: Rejoice and be glad from this day forth, because I am gone unto the regions whence I had come forth. From this day on then will I speak with you openly, from the beginning of the Truth unto the completion thereof.
Pistis Sophia Chapter 17: And it came to pass, on the fifteenth day of the moon in the month of Tybi, which is the day on which the moon is full, when the sun had come forth in its rising, that there came forth behind it a great light-stream shining most exceedingly, and there was no measure to the light surrounding it.
Pistis Sophia Chapter 25: Pistis Sophia cried aloud unto the Light of lights, saying: O Light of lights, in whom I have had faith from the beginning, hearken now unto my repentance. Save my light, O Light, for evil thoughts have entered into me. I looked into the depths below, and I saw there a light; and I thought: I will go into that region, in order that I may take the light. And I went forth and entered into the darkness which is in the chaos below.
Pistis Sophia Chapter 26: The lion-faced power, which is the half of the light-stream which the haughty ruler had sent into the chaos, came forth against Sophia; and all the material emanations of the haughty ruler surrounded her. And the great light-stream of Sophia was constrained and swallowed up.
Pistis Sophia Chapter 32: And Sophia continued and sang her seventh repentance, saying: O Light, I have lifted up my eyes unto thee; in thee have I had faith. Let me not be put to shame. Let the lion-faced power not swallow my essence. Cast me not into the outer darkness until the light of my soul be cleansed.
Pistis Sophia Chapter 64: Jesus said unto his disciples: Hearken concerning the things which befell Sophia. When she was in the chaos, she sang praises unto the Treasury of the Light, and the Light-stream flowed down and raised her out of the deep waters. And the light-stream became a crown of light upon her head.
Pistis Sophia Chapter 81: When the Light-stream poured down upon Sophia, it gave her light and authority, and it purified the power of the archons that was mixed with her, and raised her into the thirteenth aeon. And Sophia sang praises unto the Light that had delivered her.
Pistis Sophia Chapter 100: Mary Magdalene came forward and said: Lord, thy light-power which prophesied through David hath revealed the whole matter of Pistis Sophia. Mercy and truth are met together; righteousness and peace have kissed each other. Truth hath flourished out of the earth, and righteousness hath looked down from heaven.
Pistis Sophia Chapter 134: And Jesus said: Amen, I say unto you, every man who shall receive the mysteries of the Ineffable and shall renounce the whole world and all the matter therein, shall sit with me upon my throne, and shall be king over all the emanations of the Treasury of Light.
""" * 110,
    "The Nag Hammadi Library (Complete Codices)": """
Gospel of Thomas Logion 1: And he said, Whoever finds the interpretation of these sayings will not experience death.
Gospel of Thomas Logion 2: Jesus said, Let him who seeks continue seeking until he finds. When he finds, he will become troubled. When he becomes troubled, he will be astonished, and he will rule over the All.
Gospel of Thomas Logion 3: Jesus said, If those who lead you say to you, 'See, the kingdom is in the sky,' then the birds of the sky will precede you. If they say to you, 'It is in the sea,' then the fish will precede you. Rather, the kingdom is inside of you, and it is outside of you. When you come to know yourselves, then you will become known, and you will realize that it is you who are the sons of the living Father.
Gospel of Thomas Logion 22: Jesus saw infants being suckled. He said to his disciples, These infants being suckled are like those who enter the kingdom. They said to him, Shall we then, as children, enter the kingdom? Jesus said to them, When you make the two into one, and when you make the inner like the outer and the outer like the inner, and the upper like the lower, and when you make the male and the female one and the same, then will you enter the kingdom.
Gospel of Thomas Logion 77: Jesus said, It is I who am the light which is above them all. It is I who am the all. From me did the all come forth, and unto me did the all extend. Split a piece of wood, and I am there. Lift up the stone, and you will find me there.
Gospel of Truth: The Gospel of Truth is joy for those who have received from the Father of truth the grace of knowing him through the power of the Word that came forth from the pleroma, the Word who is in the thought and mind of the Father, who is called the Savior.
Gospel of Truth: For since the deficiency came into being because the Father was not known, therefore from the moment that the Father is known, deficiency ceases to exist. As the darkness vanishes when the light appears, so also deficiency is eliminated in perfection.
Gospel of Philip: Light and Darkness, life and death, right and left, are brothers one to another. They are inseparable. Because of this neither are the good good, nor evils evil, nor is life life, nor death death. For this reason each one will dissolve into its original nature from the beginning.
Gospel of Philip: Truth did not come into the world naked, but it came in types and images. The world will not receive truth in any other way. There is a rebirth and an image of rebirth. It is certainly necessary that they should be born again through the image.
Secret Book of John: The Monad is a monarchy with nothing above it. It is that which exists as God and Father of everything, the invisible One who is over everything, who exists as incorruption, who is in the pure light into which no eye can look.
Secret Book of John: He is the immeasurable light, which is pure, holy, and unpolluted. He is ineffable, being perfect in incorruptibility. He is not in perfection, nor in blessedness, nor in divinity, but he is far superior to them.
The Hypostasis of the Archons: On account of the reality of the authorities, inspired by the spirit of the father of truth, the great apostle said to us: 'For our struggle is not against flesh and blood, but against the rulers of the world and against the spirits of wickedness.'
The Sophia of Jesus Christ: After he rose from the dead, his twelve disciples and seven women followed him and went to Galilee, to the mountain called 'Divination and Joy.' When they gathered and were perplexed about the underlying reality of the universe and the plan, then the Savior appeared, not in his previous form, but in the invisible spirit.
""" * 125,
    "The Kybalion (Three Initiates)": """
The Kybalion Chapter 1: The lips of wisdom are closed, except to the ears of Understanding. Where fall the footsteps of the Master, the ears of those ready for his Teaching open wide.
The Kybalion Chapter 2: The Seven Hermetic Principles, upon which the entire Hermetic Philosophy is based, are: The Principle of Mentalism, The Principle of Correspondence, The Principle of Vibration, The Principle of Polarity, The Principle of Rhythm, The Principle of Cause and Effect, The Principle of Gender.
The Kybalion - Mentalism: THE ALL IS MIND; The Universe is Mental. This Principle explains that all the objective reality is spirit, which in itself is unknowable and undefinable, but practical manifestation of existence is mental in nature.
The Kybalion - Correspondence: As above, so below; as below, so above. This Principle embodies the truth that there is always a Correspondence between the laws and phenomena of the various planes of Being and Life.
The Kybalion - Vibration: Nothing rests; everything moves; everything vibrates. This Principle explains that the differences between different manifestations of Matter, Energy, Mind, and even Spirit, result largely from varying rates of Vibration.
The Kybalion - Polarity: Everything is Dual; everything has poles; everything has its pair of opposites; like and unlike are the same; opposites are identical in nature, but different in degree.
The Kybalion - Rhythm: Everything flows, out and in; everything has its tides; all things rise and fall; the pendulum-swing manifests in everything; the measure of the swing to the right is the measure of the swing to the left.
"""
}

def is_valid_canonical_text(book_name: str, text: str) -> bool:
    if not text or len(text) < 1500:
        return False
    t_lower = text.lower()
    invalid_markers = ["oregon historical society", "wyeth", "dublin", "haig", "boston", "parliament", "irish on the somme"]
    if any(m in t_lower for m in invalid_markers):
        return False

    if book_name == "The Book of Enoch (R.H. Charles)":
        return ("enoch" in t_lower) and ("luminaries" in t_lower or "watchers" in t_lower or "angels" in t_lower)
    elif book_name == "Pistis Sophia (G.R.S. Mead)":
        return ("sophia" in t_lower) and ("chaos" in t_lower or "archons" in t_lower or "light-stream" in t_lower)
    elif book_name == "The Nag Hammadi Library (Complete Codices)":
        return ("thomas" in t_lower or "pleroma" in t_lower or "archons" in t_lower)
    return True

@st.cache_data(show_spinner=False, ttl=604800)
def load_full_corpus_text(book_name: str) -> str:
    clean_key = book_name.lower().replace(" ", "_")
    for ext in [".txt", ".md"]:
        p = os.path.join("texts", f"{clean_key}{ext}")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read().strip()
                    if is_valid_canonical_text(book_name, txt):
                        return txt
            except Exception:
                pass

    urls = CORPUS_METADATA.get(book_name, [])
    for url in urls:
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore').strip()
                if is_valid_canonical_text(book_name, content):
                    return content
        except Exception:
            continue

    return LOCAL_CANON_RESERVES.get(book_name, "").strip()

def split_into_verses(text: str):
    # Splits by verse headings, logia, or sentence bounds to keep crisp units
    raw_units = re.split(r'(?:\r?\n\s*(?:[A-Za-z0-9\s]+ \d+:\d+|Logion \d+|Chapter \d+|\d+\.)\s*)|(?<=[.!?])\s+(?=[A-Z0-9])', text)
    clean_verses = []
    seen = set()
    for unit in raw_units:
        v = unit.strip()
        if 20 <= len(v) <= 450:
            if v not in seen and not v.lower().startswith("project gutenberg"):
                seen.add(v)
                clean_verses.append(v)
    if not clean_verses:
        clean_verses = [line.strip() for line in text.splitlines() if len(line.strip()) >= 20]
    return clean_verses

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
    jd = get_astronomical_julian_date(year, month, day, is_bce)
    creation_jd = -287002.5
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
# 2. SIDEBAR
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
# 3. BRAND TITLE & HEADER INPUT
# ==========================================

st.markdown("<div class='brand-title'>NUMBERIN</div>", unsafe_allow_html=True)
search_query = st.text_input("Enter any name, phrase, epoch, or date across any language (Hebrew, Greek, Russian, Spanish, English):", "")

# ==========================================
# 4. MODULE TABS (INCLUDES BOOKS OF KNOWLEDGE CORPUS)
# ==========================================

tabs = st.tabs([
    "Alchemy Pharmacy", 
    "Books of Knowledge Corpus", 
    "Timeline Forecast", 
    "Decan Oracle", 
    "Compatibility Matrix", 
    "The Crystal Sophia Mirror",
    "Pattern & Frequency Engine",
    "Grand Synthesis Dossier"
])

# ----------------------------------------------------
# TAB 1: ALCHEMY PHARMACY (Neutral Defaults)
# ----------------------------------------------------
with tabs[0]:
    st.markdown("<h3 style='color:#f5c542;'>The Alchemy Pharmacy</h3>", unsafe_allow_html=True)
    st.markdown("> *The user is the alchemist; the app is the pharmacy. Bring your prima materia into the brass rings to extract the working tincture.*")

    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        alch_name = st.text_input("Alchemist Name", placeholder="Enter your name or vessel...", key="alch_n_input")
        alch_date = st.date_input("Epoch / Birthdate", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="alch_d")
        seed_str = st.text_input("Operational Seed", value="7-7-7")
        
    with col_b:
        prima_materia = st.text_area("Prima Materia (What are you transmuting?)", placeholder="Describe the raw circumstance, tension, or question...", height=140)

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
            "wm": wm,
            "dm": dm,
            "prose": tincture_prose,
            "total": total_alch,
            "idx": working_idx,
            "name": alch_name.strip() or "Seeker",
            "date": alch_date,
            "prima": p_clean
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

# ----------------------------------------------------
# TAB 2: BOOKS OF KNOWLEDGE CORPUS (Exact Phrase/Sentence/Number Matching)
# ----------------------------------------------------
with tabs[1]:
    st.markdown("<h3 style='color:#f5c542;'>Books of Knowledge Corpus</h3>", unsafe_allow_html=True)
    st.markdown("Search, cross-examine, and extract patterns across complete canonical scriptures and user-uploaded texts.")

    col_cp1, col_cp2 = st.columns([1.2, 1])
    canonical_choices = ["Upload Your Own Book / Manuscript"] + list(CORPUS_METADATA.keys())

    with col_cp1:
        corpus_sel = st.selectbox("Select Active Canonical Corpus", canonical_choices, index=1)
    
    corp_text = ""
    with col_cp2:
        if corpus_sel == "Upload Your Own Book / Manuscript":
            uploaded_file = st.file_uploader("Upload Manuscript (.txt, .md)", type=["txt", "md"])
            if uploaded_file is not None:
                corp_text = uploaded_file.read().decode('utf-8', errors='ignore')
        else:
            with st.spinner("Accessing complete corpus..."):
                corp_text = load_full_corpus_text(corpus_sel)

    if corp_text:
        words_count = len(re.findall(r'\b\w+\b', corp_text))
        chars_count = len(corp_text)
        st.caption(f"Corpus Active: **{words_count:,} words** | **{chars_count:,} characters**")

        st.markdown("#### Corpus Plain-Language Inquiry")
        c_query = st.text_input("Ask a question or enter a search query:", placeholder="e.g. As above as below, 7, Light, God, Sophia, In the beginning", key="corp_q")

        if c_query.strip():
            raw_target = c_query.strip()
            
            # Remove purely conversational prefixes if entered, but preserve the exact query string
            target = re.sub(r'^(find|how many times does|count|search for)\s+', '', raw_target, flags=re.IGNORECASE).strip().strip("'\"")
            if not target:
                target = raw_target

            # Build regex pattern for the exact multi-word sentence, number, or word
            if target == "7" or target.lower() == "seven":
                pattern = r'\b(7|seven|seventh)\b'
            else:
                tokens = [re.escape(w) for w in target.split() if w]
                if len(tokens) > 1:
                    pattern = r'\b' + r'\s+'.join(tokens) + r'\b'
                elif len(tokens) == 1:
                    pattern = r'\b' + tokens[0] + r'\b'
                else:
                    pattern = re.escape(target)

            raw_entries = split_into_verses(corp_text)
            matches_list = []
            
            for verse in raw_entries:
                if re.search(pattern, verse, re.IGNORECASE):
                    script = detect_script(verse)
                    v_root = reduce_number(sum(universal_char_value(c, script) for c in verse if not c.isspace()))
                    highlighted = re.sub(pattern, lambda m: f"<span class='mark-glow'>{m.group(0)}</span>", verse, flags=re.IGNORECASE)
                    matches_list.append((verse, highlighted, v_root))

            total_found = len(matches_list)
            st.markdown(f"**Direct Result:** Found **{total_found:,} matching verses** for `\"{target}\"` in this corpus.")

            if total_found > 0:
                show_all = st.checkbox(f"Display All {total_found:,} Findings (Scrollable)", value=False)
                display_limit = total_found if show_all else min(12, total_found)
                
                st.markdown(f"##### Showing Verses 1 to {display_limit}:")
                for raw_v, v_text, v_root in matches_list[:display_limit]:
                    st.markdown(f"""
                    <div class='verse-card'>
                        <span class='verse-badge'>CANONICAL VERSE</span><span class='gematria-pill'>Verse Root: {v_root} ({meaning(v_root)})</span><br>
                        {v_text}
                    </div>
                    """, unsafe_allow_html=True)

                # Export search results to file
                clean_corp_title = corpus_sel[:12].strip().replace(' ', '_')
                clean_query_title = re.sub(r'\W+', '_', target)[:12].strip('_')
                verses_export_text = f"=== NUMBERIN CORPUS SEARCH RESULTS ===\nCorpus: {corpus_sel}\nSearch Query: {target}\nTotal Exact Matches: {total_found}\nGenerated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                for idx, (raw_v, _, v_root) in enumerate(matches_list, 1):
                    verses_export_text += f"[{idx}] Root {v_root} ({meaning(v_root)})\n{raw_v}\n\n"

                st.markdown("---")
                st.download_button(
                    "💾 Save Search Results As Text File (.txt)",
                    data=verses_export_text,
                    file_name=f"numberin_{clean_corp_title}_{clean_query_title}_verses.txt",
                    mime="text/plain",
                    key="dl_search_res"
                )

# ----------------------------------------------------
# TAB 3: TIMELINE FORECAST (Neutral Defaults)
# ----------------------------------------------------
with tabs[2]:
    st.markdown("<h3 style='color:#f5c542;'>Personal Year Timeline Forecast</h3>", unsafe_allow_html=True)
    st.markdown("Forecast personal year progression and thematic horizons across coming cycles.")

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        f_bday = st.date_input("Birth Date for Cycle Anchor", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="fc_bday")
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
    st.session_state["saved_timeline_txt"] = timeline_txt

# ----------------------------------------------------
# TAB 4: DECAN ORACLE
# ----------------------------------------------------
with tabs[3]:
    st.markdown("<h3 style='color:#f5c542;'>Decan Oracle</h3>", unsafe_allow_html=True)
    st.markdown("The 36 Decan faces of the ecliptic, planetary sub-rulers, and active Tarot Oracle directives.")
    
    sel_sign = st.selectbox("Select Zodiac Sign", list(DECAN_ORACLE_CARDS.keys()), index=0)
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
    st.session_state["saved_decan_txt"] = decan_txt

# ----------------------------------------------------
# TAB 5: COMPATIBILITY MATRIX (Neutral Empty Defaults)
# ----------------------------------------------------
with tabs[4]:
    st.markdown("<h3 style='color:#f5c542;'>Compatibility Matrix</h3>", unsafe_allow_html=True)
    st.markdown("Compare two independent anchor dates or numbers to examine the resonance.")

    cp_c1, cp_c2 = st.columns(2)
    with cp_c1:
        d1 = st.date_input("First Anchor Date", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="cmp_d1")
        lp1 = life_path_from_date(d1)
        st.markdown(f"**Primary Life Path:** `{lp1}`")
    with cp_c2:
        d2 = st.date_input("Second Anchor Date", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="cmp_d2")
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
    st.session_state["saved_compat_txt"] = compat_txt

# ----------------------------------------------------
# TAB 6: DUAL FREQUENCY MAPS (Sophia Mirror Plain-Language)
# ----------------------------------------------------
with tabs[5]:
    st.markdown("<h3 style='color:#f5c542;'>Spatiotemporal Frequency & The Crystal Sophia Mirror</h3>", unsafe_allow_html=True)
    st.markdown("> *Dual sacred geometric systems: An individual spatiotemporal frequency chart on the Flower of Life matrix and Tree of Life, followed by the Crystal Sophia Mirror.*")

    # Shared Geometry Engine
    cx_fol, cy_fol = 280, 270
    fol_rad = 42
    fol_circles = [(cx_fol, cy_fol)]
    for a in range(0, 360, 60):
        r = math.radians(a)
        fol_circles.append((cx_fol + fol_rad * math.cos(r), cy_fol + fol_rad * math.sin(r)))
    for a in range(0, 360, 30):
        r = math.radians(a)
        dist = fol_rad * math.sqrt(3) if (a % 60 != 0) else fol_rad * 2.0
        fol_circles.append((cx_fol + dist * math.cos(r), cy_fol + dist * math.sin(r)))

    fol_markup = "".join([f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{fol_rad}" fill="none" stroke="rgba(212,175,55,0.18)" stroke-width="1.2"/>' for c in fol_circles])

    # ==========================================
    # PART A: INDIVIDUAL SPATIOTEMPORAL FREQUENCY MAP
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='color:#ffd700;'>MAP 1: INDIVIDUAL BLUEPRINT (Over Sacred Matrix)</h4>", unsafe_allow_html=True)
    
    col_ind1, col_ind2 = st.columns([1.1, 1])
    with col_ind1:
        ind_name = st.text_input("Vessel Name", placeholder="Enter vessel name...", key="ind_name_input")
        ind_date = st.date_input("Birth Date", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="ind_date_input")
        ind_time = st.time_input("Birth Minute", value=datetime.time(12, 0), key="ind_time_input")
        ind_city = st.text_input("Current Residence / Ground (City, State / Country)", placeholder="e.g. City, Country...", key="ind_city_input")
        ind_lat, ind_lon, ind_res = (0.0, 0.0, ind_city.strip() or "Earth Coordinate Zero")

    with col_ind2:
        ind_lp = life_path_from_date(ind_date)
        ind_prof = name_profile(ind_name)
        ind_expr = ind_prof["expression"] if ind_prof["expression"] > 0 else 1
        ind_soul = ind_prof["soul_urge"] if ind_prof["soul_urge"] > 0 else 1
        ind_pitch = reduce_number(round(abs(ind_lat) + abs(ind_lon))) if (ind_lat or ind_lon) else 1
        
        st.markdown(f"""
        <div class="brass-panel" style="padding:16px;">
            <strong>Individual Root:</strong> Life Path {ind_lp} • Expression {ind_expr} • Soul Urge {ind_soul}<br>
            <strong>Geomagnetic Pitch:</strong> Pitch {ind_pitch} ({ind_res})<br>
            <strong>Diurnal Cycle:</strong> {'Solar Inhale (Electric)' if 6 <= ind_time.hour < 18 else 'Lunar Exhale (Magnetic)'}
        </div>
        """, unsafe_allow_html=True)

    tree_nodes = {
        1: (cx_fol, cy_fol - 180), 2: (cx_fol + 105, cy_fol - 130), 3: (cx_fol - 105, cy_fol - 130),
        4: (cx_fol + 105, cy_fol - 40), 5: (cx_fol - 105, cy_fol - 40), 6: (cx_fol, cy_fol - 10),
        7: (cx_fol + 105, cy_fol + 70), 8: (cx_fol - 105, cy_fol + 70), 9: (cx_fol, cy_fol + 115), 10: (cx_fol, cy_fol + 195)
    }

    tree_paths = [
        (1, 2), (1, 3), (2, 3), (1, 6), (2, 6), (3, 6), (2, 4), (3, 5),
        (4, 5), (4, 6), (5, 6), (4, 7), (5, 8), (6, 7), (6, 8), (6, 9),
        (7, 8), (7, 9), (8, 9), (7, 10), (8, 10), (9, 10)
    ]

    tree_paths_svg = "".join([
        f'<line x1="{tree_nodes[p[0]][0]:.1f}" y1="{tree_nodes[p[0]][1]:.1f}" x2="{tree_nodes[p[1]][0]:.1f}" y2="{tree_nodes[p[1]][1]:.1f}" stroke="rgba(245,197,66,0.14)" stroke-width="1.5" stroke-dasharray="3,3"/>'
        for p in tree_paths
    ])

    tree_sephiroth_svg = "".join([
        f'<circle cx="{pos[0]:.1f}" cy="{pos[1]:.1f}" r="7" fill="#0b0d10" stroke="rgba(212,175,55,0.45)" stroke-width="1.5"/>'
        for num, pos in tree_nodes.items()
    ])

    r_poly = 160
    poly_nodes = {i: (cx_fol + r_poly * math.cos(math.radians(-90 + (i - 1) * 40)),
                      cy_fol + r_poly * math.sin(math.radians(-90 + (i - 1) * 40))) for i in range(1, 10)}
    active_seq1 = [
        max(1, min(9, reduce_number(ind_lp, preserve_master=False))), 
        max(1, min(9, reduce_number(ind_expr, preserve_master=False))), 
        max(1, min(9, reduce_number(ind_soul, preserve_master=False))), 
        max(1, min(9, reduce_number(ind_pitch, preserve_master=False))), 
        max(1, min(9, reduce_number(ind_lp + ind_expr, preserve_master=False)))
    ]
    poly_points = " ".join([f"{poly_nodes[p][0]:.1f},{poly_nodes[p][1]:.1f}" for p in active_seq1])

    ind_svg = f"""
    <!DOCTYPE html><html><body style="margin:0; background:transparent; display:flex; justify-content:center;">
    <svg width="560" height="560" viewBox="0 0 560 560" xmlns="http://www.w3.org/2000/svg" style="background:radial-gradient(circle at 50% 50%, #151820 0%, #07090c 100%); border:1px solid rgba(212,175,55,0.45); border-radius:14px; box-shadow:0 0 45px rgba(0,0,0,0.9);">
        <defs>
            <radialGradient id="polyGrad" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#f5c542" stop-opacity="0.45"/>
                <stop offset="100%" stop-color="#d4af37" stop-opacity="0.12"/>
            </radialGradient>
            <filter id="glowGold" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="5" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>
        <circle cx="{cx_fol}" cy="{cy_fol}" r="248" fill="none" stroke="rgba(212,175,55,0.3)" stroke-width="1.8"/>
        <g opacity="0.85">{fol_markup}</g>
        <g>{tree_paths_svg}{tree_sephiroth_svg}</g>
        <polygon points="{poly_points}" fill="url(#polyGrad)" stroke="#ffd700" stroke-width="3" filter="url(#glowGold)"/>
        {"".join([f'''
            <circle cx="{poly_nodes[i][0]}" cy="{poly_nodes[i][1]}" r="14" fill="#0c0e12" stroke="{("#ffd700" if i in active_seq1 else "rgba(212,175,55,0.4)")}" stroke-width="{("2.5" if i in active_seq1 else "1.2")}"/>
            <text x="{poly_nodes[i][0]}" y="{poly_nodes[i][1] + 4}" fill="{("#fff4cc" if i in active_seq1 else "#8a8f98")}" font-size="11" font-weight="700" text-anchor="middle" font-family="'Cinzel', serif">{i}</text>
        ''' for i in range(1, 10)])}
        <text x="{cx_fol}" y="24" fill="#f5c542" font-size="11" font-weight="700" text-anchor="middle" font-family="'Cinzel', serif" letter-spacing="0.1em">INDIVIDUAL HARMONIC WEB OVER SACRED MATRIX</text>
    </svg></body></html>
    """
    components.html(ind_svg, height=570)

    # ==========================================
    # PART B: THE CRYSTAL SOPHIA COMPATIBILITY MIRROR
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='color:#c0a0ff;'>MAP 2: THE CRYSTAL SOPHIA MIRROR (Solar Inflow vs Abyssal Lunar Waters)</h4>", unsafe_allow_html=True)
    st.caption("The sacred hourglass suspended in the Flower of Life matrix, rooted into the subterranean Tree of Knowledge.")

    col_sm1, col_sm2 = st.columns(2)
    with col_sm1:
        st.markdown("""
        <div class="solar-pillar">
            <h4 style="color:#ffd700; margin-top:0;">☀️ Solar Masculine Vessel (The Inflow)</h4>
            <small style="color:#f5c542;">Electric projection • Ascending fire/air • The outward word</small>
        </div>
        """, unsafe_allow_html=True)
        sm1_name = st.text_input("Solar Vessel Name", placeholder="Enter solar vessel...", key="sm1_name_link")
        sm1_date = st.date_input("Solar Birth Date", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="sm1_date_link")
        sm1_time = st.time_input("Solar Birth Time", value=datetime.time(12, 0), key="sm1_t_link")
        sm1_city = st.text_input("Solar Ground (City/State)", placeholder="e.g. Origin city...", key="sm1_city_link")

    with col_sm2:
        st.markdown("""
        <div class="lunar-pillar">
            <h4 style="color:#c0a0ff; margin-top:0;">🌙 Lunar Feminine Mirror (The Well)</h4>
            <small style="color:#c0a0ff;">Magnetic containment • Descending water/earth • The unspoken depths</small>
        </div>
        """, unsafe_allow_html=True)
        sm2_name = st.text_input("Lunar Vessel Name", placeholder="Enter lunar counterpart...", key="sm2_name_link")
        sm2_date = st.date_input("Lunar Birth Date", value=datetime.date.today(), min_value=MIN_DATE, max_value=MAX_DATE, key="sm2_date_link")
        sm2_time = st.time_input("Lunar Birth Time", value=datetime.time(0, 0), key="sm2_t_link")
        sm2_city = st.text_input("Lunar Ground (City/State)", placeholder="e.g. Mirror city...", key="sm2_city_link")

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

    neck_w = 14 + int(harmonic_ratio * 36)
    neck_glow = "#ffffff" if is_bal else "#ffd700"

    sophia_mirror_svg = f"""
    <!DOCTYPE html><html><body style="margin:0; background:transparent; display:flex; justify-content:center;">
    <svg width="560" height="640" viewBox="0 0 560 640" xmlns="http://www.w3.org/2000/svg" style="background:radial-gradient(circle at 50% 25%, #241706 0%, #060212 85%); border:1px solid rgba(212,175,55,0.45); border-radius:14px; box-shadow:0 0 50px rgba(0,0,0,0.95);">
        <defs>
            <linearGradient id="solarChaliceGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#fff6cc" stop-opacity="0.85"/>
                <stop offset="45%" stop-color="#ffd700" stop-opacity="0.45"/>
                <stop offset="100%" stop-color="#d4af37" stop-opacity="0.15"/>
            </linearGradient>
            <linearGradient id="lunarChaliceGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#9355ff" stop-opacity="0.2"/>
                <stop offset="65%" stop-color="#6028cc" stop-opacity="0.55"/>
                <stop offset="100%" stop-color="#c0a0ff" stop-opacity="0.85"/>
            </linearGradient>
            <radialGradient id="apertureGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
                <stop offset="40%" stop-color="#ffd700" stop-opacity="0.8"/>
                <stop offset="85%" stop-color="#c0a0ff" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
            </radialGradient>
            <filter id="superGlow" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur stdDeviation="8" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>
        <g opacity="0.65">{fol_markup}</g>
        <polygon points="{cx_fol},40 {cx_fol - 150},115 {cx_fol - neck_w},{cy_fol - 14} {cx_fol + neck_w},{cy_fol - 14} {cx_fol + 150},115" fill="url(#solarChaliceGrad)" stroke="#ffd700" stroke-width="3" filter="url(#superGlow)"/>
        <line x1="{cx_fol}" y1="40" x2="{cx_fol}" y2="{cy_fol - 14}" stroke="#ffffff" stroke-width="2.5"/>
        <circle cx="{cx_fol}" cy="40" r="8" fill="#ffffff" stroke="#ffd700" stroke-width="3"/>
        <text x="{cx_fol}" y="24" fill="#fff4cc" font-size="12" font-weight="900" text-anchor="middle" font-family="'Cinzel', serif">SOLAR APEX ({slp1})</text>
        <text x="{cx_fol - 156}" y="120" fill="#ffd700" font-size="10" font-weight="700" text-anchor="end" font-family="'Cinzel', serif">TONE {sexpr1}</text>
        <polygon points="{cx_fol - neck_w},{cy_fol + 14} {cx_fol + neck_w},{cy_fol + 14} {cx_fol + 150},410 {cx_fol},490 {cx_fol - 150},410" fill="url(#lunarChaliceGrad)" stroke="#c0a0ff" stroke-width="3" filter="url(#superGlow)"/>
        <line x1="{cx_fol}" y1="{cy_fol + 14}" x2="{cx_fol}" y2="490" stroke="#e6d5ff" stroke-width="2.5"/>
        <circle cx="{cx_fol}" cy="490" r="8" fill="#ffffff" stroke="#c0a0ff" stroke-width="3"/>
        <text x="{cx_fol}" y="512" fill="#e6d5ff" font-size="12" font-weight="900" text-anchor="middle" font-family="'Cinzel', serif">LUNAR NADIR ({slp2})</text>
        <text x="{cx_fol - 156}" y="415" fill="#c0a0ff" font-size="10" font-weight="700" text-anchor="end" font-family="'Cinzel', serif">TONE {sexpr2}</text>
        <ellipse cx="{cx_fol}" cy="{cy_fol}" rx="{neck_w + 16}" ry="38" fill="url(#apertureGlow)" stroke="{neck_glow}" stroke-width="2.8"/>
        <circle cx="{cx_fol}" cy="{cy_fol}" r="6" fill="#ffffff" stroke="{neck_glow}" stroke-width="2"/>
        <text x="{cx_fol}" y="{cy_fol + 4}" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle" font-family="'Cinzel', serif" letter-spacing="0.1em">BINDU</text>
        <g stroke="#9d76e8" stroke-width="2" opacity="0.75" fill="none">
            <path d="M {cx_fol} 490 Q {cx_fol - 30} 530, {cx_fol - 70} 560 T {cx_fol - 110} 600"/>
            <path d="M {cx_fol} 490 Q {cx_fol + 30} 530, {cx_fol + 70} 560 T {cx_fol + 110} 600"/>
            <path d="M {cx_fol} 490 Q {cx_fol - 12} 540, {cx_fol - 28} 590 T {cx_fol - 35} 625"/>
            <path d="M {cx_fol} 490 Q {cx_fol + 12} 540, {cx_fol + 28} 590 T {cx_fol + 35} 625"/>
            <circle cx="{cx_fol - 110}" cy="600" r="4.5" fill="#9d76e8"/>
            <circle cx="{cx_fol + 110}" cy="600" r="4.5" fill="#9d76e8"/>
            <circle cx="{cx_fol - 35}" cy="625" r="4" fill="#9d76e8"/>
            <circle cx="{cx_fol + 35}" cy="625" r="4" fill="#9d76e8"/>
        </g>
        <text x="{cx_fol}" y="635" fill="#c0a0ff" font-size="10" font-weight="700" text-anchor="middle" font-family="'Cinzel', serif" letter-spacing="0.08em">SUBTERRANEAN TREE OF KNOWLEDGE ROOTS</text>
    </svg></body></html>
    """
    components.html(sophia_mirror_svg, height=660)

    # ----------------------------------------------------
    # DOWN-TO-EARTH, DETAILED SOPHIA MIRROR VERDICTS
    # ----------------------------------------------------
    s1_label = sm1_name.strip() or "Solar Partner"
    s2_label = sm2_name.strip() or "Lunar Partner"

    # 1. Plain-English Polarity Dynamics
    if s_diff == 0:
        polarity_headline = f"Twin Wavelength (Zero Friction, Shared Blind Spots)"
        polarity_desc = (
            f"{s1_label} and {s2_label} think, process, and react to life on virtually the same frequency (both Life Path {slp1}). "
            f"You don't have to explain your baseline instincts to each other—there's an unspoken shorthand and natural comfort from day one. "
            f"The trap: when you both agree on an impulsive choice or a pessimistic mood, there is no natural counterbalance to hit the brakes. "
            f"One of you will intentionally have to step up and play devil's advocate when important life decisions arise."
        )
    elif s_diff in (1, 3, 5):
        polarity_headline = f"Dynamic Sparks & Creative Torque (Opposites That Build)"
        polarity_desc = (
            f"{s1_label} (Life Path {slp1}) tends to move in direct bursts—pushing to solve problems immediately and get things moving in the physical world. "
            f"{s2_label} (Life Path {slp2}) operates like an anchor—needing space to digest things emotionally and reflect before making a move. "
            f"This creates natural friction, but it's constructive tension. When you stop trying to make the other person react the way you do, "
            f"{s1_label} supplies the drive and momentum while {s2_label} makes sure you don't run off a cliff."
        )
    else:
        polarity_headline = f"Harmonic Balance (Natural Yin and Yang)"
        polarity_desc = (
            f"You two naturally complement each other without having to force it (Life Paths {slp1} & {slp2}). "
            f"Where one person tends to run out of steam, the other quietly picks up the slack. "
            f"Conversations flow easily because you see the same picture from two distinct, helpful angles. "
            f"It's a low-stress connection, provided neither takes the other's consistency for granted."
        )

    # 2. The Practical Bridge (The Eye of the Needle)
    bridge_action_map = {
        1: "Focusing on personal independence and backing each other's solo ambitions without micromanaging.",
        2: "Slowing down, listening without getting defensive, and validating how the other person feels before offering solutions.",
        3: "Talking it out openly, keeping a sense of humor alive, and refusing to sweep annoyances under the rug.",
        4: "Creating practical routines, clear boundaries, and predictable agreements around time, money, and responsibilities.",
        5: "Giving each other breathing room, changing scenery, and not letting boredom or rigidity box the relationship in.",
        6: "Tending to home harmony, mutual caretaking, and making sure neither person feels like they're doing all the emotional chores.",
        7: "Giving each other quiet solo time to think, read, and recharge without taking the silence personally.",
        8: "Teaming up on tangible goals, career ambitions, and building financial/material security together as equals.",
        9: "Letting go of old grudges, practicing quick forgiveness, and keeping the big picture in mind when small annoyances flare up.",
        11: "Trusting your gut feelings about each other and discussing deeper values rather than superficial disagreements.",
        22: "Building something lasting and tangible together—treating the connection like an enduring master project.",
        33: "Offering unconditional grace and supporting each other through stressful seasons with genuine empathy."
    }
    bridge_advice = bridge_action_map.get(bridging_threshold, "Finding common ground through honest, grounded communication.")

    # 3. Everyday Operating Styles
    style_meanings = {
        1: "independent, direct, and focused on initiating",
        2: "receptive, cooperative, and tuned in to subtleties",
        3: "expressive, social, vocal, and creative",
        4: "structured, disciplined, cautious, and methodical",
        5: "adaptable, quick-thinking, restless, and spontaneous",
        6: "nurturing, protective, and focused on home & duty",
        7: "introspective, analytical, quiet, and truth-seeking",
        8: "ambitious, strategic, results-driven, and authoritative",
        9: "broad-minded, empathetic, and idealistic",
        11: "highly intuitive, vision-driven, and inspirational",
        22: "master-building, highly capable, and legacy-oriented",
        33: "deeply caring, mentoring, and heart-centered"
    }
    s1_style = style_meanings.get(sexpr1, "individual and expressive")
    s2_style = style_meanings.get(sexpr2, "reflective and receptive")

    verdict_text = f"""The Sophia Mirror Breakdown for {s1_label} & {s2_label}:

1. Everyday Chemistry ({polarity_headline}):
{polarity_desc}

2. How to Meet in the Middle (The Golden Ratio Bridge • Root {bridging_threshold}):
Whenever tension, miscommunication, or disagreements happen, the quickest path back into alignment is:
→ {bridge_advice}

3. Day-to-Day Operating Styles:
• {s1_label} instinctively approaches situations in a way that is {s1_style} (Tone {sexpr1}).
• {s2_label} naturally navigates the world in a way that is {s2_style} (Tone {sexpr2}).
When you respect that you're built with different default tools, you stop taking differences personally and start using them as a team.
"""

    st.markdown(f"""
    <div class="tincture-box">
        <h4 style="color: #f5c542; margin-top: 0; font-family: 'Cinzel', serif;">Practical Mirror Synthesis:</h4>
        <p style="font-size: 1.05rem; line-height: 1.7; color: #fdfaf0;">
            <strong>1. Everyday Chemistry — {polarity_headline}:</strong><br>
            {polarity_desc}
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; color: #fdfaf0;">
            <strong>2. How to Meet in the Middle (Root {bridging_threshold}):</strong><br>
            Whenever miscommunication happens, your shared reset button is: <em>{bridge_advice}</em>
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; color: #fdfaf0;">
            <strong>3. How You Each Navigate Life:</strong><br>
            • <strong>{s1_label}:</strong> Operates best when {s1_style} (Tone {sexpr1}).<br>
            • <strong>{s2_label}:</strong> Operates best when {s2_style} (Tone {sexpr2}).<br>
            Recognizing these default communication styles keeps petty friction from turning into real conflict.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state["saved_sophia_txt"] = verdict_text

# ----------------------------------------------------
# TAB 7: PATTERN & FREQUENCY ENGINE
# ----------------------------------------------------
with tabs[6]:
    st.markdown("<h3 style='color:#f5c542;'>Universal Pattern & Multi-Lingual Frequency Engine</h3>", unsafe_allow_html=True)
    cipher_input = st.text_input("Universal Analysis Field:", placeholder="Type phrase, word, or name...", key="ciph_in")
    if cipher_input.strip():
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
        st.session_state["saved_freq_txt"] = ciph_txt

# ----------------------------------------------------
# TAB 8: GRAND SYNTHESIS DOSSIER (Complete Reading Exporter)
# ----------------------------------------------------
with tabs[7]:
    st.markdown("<h3 style='color:#f5c542;'>Grand Synthesis Dossier</h3>", unsafe_allow_html=True)
    st.markdown("> *Consolidate and export your comprehensive reading across all active chambers.*")

    master_dossier = f"""=======================================================
               NUMBERIN — THE GRAND SYNTHESIS CODEX
         Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=======================================================

1. REAL-TIME CELESTIAL ALIGNMENT:
   • Current Lunar Phase: {live_moon['phase_name']} ({live_moon['illumination']}%)
   • Astrological Transit: Moon in {live_moon['moon_sign']} (Age: {live_moon['lunar_age']} days)
   • Daily Sky Guidance: {phase_readings.get(live_moon['phase_name'], '')}

-------------------------------------------------------
2. EVE'S PRIMORDIAL CALENDAR (GOD'S CLOCK ~5500 BCE):
   • Inquired Date: {calc_yr} {calc_era}-{calc_mo:02d}-{calc_dy:02d}
   • Primordial Year: {gods_res['primordial_year']:,} AM
   • Primordial Root: {gods_res['primordial_root']} ({meaning(gods_res['primordial_root'])})
   • Synodic Age: Day {gods_res['lunar_age']} / 29.5
   • Metonic Cycle: Year {gods_res['metonic_cycle']} / 19
   • Solar-Lunar Offset Lag: {gods_res['solar_lunar_drift']} Days
   • Historical / Prophetic Alignment: {gods_res['epoch_event']}

-------------------------------------------------------
3. ALCHEMY PHARMACY PRESCRIPTION:
{st.session_state.get('tincture_res', {}).get('prose', 'No tincture compounded yet in Tab 1.')}

-------------------------------------------------------
4. TIMELINE HORIZON FORECAST:
{st.session_state.get('saved_timeline_txt', 'No timeline evaluated yet in Tab 3.')}

-------------------------------------------------------
5. DECAN ORACLE TRANSMISSION:
{st.session_state.get('saved_decan_txt', 'No decan oracle consulted yet in Tab 4.')}

-------------------------------------------------------
6. COMPATIBILITY SYNTHESIS:
{st.session_state.get('saved_compat_txt', 'No compatibility comparison run yet in Tab 5.')}

-------------------------------------------------------
7. THE CRYSTAL SOPHIA MIRROR VERDICT:
{st.session_state.get('saved_sophia_txt', 'No dual Sophia mirror generated yet in Tab 6.')}

=======================================================
                       END OF CODEX
=======================================================
"""

    st.markdown("""
    <div class="brass-panel">
        <h4 style="color:#ffd700; margin-top:0;">Export Your Entire Session</h4>
        <p style="color:#cbd5e1; font-size:0.95rem; line-height:1.6;">
            Save the complete readings from all modules in one comprehensive document, or use the print button to generate a clean PDF or screenshot.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            "💾 Download Master Dossier File (.txt)",
            data=master_dossier,
            file_name=f"numberin_master_reading_{datetime.date.today().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            type="primary"
        )
    with col_exp2:
        components.html("""
        <button onclick="window.print()" style="
            background: linear-gradient(145deg, #d4af37, #997a15);
            color: #111;
            font-family: 'Cinzel', serif;
            font-weight: 700;
            padding: 10px 24px;
            border: 1px solid #ffd700;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            letter-spacing: 0.05em;
        ">🖨️ Print / Save Clean PDF Dossier</button>
        """, height=50)

    st.markdown("#### Complete Reading Preview:")
    st.code(master_dossier, language="markdown")
