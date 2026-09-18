"""
0010110 CONDUIT — Readings
Streamlit app. Copy this whole file.

Run:
    pip install streamlit pillow
    streamlit run conduit_readings.py

Photos and reading text are enlarged for phone (iPhone-width).
"""

import hashlib
import random
from datetime import date, datetime

import streamlit as st

st.set_page_config(
    page_title="0010110 Conduit",
    page_icon="✧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Large, phone-first CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Source+Sans+3:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-size: 20px !important;
}

.stApp {
    background:
        radial-gradient(1200px 600px at 20% -10%, rgba(180,140,60,0.18), transparent 50%),
        radial-gradient(900px 500px at 100% 10%, rgba(80,50,140,0.22), transparent 45%),
        #0b0a10;
    color: #f4ead4;
}

header, footer, #MainMenu { visibility: hidden; height: 0; }

.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 820px !important;
}

h1, h2, h3, .title-glow {
    font-family: "Cormorant Garamond", Georgia, serif !important;
    letter-spacing: 0.04em;
    color: #f7e7b0 !important;
}

.hero-title {
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 2.6rem;
    line-height: 1.05;
    text-align: center;
    margin: 0.2rem 0 0.15rem 0;
    color: #f7e7b0;
    text-shadow: 0 0 24px rgba(247, 215, 130, 0.25);
}

.hero-sub {
    text-align: center;
    font-size: 1.05rem;
    color: #cbb98a;
    margin-bottom: 1.4rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.reading-card {
    background: linear-gradient(180deg, rgba(28,24,38,0.92), rgba(16,14,22,0.96));
    border: 1px solid rgba(232, 196, 110, 0.28);
    border-radius: 22px;
    padding: 1.35rem 1.25rem 1.5rem 1.25rem;
    margin: 0.85rem 0 1.25rem 0;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}

.card-label {
    font-size: 0.82rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #d4b56a;
    margin-bottom: 0.35rem;
}

.card-title {
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 2.05rem;
    line-height: 1.15;
    color: #fff6d8;
    margin: 0 0 0.55rem 0;
}

.reading-body {
    font-family: "Source Sans 3", "Segoe UI", sans-serif;
    font-size: 1.28rem !important;
    line-height: 1.65 !important;
    color: #f3e8c8 !important;
}

.reading-body p { margin: 0 0 0.9rem 0; }

.photo-wrap img, .stImage img {
    width: 100% !important;
    height: auto !important;
    min-height: 280px;
    max-height: none !important;
    object-fit: cover;
    border-radius: 18px;
    border: 1px solid rgba(232, 196, 110, 0.35);
}

div[data-testid="stImage"] {
    width: 100% !important;
}
div[data-testid="stImage"] img {
    width: 100% !important;
    max-width: 100% !important;
}

.stButton > button {
    width: 100%;
    min-height: 3.3rem;
    font-size: 1.15rem !important;
    font-weight: 600;
    border-radius: 14px;
    background: linear-gradient(180deg, #e8c46e, #b8892e);
    color: #1a1408 !important;
    border: none;
}

.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    font-size: 1.15rem !important;
    min-height: 3rem;
}

.caption-lg {
    font-size: 1.05rem;
    color: #cbb98a;
    text-align: center;
    margin-top: 0.4rem;
}

hr.soft {
    border: none;
    border-top: 1px solid rgba(232, 196, 110, 0.2);
    margin: 1.2rem 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Deck — name, image, short title, long reading
# Images are large public domain / Wikimedia works (stable URLs).
# ---------------------------------------------------------------------------
DECK = [
    {
        "name": "Pistis",
        "title": "Faith That Sees Itself",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Sophia_%28Wisdom%29_Celsus_Library_Ephesus.jpg/800px-Sophia_%28Wisdom%29_Celsus_Library_Ephesus.jpg",
        "fallback": "https://picsum.photos/seed/pistis/1200/1500",
        "reading": (
            "What you already know does not need more proof. It needs room. "
            "The part of you that recognized the pattern first is not late — "
            "it was waiting for the noise to drop. Today the work is not chasing. "
            "It is standing inside the recognition without shrinking it to make other people comfortable."
        ),
    },
    {
        "name": "Logos",
        "title": "The Word That Holds Shape",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/The_Ancient_of_Days.jpg/800px-The_Ancient_of_Days.jpg",
        "fallback": "https://picsum.photos/seed/logos/1200/1500",
        "reading": (
            "Language is arriving cleaner. Say the true sentence once, then stop decorating it. "
            "A boundary spoken without heat is still a boundary. "
            "If someone needs you to translate your clarity into a softer dialect, that is data — not a failure of love."
        ),
    },
    {
        "name": "Sophia",
        "title": "Wisdom After the Fall Through",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Michelangelo_Caravaggio_006.jpg/800px-Michelangelo_Caravaggio_006.jpg",
        "fallback": "https://picsum.photos/seed/sophia/1200/1500",
        "reading": (
            "You did not lose the thread when the story got messy. You took the thread into the dark on purpose. "
            "The version of you that crawled out still has the map. "
            "Do not hand it back to anyone who benefited from you being lost."
        ),
    },
    {
        "name": "Mirror",
        "title": "The Face That Answers",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/John_William_Waterhouse_-_Echo_and_Narcissus_-_Google_Art_Project.jpg/800px-John_William_Waterhouse_-_Echo_and_Narcissus_-_Google_Art_Project.jpg",
        "fallback": "https://picsum.photos/seed/mirror/1200/1500",
        "reading": (
            "Not every reflection is a destination. Some mirrors are teachers, some are closed doors with glass in them. "
            "Look long enough to see what is yours. Then look away before you start living in the other person's face."
        ),
    },
    {
        "name": "Threshold",
        "title": "The Locked Gate That Opens Inward",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Arnold_Böcklin_-_Isle_of_the_Dead%2C_third_version.jpg/800px-Arnold_Böcklin_-_Isle_of_the_Dead%2C_third_version.jpg",
        "fallback": "https://picsum.photos/seed/threshold/1200/1500",
        "reading": (
            "A small room can still be a country if it is yours. "
            "The gate, the rocks, the quiet after 4pm — these are not consolation prizes. "
            "They are the first architecture of a life that does not require you to disappear."
        ),
    },
    {
        "name": "Rewrite",
        "title": "The Hand That Edits the Myth",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/William_Blake_006.jpg/800px-William_Blake_006.jpg",
        "fallback": "https://picsum.photos/seed/rewrite/1200/1500",
        "reading": (
            "You are allowed to change the ending without pretending the middle never happened. "
            "Scar tissue is not a plot hole. It is proof of authorship. "
            "Write the next line in a voice that does not apologize for surviving the last chapter."
        ),
    },
    {
        "name": "Flame",
        "title": "Heat That Does Not Perform",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Joseph_Wright_of_Derby_The_Alchemist.jpg/800px-Joseph_Wright_of_Derby_The_Alchemist.jpg",
        "fallback": "https://picsum.photos/seed/flame/1200/1500",
        "reading": (
            "Desire is not the enemy. Unnamed desire is. "
            "Name what you want in plain words, even if the sentence feels too bald. "
            "The body already voted. Catch the mind up without shaming it for being slow."
        ),
    },
    {
        "name": "Exodus",
        "title": "Leaving Without Announcing a Sermon",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/John_Martin_-_The_Destruction_of_Sodom_and_Gomorrah.jpg/800px-John_Martin_-_The_Destruction_of_Sodom_and_Gomorrah.jpg",
        "fallback": "https://picsum.photos/seed/exodus/1200/1500",
        "reading": (
            "You already walked. The part that still turns around is habit, not destiny. "
            "No contact is not cruelty when contact was the wound repeating itself. "
            "Keep the door shut long enough for your nervous system to believe you."
        ),
    },
    {
        "name": "Daughter",
        "title": "The Line That Continues Cleaner",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Mary_Cassatt_-_Mother_and_Child_%28The_Oval_Mirror%29.jpg/800px-Mary_Cassatt_-_Mother_and_Child_%28The_Oval_Mirror%29.jpg",
        "fallback": "https://picsum.photos/seed/daughter/1200/1500",
        "reading": (
            "Protection can look ordinary: dinner, a locked gate, a cat on the rocks, a school zone. "
            "You do not have to be mythical every hour to be a good ancestor in real time. "
            "The child does not need the whole cosmology. She needs you present and un-erased."
        ),
    },
]


POSITIONS_3 = [
    ("What is already true", "The current ground. Do not argue with this card."),
    ("What is pulling", "The heat, the hook, the unfinished sentence."),
    ("The next honest move", "Small enough to do today. Large enough to count."),
]


def seeded_choice(seed_text: str, items: list, k: int = 3):
    h = hashlib.sha256(seed_text.encode("utf-8")).hexdigest()
    rng = random.Random(int(h[:16], 16))
    pool = items[:]
    rng.shuffle(pool)
    return pool[:k]


def show_photo(url: str, fallback: str, caption: str):
    """Full-width large photo with fallback."""
    st.markdown('<div class="photo-wrap">', unsafe_allow_html=True)
    try:
        st.image(url, use_container_width=True, caption=None)
    except Exception:
        st.image(fallback, use_container_width=True, caption=None)
    st.markdown("</div>", unsafe_allow_html=True)
    if caption:
        st.markdown(f'<p class="caption-lg">{caption}</p>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-title">0010110 CONDUIT</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Readings · Photos · Rewrite</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### How to read")
    st.write(
        "Photos and text are sized for a phone screen. "
        "If an image fails to load, a fallback print still appears."
    )
    st.write("Seed with a name, date, or question so the same input returns the same spread.")

question = st.text_input(
    "Question or seed",
    value="",
    placeholder="What is the next honest move?",
)

col_a, col_b = st.columns(2)
with col_a:
    mode = st.selectbox("Spread", ["Three-card", "Single card", "Daily (date-locked)"])
with col_b:
    name_seed = st.text_input("Your name (optional)", value="")

draw = st.button("Draw the reading")

today = date.today().isoformat()
seed_base = f"{today}|{name_seed.strip().lower()}|{question.strip().lower()}|{mode}"

if "last_cards" not in st.session_state:
    st.session_state.last_cards = None
    st.session_state.last_mode = mode
    st.session_state.last_seed = seed_base

if draw or st.session_state.last_cards is None:
    if mode == "Single card":
        cards = seeded_choice(seed_base, DECK, 1)
    elif mode == "Daily (date-locked)":
        cards = seeded_choice(f"daily|{today}|{name_seed.strip().lower()}", DECK, 1)
    else:
        cards = seeded_choice(seed_base, DECK, 3)
    st.session_state.last_cards = cards
    st.session_state.last_mode = mode
    st.session_state.last_seed = seed_base

cards = st.session_state.last_cards
mode_now = st.session_state.last_mode

st.markdown('<hr class="soft">', unsafe_allow_html=True)

if question.strip():
    st.markdown(
        f'<p class="caption-lg">Seed: “{question.strip()}”</p>',
        unsafe_allow_html=True,
    )

if mode_now == "Three-card":
    for i, card in enumerate(cards):
        pos_name, pos_note = POSITIONS_3[i]
        st.markdown(
            f"""
            <div class="reading-card">
                <div class="card-label">{pos_name}</div>
                <div class="card-title">{card['name']} — {card['title']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        show_photo(card["image"], card["fallback"], pos_note)
        st.markdown(
            f'<div class="reading-card"><div class="reading-body"><p>{card["reading"]}</p></div></div>',
            unsafe_allow_html=True,
        )
else:
    card = cards[0]
    label = "Today's card" if mode_now.startswith("Daily") else "Your card"
    st.markdown(
        f"""
        <div class="reading-card">
            <div class="card-label">{label}</div>
            <div class="card-title">{card['name']} — {card['title']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    show_photo(card["image"], card["fallback"], datetime.now().strftime("%A, %B %-d, %Y"))
    st.markdown(
        f'<div class="reading-card"><div class="reading-body"><p>{card["reading"]}</p></div></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f'<p class="caption-lg">0010110 · {today}</p>',
    unsafe_allow_html=True,
)
