# numberin
# NUMBERIN

Local Pythagorean / Chaldean / multi-script numerology playground with a moon widget.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Files

- `engine.py` — reduction, ciphers, name chart, life path, moon phase
- `app.py` — Streamlit UI

## What it does

- Decode a letter or a name (Pythagorean chips, Destiny / Soul Urge / Personality)
- Body chart: 3-cycle Life Path (masters 11/22/33 kept), Birthday, Attitude, Personal Year / Month / Day
- All ciphers: Pythagorean, Chaldean, Ordinal, Reverse, Agrippa, Sumerian
- Auto-detect Hebrew, Greek, Arabic abjad, Katapayadi, Cyrillic
- Moon widget + moon tab
- Two-person compare
- Optional numbersapi.com + bible-api.com lookups (no keys)

Y is a vowel only when that name-token has no A/E/I/O/U.
Karmic debts 13 / 14 / 16 / 19 are flagged in reduction trails.
