Or deploy from this repo on (https://share.streamlit.io) — it reads `requirements.txt` and launches `app.py`.

## What it does

### Decode
Drop a name, a letter, a date, a verse, a phone number, or junk from your notes. You get:

- **Destiny / Expression** — every letter, the vehicle
- **Soul Urge** — vowels only, the private hunger
- **Personality** — consonants only, the face the room meets
- **Cornerstone** — first letter, how it walks in
- **Capstone** — last letter, how it finishes
- **First vowel** — first private note
- **Hidden passion** — the number that repeats most
- **Intensity 1–9** — what's loud, what's absent
- **Word-by-word** — each token counted separately
- **Letter-by-letter** — every letter with its value, kind, and meaning
- **Shadow lines** under each major number
- **Full current** expanders — six layers per number: Current, Body, Work, Bond, Shadow, Karmic/angel
- **Digit stream** — first 18 digits reduced, with angel omens and karmic warnings
- **Dates & times detected** from the input
- **Earth block** — place, lat/lon, Earth number, Lat number, Lon number, place-name Destiny

### Body chart
- Name + birth date → Destiny, Soul Urge, Personality with depth
- **3-cycle Life Path** (month, day, year reduced separately) — Birthday, Attitude
- **Personal Year / Month / Day** as of any date you pick
- Optional **birth time** → natal hour (midnight = 24 → 6) and HHMM stamp (e.g. 4:27 PM → 1627 → 7), each with depth and karmic flags
- Optional **birth place + coordinates** → Earth profile with hemisphere indicators

### All ciphers
Same specimen through every temple. Disagreement is information.

**Latin:** Pythagorean, Chaldean, English Ordinal, Reverse Ordinal, Reverse Reduction, Agrippa (1531), Sumerian (×6)

**Scripts (auto-detected):** Hebrew Mispar Hechrachi + Mispar Gadol, Greek Isopsephy, Coptic, Aramaic Square + Syriac, Arabic Abjad, Sanskrit Katapayadi, Russian Cyrillic, Ukrainian Cyrillic, Georgian Mkhedruli, Armenian

Each shows raw → reduced, reduction steps, blurb, and a full-current expander.

### Language lens
Pick a script from the sidebar and Latin input gets **transliterated** into that script before counting — so `Erin` + Russian actually runs the Cyrillic cipher. Converted line shown under the seal.

### Moon
- Synodic phase for today or any date (SVG diagram, name, illumination %, age in cycle)
- Numerology tie-in: new moon likes 1-work, full moon likes 9-work
- Sidebar shows current moon; Moon tab lets you pick any date

### Compare
Two names, two birth dates, side by side — Life Path, Destiny, Soul Urge, Personality, with notes on sameness or root equivalence.

### Lookups (optional)
- **Numbers API** — trivia for the reduced value (and raw if different)
- **Bible API** — detects `Book chapter:verse` (e.g. `John 1:1`), pulls text + translation, runs Pythagorean on the verse body
- Toggle in the sidebar. No API keys.

### Save
- **Save reading as file** → `.md` with the full report (seal, input, name chart, digit stream, dates, birth time, earth, scripts)
- **Save reading as photo** → gold-and-cyan phone-size `.png`

### New reading
Gold button (page + sidebar) clears the box, resets language to Auto, birth place/coords, time toggle, and music — clean specimen, fresh count.

### Grimes — ethereal
Sidebar selector: Off, Genesis, Genesis (audio), So Heavy I Fell Through the Earth, Oblivion, 4ÆM, You'll miss me when I'm not around. Official 4AD YouTube embed, headphones recommended.

### The seal
Every input gets a deterministic glyph-seal from its SHA-256 — same text, same seal. Shown under the title.

## The rules

- **Y** is a vowel only when its name-token has no A/E/I/O/U
- Masters **11, 22, 33** are kept; everything else reduces to 1–9
- Karmic debts **13 / 14 / 16 / 19** are flagged, not reduced away
- Counting is local. APIs only decorate.

## The files

| File | Role |
|---|---|
| `app.py` | Streamlit UI — lenses, tabs, music, save, reset |
| `engine.py` | All the math: reduction, ciphers, name chart, life path, moon, meanings, depth layers |
| `requirements.txt` | `streamlit`, `requests`, `pillow` |