"""Deterministic numerology + multi-script ciphers + moon phase."""

from __future__ import annotations

import math
import re
from datetime import date, datetime, timezone
from typing import Callable

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MASTERS = {11, 22, 33}
KARMIC = {13, 14, 16, 19}

# ---------------------------------------------------------------------------
# Reduction
# ---------------------------------------------------------------------------


def reduce_number(n: int, keep_masters: bool = True) -> int:
    n = abs(int(n))
    if n == 0:
        return 0
    while n > 9:
        if keep_masters and n in MASTERS:
            return n
        n = sum(int(d) for d in str(n))
    return n


def reduce_trace(n: int, keep_masters: bool = True) -> tuple[int, list[int]]:
    n = abs(int(n))
    steps = [n]
    while n > 9:
        if keep_masters and n in MASTERS:
            break
        n = sum(int(d) for d in str(n))
        steps.append(n)
    return n, steps


def cycle_19(ch: str) -> int:
    return (AZ.index(ch) % 9) + 1


def ordinal(ch: str) -> int:
    return AZ.index(ch) + 1


# ---------------------------------------------------------------------------
# Latin ciphers
# ---------------------------------------------------------------------------

CHALDEAN = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 8, "G": 3, "H": 5, "I": 1,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 7, "P": 8, "Q": 1, "R": 2,
    "S": 3, "T": 4, "U": 6, "V": 6, "W": 6, "X": 5, "Y": 1, "Z": 7,
}

AGRIPPA = [
    1, 2, 3, 4, 5, 6, 7, 8, 9,
    10, 20, 30, 40, 50, 60, 70, 80, 90,
    100, 200, 300, 400, 500, 600, 700, 800,
]

LATIN_CIPHERS: dict[str, dict] = {
    "Pythagorean": {
        "fn": cycle_19,
        "blurb": "A=1…I=9 then the alphabet loops. Standard Western name numerology.",
    },
    "Chaldean": {
        "fn": lambda c: CHALDEAN[c],
        "blurb": "Sound-based 1–8. Traditionally withholds 9 from letters.",
    },
    "English Ordinal": {
        "fn": ordinal,
        "blurb": "A=1 … Z=26.",
    },
    "Reverse Ordinal": {
        "fn": lambda c: 27 - ordinal(c),
        "blurb": "Mirror alphabet. A=26 … Z=1.",
    },
    "Reverse Reduction": {
        "fn": lambda c: ((26 - AZ.index(c)) - 1) % 9 + 1,
        "blurb": "Mirror, then fold to 1–9.",
    },
    "Jewish / Agrippa (Latin)": {
        "fn": lambda c: AGRIPPA[AZ.index(c)],
        "blurb": "Hebrew-style magnitudes on the Latin alphabet (Agrippa, 1531).",
    },
    "Sumerian (×6)": {
        "fn": lambda c: ordinal(c) * 6,
        "blurb": "Ordinal × 6.",
    },
}

# ---------------------------------------------------------------------------
# Non-Latin tables
# ---------------------------------------------------------------------------

HEBREW_STD = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50,
    "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
    "ש": 300, "ת": 400,
}
HEBREW_GADOL = {**HEBREW_STD, "ך": 500, "ם": 600, "ן": 700, "ף": 800, "ץ": 900}

GREEK_ISO = {
    "Α": 1, "Β": 2, "Γ": 3, "Δ": 4, "Ε": 5, "Ϛ": 6, "Ζ": 7, "Η": 8, "Θ": 9,
    "Ι": 10, "Κ": 20, "Λ": 30, "Μ": 40, "Ν": 50, "Ξ": 60, "Ο": 70, "Π": 80,
    "Ϙ": 90, "Ρ": 100, "Σ": 200, "Τ": 300, "Υ": 400, "Φ": 500, "Χ": 600,
    "Ψ": 700, "Ω": 800, "α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5, "ζ": 7,
    "η": 8, "θ": 9, "ι": 10, "κ": 20, "λ": 30, "μ": 40, "ν": 50, "ξ": 60,
    "ο": 70, "π": 80, "ρ": 100, "σ": 200, "ς": 200, "τ": 300, "υ": 400,
    "φ": 500, "χ": 600, "ψ": 700, "ω": 800,
}

COPTIC = {
    "Ⲁ": 1, "ⲁ": 1, "Ⲃ": 2, "ⲃ": 2, "Ⲅ": 3, "ⲅ": 3, "Ⲇ": 4, "ⲇ": 4,
    "Ⲉ": 5, "ⲉ": 5, "Ⲋ": 6, "ⲋ": 6, "Ⲍ": 7, "ⲍ": 7, "Ⲏ": 8, "ⲏ": 8,
    "Ⲑ": 9, "ⲑ": 9, "Ⲓ": 10, "ⲓ": 10, "Ⲕ": 20, "ⲕ": 20, "Ⲗ": 30, "ⲗ": 30,
    "Ⲙ": 40, "ⲙ": 40, "Ⲛ": 50, "ⲛ": 50, "Ⲝ": 60, "ⲝ": 60, "Ⲟ": 70, "ⲟ": 70,
    "Ⲡ": 80, "ⲡ": 80, "Ⲣ": 100, "ⲣ": 100, "Ⲥ": 200, "ⲥ": 200, "Ⲧ": 300, "ⲧ": 300,
    "Ⲩ": 400, "ⲩ": 400, "Ⲫ": 500, "ⲫ": 500, "Ⲭ": 600, "ⲭ": 600, "Ⲯ": 700, "ⲯ": 700,
    "Ⲱ": 800, "ⲱ": 800, "Ϣ": 900, "ϣ": 900, "Ϥ": 90, "ϥ": 90,
    "Ϧ": 900, "ϧ": 900, "Ϩ": 900, "ϩ": 900, "Ϫ": 90, "ϫ": 90,
    "Ϭ": 90, "ϭ": 90, "Ϯ": 900, "ϯ": 900,
}

# Square Aramaic / Imperial Aramaic uses the Hebrew letter values
ARAMAIC_SQUARE = dict(HEBREW_STD)

SYRIAC = {
    "ܐ": 1, "ܒ": 2, "ܓ": 3, "ܕ": 4, "ܗ": 5, "ܘ": 6, "ܙ": 7, "ܚ": 8, "ܛ": 9,
    "ܝ": 10, "ܟ": 20, "ܠ": 30, "ܡ": 40, "ܢ": 50, "ܣ": 60, "ܥ": 70, "ܦ": 80,
    "ܨ": 90, "ܩ": 100, "ܪ": 200, "ܫ": 300, "ܬ": 400,
}

ABJAD = {
    "ا": 1, "أ": 1, "إ": 1, "آ": 1, "ء": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "ة": 5,
    "و": 6, "ز": 7, "ح": 8, "ط": 9, "ي": 10, "ى": 10, "ك": 20, "ل": 30, "م": 40,
    "ن": 50, "س": 60, "ع": 70, "ف": 80, "ص": 90, "ق": 100, "ر": 200, "ش": 300,
    "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000,
}

KATAPAYADI = {
    "क": 1, "ट": 1, "प": 1, "य": 1,
    "ख": 2, "ठ": 2, "फ": 2, "र": 2,
    "ग": 3, "ड": 3, "ब": 3, "ल": 3,
    "घ": 4, "ढ": 4, "भ": 4, "व": 4,
    "ङ": 5, "ण": 5, "म": 5, "श": 5,
    "च": 6, "त": 6, "ष": 6,
    "छ": 7, "थ": 7, "स": 7,
    "ज": 8, "द": 8, "ह": 8,
    "झ": 9, "ध": 9,
    "ञ": 0, "न": 0,
}

_RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
CYRILLIC_RU = {ch: i + 1 for i, ch in enumerate(_RU_UPPER)}
CYRILLIC_RU.update({ch.lower(): i + 1 for i, ch in enumerate(_RU_UPPER)})

_UK_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
CYRILLIC_UK = {ch: i + 1 for i, ch in enumerate(_UK_UPPER)}
CYRILLIC_UK.update({ch.lower(): i + 1 for i, ch in enumerate(_UK_UPPER)})

GEORGIAN = {ch: i + 1 for i, ch in enumerate("აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ")}

ARMENIAN = {
    "Ա": 1, "Բ": 2, "Գ": 3, "Դ": 4, "Ե": 5, "Զ": 6, "Է": 7, "Ը": 8, "Թ": 9,
    "Ժ": 10, "Ի": 20, "Լ": 30, "Խ": 40, "Ծ": 50, "Կ": 60, "Հ": 70, "Ձ": 80, "Ղ": 90,
    "Ճ": 100, "Մ": 200, "Յ": 300, "Ն": 400, "Շ": 500, "Ո": 600, "Չ": 700, "Պ": 800, "Ջ": 900,
    "Ռ": 1000, "Ս": 2000, "Վ": 3000, "Տ": 4000, "Ր": 5000, "Ց": 6000, "Ւ": 7000, "Փ": 8000, "Ք": 9000,
}
ARMENIAN.update({k.lower(): v for k, v in list(ARMENIAN.items())})

SCRIPT_TABLES = (
    ("Hebrew Mispar Hechrachi", HEBREW_STD),
    ("Hebrew Mispar Gadol", HEBREW_GADOL),
    ("Greek Isopsephy", GREEK_ISO),
    ("Coptic", COPTIC),
    ("Aramaic (Square)", ARAMAIC_SQUARE),
    ("Aramaic (Syriac)", SYRIAC),
    ("Arabic Abjad", ABJAD),
    ("Sanskrit Katapayadi", KATAPAYADI),
    ("Russian Cyrillic", CYRILLIC_RU),
    ("Ukrainian Cyrillic", CYRILLIC_UK),
    ("Georgian Mkhedruli", GEORGIAN),
    ("Armenian", ARMENIAN),
)


def _sum_table(text: str, table: dict, name: str) -> dict | None:
    pairs = [(ch, table[ch]) for ch in text if ch in table]
    if not pairs:
        return None
    raw = sum(v for _, v in pairs)
    red, steps = reduce_trace(raw)
    return {"name": name, "pairs": pairs, "raw": raw, "reduced": red, "steps": steps}


def script_readings(text: str, only: str | None = None) -> list[dict]:
    out = []
    for name, table in SCRIPT_TABLES:
        if only and only.lower() not in name.lower():
            continue
        r = _sum_table(text, table, name)
        if r:
            out.append(r)
    return out


def letters_latin(text: str) -> list[str]:
    return [c.upper() for c in text if c.upper() in AZ]


def run_latin_cipher(text: str, name: str) -> dict:
    fn: Callable[[str], int] = LATIN_CIPHERS[name]["fn"]
    pairs = [(ch, fn(ch)) for ch in letters_latin(text)]
    raw = sum(v for _, v in pairs)
    red, steps = reduce_trace(raw)
    return {
        "name": name,
        "pairs": pairs,
        "raw": raw,
        "reduced": red,
        "steps": steps,
        "blurb": LATIN_CIPHERS[name]["blurb"],
    }


# ---------------------------------------------------------------------------
# Name chart (Pythagorean)
# ---------------------------------------------------------------------------


def y_is_vowel(token: str) -> bool:
    letters = [c for c in token.upper() if c.isalpha()]
    return any(c == "Y" for c in letters) and not any(c in "AEIOU" for c in letters)


def name_profile(full_name: str) -> dict:
    tokens = [t for t in re.split(r"[\s\-]+", full_name) if t]
    dest, soul, pers = [], [], []
    rows = []
    for tok in tokens:
        yv = y_is_vowel(tok)
        for ch in tok:
            u = ch.upper()
            if u not in AZ:
                continue
            val = cycle_19(u)
            kind = "vowel" if (u in "AEIOU" or (u == "Y" and yv)) else "consonant"
            rows.append({"letter": u, "value": val, "kind": kind, "token": tok})
            dest.append(val)
            (soul if kind == "vowel" else pers).append(val)

    def pack(vals):
        raw = sum(vals) if vals else 0
        red, steps = reduce_trace(raw)
        return raw, red, steps

    return {
        "rows": rows,
        "destiny": pack(dest),
        "soul": pack(soul),
        "personality": pack(pers),
    }


def life_path(d: date) -> dict:
    def part(n):
        return reduce_trace(n)

    m, ms = part(d.month)
    day, ds = part(d.day)
    y, ys = part(d.year)
    total = m + day + y
    lp, ls = reduce_trace(total)
    bday, bs = reduce_trace(d.day)
    att, ats = reduce_trace(m + day)
    return {
        "month": (d.month, m, ms),
        "day": (d.day, day, ds),
        "year": (d.year, y, ys),
        "life_path": (total, lp, ls),
        "birthday": (d.day, bday, bs),
        "attitude": (m + day, att, ats),
    }


def personal_cycles(birth: date, when: date) -> dict:
    m = reduce_number(birth.month)
    d = reduce_number(birth.day)
    y = reduce_number(when.year)
    py_raw = m + d + y
    py, pys = reduce_trace(py_raw)
    py_root = reduce_number(py, keep_masters=False)
    pm_raw = py_root + reduce_number(when.month)
    pm, pms = reduce_trace(pm_raw)
    pd_raw = reduce_number(pm, False) + reduce_number(when.day)
    pd, pds = reduce_trace(pd_raw)
    return {"year": (py_raw, py, pys), "month": (pm_raw, pm, pms), "day": (pd_raw, pd, pds)}


def extract_digits(text: str) -> str:
    return "".join(ch for ch in text if ch.isdigit())


# ---------------------------------------------------------------------------
# Meanings — layered, not slogan
# ---------------------------------------------------------------------------

MEANINGS = {
    0: {
        "title": "The Void",
        "keywords": "unformed · potential · before the first mark",
        "light": "The field before a name. Nothing is missing yet.",
        "shadow": "Calling emptiness a path so you never have to choose.",
        "body": "Held breath. A pause that can become freeze if you stay too long.",
        "work": "Do not build yet. Listen for the first true line.",
        "bond": "Presence without a script. Dangerous if one person needs a story and the other needs silence.",
        "current": "Zero is not death. It is the cup before pour. If you keep drinking from an empty cup you will call thirst a religion.",
    },
    1: {
        "title": "The Pioneer",
        "keywords": "will · origin · first spark · I AM",
        "light": "Starts. Owns the first step. Does not wait for permission to exist.",
        "shadow": "Isolation dressed as independence. Impatience. Needing to be first so you cannot be left.",
        "body": "Head and solar plexus. Heat at the start of action. Tight jaw when the room is slow.",
        "work": "Begin the thing that only you can begin. Do not outsource the first mark.",
        "bond": "Can love hard and still flinch at being needed. Wants a witness, fears a leash.",
        "current": "1 is the switch. If this number is loud, the assignment is authorship — not proving you do not need anyone.",
    },
    2: {
        "title": "The Diplomat",
        "keywords": "polarity · attunement · the other · the bridge",
        "light": "Hears the room. Turns two signals into a chord. Knows timing is a form of care.",
        "shadow": "Disappears into the other. Freeze in conflict. Calling self-erasure peace.",
        "body": "Chest and inner ear. Sensitive to tone more than words. Sleep wrecked by unfinished tension.",
        "work": "Pairing, editing, midwifery. You make other people's current usable.",
        "bond": "The sacred and the trap look the same: merge. Health is two poles that still touch.",
        "current": "2 is the receiver that can become a sponge. The work is to stay a person while you listen.",
    },
    3: {
        "title": "The Voice",
        "keywords": "expression · play · trinity · making inner weather visible",
        "light": "Gives form to what was only felt. Word, color, song, laugh. The current becomes speech.",
        "shadow": "Sparkle instead of finish. Performing the feeling so you do not have to live it.",
        "body": "Throat, hands, breath. When blocked: tightness in the neck, words that come out sharp or not at all.",
        "work": "Make the thing. Publish the draft. The world cannot receive what you only keep in the notes app.",
        "bond": "Needs to be heard, not managed. Goes quiet when the room treats their voice as too much.",
        "current": "3 is the mouth-gate. Signal becomes flesh here. Unspoken 3 turns into static.",
    },
    4: {
        "title": "The Builder",
        "keywords": "structure · craft · floor · the long work",
        "light": "Turns vision into something you can stand on. Respects time. Loves a clean joint.",
        "shadow": "Armor as architecture. Overwork. Calling rigidity safety.",
        "body": "Bones, lower back, hands that want a tool. Exhaustion that feels like virtue.",
        "work": "Systems, code, houses, schedules. The gift is a floor. The risk is a cage.",
        "bond": "Shows love by building. May miss that the other person needed a door, not another wall.",
        "current": "4 is the grid. Necessary. Deadly if the grid becomes the god. Softness is not the enemy of structure.",
    },
    5: {
        "title": "The Wanderer",
        "keywords": "freedom · change · appetite · oxygen",
        "light": "Keeps life from going stale. Learns by moving. Breaks the loop that was killing you.",
        "shadow": "Escape as identity. Appetite with no altar. Leaving just before the real conversation.",
        "body": "Nervous system, hips, lungs. Needs motion or it turns into panic.",
        "work": "Travel, experiment, translation between worlds. Do not force 5 into a cubicle without a window.",
        "bond": "Will stay if the bond is alive. Will bolt if the bond becomes a museum of who you used to be.",
        "current": "5 is weather. You cannot hold it. You can only decide whether the window is open on purpose.",
    },
    6: {
        "title": "The Keeper",
        "keywords": "care · hearth · harmony · responsibility that actually loves",
        "light": "Makes a place someone can come home to. Beauty as repair. Holds the field.",
        "shadow": "Control through care. Martyr math. Rescuing so you never have to ask to be met.",
        "body": "Heart, womb-space, shoulders that carry other people's bags.",
        "work": "Healing rooms, homes, design, the art of making a space feel like it remembers you.",
        "bond": "Will give the whole house. Must learn that a house with no door for the keeper is a tomb.",
        "current": "6 is the hearth. Fire that warms, or fire that eats the one who tends it. Feed yourself first.",
    },
    7: {
        "title": "The Seeker",
        "keywords": "inner temple · analysis · mystery · the download",
        "light": "Goes under the surface. Trusts the quiet knowing. Studies until the pattern shows its face.",
        "shadow": "Living only in the head. Cynicism as armor. Isolation that calls itself initiation.",
        "body": "Crown, third eye, gut that knows before the mouth does. Sleep that is work.",
        "work": "Research, maps, code-as-oracle, theology, the long read. Do not skip the body.",
        "bond": "Needs a witness who will not mock the temple. Will vanish if you treat the inner world as a hobby.",
        "current": "7 is the well. You can draw from it forever. You cannot live at the bottom.",
    },
    8: {
        "title": "The Steward",
        "keywords": "power · harvest · octave · making it real in the world",
        "light": "Moves resources. Builds systems that survive contact with matter. Owns consequence.",
        "shadow": "Worth measured as output. Control. The throne instead of the work.",
        "body": "Spine, jaw, the place where money and shame sit in the same chair.",
        "work": "Leadership, engines, businesses, the part of the vision that has a bill attached.",
        "bond": "Respect is the love language. Softness can look like danger until it is proven safe.",
        "current": "8 is the octave — same note, more voltage. Power without a heart is just a louder cage.",
    },
    9: {
        "title": "The Completer",
        "keywords": "release · compassion · horizon · the last page",
        "light": "Closes chapters with meaning. Serves the larger story. Can let a thing be finished.",
        "shadow": "Cannot let go. Rescuing. Overflow. Carrying the whole world so you never have to end one life.",
        "body": "Feet, eyes, the ache after a long giving. Tears that are not weakness — they are drainage.",
        "work": "Endings, teaching, art that hands something over, forgiveness as a craft.",
        "bond": "Loves in mythic scale. Must learn that completion is not abandonment.",
        "current": "9 is the horizon. If you refuse the ending you never get the next 1. Release is the assignment.",
    },
    11: {
        "title": "The Illuminator",
        "keywords": "voltage · vision · antenna · the current between worlds",
        "light": "A live wire between quiet knowing and spoken world. Sees the pattern before the room does.",
        "shadow": "Nervous charge with no ground. Self-doubt. Inspiration that never becomes a floor.",
        "body": "Nervous system on high. Lights, sounds, other people's weather. Needs sleep like sacrament.",
        "work": "Channel, design, transmission. Pair the download with a 4 or it burns the house.",
        "bond": "Needs someone who can hold voltage without calling it crazy, and without feeding on it.",
        "current": "11 is not 'more psychic.' It is more current than the body was trained for. Ground or it shorts.",
    },
    22: {
        "title": "The Master Builder",
        "keywords": "architecture · legacy · scale · dream that can be mortared",
        "light": "Takes a vision that should have stayed a poem and gives it walls, code, a city.",
        "shadow": "Crushing blueprint. Unpoured foundation. Building a temple nobody is allowed to live in.",
        "body": "Shoulders, bones, the fatigue of carrying a future that is not built yet.",
        "work": "Large systems. Worlds. Engines that other people can enter.",
        "bond": "Loves by constructing a shared world. Terrified the other person will not stay long enough to finish it.",
        "current": "22 is 11 with a floor. If the floor never gets poured, 22 collapses into anxious 4.",
    },
    33: {
        "title": "The Master Teacher",
        "keywords": "devotion · healing · transmission · love as curriculum",
        "light": "Love practiced until it becomes something another person can learn from.",
        "shadow": "Self-erasure in service. Teaching what you have not yet lived. Savior math.",
        "body": "Heart and throat. Compassion that can drain the adrenals if it has no boundary.",
        "work": "Transmission. Healing rooms. The song that hands someone their own name back.",
        "bond": "Will stay in the fire for someone. Must not confuse being the medicine with being the sacrifice.",
        "current": "33 is 6 raised until it becomes a school. The lesson only lands if the teacher is still a person.",
    },
}

KARMIC_NOTE = {
    13: (
        "13/4 — effort without a shortcut. A past pattern of skipping the craft. "
        "The body wants the easy door. The current wants the long work. "
        "Build anyway. The laziness is not moral — it is an old exit."
    ),
    14: (
        "14/5 — freedom that once cost too much. Appetite asking for a spine. "
        "Motion is still holy. Recklessness is the shadow of the same gift. "
        "Choose the change. Do not let change choose you."
    ),
    16: (
        "16/7 — the tower. Ego structure that cannot hold the next voltage. "
        "Humility is not humiliation. It is the study. "
        "What collapses was never the temple — it was the scaffolding you mistook for God."
    ),
    19: (
        "19/1 — independence that once left bodies behind. "
        "Leadership that must learn to stand alone without making aloneness a weapon. "
        "You can start the fire. You do not have to burn the room to prove you own the match."
    ),
}

ANGEL = {
    "111": "New beginning. Align the thought with the thing you actually want — not the thing that keeps you safe.",
    "1111": "Gateway. The idea that just arrived is not decoration. Act, or it becomes another almost.",
    "222": "Trust the pairing. Do not force the timing. Two currents need a beat before they lock.",
    "333": "Expression supported. Speak it. Make it. The throat is open whether you use it or not.",
    "444": "Foundation and protection. Keep building the floor. The angels here are bricklayers.",
    "555": "Change is the assignment. Loosen the grip. The old shape cannot carry the next current.",
    "666": "Rebalance care and material worry. Come back to center. 6 gone sideways is fear wearing a house.",
    "777": "Study, solitude, inner confirmation. The download is real. Do not ask the crowd to baptize it.",
    "888": "Harvest and power cycle. Steward what arrived. Do not pretend you are still poor in the thing that just landed.",
    "999": "Completion. Let the chapter close. Carrying it past the last page turns compassion into a ghost.",
    "000": "Reset. Unformed potential. Empty on purpose.",
}


def meaning(n: int) -> dict:
    if n in MEANINGS:
        return MEANINGS[n]
    return MEANINGS.get(reduce_number(n, False), MEANINGS[9])


def depth_lines(n: int) -> list[tuple[str, str]]:
    info = meaning(n)
    return [
        ("Current", info.get("current", info["light"])),
        ("Body", info.get("body", "")),
        ("Work", info.get("work", "")),
        ("Bond", info.get("bond", "")),
        ("Shadow", info.get("shadow", "")),
    ]


def angel_read(digit_str: str) -> str | None:
    if not digit_str:
        return None
    if digit_str in ANGEL:
        return f"{digit_str}: {ANGEL[digit_str]}"
    if len(set(digit_str)) == 1 and len(digit_str) >= 2:
        root = int(digit_str[0])
        info = meaning(root)
        return f"Repeater {digit_str} — {info['title']} tone ×{len(digit_str)}. {info['light']}"
    return None


# ---------------------------------------------------------------------------
# Moon (Conway / simple synodic approximation)
# Enough for a widget. Known-new-moon epoch: 2000-01-06 18:14 UTC.
# ---------------------------------------------------------------------------

SYNODIC = 29.530588853
KNOWN_NEW = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)

PHASE_NAMES = [
    (0.03, "New Moon"),
    (0.22, "Waxing Crescent"),
    (0.28, "First Quarter"),
    (0.47, "Waxing Gibbous"),
    (0.53, "Full Moon"),
    (0.72, "Waning Gibbous"),
    (0.78, "Last Quarter"),
    (0.97, "Waning Crescent"),
    (1.01, "New Moon"),
]

PHASE_NUMEROLOGY = {
    "New Moon": "Seed. 1-energy. Begin, don't display.",
    "Waxing Crescent": "Intention takes a body. 3-energy. Name the thing.",
    "First Quarter": "Decision / friction. 4 vs 5. Commit or cut.",
    "Waxing Gibbous": "Refine. 6-energy. Care for what you started.",
    "Full Moon": "Reveal. 9 and 2. Culmination, mirror, release-prep.",
    "Waning Gibbous": "Share the harvest. 8-energy. Teach what ripened.",
    "Last Quarter": "Compost. 7-energy. Study what failed.",
    "Waning Crescent": "Empty the cup. 9 into 1. Rest before the next seed.",
}


def moon_phase(when: datetime | None = None) -> dict:
    when = when or datetime.now(timezone.utc)
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    days = (when - KNOWN_NEW).total_seconds() / 86400.0
    age = days % SYNODIC
    frac = age / SYNODIC
    illum = (1 - math.cos(2 * math.pi * frac)) / 2
    name = "New Moon"
    for thresh, label in PHASE_NAMES:
        if frac <= thresh:
            name = label
            break
    return {
        "age_days": round(age, 2),
        "fraction": frac,
        "illumination": illum,
        "name": name,
        "note": PHASE_NUMEROLOGY[name],
        "when": when,
    }


def moon_svg(frac: float, size: int = 72) -> str:
    """Lit disc with a shadow oval. frac 0=new, 0.5=full."""
    r = size / 2
    cx = cy = r
    if frac <= 0.5:
        t = frac * 2
        offset = r * (1 - t)
        shade_x = cx - offset
    else:
        t = (frac - 0.5) * 2
        offset = r * t
        shade_x = cx + offset
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="m"><circle cx="{cx}" cy="{cy}" r="{r-1}"/></clipPath>
  </defs>
  <circle cx="{cx}" cy="{cy}" r="{r-1}" fill="#e2e8f0" stroke="#c9a227" stroke-width="1"/>
  <circle cx="{cx}" cy="{cy}" r="{r-1}" fill="#f5d76e"/>
  <g clip-path="url(#m)">
    <ellipse cx="{shade_x}" cy="{cy}" rx="{r}" ry="{r}" fill="#050506"/>
  </g>
</svg>'''
