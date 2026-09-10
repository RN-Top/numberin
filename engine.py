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

# Arabic abjad (Eastern / Hebrew-aligned common table)
ABJAD = {
    "ا": 1, "أ": 1, "إ": 1, "آ": 1, "ء": 1, "ب": 2, "ج": 3, "د": 4, "ه": 5, "ة": 5,
    "و": 6, "ز": 7, "ح": 8, "ط": 9, "ي": 10, "ى": 10, "ك": 20, "ل": 30, "م": 40,
    "ن": 50, "س": 60, "ع": 70, "ف": 80, "ص": 90, "ق": 100, "ر": 200, "ش": 300,
    "ت": 400, "ث": 500, "خ": 600, "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000,
}

# Katapayadi (simplified: common Devanagari consonants → 1–9, 0)
# Vowels ignored in classic katapayadi; we still count them as 0 so traces show.
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

CYRILLIC_ORD = {
    ch: i + 1
    for i, ch in enumerate("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
}


def _sum_table(text: str, table: dict, name: str) -> dict | None:
    pairs = [(ch, table[ch]) for ch in text if ch in table]
    if not pairs:
        return None
    raw = sum(v for _, v in pairs)
    red, steps = reduce_trace(raw)
    return {"name": name, "pairs": pairs, "raw": raw, "reduced": red, "steps": steps}


def script_readings(text: str) -> list[dict]:
    out = []
    for name, table in (
        ("Hebrew Mispar Hechrachi", HEBREW_STD),
        ("Hebrew Mispar Gadol", HEBREW_GADOL),
        ("Greek Isopsephy", GREEK_ISO),
        ("Arabic Abjad", ABJAD),
        ("Sanskrit Katapayadi", KATAPAYADI),
        ("Cyrillic Ordinal", CYRILLIC_ORD),
    ):
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
# Meanings (traditional Western short-form)
# ---------------------------------------------------------------------------

MEANINGS = {
    0: {"title": "The Void", "keywords": "unformed · potential",
        "light": "Before the count.", "shadow": "Dissociation as mysticism."},
    1: {"title": "The Pioneer", "keywords": "will · independence · origin",
        "light": "Starts. Owns the first step. Original will.",
        "shadow": "Isolation, impatience, needing to be first."},
    2: {"title": "The Diplomat", "keywords": "partnership · attunement · polarity",
        "light": "Bridges. Hears the room. Makes two into a chord.",
        "shadow": "People-pleasing, freeze in conflict."},
    3: {"title": "The Voice", "keywords": "expression · play · trinity",
        "light": "Makes inner weather visible. Words, color, laugh.",
        "shadow": "Scattered sparkle, unfinished songs."},
    4: {"title": "The Builder", "keywords": "structure · craft · earth",
        "light": "Turns vision into a floor you can stand on.",
        "shadow": "Rigidity, overwork, fear of change."},
    5: {"title": "The Wanderer", "keywords": "freedom · change · curiosity",
        "light": "Keeps life oxygenated. Learns by moving.",
        "shadow": "Restlessness, escape as identity."},
    6: {"title": "The Keeper", "keywords": "care · harmony · responsibility",
        "light": "Makes a hearth. Beauty as repair.",
        "shadow": "Overgiving, controlling through care."},
    7: {"title": "The Seeker", "keywords": "analysis · mystery · inner temple",
        "light": "Goes under the surface. Trusts the quiet download.",
        "shadow": "Isolation, cynicism, living only in the head."},
    8: {"title": "The Steward", "keywords": "power · manifestation · octave",
        "light": "Moves resources. Builds systems that last in the world.",
        "shadow": "Control, worth measured as output."},
    9: {"title": "The Completer", "keywords": "compassion · release · horizon",
        "light": "Closes chapters with meaning. Serves the larger story.",
        "shadow": "Cannot let go, rescuing, overflow."},
    11: {"title": "The Illuminator", "keywords": "intuition · voltage · vision",
         "light": "Channel between quiet knowing and spoken world.",
         "shadow": "Nervous charge, self-doubt, ungrounded inspiration."},
    22: {"title": "The Master Builder", "keywords": "architecture · legacy · scale",
         "light": "Dreams that can actually be mortared.",
         "shadow": "Crushing blueprint, unpoured foundation."},
    33: {"title": "The Master Teacher", "keywords": "devotion · healing · transmission",
         "light": "Love practiced until it becomes curriculum.",
         "shadow": "Self-erasure in service."},
}

KARMIC_NOTE = {
    13: "13/4 — effort without shortcut. Laziness in a past pattern asking for craft.",
    14: "14/5 — freedom misused. Appetite asking for discipline inside motion.",
    16: "16/7 — tower / ego collapse. Humility as the real study.",
    19: "19/1 — independence abused. Leadership that must learn to stand alone cleanly.",
}

ANGEL = {
    "111": "New beginning, align thought with the thing you actually want.",
    "1111": "Gateway / alignment flash. Act on the idea that just arrived.",
    "222": "Trust the pairing. Do not force the timing.",
    "333": "Expression supported. Speak, make, teach.",
    "444": "Foundation / protection. Keep building the floor.",
    "555": "Change is the assignment. Loosen the grip.",
    "666": "Rebalance care and material worry. Come back to center.",
    "777": "Study, solitude, inner confirmation.",
    "888": "Harvest / power cycle. Steward what arrived.",
    "999": "Completion. Let the chapter close.",
    "000": "Reset. Unformed potential.",
}


def meaning(n: int) -> dict:
    if n in MEANINGS:
        return MEANINGS[n]
    return MEANINGS.get(reduce_number(n, False), MEANINGS[9])


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
    frac = age / SYNODIC  # 0 = new, 0.5 = full
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
    # shadow offset: from full cover (new) through none (full) to other side
    if frac <= 0.5:
        # waxing: shadow on the left, shrinking
        t = frac * 2  # 0..1
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
  <circle cx="{cx}" cy="{cy}" r="{r-1}" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
  <circle cx="{cx}" cy="{cy}" r="{r-1}" fill="#f8fafc"/>
  <g clip-path="url(#m)">
    <ellipse cx="{shade_x}" cy="{cy}" rx="{r}" ry="{r}" fill="#0f172a"/>
  </g>
</svg>'''
