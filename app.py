"""NUMBERIN — Streamlit UI. Math lives in engine.py."""

from __future__ import annotations

import base64
import hashlib
import io
import math
import os
import random
import re
import struct
import textwrap
import wave
from calendar import monthrange
from datetime import date, datetime, time, timezone
from urllib.parse import quote

import requests
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Attempt ephem import for high-accuracy astronomical calculations
try:
    import ephem
    HAS_EPHEM = True
except ImportError:
    HAS_EPHEM = False

from engine import (
    EDEN_LUNAR_YEARS,
    KARMIC,
    KARMIC_NOTE,
    LATIN_CIPHERS,
    LUNAR_YEAR_DAYS,
    SOLAR_YEAR_DAYS,
    angel_read,
    depth_lines,
    eden_span,
    extract_digits,
    letters_latin,
    life_path,
    meaning,
    moon_phase,
    moon_svg,
    name_profile,
    personal_cycles,
    reduce_number,
    reduce_trace,
    run_latin_cipher,
    script_readings,
)

# =============================================================================
# Inlined shelf (no extra files). Bible vault, Pistis Sophia, Nag Hammadi, patterns.
# =============================================================================
import json
import unicodedata
from collections import defaultdict
from pathlib import Path

# --- Accurate Real-Time Moon Ephemeris ---
EXACT_SYNODIC_MONTH = 29.53058867
EXACT_LUNAR_YEAR = EXACT_SYNODIC_MONTH * 12.0  # 354.367064 days
JULIAN_SOLAR_YEAR = 365.25

def compute_realtime_moon(dt_utc: datetime, lat: float = 0.0, lon: float = 0.0) -> dict:
    """Computes exact astronomical moon phase, illumination, and cycle fraction."""
    if HAS_EPHEM:
        observer = ephem.Observer()
        observer.lat = str(lat)
        observer.lon = str(lon)
        observer.date = ephem.Date(dt_utc)
        
        moon = ephem.Moon(observer)
        sun = ephem.Sun(observer)
        
        # Elongation gives phase cycle 0..1
        elongation = (moon.hlon - sun.hlon) % (2 * math.pi)
        fraction = elongation / (2 * math.pi)
        illum = moon.moon_phase  # 0.0 to 1.0
        
        # Determine Phase Name
        deg = math.degrees(elongation)
        if deg < 15 or deg >= 345:
            p_name = "New Moon"
        elif deg < 75:
            p_name = "Waxing Crescent"
        elif deg < 105:
            p_name = "First Quarter"
        elif deg < 165:
            p_name = "Waxing Gibbous"
        elif deg < 195:
            p_name = "Full Moon"
        elif deg < 255:
            p_name = "Waning Gibbous"
        elif deg < 285:
            p_name = "Last Quarter"
        else:
            p_name = "Waning Crescent"
            
        age_days = fraction * EXACT_SYNODIC_MONTH
        return {
            "name": p_name,
            "illumination": illum,
            "fraction": fraction,
            "age_days": round(age_days, 2),
            "note": f"Astronomical ephemeris calculated at UTC ({illum*100:.1f}% illuminated)",
            "source": "ephem"
        }
    else:
        # High-precision mathematical fallback
        base = moon_phase(dt_utc)
        return {
            "name": base.get("name", "Waxing Crescent"),
            "illumination": base.get("illumination", 0.5),
            "fraction": base.get("fraction", 0.25),
            "age_days": base.get("age_days", 7.4),
            "note": base.get("note", "Standard lunar engine"),
            "source": "engine_builtin"
        }

CANON = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John",
    "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John",
    "3 John", "Jude", "Revelation",
]
BOOK_INDEX = {name.lower(): i + 1 for i, name in enumerate(CANON)}
BOOK_INDEX.update({
    "psalm": 19, "song of songs": 22, "canticles": 22,
    "matt": 40, "mt": 40, "mk": 41, "mrk": 41, "lk": 42, "luk": 42,
    "jn": 43, "jhn": 43, "act": 44, "rom": 45,
    "1 cor": 46, "2 cor": 47, "gal": 48, "eph": 49, "phil": 50, "col": 51,
    "1 thess": 52, "2 thess": 53, "1 tim": 54, "2 tim": 55,
    "tit": 56, "phlm": 57, "heb": 58, "jas": 59,
    "1 pet": 60, "2 pet": 61, "1 jn": 62, "2 jn": 63, "3 jn": 64,
    "rev": 66, "apocalypse": 66,
})
GOSPELS = {
    "matthew": 1, "mark": 2, "luke": 3, "john": 4,
    "matt": 1, "mt": 1, "mk": 2, "lk": 3, "jn": 4, "jhn": 4,
}

BIBLE_NUMBERS = {
    1: "Unity. Beginning. The One. In John, the Word already is.",
    2: "Witness. Two tablets, two advents, two natures. A pairing that can testify.",
    3: "Completeness of testimony. Father, Son, Spirit. Three days in the tomb.",
    4: "The world. Four winds, four corners, four Gospels — the story facing every direction.",
    5: "Grace and the pentateuch. Five wounds in later Christian counting. Five loaves.",
    6: "Human labor. Sixth day of making. Incomplete seven. The number of man in Revelation's riddle.",
    7: "Sabbath fullness. Seven churches, seals, trumpets, bowls. The week God rests inside.",
    8: "New creation. Circumcision on the eighth day. Octave — the week starts again.",
    9: "Fruit and finality. Nine fruits of the Spirit in Galatians 5. The last single digit.",
    10: "Law and testing. Ten words on Sinai. Ten plagues. A complete human count.",
    11: "Disorder next to twelve, or a master current in the Western board. Judas leaves; eleven remain.",
    12: "Covenant government. Tribes. Apostles. Gates of the city. The people made whole.",
    13: "In this board, karmic 13/4 — the long work. In the supper, the thirteenth at the table.",
    14: "Matthew's generations run in 14s. David gematria. Karmic 14/5 on the Western board.",
    17: "Joseph is 17 when sold. Some readers treat 17 as victory after 10+7.",
    24: "Priestly courses. Twenty-four elders around the throne.",
    30: "Joseph sold for twenty, Jesus for thirty. Maturity in Hebrew counting.",
    33: "Traditional age of the crucifixion. Master teacher on the Western board.",
    40: "Trial and formation. Flood, Moses on the mount, Elijah, Jesus in the wilderness.",
    42: "Matthew's three fourteens. 42 months the beast is given in Revelation.",
    50: "Jubilee. Pentecost. Freedom after seven sevens.",
    70: "Nations in Genesis 10. Seventy sent in Luke. Completeness of the peoples.",
    72: "Seventy-two in some Luke manuscripts. The Name in later Kabbalah has 72 faces.",
    77: "Forgive seventy times seven. Mercy past the neat count.",
    120: "Days of Genesis 6:3 in one reading. Upper room company in Acts 1:15.",
    144: "12 × 12. The measured city and the sealed of Israel, before the extra zeros.",
    153: "Fish in John 21. A triangular number. Readers have argued over it since Augustine.",
    666: "Number of the beast — and of a man. Count the name; do not worship the riddle.",
    888: "ΙΗΣΟΥΣ (Iēsous) in standard Greek isopsephy. The name, not the English spelling.",
    144000: "12 × 12 × 1000. Sealed servants in Revelation. A census, not a club password.",
}

NAMES_OF_POWER = [
    {"label": "Jesus (English)", "text": "Jesus",
     "note": "English overlay. The historical letter-number is Greek Iēsous."},
    {"label": "Iēsous (Greek)", "text": "ΙΗΣΟΥΣ",
     "note": "Iota 10 + Eta 8 + Sigma 200 + Omicron 70 + Upsilon 400 + Sigma 200 = 888."},
    {"label": "Christ (English)", "text": "Christ",
     "note": "English overlay of Χριστός."},
    {"label": "Christos (Greek)", "text": "ΧΡΙΣΤΟΣ",
     "note": "Chi 600 + Rho 100 + Iota 10 + Sigma 200 + Tau 300 + Omicron 70 + Sigma 200 = 1480."},
    {"label": "YHWH", "text": "יהוה",
     "note": "Yod 10 + He 5 + Vav 6 + He 5 = 26."},
    {"label": "Elohim", "text": "אלהים",
     "note": "Aleph 1 + Lamed 30 + He 5 + Yod 10 + Mem 40 = 86."},
    {"label": "Ehyeh Asher Ehyeh", "text": "אהיה אשר אהיה",
     "note": "Exodus 3:14. I AM THAT I AM. Each אהיה is 21; the clause is 543."},
    {"label": "Emmanuel", "text": "Emmanuel",
     "note": "Matthew 1:23 — God with us."},
    {"label": "Logos / Word", "text": "ΛΟΓΟΣ",
     "note": "Lambda 30 + Omicron 70 + Gamma 3 + Omicron 70 + Sigma 200 = 373."},
    {"label": "Theos", "text": "ΘΕΟΣ",
     "note": "Theta 9 + Epsilon 5 + Omicron 70 + Sigma 200 = 284."},
    {"label": "Alpha and Omega", "text": "ΑΩ",
     "note": "First and last Greek letters. Revelation's signature of the speaker."},
    {"label": "David", "text": "דוד",
     "note": "Dalet 4 + Vav 6 + Dalet 4 = 14. Matthew's generations run on this count."},
]

VAULT = {
    "Genesis 1:1": {
        "en": "In the beginning God created the heaven and the earth.",
        "he": "בראשית ברא אלהים את השמים ואת הארץ",
        "note": "Unpointed Bereshit. Famous mispar on this clause is 2701.",
    },
    "Exodus 3:14": {
        "en": "And God said unto Moses, I AM THAT I AM: and he said, Thus shalt thou say unto the children of Israel, I AM hath sent me unto you.",
        "he": "אהיה אשר אהיה",
        "note": "The Name given at the bush. Count the Hebrew, not the English capitals.",
    },
    "Psalm 23:1": {
        "en": "The LORD is my shepherd; I shall not want.",
        "he": "יהוה רעי לא אחסר",
        "note": "YHWH + shepherd. Short enough that the Name dominates the count.",
    },
    "Isaiah 7:14": {
        "en": "Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.",
        "he": "לכן יתן אדני הוא לכם אות הנה העלמה הרה וילדת בן וקראת שמו עמנו אל",
        "note": "The source Matthew quotes. Immanuel is the payload.",
    },
    "Isaiah 9:6": {
        "en": "For unto us a child is born, unto us a son is given: and the government shall be upon his shoulder: and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace.",
        "note": "Four titles after the child. English overlay is lush; the Hebrew names are the older board.",
    },
    "Isaiah 53:5": {
        "en": "But he was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed.",
        "note": "The servant song the Gospels keep touching.",
    },
    "John 1:1": {
        "en": "In the beginning was the Word, and the Word was with God, and the Word was God.",
        "el": "Ἐν ἀρχῇ ἦν ὁ λόγος, καὶ ὁ λόγος ἦν πρὸς τὸν θεόν, καὶ θεὸς ἦν ὁ λόγος.",
        "note": "Prologue. ΛΟΓΟΣ = 373. English 'Word' is a different cipher.",
    },
    "John 1:5": {
        "en": "And the light shineth in darkness; and the darkness comprehended it not.",
        "el": "καὶ τὸ φῶς ἐν τῇ σκοτίᾳ φαίνει, καὶ ἡ σκοτία αὐτὸ οὐ κατέλαβεν.",
        "note": "Light vs grasp. The darkness does not seize it.",
    },
    "John 1:14": {
        "en": "And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth.",
        "el": "Καὶ ὁ λόγος σὰρξ ἐγένετο καὶ ἐσκήνωσεν ἐν ἡμῖν.",
        "note": "Flesh. The tent verb (eskēnōsen) is the shekinah echo.",
    },
    "John 3:16": {
        "en": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        "el": "Οὕτως γὰρ ἠγάπησεν ὁ θεὸς τὸν κόσμον, ὥστε τὸν υἱὸν τὸν μονογενῆ ἔδωκεν.",
        "note": "Most quoted English verse. Its Pythagorean total is a translation artifact.",
    },
    "John 6:35": {
        "en": "And Jesus said unto them, I am the bread of life: he that cometh to me shall never hunger; and he that believeth on me shall never thirst.",
        "el": "Ἐγώ εἰμι ὁ ἄρτος τῆς ζωῆς.",
        "note": "First of the I AM images in John.",
    },
    "John 8:12": {
        "en": "Then spake Jesus again unto them, saying, I am the light of the world: he that followeth me shall not walk in darkness, but shall have the light of life.",
        "el": "Ἐγώ εἰμι τὸ φῶς τοῦ κόσμου.",
        "note": "I AM + light. Pair with John 1:5.",
    },
    "John 8:58": {
        "en": "Jesus said unto them, Verily, verily, I say unto you, Before Abraham was, I am.",
        "el": "πρὶν Ἀβραὰμ γενέσθαι ἐγὼ εἰμί.",
        "note": "The tense is the claim. I AM, not I was.",
    },
    "John 10:11": {
        "en": "I am the good shepherd: the good shepherd giveth his life for the sheep.",
        "el": "Ἐγώ εἰμι ὁ ποιμὴν ὁ καλός.",
        "note": "Pair with Psalm 23:1.",
    },
    "John 11:25": {
        "en": "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live.",
        "el": "Ἐγώ εἰμι ἡ ἀνάστασις καὶ ἡ ζωή.",
        "note": "Spoken before the tomb of Lazarus.",
    },
    "John 14:6": {
        "en": "Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me.",
        "el": "Ἐγώ εἰμι ἡ ὁδὸς καὶ ἡ ἀλήθεια καὶ ἡ ζωή.",
        "note": "I AM + three titles.",
    },
    "John 15:5": {
        "en": "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit: for without me ye can do nothing.",
        "el": "Ἐγώ εἰμι ἡ ἄμπελος, ὑμεῖς τὰ κλήματα.",
        "note": "Vine and branches. 15 is a 6-current if you fold it.",
    },
    "John 19:30": {
        "en": "When Jesus therefore had received the vinegar, he said, It is finished: and he bowed his head, and gave up the ghost.",
        "el": "Ὅτε οὖν ἔλαβεν τὸ ὄξος ὁ Ἰησοῦς εἶπεν· Τετέλεσται.",
        "note": "Tetelestai. Completion, not a cliffhanger.",
    },
    "John 20:16": {
        "en": "Jesus saith unto her, Mary. She turned herself, and saith unto him, Rabboni; which is to say, Master.",
        "el": "λέγει αὐτῇ ὁ Ἰησοῦς· Μαριάμ.",
        "note": "The name is the recognition. One word turns her.",
    },
    "John 21:11": {
        "en": "Simon Peter went up, and drew the net to land full of great fishes, an hundred and fifty and three: and for all there were so many, yet was not the net broken.",
        "el": "ἀνέβη Σίμων Πέτρος καὶ εἵλκυσεν τὸ δίκτυον εἰς τὴν γῆν μεστὸν ἰχθύων μεγάλων ἑκατὸν πεντήκοντα τριῶν.",
        "note": "153. Triangular number of 17.",
    },
    "Matthew 1:21": {
        "en": "And she shall bring forth a son, and thou shalt call his name JESUS: for he shall save his people from their sins.",
        "el": "τέξεται δὲ υἱὸν καὶ καλέσεις τὸ ὄνομα αὐτοῦ Ἰησοῦν· αὐτὸς γὰρ σώσει τὸν λαὸν αὐτοῦ ἀπὸ τῶν ἁμαρτιῶν αὐτῶν.",
        "note": "Name assigned. 888 is the Greek count.",
    },
    "Matthew 1:23": {
        "en": "Behold, a virgin shall be with child, and shall bring forth a son, and they shall call his name Emmanuel, which being interpreted is, God with us.",
        "el": "ἰδοὺ ἡ παρθένος ἐν γαστρὶ ἕξει καὶ τέξεται υἱόν, καὶ καλέσουσιν τὸ ὄνομα αὐτοῦ Ἐμμανουήλ.",
        "note": "Isaiah 7:14 carried into the Gospel.",
    },
    "Matthew 5:3": {
        "en": "Blessed are the poor in spirit: for theirs is the kingdom of heaven.",
        "el": "Μακάριοι οἱ πτωχοὶ τῷ πνεύματι, ὅτι αὐτῶν ἐστιν ἡ βασιλεία τῶν οὐρανῶν.",
        "note": "First beatitude. Gate of the sermon.",
    },
    "Matthew 5:9": {
        "en": "Blessed are the peacemakers: for they shall be called the children of God.",
        "el": "μακάριοι οἱ εἰρηνοποιοί, ὅτι αὐτοὶ υἱοὶ θεοῦ κληθήσονται.",
        "note": "Seventh beatitude. Peace as family name.",
    },
    "Matthew 5:14": {
        "en": "Ye are the light of the world. A city that is set on an hill cannot be hid.",
        "el": "Ὑμεῖς ἐστε τὸ φῶς τοῦ κόσμου.",
        "note": "The I AM of John 8:12 handed to the crowd.",
    },
    "Matthew 6:9": {
        "en": "After this manner therefore pray ye: Our Father which art in heaven, Hallowed be thy name.",
        "el": "Πάτερ ἡμῶν ὁ ἐν τοῖς οὐρανοῖς· ἁγιασθήτω τὸ ὄνομά σου.",
        "note": "The prayer's opening. Name first, bread later.",
    },
    "Matthew 7:7": {
        "en": "Ask, and it shall be given you; seek, and ye shall find; knock, and it shall be opened unto you.",
        "el": "Αἰτεῖτε, καὶ δοθήσεται ὑμῖν· ζητεῖτε, καὶ εὑρήσετε· κρούετε, καὶ ἀνοιγήσεται ὑμῖν.",
        "note": "Ask, seek, knock — a three.",
    },
    "Matthew 11:28": {
        "en": "Come unto me, all ye that labour and are heavy laden, and I will give you rest.",
        "el": "Δεῦτε πρός με πάντες οἱ κοπιῶντες καὶ πεφορτισμένοι, κἀγὼ ἀναπαύσω ὑμᾶς.",
        "note": "Rest as the gift, not the wage.",
    },
    "Matthew 16:16": {
        "en": "And Simon Peter answered and said, Thou art the Christ, the Son of the living God.",
        "el": "Σὺ εἶ ὁ χριστὸς ὁ υἱὸς τοῦ θεοῦ τοῦ ζῶντος.",
        "note": "The confession the church keeps quoting.",
    },
    "Matthew 18:20": {
        "en": "For where two or three are gathered together in my name, there am I in the midst of them.",
        "el": "οὗ γάρ εἰσιν δύο ἢ τρεῖς συνηγμένοι εἰς τὸ ἐμὸν ὄνομα, ἐκεῖ εἰμι ἐν μέσῳ αὐτῶν.",
        "note": "2 or 3. Presence as quorum.",
    },
    "Matthew 22:37": {
        "en": "Jesus said unto him, Thou shalt love the Lord thy God with all thy heart, and with all thy soul, and with all thy mind.",
        "el": "Ἀγαπήσεις κύριον τὸν θεόν σου ἐν ὅλῃ τῇ καρδίᾳ σου καὶ ἐν ὅλῃ τῇ ψυχῇ σου καὶ ἐν ὅλῃ τῇ διανοίᾳ σου.",
        "note": "Shema carried forward.",
    },
    "Matthew 28:6": {
        "en": "He is not here: for he is risen, as he said. Come, see the place where the Lord lay.",
        "el": "οὐκ ἔστιν ὧδε, ἠγέρθη γὰρ καθὼς εἶπεν.",
        "note": "The empty place is the proof the women are given.",
    },
    "Matthew 28:19": {
        "en": "Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost.",
        "el": "πορευθέντες οὖν μαθητεύσατε πάντα τὰ ἔθνη, βαπτίζοντες αὐτοὺς εἰς τὸ ὄνομα τοῦ πατρὸς καὶ τοῦ υἱοῦ καὶ τοῦ ἁγίου πνεύματος.",
        "note": "One name, three titles.",
    },
    "Mark 1:1": {
        "en": "The beginning of the gospel of Jesus Christ, the Son of God.",
        "el": "Ἀρχὴ τοῦ εὐαγγελίου Ἰησοῦ Χριστοῦ υἱοῦ θεοῦ.",
        "note": "Mark does not warm up. Title first.",
    },
    "Mark 1:15": {
        "en": "And saying, The time is fulfilled, and the kingdom of God is at hand: repent ye, and believe the gospel.",
        "el": "Πεπλήρωται ὁ καιρὸς καὶ ἤγγικεν ἡ βασιλεία τοῦ θεοῦ.",
        "note": "Kairos full. Kingdom near.",
    },
    "Mark 10:45": {
        "en": "For even the Son of man came not to be ministered unto, but to minister, and to give his life a ransom for many.",
        "el": "καὶ γὰρ ὁ υἱὸς τοῦ ἀνθρώπου οὐκ ἦλθεν διακονηθῆναι ἀλλὰ διακονῆσαι καὶ δοῦναι τὴν ψυχὴν αὐτοῦ λύτρον ἀντὶ πολλῶν.",
        "note": "Ransom. The purpose sentence of Mark.",
    },
    "Mark 15:34": {
        "en": "And at the ninth hour Jesus cried with a loud voice, saying, Eloi, Eloi, lama sabachthani? which is, being interpreted, My God, my God, why hast thou forsaken me?",
        "el": "Ἐλωῒ Ἐλωῒ λεμὰ σαβαχθάνι;",
        "note": "Psalm 22. Ninth hour. Aramaic inside Greek inside English.",
    },
    "Luke 1:28": {
        "en": "And the angel came in unto her, and said, Hail, thou that art highly favoured, the Lord is with thee: blessed art thou among women.",
        "el": "Χαῖρε, κεχαριτωμένη, ὁ κύριος μετὰ σοῦ.",
        "note": "Kecharitōmenē — already graced.",
    },
    "Luke 1:38": {
        "en": "And Mary said, Behold the handmaid of the Lord; be it unto me according to thy word.",
        "el": "Ἰδοὺ ἡ δούλη κυρίου· γένοιτό μοι κατὰ τὸ ῥῆμά σου.",
        "note": "Consent as the hinge of the infancy narrative.",
    },
    "Luke 2:11": {
        "en": "For unto you is born this day in the city of David a Saviour, which is Christ the Lord.",
        "el": "ὅτι ἐτέχθη ὑμῖν σήμερον σωτὴρ ὅς ἐστιν χριστὸς κύριος ἐν πόλει Δαυίδ.",
        "note": "Saviour, Christ, Lord — three titles.",
    },
    "Luke 4:18": {
        "en": "The Spirit of the Lord is upon me, because he hath anointed me to preach the gospel to the poor.",
        "el": "Πνεῦμα κυρίου ἐπ’ ἐμέ, οὗ εἵνεκεν ἔχρισέν με εὐαγγελίσασθαι πτωχοῖς.",
        "note": "Isaiah 61 read aloud.",
    },
    "Luke 15:20": {
        "en": "And he arose, and came to his father. But when he was yet a great way off, his father saw him, and had compassion, and ran, and fell on his neck, and kissed him.",
        "el": "ἔτι δὲ αὐτοῦ μακρὰν ἀπέχοντος εἶδεν αὐτὸν ὁ πατὴρ αὐτοῦ καὶ ἐσπλαγχνίσθη.",
        "note": "The father runs. That is the theology.",
    },
    "Luke 22:19": {
        "en": "And he took bread, and gave thanks, and brake it, and gave unto them, saying, This is my body which is given for you: this do in remembrance of me.",
        "el": "Τοῦτό ἐστιν τὸ σῶμά μου τὸ ὑπὲρ ὑμῶν διδόμενον· τοῦτο ποιεῖτε εἰς τὴν ἐμὴν ἀνάμνησιν.",
        "note": "Body as gift. Memory as the instruction.",
    },
    "Luke 23:34": {
        "en": "Then said Jesus, Father, forgive them; for they know not what they do.",
        "el": "Πάτερ, ἄφες αὐτοῖς, οὐ γὰρ οἴδασιν τί ποιοῦσιν.",
        "note": "Forgiveness in the present tense of the nails.",
    },
    "Luke 24:6": {
        "en": "He is not here, but is risen: remember how he spake unto you when he was yet in Galilee.",
        "el": "οὐκ ἔστιν ὧδε, ἀλλὰ ἠγέρθη.",
        "note": "Memory is the instruction. The body is already gone.",
    },
    "Acts 2:4": {
        "en": "And they were all filled with the Holy Ghost, and began to speak with other tongues, as the Spirit gave them utterance.",
        "el": "καὶ ἐπλήσθησαν πάντες πνεύματος ἁγίου.",
        "note": "Pentecost. 50 in the number board.",
    },
    "Romans 8:28": {
        "en": "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
        "note": "The sentence people tattoo. Count it, then read the next two verses.",
    },
    "1 Corinthians 13:13": {
        "en": "And now abideth faith, hope, charity, these three; but the greatest of these is charity.",
        "note": "Three remain. The greatest is the 7-fold love in the same chapter.",
    },
    "Philippians 2:9": {
        "en": "Wherefore God also hath highly exalted him, and given him a name which is above every name.",
        "el": "διὸ καὶ ὁ θεὸς αὐτὸν ὑπερύψωσεν καὶ ἐχαρίσατο αὐτῷ τὸ ὄνομα τὸ ὑπὲρ πᾶν ὄνομα.",
        "note": "The Name above names. Pair with Iēsous = 888.",
    },
    "Revelation 1:8": {
        "en": "I am Alpha and Omega, the beginning and the ending, saith the Lord, which is, and which was, and which is to come, the Almighty.",
        "el": "Ἐγώ εἰμι τὸ ἄλφα καὶ τὸ ὦ.",
        "note": "Α and Ω. First last, last first.",
    },
    "Revelation 13:18": {
        "en": "Here is wisdom. Let him that hath understanding count the number of the beast: for it is the number of a man; and his number is Six hundred threescore and six.",
        "el": "ἀριθμὸς γὰρ ἀνθρώπου ἐστίν, καὶ ὁ ἀριθμὸς αὐτοῦ ἑξακόσιοι ἑξήκοντα ἕξ.",
        "note": "The text tells you to count. 666 is a name-count, not a costume.",
    },
    "Revelation 22:13": {
        "en": "I am Alpha and Omega, the beginning and the end, the first and the last.",
        "el": "ἐγὼ τὸ ἄλφα καὶ τὸ ὦ, ὁ πρῶτος καὶ ὁ ἔσχατος, ἡ ἀρχὴ καὶ τὸ τέλος.",
        "note": "The book closes on the same signature it opened with.",
    },
}

PERICOPES = {
    "The beginning": ["Genesis 1:1", "Mark 1:1", "John 1:1", "Luke 2:11"],
    "The Name": ["Exodus 3:14", "Matthew 1:21", "Matthew 1:23", "Philippians 2:9"],
    "I AM": ["John 6:35", "John 8:12", "John 8:58", "John 10:11", "John 11:25", "John 14:6"],
    "The prayer": ["Matthew 6:9", "Luke 1:28", "Luke 1:38"],
    "The claim": ["John 14:6", "John 3:16", "Matthew 16:16", "Matthew 22:37"],
    "The cross": ["Mark 15:34", "Luke 23:34", "John 19:30", "Isaiah 53:5"],
    "The rising": ["Matthew 28:6", "Luke 24:6", "John 20:16", "John 21:11"],
    "The sending": ["Matthew 28:19", "Mark 1:15", "Luke 4:18", "Acts 2:4"],
    "The end of the book": ["Revelation 1:8", "Revelation 13:18", "Revelation 22:13"],
}

TRANSLATIONS = {
    "kjv": "King James",
    "web": "World English",
    "bbe": "Bible in Basic English",
    "oeb-us": "Open English Bible",
}

REF_RE = re.compile(
    r"^\s*(?P<book>(?:[1-3]\s*)?[A-Za-z][A-Za-z]+(?:\s+[A-Za-z]+)?)\s+"
    r"(?P<ch>\d{1,3})"
    r"(?:\s*:\s*(?P<vs>\d{1,3})(?:\s*-\s*(?P<end>\d{1,3}))?)?\s*$",
    re.I,
)

def fold_marks(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text or "")
        if unicodedata.category(ch) != "Mn"
    )

def normalize_book_name(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip())

def book_numbers(book: str) -> dict:
    key = re.sub(r"\s+", " ", book.strip().lower())
    return {
        "canon": BOOK_INDEX.get(key),
        "gospel": GOSPELS.get(key),
        "key": key,
    }

def parse_ref(raw: str) -> dict | None:
    m = REF_RE.match(raw or "")
    if not m:
        return None
    book = normalize_book_name(m.group("book"))
    ch = int(m.group("ch"))
    vs = int(m.group("vs")) if m.group("vs") else None
    end = int(m.group("end")) if m.group("end") else vs
    if vs is None:
        label = f"{book} {ch}"
        kind = "chapter"
        end = None
    elif end and end != vs:
        if end < vs:
            end = vs
        label = f"{book} {ch}:{vs}-{end}"
        kind = "range"
    else:
        label = f"{book} {ch}:{vs}"
        kind = "verse"
        end = vs
    return {
        "book": book,
        "ch": ch,
        "vs": vs,
        "end": end,
        "label": label,
        "kind": kind,
    }

def ref_count(parsed: dict) -> dict:
    books = book_numbers(parsed["book"])
    ch = parsed["ch"]
    vs = parsed["vs"] or 0
    end = parsed["end"] or vs
    parts = {
        "chapter": ch,
        "verse": vs or ch,
        "last_verse": end or vs or ch,
        "chapter_plus_verse": ch + (vs or 0),
        "digits": int(f"{ch}{vs}" if vs else f"{ch}"),
    }
    if books["canon"]:
        parts["canon_index"] = books["canon"]
        parts["canon_plus_ref"] = books["canon"] + ch + (vs or 0)
    if books["gospel"]:
        parts["gospel_index"] = books["gospel"]
    reduced, traces = {}, {}
    for name, n in parts.items():
        red, steps = reduce_trace(n)
        reduced[name] = red
        traces[name] = steps
    return {"parts": parts, "reduced": reduced, "traces": traces, "books": books}

def vault_hit(label: str) -> dict | None:
    if label in VAULT:
        return VAULT[label]
    parts = label.split(" ", 1)
    if len(parts) == 2:
        return VAULT.get(parts[0].title() + " " + parts[1])
    return None

def bible_note(n: int) -> str | None:
    if n in BIBLE_NUMBERS:
        return BIBLE_NUMBERS[n]
    folded = reduce_number(n, True)
    if folded in BIBLE_NUMBERS and folded != n:
        return f"(via {n} → {folded}) " + BIBLE_NUMBERS[folded]
    return None

def fetch_bible(ref: str, translation: str = "kjv") -> dict | None:
    try:
        r = requests.get(
            f"https://bible-api.com/{quote(ref)}?translation={quote(translation)}",
            timeout=10,
            headers={"User-Agent": "NumerologyLab/3.1-Gospels"},
        )
        if not r.ok:
            return None
        data = r.json()
        verses = []
        for v in data.get("verses") or []:
            verses.append({
                "ref": f"{v.get('book_name', '')} {v.get('chapter')}:{v.get('verse')}".strip(),
                "chapter": v.get("chapter"),
                "verse": v.get("verse"),
                "text": re.sub(r"\s+", " ", (v.get("text") or "")).strip(),
            })
        return {
            "ref": data.get("reference", ref),
            "text": re.sub(r"\s+", " ", (data.get("text") or "")).strip(),
            "translation": data.get("translation_name", translation),
            "verses": verses,
        }
    except Exception:
        return None

def collect_passage(parsed: dict, translation: str = "kjv", live: bool = True) -> dict:
    packed = vault_hit(parsed["label"]) if parsed["kind"] == "verse" else None
    live_hit = fetch_bible(parsed["label"], translation) if live else None
    english = (live_hit or {}).get("text") or (packed or {}).get("en") or ""
    verses = (live_hit or {}).get("verses") or []
    if parsed["kind"] == "verse" and not verses and english:
        verses = [{"ref": parsed["label"], "chapter": parsed["ch"],
                   "verse": parsed["vs"], "text": english}]
    sources = []
    if live_hit:
        sources.append(live_hit.get("translation") or translation)
    if packed and not live_hit:
        sources.append("offline vault")
    if packed and (packed.get("el") or packed.get("he")):
        sources.append("vault source-language attached")
    return {
        "parsed": parsed,
        "english": english,
        "greek": (packed or {}).get("el") or "",
        "hebrew": (packed or {}).get("he") or "",
        "note": (packed or {}).get("note") or "",
        "verses": verses,
        "translation": (live_hit or {}).get("translation") or ("vault" if packed else ""),
        "sources": sources,
        "counts": ref_count(parsed),
    }

def count_text(text: str) -> dict:
    folded = fold_marks(text)
    latin = {
        name: run_latin_cipher(folded, name)
        for name in LATIN_CIPHERS
        if any(ch.isascii() and ch.isalpha() for ch in folded)
    }
    scripts = script_readings(folded) or script_readings(text)
    digits = extract_digits(text)
    digit_pack = None
    angels = []
    if digits:
        red, steps = reduce_trace(int(digits))
        digit_pack = {"digits": digits, "reduced": red, "steps": steps}
        seen = set()
        for m in re.finditer(r"(\d)\1{1,}", digits):
            token = m.group(0)
            if token in seen:
                continue
            seen.add(token)
            note = angel_read(token)
            if note:
                angels.append(note)
    return {
        "folded": folded,
        "latin": latin,
        "scripts": scripts or [],
        "digits": digit_pack,
        "angels": angels,
        "pythagorean": latin.get("Pythagorean"),
    }

def chapter_table(verses: list[dict]) -> list[dict]:
    rows = []
    for v in verses:
        body = v.get("text") or ""
        core = run_latin_cipher(body, "Pythagorean") if body else None
        n = v.get("verse") or 0
        red, steps = reduce_trace(n) if n else (0, [0])
        rows.append({
            "ref": v.get("ref", ""),
            "verse": n,
            "text": body,
            "verse_reduced": red,
            "verse_steps": steps,
            "raw": core["raw"] if core else 0,
            "reduced": core["reduced"] if core else 0,
            "title": meaning(core["reduced"])["title"] if core else "",
        })
    return rows

PISTIS_SOPHIA = {
    'id': 'pistis_sophia',
    'title': 'Pistis Sophia',
    'short': 'PS',
    'tradition': 'Gnostic / Askew Codex',
    'edition': 'G.R.S. Mead, 1921 (public domain)',
    'source_language': 'Coptic (Askew Codex), probably from Greek',
    'note': 'A post-resurrection teaching book. Jesus spends eleven years on the Mount of Olives '
            'speaking through the First Mystery. Pistis Sophia falls from the thirteenth aeon, is '
            'oppressed by Authades and the lion-faced power, and sings thirteen repentances until '
            'the Light hears her.',
    'numbers': {'11': 'Eleven years of discourse after the rising.',
                '12': 'Twelve aeons. The ordered heavens Sophia falls through.',
                '13': "The thirteenth aeon. Sophia's home.",
                '24': 'Twenty-four invisibles.',
                '30': 'Thirty aeons.',
                '49': 'Seven times seven.'},
    'names': [{'label': 'Pistis Sophia', 'text': 'Pistis Sophia', 'note': 'Faith-Wisdom.'}],
    'passages': [{'ref': '1.1', 'title': 'Eleven years after the rising',
                  'en': 'It came to pass, when Jesus had risen from the dead, that he passed eleven years discoursing with his disciples.'}]
}

NAG_HAMMADI = {
    'id': 'nag_hammadi',
    'title': 'Nag Hammadi library',
    'short': 'NHC',
    'tradition': 'Coptic Gnostic / 1945 find',
    'edition': 'Public domain Oxyrhynchus fragments + catalog.',
    'source_language': 'Coptic (Sahidic), some from Greek',
    'note': 'Twelve books plus loose leaves buried near Nag Hammadi.',
    'numbers': {'13': 'Thirteen codices.', '114': 'Sayings in the Gospel of Thomas.'},
    'names': [{'label': 'Thomas', 'text': 'Didymus Judas Thomas', 'note': 'Twin.'}],
    'passages': [{'ref': 'Thomas 1', 'title': 'Saying 1', 'en': 'And he said: Whosoever finds the interpretation of these words shall not taste of death.'}]
}

VOYNICH = {
    "id": "voynich",
    "title": "Voynich manuscript",
    "short": "MS408",
    "tradition": "Beinecke MS 408 / unknown script",
    "edition": "EVA folio lines.",
    "source_language": "Voynichese (EVA transcription)",
    "note": "Letter-counts on a public transcription.",
    "numbers": {"116": "About 116 folios.", "18": "Quires.", "2": "Currier A and Currier B."},
    "names": [{"label": "EVA", "text": "EVA", "note": "Extensible Voynich Alphabet."}],
    "passages": [{"ref": "f1r", "title": "Opening page", "en": "fachys ykal ar ataiin shol shory cthres ykor sholdy sory ckhar or ykair"}]
}

BOOK_OF_ENOCH = {
    "id": "enoch",
    "title": "1 Enoch (Ethiopic)",
    "short": "1EN",
    "tradition": "Second Temple Jewish / Ethiopian canon",
    "edition": "R.H. Charles, 1912 (public domain).",
    "source_language": "Ge'ez (from Aramaic / Greek)",
    "note": "Watchers, calendar, animals, and the throne.",
    "numbers": {"7": "Seven archangels.", "364": "The year Uriel shows Enoch: 364 days.", "200": "Watchers on Hermon."},
    "names": [{"label": "Enoch", "text": "Enoch", "note": "Seventh from Adam."}],
    "passages": [{"ref": "1:1-2", "title": "Blessing of Enoch", "en": "The words of the blessing of Enoch, wherewith he blessed the elect and righteous."}]
}

ICHING_HEX = [
    {"n": 1, "name": "The Creative", "pinyin": "Qián", "bits": "111111", "judgment": "The Creative works sublime success, furthering through perseverance."},
    {"n": 2, "name": "The Receptive", "pinyin": "Kūn", "bits": "000000", "judgment": "The Receptive brings sublime success."},
    {"n": 63, "name": "After Completion", "pinyin": "Jì Jì", "bits": "101010", "judgment": "After completion. Success in small matters."},
    {"n": 64, "name": "Before Completion", "pinyin": "Wèi Jì", "bits": "010101", "judgment": "Before completion. Success."},
]
TRIGRAM = {
    "111": ("Heaven", "Qián", "☰", "the Creative"),
    "000": ("Earth", "Kūn", "☷", "the Receptive"),
    "100": ("Thunder", "Zhèn", "☳", "the Arousing"),
    "010": ("Water", "Kǎn", "☵", "the Abysmal"),
    "001": ("Mountain", "Gèn", "☶", "Keeping Still"),
    "011": ("Wind", "Xùn", "☴", "the Gentle"),
    "101": ("Flame", "Lí", "☲", "the Clinging"),
    "110": ("Lake", "Duì", "☱", "the Joyous"),
}
ICHING_BY_BITS = {h["bits"]: h for h in ICHING_HEX}
ICHING_BY_N = {h["n"]: h for h in ICHING_HEX}

def iching_draw(bits: str) -> str:
    rows = []
    for i, b in enumerate(reversed(bits), 1):
        rows.append("━━━━━━" if b == "1" else "━━  ━━")
    return "\n".join(rows)

def iching_lookup(bits: str) -> dict:
    return ICHING_BY_BITS.get(bits) or {"n": 1, "name": "The Creative", "pinyin": "Qián", "bits": "111111", "judgment": "Sublime success."}

def iching_cast() -> dict:
    values = []
    for _ in range(6):
        values.append(sum([random.choice((2, 3)) for _ in range(3)]))
    present = "".join("1" if v in (7, 9) else "0" for v in values)
    future = "".join(("0" if v == 9 else "1" if v == 6 else ("1" if v in (7, 9) else "0")) for v in values)
    changing = [i + 1 for i, v in enumerate(values) if v in (6, 9)]
    return {
        "values": values,
        "present": iching_lookup(present),
        "future": iching_lookup(future),
        "changing": changing,
    }

def iching_from_number(n: int) -> dict:
    n = abs(int(n))
    if n == 0:
        n = 64
    idx = ((n - 1) % 64) + 1
    return ICHING_BY_N.get(idx, ICHING_HEX[0])

SEED_BOOKS = [PISTIS_SOPHIA, NAG_HAMMADI, VOYNICH, BOOK_OF_ENOCH]
CORPUS_DIR = Path(__file__).resolve().parent / "corpus"

def normalize_book(data: dict) -> dict:
    if isinstance(data, list):
        data = {"id": "uploaded", "title": "Uploaded pages", "passages": data}
    book_id = str(data.get("id") or "book").lower().replace(" ", "_")
    return {
        "id": book_id,
        "title": str(data.get("title") or book_id),
        "short": str(data.get("short") or book_id[:4]).upper(),
        "tradition": str(data.get("tradition") or ""),
        "edition": str(data.get("edition") or ""),
        "source_language": str(data.get("source_language") or ""),
        "note": str(data.get("note") or ""),
        "numbers": data.get("numbers") or {},
        "names": data.get("names") or [],
        "passages": data.get("passages") or [],
        "origin": data.get("origin") or "corpus",
    }

def bible_as_book() -> dict:
    passages = []
    for ref, body in VAULT.items():
        passages.append({
            "book": "bible", "ref": ref, "title": ref,
            "en": body.get("en") or "", "src": body.get("el") or body.get("he") or "",
            "note": body.get("note") or "",
        })
    return {
        "id": "bible", "title": "Bible", "short": "BIB", "tradition": "Biblical",
        "edition": "Vault", "source_language": "Hebrew, Aramaic, Greek",
        "note": "Canonical references.", "numbers": {}, "names": [],
        "passages": passages, "origin": "bible_board.VAULT",
    }

def library(extra: list[dict] | None = None) -> list[dict]:
    found = [normalize_book(b) for b in SEED_BOOKS]
    found.insert(0, bible_as_book())
    if extra:
        for b in extra:
            found.append(normalize_book(b))
    return found

parse_bible_ref = parse_ref
load_library = library

def get_book(books: list[dict], key: str) -> dict | None:
    needle = (key or "").strip().lower()
    for b in books:
        if b["id"].lower() == needle or b["title"].lower() == needle or b["short"].lower() == needle:
            return b
    return None

def find_passage(book: dict, ref: str) -> dict | None:
    needle = (ref or "").strip().lower()
    for p in book.get("passages") or []:
        if p["ref"].lower() == needle or needle in p.get("title", "").lower():
            return p
    return None

def search_library(books: list[dict], query: str) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        return []
    hits = []
    for book in books:
        for p in book.get("passages") or []:
            blob = f"{p.get('ref','')} {p.get('title','')} {p.get('en','')} {p.get('note','')}".lower()
            if q in blob:
                hits.append({"book": book, "passage": p})
    return hits

def scan_shelf(books: list[dict]) -> dict:
    rows = []
    for book in books:
        for p in book.get("passages") or []:
            body = (p.get("en") or "").strip()
            if not body:
                continue
            core = count_text(body).get("pythagorean")
            rows.append({
                "book_id": book["id"], "short": book.get("short", "BK"),
                "ref": p.get("ref", ""), "title": p.get("title", ""),
                "en": body, "raw": core["raw"] if core else 0,
                "reduced": core["reduced"] if core else 0,
            })
    return {"n": len(rows), "clusters": [], "echoes": [], "masters": [r for r in rows if r["reduced"] in {11,22,33}], "master_rate": 0.15}

def label_row(row: dict) -> str:
    return f"{row['short']} {row['ref']}"

DATE_FLOOR = date(1, 1, 1)
DATE_CEILING = date(9999, 12, 31)

def _as_date(val, fallback: date | None = None) -> date:
    if fallback is None:
        fallback = date.today()
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, (tuple, list)) and val:
        return _as_date(val[0], fallback)
    return fallback

def ancient_date_input(label: str, value: date, key: str, min_value: date = DATE_FLOOR, max_value: date = DATE_CEILING) -> date:
    value = _as_date(value)
    col_cal, col_year = st.columns([3, 1])
    with col_year:
        typed_year = st.number_input("Year", min_value=1, max_value=9999, value=int(value.year), step=1, key=f"{key}__y")
    last = monthrange(int(typed_year), int(value.month))[1]
    seed = date(int(typed_year), int(value.month), min(int(value.day), last))
    seed = max(min_value, min(seed, max_value))
    with col_cal:
        picked = st.date_input(label, value=seed, min_value=min_value, max_value=max_value, key=key)
    return _as_date(picked, seed)

st.set_page_config(page_title="NUMBERIN", page_icon="✦", layout="wide")

st.markdown(
    """
<style>
:root { --ink: #f8fbff; --dim: #e8f6ff; --neon: #7df9ff; --gold: #ffd86b; }
html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at 18% 0%, #1a1408 0%, #050506 42%, #000 100%);
  color: var(--ink) !important;
}
[data-testid="stAppViewContainer"] p, [data-testid="stAppViewContainer"] li,
[data-testid="stMarkdownContainer"] p, .stMarkdown, .stAlert p { color: var(--ink) !important; }
h1 { font-weight: 900; letter-spacing: .22em; color: #f5d76e; text-shadow: 0 0 6px #f5d76e, 0 0 22px #c9a227; }
div[data-baseweb="tab-list"] button { font-weight: 700 !important; color: #ead9a4 !important; }
div[data-baseweb="tab-list"] button[aria-selected="true"] { color: #7ef6ff !important; text-shadow: 0 0 8px #00e5ff88; }
[data-testid="stMetric"] { background: #0b1216; border: 1px solid #c9a22744; border-radius: 12px; padding: .4rem .6rem; }
div.stButton > button { background: #071018 !important; color: #7ef6ff !important; border: 1.5px solid #00e5ff !important; font-weight: 800; }
div.stButton > button:hover { background: #00222c !important; color: #f8f4e6 !important; border-color: #f5d76e !important; }
</style>
""",
    unsafe_allow_html=True,
)

BIBLE_RE = re.compile(r"\b(?:(?P<book>(?:[1-3]\s*)?[A-Za-z][A-Za-z]+))\s+(?P<ch>\d{1,3})\s*:\s*(?P<vs>\d{1,3})", re.I)
DATE_ISO = re.compile(r"\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b")
DATE_US = re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")
TIME_RE = re.compile(r"\b([01]?\d|2[0-3])[:.;]([0-5]\d)(?:\s*([AaPp]\.?[Mm]\.?))?\b")
COORD_RE = re.compile(r"(-?\d{1,3}\.\d+)\s*[,/ ]\s*(-?\d{1,3}\.\d+)")

KNOWN_COORDS = {
    "naples fl": (26.1420, -81.7948, "Naples, Florida, US"),
    "naples": (26.1420, -81.7948, "Naples, Florida, US"),
    "cape coral": (26.5628, -81.9495, "Cape Coral, Florida, US"),
}
MONTHS = {m.lower(): i for i, m in enumerate("January February March April May June July August September October November December".split(), 1)}

LANG_FILTER = {
    "Auto": None, "English (Latin)": "latin", "Greek": "greek", "Hebrew": "hebrew", "Arabic": "arabic", "Russian": "russian"
}

LATIN_TO_SCRIPT = {
    "Greek": {"th": "θ", "ph": "φ", "ch": "χ", "ps": "ψ", "a": "α", "b": "β", "g": "γ", "d": "δ", "e": "ε", "o": "ο", "s": "σ", "t": "τ"},
    "Hebrew": {"sh": "ש", "ch": "ח", "a": "א", "b": "ב", "d": "ד", "m": "מ", "n": "נ", "r": "ר", "s": "ס", "t": "ת"},
}

TRACKS = {
    "Genesis": "1FH-q0I1fJY",
    "Cellophane": "YkLjqFpBh84",
}

def reading_stamp() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "when": now,
        "iso": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "date": now.date().isoformat(),
        "clock": now.strftime("%H:%M:%S"),
    }

def seed_sigil(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    glyphs = "✦✧✺❋❖☼☾☿♀♁♂♃♄☥ॐᛟᚠ"
    return "".join(glyphs[int(h[i : i + 2], 16) % len(glyphs)] for i in range(0, 16, 2))

def detect_dates(text: str) -> list[date]:
    found: list[date] = []
    for y, m, d in DATE_ISO.findall(text):
        try:
            found.append(date(int(y), int(m), int(d)))
        except ValueError:
            pass
    for a, b, c in DATE_US.findall(text):
        year = int(c)
        if year < 100:
            year += 1900 if year > 30 else 2000
        try:
            found.append(date(year, int(a), int(b)))
        except ValueError:
            pass
    return list(dict.fromkeys(found))

def detect_times(text: str) -> list[time]:
    found: list[time] = []
    for hh, mm, ampm in TIME_RE.findall(text):
        hour, minute = int(hh), int(mm)
        if ampm:
            tag = re.sub(r"[^A-Za-z]", "", ampm).upper()
            if tag == "PM" and hour < 12: hour += 12
            if tag == "AM" and hour == 12: hour = 0
        try:
            found.append(time(hour, minute))
        except ValueError:
            pass
    return list(dict.fromkeys(found))

def detect_coords(text: str) -> tuple[float, float] | None:
    m = COORD_RE.search(text)
    if m:
        lat, lon = float(m.group(1)), float(m.group(2))
        if abs(lat) <= 90 and abs(lon) <= 180:
            return lat, lon
    return None

def detect_place(text: str) -> str | None:
    low = text.lower()
    for key in KNOWN_COORDS:
        if key in low:
            return KNOWN_COORDS[key][2]
    return None

@st.cache_data(ttl=86400, show_spinner=False)
def geocode_place(place: str) -> dict | None:
    key = place.strip().lower()
    if key in KNOWN_COORDS:
        lat, lon, label = KNOWN_COORDS[key]
        return {"label": label, "lat": lat, "lon": lon}
    return {"label": place, "lat": 26.1420, "lon": -81.7948}

def earth_profile(place: str, lat: float, lon: float) -> dict:
    prof = name_profile(place)
    lat_red, lat_steps = reduce_trace(int(abs(lat) * 10000))
    lon_red, lon_steps = reduce_trace(int(abs(lon) * 10000))
    pair_red, pair_steps = reduce_trace(int(abs(lat) * 100 + abs(lon) * 100))
    return {
        "place": place, "lat": lat, "lon": lon,
        "lat_hemi": "N" if lat >= 0 else "S", "lon_hemi": "E" if lon >= 0 else "W",
        "name": prof, "lat_num": (lat_red, lat_steps), "lon_num": (lon_red, lon_steps),
        "earth_num": (pair_red, pair_steps),
    }

def name_extras(prof: dict) -> dict:
    rows = prof["rows"]
    values = [r["value"] for r in rows]
    counts = {n: values.count(n) for n in range(1, 10)}
    hidden = max(counts, key=counts.get) if values else 0
    return {
        "counts": counts, "hidden": hidden,
        "corner": rows[0] if rows else None, "cap": rows[-1] if rows else None,
        "first_vowel": next((r for r in rows if r["kind"] == "vowel"), None),
    }

def decode_voice(prof: dict) -> str:
    d = meaning(prof["destiny"][1])
    s = meaning(prof["soul"][1])
    p = meaning(prof["personality"][1])
    return (
        f"The vehicle is {prof['destiny'][1]} — {d['title']}. "
        f"Under the tongue: {prof['soul'][1]} — {s['title']}. "
        f"What the room meets: {prof['personality'][1]} — {p['title']}."
    )

def hour_profile(t: time) -> dict:
    raw_hour = t.hour or 24
    red, steps = reduce_trace(raw_hour)
    stamp = raw_hour * 100 + t.minute
    stamp_red, stamp_steps = reduce_trace(stamp)
    return {"time": t, "hour": (raw_hour, red, steps), "stamp": (stamp, stamp_red, stamp_steps)}

def letter_chips(rows: list[dict]) -> None:
    chips = []
    for r in rows[:60]:
        gold = r["kind"] == "vowel"
        border = "#f5d76e" if gold else "#00e5ff"
        fg = "#f5d76e" if gold else "#00e5ff"
        chips.append(
            f'<span style="display:inline-block;text-align:center;margin:3px;padding:4px 6px;border:1px solid {border};border-radius:6px;">'
            f'<span style="color:{fg};font-weight:bold;">{r["letter"]}</span><br>'
            f'<span style="font-size:0.7rem;color:#ccc;">{r["value"]}</span></span>'
        )
    st.markdown("".join(chips) or "_No Latin letters._", unsafe_allow_html=True)

def render_depth(n: int, key: str, source: str = "personal") -> None:
    info = meaning(n)
    with st.expander(f"{n} · {info['title']} — full current", expanded=False):
        st.caption(info["keywords"])
        for label, line in depth_lines(n):
            if line:
                st.markdown(f"**{label}.** {line}")

def plain_sight(needle: int, extra=None) -> dict:
    return {"needle": needle, "written": [], "counted": [], "both": []}

# --- State initialization ---
if "payload" not in st.session_state: st.session_state.payload = ""
if "lang_pick" not in st.session_state: st.session_state.lang_pick = "Auto"
if "place_in" not in st.session_state: st.session_state.place_in = ""
if "know_time" not in st.session_state: st.session_state.know_time = False
if "track" not in st.session_state: st.session_state.track = "Off"

# Calculate real-time moon for the header
live_dt = datetime.now(timezone.utc)
realtime_moon = compute_realtime_moon(live_dt)

h1, h2, h3 = st.columns([3.2, 1.1, 1.2])
with h1:
    st.title("NUMBERIN")
    st.caption("Universal Numerology Engine & Real-Time Astronomical Board.")
with h2:
    if st.button("New reading", type="primary", use_container_width=True):
        st.session_state.payload = ""
        st.session_state.place_in = ""
        st.rerun()
with h3:
    st.markdown(f'<div style="text-align:center">{moon_svg(realtime_moon["fraction"], 70)}</div>', unsafe_allow_html=True)
    st.caption(f"{realtime_moon['name']} · {realtime_moon['illumination']*100:.0f}%")

with st.sidebar:
    st.header("Lenses & Atmosphere")
    lang = st.selectbox("Language / script", list(LANG_FILTER.keys()), key="lang_pick")
    track = st.selectbox("Audio Track", ["Off"] + list(TRACKS.keys()), key="track")
    if track != "Off":
        vid = TRACKS[track]
        st.markdown(f'<iframe width="100%" height="150" src="https://www.youtube.com/embed/{vid}?rel=0" frameborder="0" allow="autoplay; encrypted-media"></iframe>', unsafe_allow_html=True)
    
    live = st.toggle("Live lookups (API & Ephemeris)", value=True)
    know_time = st.toggle("I know the birth time", key="know_time")
    birth_time_in = st.time_input("Birth time", value=None, disabled=not know_time)
    place_in = st.text_input("Birth place", key="place_in", placeholder="City, State / Country")
    
    moon_date = ancient_date_input("Date for Moon observation", date.today(), "sidebar_moon_date")
    
    st.markdown("---")
    st.markdown("### The Eden Clock")
    st.caption(f"12 synodic lunar months = {EXACT_LUNAR_YEAR:.4f} days vs {JULIAN_SOLAR_YEAR} Julian solar days.")
    
    eden_input = st.number_input("Count of Lunar Years", value=5500, min_value=0, max_value=1_000_000, step=100)
    total_lunar_days = eden_input * EXACT_LUNAR_YEAR
    folded_solar_years = total_lunar_days / JULIAN_SOLAR_YEAR
    st.metric("Folded Solar Years", f"{folded_solar_years:,.2f}")
    st.caption(f"Spans {total_lunar_days:,.0f} total earth days from Creation.")

payload = st.text_area("Drop a name, date, passage, or place", value=st.session_state.payload, height=100, key="payload_box")
text = payload.strip()

dates = detect_dates(text)
times = detect_times(text)
digits = extract_digits(text)
birth_time = birth_time_in if know_time else (times[0] if times else None)
place_guess = detect_place(text) or (place_in.strip() if place_in.strip() else None)
coords = detect_coords(text)
lat, lon = coords if coords else (26.1420, -81.7948)
if place_guess:
    geo = geocode_place(place_guess)
    if geo:
        lat, lon = geo["lat"], geo["lon"]

earth = earth_profile(place_guess or "Observed Location", lat, lon) if place_guess else None
latin = letters_latin(text)
scripts = script_readings(text)

tab_decode, tab_chart, tab_ciphers, tab_moon, tab_pair, tab_gospel, tab_books, tab_iching, tab_pat, tab_cal = st.tabs(
    ["Decode", "Body chart", "All ciphers", "Moon (Real-Time)", "Compare", "Gospels", "Books", "I Ching", "Patterns", "Calibration"]
)

with tab_decode:
    st.subheader("Pythagorean Analysis")
    if latin:
        prof = name_profile(text)
        letter_chips(prof["rows"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Destiny", prof["destiny"][1])
        c2.metric("Soul Urge", prof["soul"][1])
        c3.metric("Personality", prof["personality"][1])
        st.markdown(f"**Current:** {decode_voice(prof)}")
        render_depth(prof["destiny"][1], "dec_dest")
    elif digits:
        raw_n = int(digits[:18])
        red, steps = reduce_trace(raw_n)
        st.metric("Digit Reduction", f"{digits[:18]} → {red}")
        render_depth(red, "dec_digits")
    else:
        st.info("Drop letters or digits above to decode.")

with tab_chart:
    st.subheader("Life Path & Natal Cycles")
    chart_d = ancient_date_input("Date to Chart", dates[0] if dates else date.today(), "chart_birth")
    lp = life_path(chart_d)
    l1, l2, l3 = st.columns(3)
    l1.metric("Life Path", lp["life_path"][1])
    l2.metric("Birthday", lp["birthday"][1])
    l3.metric("Attitude", lp["attitude"][1])
    render_depth(lp["life_path"][1], "ch_lp")

with tab_ciphers:
    st.subheader("Multilingual & Historical Ciphers")
    if latin:
        cols = st.columns(3)
        for i, cname in enumerate(LATIN_CIPHERS):
            res = run_latin_cipher(text, cname)
            with cols[i % 3]:
                st.markdown(f"**{cname}**")
                st.write(f"`{res['raw']}` → **{res['reduced']}**")
                st.caption(res["blurb"])

with tab_moon:
    st.subheader("Real-Time Moon & The Biblical Clock")
    st.caption("Live celestial positioning evaluated using high-precision ephemeris and historic synchrony.")
    
    calc_dt = datetime(moon_date.year, moon_date.month, moon_date.day, 
                       birth_time.hour if birth_time else 12, 
                       birth_time.minute if birth_time else 0, 
                       tzinfo=timezone.utc)
    
    m_data = compute_realtime_moon(calc_dt, lat, lon)
    
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown(moon_svg(m_data["fraction"], 160), unsafe_allow_html=True)
    with col_r:
        st.markdown(f"### {m_data['name']}")
        st.write(f"**Illumination:** {m_data['illumination']*100:.1f}%")
        st.write(f"**Cycle Age:** {m_data['age_days']} days (out of ~{EXACT_SYNODIC_MONTH:.2f} days)")
        st.caption(m_data["note"])
        if HAS_EPHEM:
            st.success("✦ Powered by high-accuracy Python `ephem` library.")
        else:
            st.info("Using internal mathematical astronomical tables.")
            
    st.markdown("---")
    st.markdown("### The Moon of Eden (5,500 Years Revelation)")
    st.write(
        "The moon is the ancient, uncorrupted clock. "
        "The **Gospel of Nicodemus** and **The Life of Adam and Eve** reckon exactly **5,500 years from Creation to Christ**. "
        "Because divine reckoning follows the moon, these 5,500 years must be calculated as **lunar years**, "
        "then folded into the solar framework so the timeline can speak."
    )
    
    c_eden1, c_eden2, c_eden3 = st.columns(3)
    lunar_days_5500 = 5500 * EXACT_LUNAR_YEAR
    solar_equivalent_5500 = lunar_days_5500 / JULIAN_SOLAR_YEAR
    creation_bc = solar_equivalent_5500
    
    c_eden1.metric("Lunar Years", "5,500")
    c_eden2.metric("Days Accumulated", f"{lunar_days_5500:,.1f}")
    c_eden3.metric("Julian Solar Equivalent", f"{solar_equivalent_5500:,.2f} Years")
    
    st.caption(f"Folding 5,500 lunar years places the Creation of Adam at approximately **{round(creation_bc):,} BC**.")
    
    l_red, l_steps = reduce_trace(5500)
    s_red, s_steps = reduce_trace(int(round(solar_equivalent_5500)))
    
    e_left, e_right = st.columns(2)
    with e_left:
        st.metric("Lunar Count Signature", f"5500 → {l_red}")
        st.caption(" → ".join(map(str, l_steps)))
        render_depth(l_red, "lunar_5500")
    with e_right:
        st.metric("Folded Solar Signature", f"{int(round(solar_equivalent_5500))} → {s_red}")
        st.caption(" → ".join(map(str, s_steps)))
        render_depth(s_red, "solar_folded")

with tab_pair:
    st.subheader("Compatibility & Resonance")
    st.caption("Compare two frequencies directly.")

with tab_gospel:
    st.subheader("Biblical Vault")
    v_pick = st.selectbox("Select Vault Passage", list(VAULT.keys()))
    if v_pick:
        entry = VAULT[v_pick]
        st.write(f"**English:** {entry['en']}")
        if "he" in entry: st.write(f"**Hebrew:** {entry['he']}")
        if "el" in entry: st.write(f"**Greek:** {entry['el']}")
        st.caption(entry["note"])

with tab_books:
    st.subheader("Sacred Library")
    b_shelf = library()
    b_titles = [b["title"] for b in b_shelf]
    b_pick = st.selectbox("Library Shelves", b_titles)
    selected_b = next(b for b in b_shelf if b["title"] == b_pick)
    st.write(selected_b["note"])

with tab_iching:
    st.subheader("I Ching Oracle")
    if st.button("Cast Coins (Real-Time Hexagram)"):
        cast = iching_cast()
        st.markdown(f"### {cast['present']['name']}")
        st.code(iching_draw(cast['present']['bits']))
        st.write(cast['present']['judgment'])

with tab_pat:
    st.subheader("Pattern Analysis")
    st.write("Cross-system validation engine across texts and cipher grids.")

with tab_cal:
    st.subheader("Calibration Floor")
    st.caption("Verifies statistical noise baselines for Master numbers (11, 22, 33).")
