import streamlit as st
import datetime
import math
import re
import urllib.request
from collections import Counter

# Set Page Config
st.set_page_config(page_title="Numberin", page_icon="✨", layout="wide")

# Custom Styling (Brass & Parchment / Dark Mystery Aesthetic)
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #e6edf3; }
    .brass-card {
        background: linear-gradient(135deg, #1f1b18 0%, #161b22 100%);
        border: 1px solid #c5a059;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(197, 160, 89, 0.15);
    }
    .ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 20px 0;
    }
    .ring-badge {
        padding: 12px 24px;
        border-radius: 30px;
        border: 2px solid #d4af37;
        background: #111418;
        color: #f3e5ab;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }
    .tincture-box {
        background: #12100e;
        border-left: 4px solid #c5a059;
        padding: 18px;
        border-radius: 4px;
        font-size: 1.08rem;
        line-height: 1.7;
        color: #f5eedc;
    }
    .ref-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #d4af37;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.92rem;
        color: #e6edf3;
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

# ==========================================
# 2. CORE HELPER FUNCTIONS & DEEP-TIME CALCS
# ==========================================

def reduce_number(n: int, preserve_master: bool = True) -> int:
    n = abs(n)
    while n > 9:
        if preserve_master and n in (11, 22, 33):
            return n
        n = sum(int(d) for d in str(n))
    return n

def reduce_trace(n: int) -> list:
    trace = [abs(n)]
    curr = abs(n)
    while curr > 9 and curr not in (11, 22, 33):
        curr = sum(int(d) for d in str(curr))
        trace.append(curr)
    return trace

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
        return {"expression": 0, "soul_urge": 0, "personality": 0, "pyth_sum": 0, "chaldean_sum": 0}
    
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
        "chaldean_sum": sum(c_vals)
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

def depth_lines(n: int) -> str:
    return f"Root frequency {n} is operating at prime density. Its current polarity encourages stillness before translation."

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
        return "Resonant Unity: Shared primary frequency. Immediate mutual mirror, potential for echo chamber."
    elif diff in (2, 4):
        return "Harmonic Accord: Complementary rhythm. The difference creates productive leverage."
    elif diff in (1, 3):
        return "Friction and Spark: Dynamic tension. Progress requires deliberate accommodation."
    return "Neutral Orbit: Independent wavelengths that interact without friction or fusion."

# Helper to find snippets/references for words in text
def extract_references(full_text: str, query_token: str, max_refs: int = 5):
    lines = full_text.splitlines()
    matches = []
    pattern = re.compile(rf'\b{re.escape(query_token)}\b', re.IGNORECASE)
    for idx, line in enumerate(lines):
        clean_l = line.strip()
        if not clean_l:
            continue
        if pattern.search(clean_l):
            matches.append(f"Line {idx+1}: {clean_l}")
            if len(matches) >= max_refs:
                break
    return matches

# ==========================================
# 3. SIDEBAR: AUDIO & NATAL ANCHOR
# ==========================================

with st.sidebar:
    st.title("⚓ Natal Anchor")
    
    st.subheader("Frequency Carrier")
    freq_choice = st.radio("Solfeggio Carrier", ["Silence", "432 Hz", "528 Hz"], horizontal=True)
    if freq_choice == "432 Hz":
        st.caption("Carrier active: Natural harmonic geometry (432 Hz)")
    elif freq_choice == "528 Hz":
        st.caption("Carrier active: Miraculous repair frequency (528 Hz)")

    st.markdown("---")
    anchor_name = st.text_input("Anchor Name", value="Seeker")
    
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
    st.markdown("---")
    st.caption("Universal Anchor pinned across all active reading chambers.")

# ==========================================
# 4. UNIVERSAL SEARCH / INPUT CLASSIFIER
# ==========================================

st.title("NUMBERIN")
search_query = st.text_input("Enter any name, word, phrase, or date (e.g. '33 CE', '4000 BCE', '1983-11-19'):", "")

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
# 5. CHAMBERS / TABS
# ==========================================

tabs = st.tabs([
    "Alchemy Pharmacy", 
    "Corpus Knowledge Base", 
    "Milestone Timeline Lens", 
    "Decan Oracle", 
    "Compatibility Matrix", 
    "Pattern & Frequency Engine"
])

# ----------------------------------------------------
# TAB 1: ALCHEMY PHARMACY
# ----------------------------------------------------
with tabs[0]:
    st.markdown("### The Alchemy Pharmacy")
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
        <div class="brass-card">
            <h4 style="text-align: center; color: #d4af37; margin-bottom: 5px;">The Three Pivot Rings Locked</h4>
            <div class="ring-container">
                <div class="ring-badge">Outer Ring<br><small>{wm['day']}</small></div>
                <div class="ring-badge">Middle Pivot<br><small>{wm['planet']}</small></div>
                <div class="ring-badge">Inner Core<br><small>{wm['metal']}</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tincture-box">
            <strong>Prescription & Tincture:</strong><br><br>
            {td['tincture_prose']}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Examine the Bench Apparatus (Technical Breakdown)"):
            st.markdown(f"- **Historical Horizon:** `{td['a_year']} {td['a_era']}, Month {td['a_month']}, Day {td['a_day']}`")
            st.markdown(f"- **Working Modulo:** `{td['total_alch']} ≡ {td['working_idx']} (mod 7)`")
            st.markdown(f"- **Core Metal Skeleton:** {wm['metal']} ({wm['planet']})")
            st.markdown(f"- **Distraction Axis (+3):** {dm['metal']} ({dm['planet']})")

# ----------------------------------------------------
# TAB 2: CORPUS KNOWLEDGE BASE (Enhanced Query & Reference Engine)
# ----------------------------------------------------
with tabs[1]:
    st.markdown("### The Full-Corpus Library Engine")
    st.markdown("Search, cross-examine, and extract patterns across complete esoteric and sacred literature without excerpts or truncations.")

    CORPUS_URLS = {
        "King James Bible (Complete)": "https://www.gutenberg.org/cache/epub/10/pg10.txt",
        "The Kybalion (Three Initiates)": "https://www.gutenberg.org/cache/epub/14264/pg14264.txt",
        "The Book of Enoch": "https://www.gutenberg.org/cache/epub/45238/pg45238.txt",
        "Pistis Sophia": "https://www.gutenberg.org/cache/epub/44423/pg44423.txt",
        "I Ching (Legge Translation)": "https://www.gutenberg.org/cache/epub/25890/pg25890.txt"
    }

    @st.cache_data(show_spinner=False)
    def fetch_full_text(url: str) -> str:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=12) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception:
            return ""

    corpus_source = st.selectbox("Select Active Canonical Corpus", ["Custom Upload"] + list(CORPUS_URLS.keys()))
    corpus_text = ""

    if corpus_source == "Custom Upload":
        uploaded_file = st.file_uploader("Upload any complete .txt or .md manuscript", type=["txt", "md"])
        if uploaded_file is not None:
            corpus_text = uploaded_file.read().decode('utf-8', errors='ignore')
    else:
        with st.spinner(f"Loading complete text for {corpus_source}..."):
            corpus_text = fetch_full_text(CORPUS_URLS[corpus_source])
            if not corpus_text:
                st.warning("Manuscript could not be pulled from Gutenberg live mirror. Please upload a local text file.")

    if corpus_text:
        total_chars = len(corpus_text)
        words_list = re.findall(r'\b[A-Za-z]+\b', corpus_text.lower())
        total_words = len(words_list)
        
        st.caption(f"Corpus Active: **{total_words:,} words** | **{total_chars:,} characters**")

        st.markdown("#### Corpus Plain-Language Inquiry")
        query = st.text_input("Ask a question or enter a search query:", 
                              placeholder="e.g. 'what word shows up the most', 'least common words', 'fear', 'find all sevens'")

        if query:
            q_clean = query.strip().lower()
            
            # 1. MOST COMMON WORDS / WHAT SHOWS UP THE MOST
            if any(k in q_clean for k in ["most common", "shows up most", "up the most", "the much", "most frequent", "highest frequency"]):
                stop_words = {"the", "and", "of", "to", "in", "that", "he", "shall", "unto", "for", "with", "a", "is", "his", "they", "be", "not", "it", "as", "by", "all", "this", "from"}
                filtered = [w for w in words_list if w not in stop_words and len(w) > 2]
                counts = Counter(filtered).most_common(10)
                st.markdown("#### Most Frequent Words (Excluding Articles/Conjunctions):")
                for w, c in counts:
                    st.markdown(f"- **{w}**: `{c:,}` times")
                
                top_word = counts[0][0]
                st.markdown(f"##### Line References for '{top_word}':")
                refs = extract_references(corpus_text, top_word, max_refs=4)
                for r in refs:
                    st.markdown(f"<div class='ref-box'>{r}</div>", unsafe_allow_html=True)

            # 2. LEAST COMMON WORDS / SINGLE OCCURRENCES
            elif any(k in q_clean for k in ["least common", "shows up least", "the least", "rarest", "hapax"]):
                single_words = [w for w, c in Counter(words_list).items() if c == 1 and len(w) > 3]
                sample_least = single_words[:10]
                st.markdown("#### Single-Occurrence Words (Words Appearing Exactly Once):")
                st.write(", ".join(sample_least))
                
                if sample_least:
                    st.markdown(f"##### Line Reference for Rare Occurrence '{sample_least[0]}':")
                    refs = extract_references(corpus_text, sample_least[0], max_refs=1)
                    for r in refs:
                        st.markdown(f"<div class='ref-box'>{r}</div>", unsafe_allow_html=True)

            # 3. SEVENS OR DIGIT PATTERNS
            elif "seven" in q_clean or " 7 " in q_clean or q_clean == "7":
                matches = len(re.findall(r'\b(7|seven|seventh)\b', corpus_text, re.IGNORECASE))
                st.markdown(f"**Direct Result:** The number seven appears **{matches:,} times** across the full manuscript.")
                st.markdown("##### Excerpt References for 'seven':")
                refs = extract_references(corpus_text, "seven", max_refs=4)
                for r in refs:
                    st.markdown(f"<div class='ref-box'>{r}</div>", unsafe_allow_html=True)

            # 4. LETTER FREQUENCY
            elif "letter frequency" in q_clean or "letters" in q_clean:
                letters_only = [c for c in corpus_text.upper() if 'A' <= c <= 'Z']
                l_counts = Counter(letters_only).most_common(7)
                st.markdown("#### Dominant Letter Frequencies:")
                for l, count in l_counts:
                    pct = (count / len(letters_only)) * 100
                    st.markdown(f"- **{l}**: {count:,} times ({pct:.2f}%)")

            # 5. WHOLE-CORPUS NUMEROLOGY ROOT
            elif "root" in q_clean or "grand root" in q_clean:
                root_sum = sum(ord(c) - 64 for c in corpus_text.upper() if 'A' <= c <= 'Z')
                collapsed = reduce_number(root_sum)
                st.markdown(f"**Corpus Grand Root:** `{collapsed}` — {meaning(collapsed)}")

            # 6. DIRECT PHRASE / TARGET WORD SEARCH WITH REFERENCES
            else:
                target_word = re.sub(r'^(find|how many times does|how many times|count|find every time it says|search for)\s+', '', q_clean).strip().strip("'\"")
                target_word = target_word.split()[0] if target_word else q_clean
                
                raw_find = len(re.findall(rf'\b{re.escape(target_word)}\b', corpus_text, re.IGNORECASE))
                st.markdown(f"**Direct Result:** The word **'{target_word}'** appears **{raw_find:,} times** across the manuscript.")
                
                if raw_find > 0:
                    st.markdown(f"##### Line References for '{target_word}':")
                    refs = extract_references(corpus_text, target_word, max_refs=5)
                    for r in refs:
                        st.markdown(f"<div class='ref-box'>{r}</div>", unsafe_allow_html=True)
                else:
                    st.info("No exact occurrences found in this corpus.")

# ----------------------------------------------------
# TAB 3: MILESTONE TIMELINE LENS
# ----------------------------------------------------
with tabs[2]:
    st.markdown("### Milestone Timeline Lens")
    st.markdown("Track the 9-year cyclic unfoldment across any historical or future timeline.")
    
    st.markdown("**Inception Date**")
    m_c1, m_c2, m_c3 = st.columns(3)
    with m_c1:
        m_yr = st.number_input("Year", min_value=1, max_value=9999, value=s_year, key="m_y")
    with m_c2:
        m_mo = st.number_input("Month", min_value=1, max_value=12, value=s_month, key="m_m")
    with m_c3:
        m_dy = st.number_input("Day", min_value=1, max_value=31, value=s_day, key="m_d")
    
    m_years = st.slider("Timeline Horizon (Cycles)", min_value=1, max_value=81, value=9)

    st.markdown("#### Projected Sequence")
    milestone_records = []
    for y in range(m_yr, m_yr + m_years):
        res = personal_cycles_components(m_mo, m_dy, y)
        milestone_records.append({
            "Calendar Year": y,
            "Personal Year": res["personal_year"],
            "Theme": res["milestone"]
        })
    st.table(milestone_records)

# ----------------------------------------------------
# TAB 4: DECAN ORACLE
# ----------------------------------------------------
with tabs[3]:
    st.markdown("### Decan Oracle")
    st.markdown("The 36 Decan faces of the ecliptic and their planetary sub-rulers.")
    
    sel_sign = st.selectbox("Select Zodiac Sign", list(ZODIAC_DECANS.keys()))
    decans = ZODIAC_DECANS[sel_sign]
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"**First Decan**\n\n{decans[0]}")
    with c2:
        st.markdown(f"**Second Decan**\n\n{decans[1]}")
    with c3:
        st.markdown(f"**Third Decan**\n\n{decans[2]}")

# ----------------------------------------------------
# TAB 5: COMPATIBILITY MATRIX
# ----------------------------------------------------
with tabs[4]:
    st.markdown("### Compatibility Matrix")
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
        st.markdown("**Second Anchor Date (e.g. 33 CE or 2050 CE)**")
        cp2_y = st.number_input("Year", min_value=1, max_value=99999, value=33, key="cp2_y")
        cp2_m = st.number_input("Month", min_value=1, max_value=12, value=4, key="cp2_m")
        cp2_d = st.number_input("Day", min_value=1, max_value=31, value=3, key="cp2_d")
        lp2 = life_path_components(cp2_y, cp2_m, cp2_d)
        st.markdown(f"Secondary Life Path: `{lp2}`")

    comp_result = evaluate_compatibility(lp1, lp2)
    st.markdown(f"""
    <div class="brass-card">
        <h4>Synthesis Verdict</h4>
        <p>{comp_result}</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 6: PATTERN & FREQUENCY ENGINE
# ----------------------------------------------------
with tabs[5]:
    st.markdown("### Pattern & Frequency Engine")
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
