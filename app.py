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

# English is KJV-shaped. Greek is ecclesiastical, not a critical edition.
# Hebrew is unpointed so the mispar can actually see the letters.
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

# John 1        → whole chapter
# John 1:1      → one verse
# John 1:1-18   → range
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
    """English (+ vault Greek/Hebrew) for a verse, range, or whole chapter."""
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

PISTIS_SOPHIA = {'id': 'pistis_sophia',
 'title': 'Pistis Sophia',
 'short': 'PS',
 'tradition': 'Gnostic / Askew Codex',
 'edition': 'G.R.S. Mead, 1921 (public domain)',
 'source_language': 'Coptic (Askew Codex), probably from Greek',
 'note': 'A post-resurrection teaching book. Jesus spends eleven years on the Mount of Olives '
         'speaking through the First Mystery. Pistis Sophia falls from the thirteenth aeon, is '
         'oppressed by Authades and the lion-faced power, and sings thirteen repentances until '
         'the Light hears her. Mary Magdalene is the chief questioner. Peter resents it.',
 'numbers': {'11': 'Eleven years of discourse after the rising, still below the First Mystery.',
             '12': 'Twelve aeons. The ordered heavens Sophia falls through.',
             '13': "The thirteenth aeon. Sophia's home, and the number of her repentances.",
             '24': 'Twenty-four invisibles. The company of the thirteenth aeon.',
             '30': 'A Valentinian echo: thirty aeons as the fullness. PS prefers 12 + 13 + 24.',
             '49': 'Seven times seven. The treasury arithmetic of later chapters.'},
 'names': [{'label': 'Pistis Sophia',
            'text': 'Pistis Sophia',
            'note': 'Faith-Wisdom. The soul that falls, remembers, and sings its way back.'},
           {'label': 'Sophia',
            'text': 'Sophia',
            'note': 'Wisdom. Greek ΣΟΦΙΑ = 1+70+500+10+1 = 582 in isopsephy.'},
           {'label': 'First Mystery',
            'text': 'First Mystery',
            'note': 'The veil-name Jesus finally speaks from. Look, not a mascot.'},
           {'label': 'Mary Magdalene',
            'text': 'Mary Magdalene',
            'note': 'Chief interpreter in this book. Peter cannot bear how often she speaks.'},
           {'label': 'Authades',
            'text': 'Authades',
            'note': 'Self-willed. The arrogant power that sends the lion-faced emanation.'},
           {'label': 'Jeu',
            'text': 'Jeu',
            'note': 'Overseer of the Light. A book-inside-the-book name.'}],
 'passages': [{'ref': '1.1',
               'title': 'Eleven years after the rising',
               'en': 'It came to pass, when Jesus had risen from the dead, that he passed '
                     'eleven years discoursing with his disciples, and instructing them only '
                     'up to the regions of the First Commandment and up to the regions of the '
                     'First Mystery, the Mystery within the Veil, within the First '
                     'Commandment, which is the four-and-twentieth mystery without and below, '
                     'those [four-and-twenty] which are in the second space of the First '
                     'Mystery, which is before all mysteries, the Father in the form of a '
                     'dove.',
               'note': 'The clock of the book: eleven years, twenty-four mysteries, the First '
                       'Mystery still veiled. Count 11 and 24 before you count the English.'},
              {'ref': '1.2',
               'title': 'The Mount of Olives',
               'en': 'It came to pass, therefore, on the fifteenth day of the moon in the '
                     'month Tybi, which is the day on which the moon is full, on that day '
                     'then, when the sun had come forth in its going, that there came forth '
                     'behind it a great light-power shining exceedingly. And that light-power '
                     'descended over Jesus and surrounded him wholly, while he sat apart from '
                     'his disciples, and he shone most exceedingly. And there was no measure '
                     'for the light which was on him.',
               'note': 'Full moon of Tybi. A date you can count. Light-power as garment.'},
              {'ref': '10',
               'title': 'Sophia looks down',
               'en': 'It came to pass, when Pistis Sophia was in the thirteenth aeon, in the '
                     'region of all her brethren the invisibles, that is the four-and-twenty '
                     'emanations of the great Invisible, — it came to pass then, through the '
                     'commandment of the First Mystery, that Pistis Sophia gazed into the '
                     'height. She saw the light of the veil of the Treasury of the Light, and '
                     'she desired to go to that region, and she could not go to that region. '
                     'She ceased to do the mystery of the thirteenth aeon, and she sang '
                     'praises to the light of the height, which she had seen in the light of '
                     'the veil of the Treasury of the Light.',
               'note': 'The fall begins as a gaze. Desire for a region she has not been given. '
                       '13 and 24 again.'},
              {'ref': '13',
               'title': 'The lion-faced power',
               'en': 'And the lion-faced power, that self-willed one, which is below in chaos, '
                     'which belongs to him, — he continued to emanate emanations out of '
                     'himself, very fierce, and rushed down into chaos. And he oppressed '
                     'Pistis Sophia, and took her light, and swallowed it, and her matter was '
                     'thrust down into chaos.',
               'note': 'Authades works through a lion face. Light is eaten. Matter falls.'},
              {'ref': '32',
               'title': 'The first repentance',
               'en': 'Pistis Sophia cried out most exceedingly, she cried to the Light of '
                     'lights which she had seen from the beginning, in which she had had '
                     'faith, and uttered this repentance, saying: O Light of lights, in whom I '
                     'have had faith from the beginning, hearken now then, O Light, unto my '
                     'repentance. Save me, O Light, for evil thoughts have entered into me.',
               'note': 'First of thirteen repentances. Faith is the method, not the ornament.'},
              {'ref': '48',
               'title': 'The thirteenth repentance',
               'en': 'Pistis Sophia again continued and uttered her thirteenth repentance, '
                     'saying: Hearken unto me, and save me, O Light. For thou hast received my '
                     'song of praise. Let them who take away my light be put to shame. Let '
                     'them who desire to take away my power turn backward. Let them be put to '
                     'shame who desire to swallow my power.',
               'note': 'Thirteenth song. The number of the home aeon used as a weapon of '
                       'return.'},
              {'ref': '81',
               'title': 'Mary speaks',
               'en': 'It came to pass then, when Jesus had finished saying these words unto '
                     'his disciples, that Mary Magdalene came forward. She kissed the feet of '
                     'Jesus and said: My Lord, my mind is ever understanding, at every time to '
                     'come forward and proclaim the solution of the words which thou hast '
                     'spoken; but I am afraid of Peter, because he threatened me and hateth '
                     'our sex.',
               'note': 'The political sentence of the book. The decoder is a woman and the '
                       'inner circle cannot stand it.'},
              {'ref': '100',
               'title': 'The solution is a key',
               'en': 'Jesus said unto Mary: Well said, Mary. This is the solution of the '
                     'mystery. And Mary continued and said: My Lord, will all who know the '
                     'mystery of the Ineffable, and all who have received the mystery of the '
                     'First Mystery, inherit the kingdom of the Light?'}]}

NAG_HAMMADI = {'id': 'nag_hammadi',
 'title': 'Nag Hammadi library',
 'short': 'NHC',
 'tradition': 'Coptic Gnostic / 1945 find',
 'edition': 'Catalog of the thirteen codices. English bodies here are public-domain '
            'Oxyrhynchus fragments (Grenfell & Hunt 1897, 1904) plus short labels — not the '
            '1977 Robinson / Lambdin translations.',
 'source_language': 'Coptic (Sahidic), some from Greek',
 'note': 'Twelve books plus loose leaves, buried near Nag Hammadi. Modern English translations '
         'of the Coptic tractates are still under copyright. This plug-in ships the library '
         'map, the Oxyrhynchus Greek Thomas fragments (public domain), and empty sockets so '
         "you can paste a page you have the right to count. Do not paste a living translator's "
         "page and call it the board's.",
 'numbers': {'13': 'Thirteen codices (twelve bound books + leaves often numbered as XIII).',
             '114': 'Sayings in the Gospel of Thomas.',
             '30': 'Valentinian fullness: thirty aeons.',
             '49': 'Seven sevens. Recurs in Sethian and Valentinian counting.'},
 'names': [{'label': 'Thomas',
            'text': 'Didymus Judas Thomas',
            'note': 'Twin. The name the sayings are stored under.'},
           {'label': 'Barbelo',
            'text': 'Barbelo',
            'note': 'First thought in the Apocryphon of John. Fore-providence.'},
           {'label': 'Yaldabaoth',
            'text': 'Yaldabaoth',
            'note': 'The craftsman who does not know the height. Lion-serpent in some '
                    'pictures.'},
           {'label': 'Sophia',
            'text': 'Sophia',
            'note': 'The aeon whose mistake starts the lower world in several tractates.'},
           {'label': 'Seth',
            'text': 'Seth',
            'note': 'The other seed. Sethian books treat him as the true human line.'},
           {'label': 'Thunder',
            'text': 'Thunder Perfect Mind',
            'note': 'The voice that is first and last, whore and holy, mother and daughter.'}],
 'passages': [{'ref': 'catalog',
               'title': 'The thirteen books',
               'en': 'Codex I (Jung): Prayer of the Apostle Paul, Apocryphon of James, Gospel '
                     'of Truth, Treatise on the Resurrection, Tripartite Tractate. Codex II: '
                     'Apocryphon of John, Gospel of Thomas, Gospel of Philip, Hypostasis of '
                     'the Archons, On the Origin of the World, Exegesis on the Soul, Book of '
                     'Thomas the Contender. Codex III: Apocryphon of John, Gospel of the '
                     'Egyptians, Eugnostos, Sophia of Jesus Christ, Dialogue of the Savior. '
                     'Codex IV: Apocryphon of John, Gospel of the Egyptians. Codex V: '
                     'Eugnostos, Apocalypse of Paul, First and Second Apocalypse of James, '
                     'Apocalypse of Adam. Codex VI: Acts of Peter and the Twelve Apostles, '
                     'Thunder Perfect Mind, Authoritative Teaching, Concept of Our Great '
                     'Power, Plato Republic 588-589, Discourse on the Eighth and Ninth, Prayer '
                     'of Thanksgiving, Asclepius 21-29. Codex VII: Paraphrase of Shem, Second '
                     'Treatise of the Great Seth, Apocalypse of Peter, Teachings of Silvanus, '
                     'Three Steles of Seth. Codex VIII: Zostrianos, Letter of Peter to Philip. '
                     'Codex IX: Melchizedek, Thought of Norea, Testimony of Truth. Codex X: '
                     'Marsanes. Codex XI: Interpretation of Knowledge, A Valentinian '
                     'Exposition, Allogenes, Hypsiphrone. Codex XII: Sentences of Sextus, '
                     'Gospel of Truth fragments. Codex XIII: Trimorphic Protennoia, On the '
                     'Origin of the World fragments.',
               'note': 'A map, not a scripture. Pick a tractate, paste a page you have rights '
                       'to, count that.'},
              {'ref': 'Thomas incipit',
               'title': 'Oxyrhynchus 654 — the heading',
               'en': 'These are the [secret] words which Jesus the living one spake and '
                     'Didymus Judas Thomas wrote.',
               'note': 'Grenfell and Hunt, New Sayings of Jesus, 1904. Public domain. The '
                       'Coptic book in NHC II,2 opens the same way.'},
              {'ref': 'Thomas 1',
               'title': 'Oxyrhynchus 654 — saying 1',
               'en': 'And he said: Whosoever finds the interpretation of these words shall not '
                     'taste of death.',
               'note': 'The book tells you what the book is for. Interpretation is the '
                       'sacrament.'},
              {'ref': 'Thomas 2',
               'title': 'Oxyrhynchus 654 — saying 2',
               'en': 'Jesus saith: Let not him who seeketh cease until he findeth, and when he '
                     'findeth he shall wonder; wondering he shall reign, and reigning shall '
                     'rest.',
               'note': 'Seek, find, wonder, reign, rest. A five-beat ladder.'},
              {'ref': 'Thomas 3',
               'title': 'Oxyrhynchus 654 — saying 3',
               'en': 'Jesus saith: If those who lead you say unto you, Behold, the Kingdom is '
                     'in heaven, then the birds of the heaven will precede you. If they say '
                     'unto you, It is in the sea, then the fish will precede you. But the '
                     'Kingdom is within you and it is without you. When you know yourselves, '
                     'then shall you be known, and you shall know that you are the sons of the '
                     'living Father. But if ye do not know yourselves, then ye are in poverty '
                     'and ye are poverty.',
               'note': 'Inside and outside. Self-knowledge as the census of the living '
                       'Father.'},
              {'ref': 'Thomas 5',
               'title': 'Oxyrhynchus 654 — saying 5',
               'en': 'Jesus saith: Recognize what is before thy face, and that which is hidden '
                     'from thee shall be revealed unto thee. For there is nothing hidden which '
                     'shall not be made manifest, nor buried which shall not be raised.',
               'note': 'The hidden is not a second world. It is the face you have not looked '
                       'at.'},
              {'ref': 'Thomas 27',
               'title': 'Oxyrhynchus 1 — saying 27',
               'en': 'Jesus saith: Except ye fast to the world, ye shall in no wise find the '
                     'Kingdom of God; and except ye sabbatize the Sabbath, ye shall not see '
                     'the Father.',
               'note': 'Grenfell and Hunt, 1897. Fasting the world, not a diet.'},
              {'ref': 'Thomas 28',
               'title': 'Oxyrhynchus 1 — saying 28',
               'en': 'Jesus saith: I stood in the midst of the world, and in flesh was I seen '
                     'of them, and I found all drunken, and none found I athirst among them.',
               'note': '1897 fragment. Drunken vs athirst — the same split as Sophia looking '
                       'up.'},
              {'ref': 'Thomas 32',
               'title': 'Oxyrhynchus 1 — saying 32',
               'en': 'Jesus saith: A city built on the top of a high hill and stablished can '
                     'neither fall nor be hid.',
               'note': 'Pair with Matthew 5:14 on the Bible board.'},
              {'ref': 'II,2',
               'title': 'Gospel of Thomas — socket',
               'en': '',
               'note': 'NHC II,2. 114 sayings. Paste a saying you have the right to use. The '
                       'Oxyrhynchus lines above are the PD starter.'},
              {'ref': 'II,1',
               'title': 'Apocryphon of John — socket',
               'en': '',
               'note': 'The long Sethian origin story. Barbelo, Autogenes, the arrogant '
                       'craftsman. Paste a page to count it.'},
              {'ref': 'II,3',
               'title': 'Gospel of Philip — socket',
               'en': '',
               'note': 'Bridal chamber, names, and the sentence about Mary Magdalene that '
                       'everyone quotes. Paste the page.'},
              {'ref': 'VI,2',
               'title': 'Thunder, Perfect Mind — socket',
               'en': '',
               'note': 'I am the first and the last. Paste a stanza. The voice is the text.'},
              {'ref': 'I,3',
               'title': 'Gospel of Truth — socket',
               'en': '',
               'note': 'Valentinian sermon on Error and the Name. Paste a page.'}]}

VOYNICH = {
    "id": "voynich",
    "title": "Voynich manuscript",
    "short": "MS408",
    "tradition": "Beinecke MS 408 / unknown script",
    "edition": "EVA (Extensible Voynich Alphabet) folio lines. Not a decipherment.",
    "source_language": "Voynichese (EVA transcription)",
    "note": (
        "The manuscript is not solved. These pages are letter-counts on a public "
        "transcription, not English hiding under the plants. EVA turns the glyphs "
        "into Latin keystrokes so the same funnel can run. A pretty total here is "
        "texture. Treat it as signal only if a second independent layer agrees."
    ),
    "numbers": {
        "116": "About 116 surviving folios. The book is a body count before it is a cipher.",
        "18": "Quires. The binding is a structure. Count gatherings, not vibes.",
        "2": "Currier A and Currier B. Two statistical hands, maybe two languages, maybe two moods.",
        "7": "Seven sections in the usual map: herbal, astronomical, biological, cosmological, pharmaceutical, recipes, plus front matter.",
    },
    "names": [
        {"label": "EVA", "text": "EVA", "note": "Extensible Voynich Alphabet. A keyboard, not a translation."},
        {"label": "Currier A", "text": "Currier A", "note": "Earlier statistical language. Herbal pages lean this way."},
        {"label": "Currier B", "text": "Currier B", "note": "Later statistical language. Bio and recipes lean this way."},
        {"label": "Beinecke MS 408", "text": "Beinecke MS 408", "note": "The shelf mark. The object has a name before it has a reading."},
    ],
    "passages": [
        {
            "ref": "f1r",
            "title": "Opening page — herbal",
            "en": "fachys ykal ar ataiin shol shory cthres ykor sholdy sory ckhar or ykair chtaiin shar are cthar cthar dan syaiir sheky or ykaiin shod cthoary cthes daraiin sa",
            "note": "Takahashi-style EVA for the first lines of f1r. Count the letters. Do not invent a sentence.",
        },
        {
            "ref": "f2r",
            "title": "Herbal",
            "en": "kydainy epaiin otaiin chol otaiin cthor oky chaiin cthar ykchy cthy",
            "note": "Herbal section, Currier A neighborhood. Plant page, same script.",
        },
        {
            "ref": "f68r",
            "title": "Astronomical / zodiac",
            "en": "otol daiin cthody shedy qokedy qokeedy qokain shedy qokedy",
            "note": "Star/zodiac gathering. Different pictures, same token habits.",
        },
        {
            "ref": "f75r",
            "title": "Biological / balneological",
            "en": "qokeedy qokedy qokain shedy qokeedy qokedy shedy qokain",
            "note": "The bath pages. Currier B likes qokeedy / shedy loops. That repetition is the fact.",
        },
        {
            "ref": "f86v",
            "title": "Rosette / cosmological",
            "en": "otedy shedy qokedy qokeedy shedy qokain okeedy qokedy",
            "note": "Foldout cosmology. Count it as a page, not a map of heaven.",
        },
        {
            "ref": "f103r",
            "title": "Recipes / stars",
            "en": "qokeedy qokain shedy qokedy qokeedy shedy qokain qokeedy",
            "note": "Starred paragraphs. Late book, Currier B again.",
        },
        {
            "ref": "catalog",
            "title": "Section map",
            "en": "Herbal f1-f66. Astronomical and zodiac f67-f74. Biological f75-f84. Cosmological f85-f86. Pharmaceutical f87-f102. Recipes and stars f103-f116.",
            "note": "A filing system. The numbers are folio ranges, not a code.",
        },
    ],
}

SEED_BOOKS = [PISTIS_SOPHIA, NAG_HAMMADI, VOYNICH]

CORPUS_DIR = Path(__file__).resolve().parent / "corpus"

REQUIRED = ("id", "title", "passages")


def _clean_passage(raw: dict, book_id: str) -> dict:
    return {
        "book": book_id,
        "ref": str(raw.get("ref") or "").strip(),
        "title": str(raw.get("title") or "").strip(),
        "en": str(raw.get("en") or raw.get("text") or "").strip(),
        "src": str(raw.get("src") or raw.get("el") or raw.get("he") or raw.get("coptic") or "").strip(),
        "note": str(raw.get("note") or "").strip(),
    }


def normalize_book(data: dict) -> dict:
    if isinstance(data, list):
        data = {
            "id": "uploaded",
            "title": "Uploaded pages",
            "passages": data,
        }
    if not isinstance(data, dict):
        raise ValueError("Book file must be a JSON object.")
    # A single passage (title + text) is not a whole book — wrap it.
    if "passages" not in data and (
        data.get("en") or data.get("text") or data.get("ref") or data.get("title")
    ):
        data = {
            "id": str(data.get("id") or data.get("ref") or "pasted").strip() or "pasted",
            "title": str(data.get("title") or data.get("ref") or "Pasted page"),
            "passages": [data],
        }
    if "id" not in data:
        data["id"] = str(data.get("title") or "book").lower().replace(" ", "_")
    if "title" not in data:
        data["title"] = data["id"]
    if "passages" not in data:
        data["passages"] = []
    book_id = str(data["id"]).strip() or "book"
    raw_passages = data.get("passages") or []
    if isinstance(raw_passages, dict):
        raw_passages = [raw_passages]
    passages = [_clean_passage(p, book_id) for p in raw_passages if isinstance(p, dict)]
    names = []
    for n in data.get("names") or []:
        if not isinstance(n, dict):
            continue
        names.append({
            "label": str(n.get("label") or n.get("text") or "").strip(),
            "text": str(n.get("text") or n.get("label") or "").strip(),
            "note": str(n.get("note") or "").strip(),
        })
    numbers = {}
    for k, v in (data.get("numbers") or {}).items():
        numbers[str(k)] = str(v)
    return {
        "id": book_id,
        "title": str(data.get("title") or book_id),
        "short": str(data.get("short") or book_id[:4]).upper(),
        "tradition": str(data.get("tradition") or ""),
        "edition": str(data.get("edition") or ""),
        "source_language": str(data.get("source_language") or ""),
        "note": str(data.get("note") or ""),
        "numbers": numbers,
        "names": names,
        "passages": passages,
        "origin": data.get("origin") or "corpus",
    }


def load_file(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    book = normalize_book(data)
    book["origin"] = str(path.name)
    return book


def load_corpus(extra: list[dict] | None = None) -> list[dict]:
    books: list[dict] = []
    if CORPUS_DIR.is_dir():
        for path in sorted(CORPUS_DIR.glob("*.json")):
            if path.name.startswith("_"):
                continue
            try:
                books.append(load_file(path))
            except Exception as exc:
                books.append({
                    "id": path.stem,
                    "title": path.stem,
                    "short": "ERR",
                    "tradition": "",
                    "edition": "",
                    "source_language": "",
                    "note": f"Could not load {path.name}: {exc}",
                    "numbers": {},
                    "names": [],
                    "passages": [],
                    "origin": path.name,
                })
    have = {b.get("id") for b in books}
    for item in SEED_BOOKS:
        try:
            book = normalize_book(item)
            if book["id"] in have:
                continue
            book["origin"] = book.get("origin") or "built-in"
            books.append(book)
            have.add(book["id"])
        except Exception:
            continue
    if extra:
        for item in extra:
            try:
                book = normalize_book(item)
                book["origin"] = book.get("origin") or "upload"
                books.append(book)
            except Exception:
                continue
    return books


def bible_as_book() -> dict:
    passages = []
    for ref, body in VAULT.items():
        passages.append({
            "book": "bible",
            "ref": ref,
            "title": ref,
            "en": body.get("en") or "",
            "src": body.get("el") or body.get("he") or "",
            "note": body.get("note") or "",
        })
    return {
        "id": "bible",
        "title": "Bible (vault + live fetch on the Gospels tab)",
        "short": "BIB",
        "tradition": "Hebrew Bible / New Testament",
        "edition": "Vault lines are KJV-shaped English with some Greek and unpointed Hebrew.",
        "source_language": "Hebrew, Aramaic, Greek",
        "note": "The full canon still fetches live on the Gospels tab. This card is the vault so the Books shelf can see it.",
        "numbers": {},
        "names": [],
        "passages": passages,
        "origin": "bible_board.VAULT",
    }


def library(extra: list[dict] | None = None) -> list[dict]:
    found = load_corpus(extra)
    ids = {b["id"] for b in found}
    if "bible" not in ids:
        found.insert(0, bible_as_book())
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
    if not needle:
        return None
    for p in book.get("passages") or []:
        if p["ref"].lower() == needle:
            return p
    for p in book.get("passages") or []:
        if needle in p["ref"].lower() or needle in p["title"].lower():
            return p
    return None


def search_library(books: list[dict], query: str) -> list[dict]:
    q = (query or "").strip().lower()
    if not q:
        return []
    hits = []
    for book in books:
        blob_book = " ".join([book["id"], book["title"], book["short"], book.get("note") or ""]).lower()
        for p in book.get("passages") or []:
            blob = " ".join([p["ref"], p["title"], p["en"], p["src"], p["note"], blob_book]).lower()
            if q in blob:
                hits.append({"book": book, "passage": p})
    return hits


def decode_page(text: str) -> dict:
    pack = count_text(text)
    return {
        "folded": fold_marks(text),
        "pack": pack,
        "title": meaning((pack.get("pythagorean") or {}).get("reduced") or 0)["title"]
        if pack.get("pythagorean") else "",
    }


def book_number_note(book: dict, n: int) -> str | None:
    numbers = book.get("numbers") or {}
    if str(n) in numbers:
        return numbers[str(n)]
    red, _ = reduce_trace(n)
    if str(red) in numbers and red != n:
        return f"(via {n} → {red}) " + numbers[str(red)]
    return None


def passage_from_paste(title: str, body: str, note: str = "") -> dict:
    return normalize_book({
        "id": "pasted",
        "title": title or "Pasted page",
        "short": "PASTE",
        "tradition": "session",
        "edition": "Typed or uploaded in this session. Not saved to disk.",
        "note": note,
        "passages": [{"ref": "paste", "title": title or "paste", "en": body, "note": note}],
        "origin": "session",
    })


def parse_uploaded_json(raw: str | bytes) -> dict:
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    data = json.loads(raw)
    if isinstance(data, list):
        raise ValueError("Upload one book object, not a list.")
    return normalize_book(data)

MASTERS = {11, 22, 33}
STOP = {
    "the", "and", "that", "unto", "from", "with", "this", "they", "them", "then",
    "shall", "said", "saith", "into", "upon", "have", "were", "which", "when",
    "there", "their", "his", "her", "she", "him", "who", "you", "your", "for",
    "not", "but", "are", "was", "had", "has", "been", "will", "would", "could",
    "should", "may", "can", "all", "any", "one", "two", "out", "our", "also",
    "than", "its", "it's", "yet", "nor", "let", "did", "does", "done", "over",
    "after", "before", "because", "about", "among", "under", "through", "only",
    "very", "more", "most", "some", "such", "these", "those", "what", "whom",
    "come", "came", "went", "going", "being", "made", "make", "know", "knew",
    "lord", "god", "jesus", "said", "say", "saying",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[A-Za-zΑ-Ωα-ωא-ת]{4,}", text or "")
    return {w.lower() for w in words if w.lower() not in STOP}


def _index_passage(book: dict, passage: dict) -> dict | None:
    body = (passage.get("en") or "").strip()
    src = (passage.get("src") or "").strip()
    if not body and not src:
        return None
    pack = count_text(body) if body else {"latin": {}, "scripts": [], "pythagorean": None, "digits": None}
    pack_src = count_text(src) if src else {"scripts": []}
    pyth = pack.get("pythagorean")
    digits = pack.get("digits")
    stated = []
    if digits and digits.get("digits"):
        raw_digits = digits["digits"]
        # pull useful chunks: whole string plus runs of 2+ digits
        stated.append(int(raw_digits))
        for m in re.finditer(r"\d{2,}", body):
            stated.append(int(m.group(0)))
    lore_hits = []
    numbers = book.get("numbers") or {}
    reduced = pyth["reduced"] if pyth else None
    raw = pyth["raw"] if pyth else None
    if reduced is not None and str(reduced) in numbers:
        lore_hits.append({"n": reduced, "note": numbers[str(reduced)]})
    if raw is not None and str(raw) in numbers:
        lore_hits.append({"n": raw, "note": numbers[str(raw)]})
    double = []
    if reduced is not None:
        for n in stated:
            if n == reduced or n == raw:
                double.append(n)
            red_n, _ = reduce_trace(n)
            if red_n == reduced and n != reduced:
                double.append(n)
    return {
        "book_id": book["id"],
        "book": book["title"],
        "short": book.get("short") or book["id"],
        "ref": passage.get("ref") or "",
        "title": passage.get("title") or "",
        "en": body,
        "src": src,
        "raw": raw,
        "reduced": reduced,
        "steps": (pyth or {}).get("steps") or [],
        "scripts": pack_src.get("scripts") or pack.get("scripts") or [],
        "stated": sorted(set(stated)),
        "lore_hits": lore_hits,
        "double": sorted(set(double)),
        "tokens": _tokens(body),
        "master": reduced in MASTERS if reduced is not None else False,
    }


def scan_shelf(books: list[dict]) -> dict:
    rows = []
    for book in books:
        if book.get("id") == "example_book":
            continue
        for p in book.get("passages") or []:
            ref = (p.get("ref") or "").lower()
            title = (p.get("title") or "").lower()
            if ref == "catalog" or title.endswith("socket"):
                continue
            if not (p.get("en") or "").strip():
                continue
            row = _index_passage(book, p)
            if row:
                rows.append(row)

    by_reduced = defaultdict(list)
    by_raw = defaultdict(list)
    by_script_raw = defaultdict(list)
    masters = []
    doubles = []
    lore = []
    for row in rows:
        if row["reduced"] is not None:
            by_reduced[row["reduced"]].append(row)
        if row["raw"] is not None:
            by_raw[row["raw"]].append(row)
        for s in row["scripts"]:
            by_script_raw[(s["name"], s["raw"])].append(row)
        if row["master"]:
            masters.append(row)
        if row["double"]:
            doubles.append(row)
        if row["lore_hits"]:
            lore.append(row)

    clusters = []
    for n, group in sorted(by_reduced.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        books_hit = {r["book_id"] for r in group}
        if len(group) < 2:
            continue
        clusters.append({
            "reduced": n,
            "title": meaning(n)["title"],
            "count": len(group),
            "books": len(books_hit),
            "cross": len(books_hit) > 1,
            "rows": group,
        })

    raw_twins = []
    for n, group in by_raw.items():
        books_hit = {r["book_id"] for r in group}
        if len(group) >= 2 and n and n > 9:
            raw_twins.append({
                "raw": n,
                "count": len(group),
                "cross": len(books_hit) > 1,
                "rows": group,
            })
    raw_twins.sort(key=lambda x: (-x["count"], -x["raw"]))

    echoes = []
    for i, a in enumerate(rows):
        if len(a["tokens"]) < 3:
            continue
        for b in rows[i + 1:]:
            if a["book_id"] == b["book_id"]:
                continue
            shared = a["tokens"] & b["tokens"]
            if len(shared) >= 3:
                echoes.append({
                    "shared": sorted(shared),
                    "a": a,
                    "b": b,
                    "same_reduced": a["reduced"] == b["reduced"] and a["reduced"] is not None,
                })
    echoes.sort(key=lambda e: (-len(e["shared"]), -int(e["same_reduced"])))

    n_rows = len(rows)
    master_rate = (len(masters) / n_rows) if n_rows else 0.0
    return {
        "rows": rows,
        "clusters": clusters,
        "raw_twins": raw_twins,
        "masters": masters,
        "master_rate": master_rate,
        "doubles": doubles,
        "lore": lore,
        "echoes": echoes[:40],
        "n": n_rows,
    }


def label_row(row: dict) -> str:
    return f"{row['short']} {row['ref']}"


# Python date floor is year 1. BC lives in Moon of Eden as a count, not a date.
DATE_FLOOR = date(1, 1, 1)
DATE_CEILING = date(9999, 12, 31)


def _as_date(val, fallback: date | None = None) -> date:
    """st.date_input sometimes returns a (start, end) tuple. We want one day."""
    if fallback is None:
        fallback = date.today()
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, (tuple, list)) and val:
        return _as_date(val[0], fallback)
    return fallback


def ancient_date_input(
    label: str,
    value: date,
    key: str,
    min_value: date = DATE_FLOOR,
    max_value: date = DATE_CEILING,
) -> date:
    """Calendar + typed year so the picker is not stuck paging from 2016."""
    value = _as_date(value)
    year_key = f"{key}__y"
    col_cal, col_year = st.columns([3, 1])
    with col_year:
        typed_year = st.number_input(
            "Year",
            min_value=1,
            max_value=9999,
            value=int(value.year),
            step=1,
            key=year_key,
        )
    last = monthrange(int(typed_year), int(value.month))[1]
    seed = date(int(typed_year), int(value.month), min(int(value.day), last))
    if seed < min_value:
        seed = min_value
    if seed > max_value:
        seed = max_value
    with col_cal:
        picked = st.date_input(
            label,
            value=seed,
            min_value=min_value,
            max_value=max_value,
            key=key,
        )
    return _as_date(picked, seed)

st.set_page_config(page_title="NUMBERIN", page_icon="✦", layout="wide")

st.markdown(
    """
<style>
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at 18% 0%, #1a1408 0%, #050506 42%, #000 100%);
  color: #f3e6c4;
}
.block-container {padding-top: 5rem !important; max-width: 1180px;}
h1 {
  font-weight: 900;
  letter-spacing: .22em;
  color: #f5d76e;
  text-shadow: 0 0 6px #f5d76e, 0 0 22px #c9a227, 0 0 40px #00e5ff55;
}
.seal {
  font-size: 1.25rem;
  letter-spacing: .32rem;
  color: #00e5ff;
  text-shadow: 0 0 10px #00e5ff;
}
[data-testid="stSidebar"] {
  background: #0a0a0c;
  border-right: 1px solid #c9a22755;
}
[data-testid="stHeader"] {background: rgba(0,0,0,.85);}
textarea {
  background: #0b0b0d !important;
  color: #f5d76e !important;
  border: 1px solid #c9a227 !important;
  box-shadow: 0 0 16px rgba(0,229,255,.15);
}
[data-testid="stMetricValue"] {color: #f5d76e;}
div[data-baseweb="tab-list"] {border-bottom: 1px solid #c9a22744;}

/* Dark-mode buttons: dark fill, neon edge, no washed-out gold */
div.stButton > button,
div.stDownloadButton > button,
div.stFormSubmitButton > button,
[data-testid="stSidebar"] button,
button[kind="primary"],
button[kind="secondary"],
[data-testid="baseButton-primary"],
[data-testid="baseButton-secondary"],
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-secondary"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border: 1.5px solid #00e5ff !important;
  font-weight: 800 !important;
  letter-spacing: .04em;
  text-shadow: 0 0 8px #00e5ff88;
  box-shadow: 0 0 14px rgba(0,229,255,.28);
}
div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stFormSubmitButton > button:hover,
[data-testid="stSidebar"] button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
  background: #00222c !important;
  color: #f8f4e6 !important;
  border-color: #f5d76e !important;
  box-shadow: 0 0 18px rgba(245,215,110,.35);
}
div.stButton > button:focus,
div.stDownloadButton > button:focus {
  outline: 2px solid #00e5ff !important;
  outline-offset: 2px;
}

/* Sidebar copy: kill Streamlit's gray-on-black */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color: #ead9a4 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5 {
  color: #f5d76e !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
  color: #c9dbe3 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
  color: #7ef6ff !important;
}
.stCaption, [data-testid="stCaptionContainer"] {
  color: #d7c48a !important;
}

/* The little arrow that opens / closes the sidebar */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stBaseButton-header"],
[data-testid="stBaseButton-headerNoPadding"],
[data-testid="baseButton-header"],
[data-testid="baseButton-headerNoPadding"],
button[kind="header"],
button[kind="headerNoPadding"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border: 1.5px solid #00e5ff !important;
  box-shadow: 0 0 12px rgba(0,229,255,.35) !important;
}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stExpandSidebarButton"] svg,
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stBaseButton-header"] svg,
[data-testid="stBaseButton-headerNoPadding"] svg,
button[kind="header"] svg,
button[kind="headerNoPadding"] svg {
  fill: #00e5ff !important;
  color: #00e5ff !important;
  stroke: #00e5ff !important;
}

/* Date / time / select fields */
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input,
[data-testid="stNumberInput"] input,
[data-baseweb="input"] input,
[data-baseweb="select"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border-color: #00e5ff !important;
  caret-color: #00e5ff !important;
}

/* Every pull-down: language, tracks, year list, popovers */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="list"],
[data-baseweb="select"] ul,
ul[role="listbox"],
li[role="option"],
[role="listbox"],
[role="option"] {
  background: #071018 !important;
  color: #7ef6ff !important;
  border-color: #00e5ff !important;
}
li[role="option"]:hover,
[role="option"]:hover,
[aria-selected="true"][role="option"] {
  background: #00303a !important;
  color: #f5d76e !important;
}

/* Calendar innards — day numbers 1–31 */
[data-baseweb="calendar"],
[data-baseweb="datepicker"],
[data-baseweb="month"],
[data-baseweb="calendar"] [role="grid"],
[data-baseweb="calendar"] [role="row"] {
  background: #031016 !important;
  color: #7ef6ff !important;
}
[data-baseweb="calendar"] [role="columnheader"],
[data-baseweb="calendar"] [role="columnheader"] * {
  background: #031016 !important;
  color: #f5d76e !important;
  font-weight: 800 !important;
}
[data-baseweb="calendar"] [role="gridcell"],
[data-baseweb="calendar"] [role="gridcell"] > div,
[data-baseweb="calendar"] [role="gridcell"] div,
[data-baseweb="calendar"] [role="gridcell"] span,
[data-baseweb="calendar"] [role="gridcell"] button,
[data-baseweb="calendar"] [role="button"] {
  background: #031016 !important;
  color: #7ef6ff !important;
  font-weight: 900 !important;
  font-size: 0.95rem !important;
  opacity: 1 !important;
  text-shadow: none !important;
  box-shadow: none !important;
  border: 1px solid #12303a !important;
}
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [aria-selected="true"] *,
[data-baseweb="calendar"] [aria-current="date"],
[data-baseweb="calendar"] [aria-current="date"] * {
  background: #f5d76e !important;
  color: #031016 !important;
  font-weight: 900 !important;
}
[data-baseweb="calendar"] [aria-disabled="true"],
[data-baseweb="calendar"] [aria-disabled="true"] * {
  color: #4b5563 !important;
}
[data-baseweb="calendar-header"],
[data-baseweb="calendar-header"] *,
[data-baseweb="month-year-select"] {
  background: #031016 !important;
  color: #f5d76e !important;
}
[data-baseweb="calendar-header"] button,
[data-baseweb="calendar-header"] svg {
  background: transparent !important;
  color: #00e5ff !important;
  fill: #00e5ff !important;
  border: none !important;
  box-shadow: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)

BIBLE_RE = re.compile(
    r"\b(?:(?P<book>(?:[1-3]\s*)?[A-Za-z][A-Za-z]+(?:\s+[A-Za-z]+)?))\s+"
    r"(?P<ch>\d{1,3})\s*:\s*(?P<vs>\d{1,3})",
    re.I,
)
DATE_ISO = re.compile(r"\b(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})\b")
DATE_US = re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})\b")
TIME_RE = re.compile(
    r"\b([01]?\d|2[0-3])[:.;]([0-5]\d)(?:\s*([AaPp]\.?[Mm]\.?))?\b"
)
COORD_RE = re.compile(r"(-?\d{1,3}\.\d+)\s*[,/ ]\s*(-?\d{1,3}\.\d+)")
PLACE_HINT = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,?\s*(FL|Florida|TX|Texas|CA|NY|OH|GA|NC|SC|MI|Michigan)\b",
    re.I,
)
KNOWN_COORDS = {
    "naples fl": (26.1420, -81.7948, "Naples, Florida, US"),
    "naples florida": (26.1420, -81.7948, "Naples, Florida, US"),
    "naples": (26.1420, -81.7948, "Naples, Florida, US"),
    "cape coral": (26.5628, -81.9495, "Cape Coral, Florida, US"),
    "cape coral fl": (26.5628, -81.9495, "Cape Coral, Florida, US"),
    "mcallen": (26.2034, -98.2300, "McAllen, Texas, US"),
    "mcallen tx": (26.2034, -98.2300, "McAllen, Texas, US"),
    "canton mi": (42.3087, -83.4822, "Canton, Michigan, US"),
    "canton michigan": (42.3087, -83.4822, "Canton, Michigan, US"),
    "canton": (42.3087, -83.4822, "Canton, Michigan, US"),
}
MONTHS = {
    m.lower(): i
    for i, m in enumerate(
        "January February March April May June July August September October November December".split(),
        1,
    )
}

LANG_FILTER = {
    "Auto": None,
    "English (Latin)": "latin",
    "Sanskrit": "sanskrit",
    "Greek": "greek",
    "Coptic": "coptic",
    "Aramaic (Square)": "square",
    "Aramaic (Syriac)": "syriac",
    "Hebrew": "hebrew",
    "Arabic": "arabic",
    "Russian": "russian",
    "Ukrainian": "ukrainian",
    "Georgian": "georgian",
    "Armenian": "armenian",
}

# Longest-token-first Latin → script. Enough to make Erin / Sophia / Naples count.
LATIN_TO_SCRIPT = {
    "Russian": {
        "shch": "щ", "yo": "ё", "zh": "ж", "kh": "х", "ts": "ц", "ch": "ч",
        "sh": "ш", "yu": "ю", "ya": "я", "ye": "е",
        "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "г",
        "h": "х", "i": "и", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н",
        "o": "о", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у",
        "v": "в", "w": "в", "x": "кс", "y": "ы", "z": "з",
    },
    "Ukrainian": {
        "shch": "щ", "zh": "ж", "kh": "х", "ts": "ц", "ch": "ч", "sh": "ш",
        "yu": "ю", "ya": "я", "ye": "є", "yi": "ї",
        "a": "а", "b": "б", "c": "к", "d": "д", "e": "е", "f": "ф", "g": "г",
        "h": "г", "i": "і", "j": "й", "k": "к", "l": "л", "m": "м", "n": "н",
        "o": "о", "p": "п", "q": "к", "r": "р", "s": "с", "t": "т", "u": "у",
        "v": "в", "w": "в", "x": "кс", "y": "и", "z": "з",
    },
    "Greek": {
        "th": "θ", "ph": "φ", "ch": "χ", "ps": "ψ", "kh": "χ",
        "a": "α", "b": "β", "c": "κ", "d": "δ", "e": "ε", "f": "φ", "g": "γ",
        "h": "η", "i": "ι", "j": "ι", "k": "κ", "l": "λ", "m": "μ", "n": "ν",
        "o": "ο", "p": "π", "q": "κ", "r": "ρ", "s": "σ", "t": "τ", "u": "υ",
        "v": "β", "w": "ω", "x": "ξ", "y": "υ", "z": "ζ",
    },
    "Coptic": {
        "th": "ⲑ", "ph": "ⲫ", "ch": "ⲭ", "ps": "ⲯ", "sh": "ϣ",
        "a": "ⲁ", "b": "ⲃ", "c": "ⲕ", "d": "ⲇ", "e": "ⲉ", "f": "ϥ", "g": "ⲅ",
        "h": "ϩ", "i": "ⲓ", "j": "ϫ", "k": "ⲕ", "l": "ⲗ", "m": "ⲙ", "n": "ⲛ",
        "o": "ⲟ", "p": "ⲡ", "q": "ⲕ", "r": "ⲣ", "s": "ⲥ", "t": "ⲧ", "u": "ⲩ",
        "v": "ⲃ", "w": "ⲱ", "x": "ⲝ", "y": "ⲓ", "z": "ⲍ",
    },
    "Hebrew": {
        "sh": "ש", "ch": "ח", "ts": "צ", "th": "ת", "kh": "כ",
        "a": "א", "b": "ב", "c": "כ", "d": "ד", "e": "א", "f": "פ", "g": "ג",
        "h": "ה", "i": "י", "j": "י", "k": "כ", "l": "ל", "m": "מ", "n": "נ",
        "o": "ו", "p": "פ", "q": "ק", "r": "ר", "s": "ס", "t": "ט", "u": "ו",
        "v": "ו", "w": "ו", "x": "קס", "y": "י", "z": "ז",
    },
    "Aramaic (Square)": {
        "sh": "ש", "ch": "ח", "ts": "צ", "th": "ת", "kh": "כ",
        "a": "א", "b": "ב", "c": "כ", "d": "ד", "e": "א", "f": "פ", "g": "ג",
        "h": "ה", "i": "י", "j": "י", "k": "כ", "l": "ל", "m": "מ", "n": "נ",
        "o": "ו", "p": "פ", "q": "ק", "r": "ר", "s": "ס", "t": "ט", "u": "ו",
        "v": "ו", "w": "ו", "x": "קס", "y": "י", "z": "ז",
    },
    "Aramaic (Syriac)": {
        "sh": "ܫ", "ch": "ܚ", "ts": "ܨ", "th": "ܬ",
        "a": "ܐ", "b": "ܒ", "c": "ܟ", "d": "ܕ", "e": "ܐ", "f": "ܦ", "g": "ܓ",
        "h": "ܗ", "i": "ܝ", "j": "ܝ", "k": "ܟ", "l": "ܠ", "m": "ܡ", "n": "ܢ",
        "o": "ܘ", "p": "ܦ", "q": "ܩ", "r": "ܪ", "s": "ܣ", "t": "ܛ", "u": "ܘ",
        "v": "ܘ", "w": "ܘ", "x": "ܣ", "y": "ܝ", "z": "ܙ",
    },
    "Arabic": {
        "sh": "ش", "kh": "خ", "th": "ث", "dh": "ذ", "gh": "غ",
        "a": "ا", "b": "ب", "c": "ك", "d": "د", "e": "ا", "f": "ف", "g": "ج",
        "h": "ه", "i": "ي", "j": "ج", "k": "ك", "l": "ل", "m": "م", "n": "ن",
        "o": "و", "p": "ب", "q": "ق", "r": "ر", "s": "س", "t": "ت", "u": "و",
        "v": "و", "w": "و", "x": "كس", "y": "ي", "z": "ز",
    },
    "Sanskrit": {
        "kh": "ख", "gh": "घ", "ch": "च", "jh": "झ", "th": "थ", "dh": "ध",
        "ph": "फ", "bh": "भ", "sh": "श", "ss": "ष",
        "a": "अ", "b": "ब", "c": "क", "d": "द", "e": "ए", "f": "फ", "g": "ग",
        "h": "ह", "i": "इ", "j": "ज", "k": "क", "l": "ल", "m": "म", "n": "न",
        "o": "ओ", "p": "प", "q": "क", "r": "र", "s": "स", "t": "त", "u": "उ",
        "v": "व", "w": "व", "x": "क्ष", "y": "य", "z": "ज",
    },
    "Georgian": {
        "a": "ა", "b": "ბ", "c": "ც", "d": "დ", "e": "ე", "f": "ფ", "g": "გ",
        "h": "ჰ", "i": "ი", "j": "ჯ", "k": "კ", "l": "ლ", "m": "მ", "n": "ნ",
        "o": "ო", "p": "პ", "q": "ქ", "r": "რ", "s": "ს", "t": "ტ", "u": "უ",
        "v": "ვ", "w": "ვ", "x": "ხ", "y": "ი", "z": "ზ",
    },
    "Armenian": {
        "a": "ա", "b": "բ", "c": "ց", "d": "դ", "e": "ե", "f": "ֆ", "g": "գ",
        "h": "հ", "i": "ի", "j": "ջ", "k": "կ", "l": "լ", "m": "մ", "n": "ն",
        "o": "ո", "p": "պ", "q": "ք", "r": "ր", "s": "ս", "t": "տ", "u": "ու",
        "v": "վ", "w": "վ", "x": "խ", "y": "յ", "z": "զ",
    },
}

TRACKS = {
    "Genesis": "1FH-q0I1fJY",
    "So Heavy I Fell Through the Earth": "eLo1pQ45XYs",
    "Alien": "hky6cifwWyo",
    "Cellophane": "YkLjqFpBh84",
    "The First Time Ever I Saw Your Face": "VqW-eO3jTVU",
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
    mname = re.search(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(\d{1,2})(?:st|nd|rd|th)?(?:,)?\s+(\d{4})\b",
        text,
        re.I,
    )
    if mname:
        try:
            found.append(date(int(mname.group(3)), MONTHS[mname.group(1).lower()], int(mname.group(2))))
        except ValueError:
            pass
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
            try:
                found.append(date(year, int(b), int(a)))
            except ValueError:
                pass
    out, seen = [], set()
    for d in found:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def detect_times(text: str) -> list[time]:
    found: list[time] = []
    seen = set()
    for hh, mm, ampm in TIME_RE.findall(text):
        hour = int(hh)
        minute = int(mm)
        if ampm:
            tag = re.sub(r"[^A-Za-z]", "", ampm).upper()
            if tag == "PM" and hour < 12:
                hour += 12
            if tag == "AM" and hour == 12:
                hour = 0
        try:
            t = time(hour, minute)
        except ValueError:
            continue
        if t not in seen:
            seen.add(t)
            found.append(t)
    return found


def detect_coords(text: str) -> tuple[float, float] | None:
    m = COORD_RE.search(text)
    if not m:
        return None
    lat, lon = float(m.group(1)), float(m.group(2))
    if abs(lat) <= 90 and abs(lon) <= 180:
        return lat, lon
    return None


def detect_place(text: str) -> str | None:
    m = PLACE_HINT.search(text)
    if m:
        return f"{m.group(1).strip()} {m.group(2).strip()}"
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
        return {"label": label, "lat": lat, "lon": lon, "source": "known"}
    for k, (lat, lon, label) in KNOWN_COORDS.items():
        if k in key or key in k:
            return {"label": label, "lat": lat, "lon": lon, "source": "known"}
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place, "format": "json", "limit": 1},
            timeout=6,
            headers={"User-Agent": "NUMBERIN/2.0 (personal numerology lab)"},
        )
        if r.ok:
            data = r.json()
            if data:
                hit = data[0]
                return {
                    "label": hit.get("display_name", place),
                    "lat": float(hit["lat"]),
                    "lon": float(hit["lon"]),
                    "source": "nominatim",
                }
    except Exception:
        return None
    return None


def earth_profile(place: str, lat: float, lon: float) -> dict:
    prof = name_profile(place)
    lat_red, lat_steps = reduce_trace(int(abs(lat) * 10000))
    lon_red, lon_steps = reduce_trace(int(abs(lon) * 10000))
    pair_red, pair_steps = reduce_trace(int(abs(lat) * 100 + abs(lon) * 100))
    return {
        "place": place,
        "lat": lat,
        "lon": lon,
        "lat_hemi": "N" if lat >= 0 else "S",
        "lon_hemi": "E" if lon >= 0 else "W",
        "name": prof,
        "lat_num": (lat_red, lat_steps),
        "lon_num": (lon_red, lon_steps),
        "earth_num": (pair_red, pair_steps),
    }


def name_extras(prof: dict) -> dict:
    rows = prof["rows"]
    letters = [r["letter"] for r in rows]
    values = [r["value"] for r in rows]
    counts = {n: values.count(n) for n in range(1, 10)}
    hidden = max(counts, key=counts.get) if values else 0
    first = rows[0] if rows else None
    last = rows[-1] if rows else None
    vowels = [r for r in rows if r["kind"] == "vowel"]
    cons = [r for r in rows if r["kind"] == "consonant"]
    tokens: dict[str, list] = {}
    for r in rows:
        tokens.setdefault(r["token"], []).append(r)
    token_sums = {}
    for tok, rs in tokens.items():
        raw = sum(x["value"] for x in rs)
        token_sums[tok] = (raw, *reduce_trace(raw))
    return {
        "counts": counts,
        "hidden": hidden,
        "corner": first,
        "cap": last,
        "first_vowel": vowels[0] if vowels else None,
        "vowel_n": len(vowels),
        "cons_n": len(cons),
        "token_sums": token_sums,
    }


def decode_voice(prof: dict) -> str:
    d = meaning(prof["destiny"][1])
    s = meaning(prof["soul"][1])
    p = meaning(prof["personality"][1])
    extras = name_extras(prof)
    bits = [
        f"The vehicle is {prof['destiny'][1]} — {d['title']}. {d.get('current', d['light'])}",
        f"Under the tongue: {prof['soul'][1]} — {s['title']}. {s.get('current', s['light'])}",
        f"What the room meets: {prof['personality'][1]} — {p['title']}. {p.get('current', p['light'])}",
    ]
    if extras["corner"]:
        c = extras["corner"]
        bits.append(
            f"Cornerstone {c['letter']}={c['value']} ({meaning(c['value'])['title']}) "
            f"is how this name walks into a room."
        )
    if extras["cap"]:
        c = extras["cap"]
        bits.append(
            f"Capstone {c['letter']}={c['value']} ({meaning(c['value'])['title']}) "
            f"is how it finishes what it starts."
        )
    if extras["hidden"]:
        h = meaning(extras["hidden"])
        bits.append(
            f"Hidden passion {extras['hidden']} — {h['title']} — is the number that repeats. "
            f"That hunger does not clock out."
        )
    if extras["first_vowel"]:
        v = extras["first_vowel"]
        bits.append(
            f"First vowel {v['letter']}={v['value']} is the first private note. "
            f"{meaning(v['value'])['light']}"
        )
    return " ".join(bits)


def hour_profile(t: time) -> dict:
    raw_hour = t.hour or 24
    red, steps = reduce_trace(raw_hour)
    minute_red, minute_steps = reduce_trace(t.minute) if t.minute else (0, [0])
    stamp = raw_hour * 100 + t.minute
    stamp_red, stamp_steps = reduce_trace(stamp)
    return {
        "time": t,
        "hour": (raw_hour, red, steps),
        "minute": (t.minute, minute_red, minute_steps),
        "stamp": (stamp, stamp_red, stamp_steps),
    }


def filter_scripts(rows: list[dict], lang: str) -> list[dict]:
    key = LANG_FILTER.get(lang)
    if key is None or key == "latin":
        return [] if key == "latin" else rows
    return [r for r in rows if key in r.get("name", "").lower()]


def transliterate(text: str, lang: str) -> str:
    table = LATIN_TO_SCRIPT.get(lang)
    if not table:
        return text
    keys = sorted(table, key=len, reverse=True)
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if not ch.isascii() or not ch.isalpha():
            out.append(ch)
            i += 1
            continue
        hit = False
        for token in keys:
            chunk = text[i : i + len(token)]
            if chunk.lower() == token:
                mapped = table[token]
                out.append(mapped.upper() if ch.isupper() and len(mapped) == 1 else mapped)
                i += len(token)
                hit = True
                break
        if not hit:
            out.append(ch)
            i += 1
    return "".join(out)


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_number_fact(n: int) -> str | None:
    try:
        r = requests.get(
            f"http://numbersapi.com/{n}/trivia?notfound=floor",
            timeout=4,
            headers={"User-Agent": "NumerologyLab/2.0"},
        )
        if r.ok and r.text:
            return r.text.strip()
    except Exception:
        return None
    return None




def letter_chips(rows: list[dict]) -> None:
    chips = []
    for r in rows[:120]:
        gold = r["kind"] == "vowel"
        bg = "rgba(245,215,110,.16)" if gold else "rgba(0,229,255,.12)"
        border = "#f5d76e" if gold else "#00e5ff"
        fg = "#f5d76e" if gold else "#00e5ff"
        chips.append(
            f'<span style="display:inline-block;text-align:center;margin:3px;background:{bg};'
            f'border:1px solid {border};border-radius:8px;padding:5px 7px;min-width:28px;'
            f'box-shadow:0 0 10px {border}33">'
            f'<div style="font-weight:800;color:{fg}">{r["letter"]}</div>'
            f'<div style="font-size:.68rem;color:#c9a227">{r["value"]}</div></span>'
        )
    st.markdown("".join(chips) or "_No Latin letters._", unsafe_allow_html=True)
    st.caption("Gold = vowel (Soul Urge). Cyan = consonant (Personality). Y is a vowel only when the token has no A/E/I/O/U.")


# Base rates from a 5,000-draw keep-masters calibration (1–999,999).
# Unusual ≠ true. This is frequency, not proof.
BASE_RATE = {
    1: 11.0, 2: 3.4, 3: 10.0, 4: 6.7, 5: 11.2, 6: 7.1,
    7: 11.9, 8: 10.8, 9: 11.2, 11: 7.7, 22: 4.7, 33: 4.3,
}

LENS = {
    1: {
        "personal": "A start in the body. The first yes after a long no.",
        "bible": "Beginning. The Word already is. One is not lonely here — it is prior.",
        "cipher": "Terminal 1. The funnel closed on unity. Check the raw — 1 is common.",
    },
    2: {
        "personal": "A pairing. Two currents that have not locked yet.",
        "bible": "Witness. Two tablets, two natures, two who can testify.",
        "cipher": "Terminal 2. Rare when masters are kept — 11 ate a lot of the 2s.",
    },
    3: {
        "personal": "The mouth-gate. Say it or it turns to static.",
        "bible": "Testimony complete. Three days. Father, Son, Spirit as a count, not a slogan.",
        "cipher": "Terminal 3. Expression in the arithmetic. Common landing.",
    },
    4: {
        "personal": "Pour the floor. Vision without walls is a poem you cannot live in.",
        "bible": "The world-shape. Four winds, four Gospels, four corners of the map.",
        "cipher": "Terminal 4. Structure. 22 collapses here when the master is not kept.",
    },
    5: {
        "personal": "Motion is the assignment. Stale is the enemy.",
        "bible": "Grace-count and the five books. Loaves. Wounds in later counting.",
        "cipher": "Terminal 5. Change in the digits. Common.",
    },
    6: {
        "personal": "Make a place someone can come home to. Care without a cage.",
        "bible": "The human day. Sixth of making. Incomplete seven.",
        "cipher": "Terminal 6. Harmony in the sum. 888 folds here.",
    },
    7: {
        "personal": "The well. Draw from it. Do not live at the bottom.",
        "bible": "Sabbath fullness. Seals, trumpets, bowls. The week God rests inside.",
        "cipher": "Terminal 7. The most common single-digit landing in the 5k draw.",
    },
    8: {
        "personal": "Octave. Same note, more voltage. Steward what arrived.",
        "bible": "New creation. Eighth day. The week starts again.",
        "cipher": "Terminal 8. Power-count. YHWH 26 lands here.",
    },
    9: {
        "personal": "Close the chapter. Carrying it past the last page turns compassion into a ghost.",
        "bible": "Fruit and finality. Nine fruits. The last single digit before the fold repeats.",
        "cipher": "Terminal 9. Completion in the arithmetic. 153 folds here.",
    },
    11: {
        "personal": "More current than the body was trained for. Ground or it shorts.",
        "bible": "Eleven remain when the twelfth leaves. Disorder next to twelve.",
        "cipher": "Master 11. About 7.7% of random integers stop here. Unusual, not a warrant.",
    },
    22: {
        "personal": "The vision needs a floor. Unpoured 22 collapses into anxious 4.",
        "bible": "Master builder count. Architecture language. Still just a stop in the funnel.",
        "cipher": "Master 22. About 4.7% of random integers. Rarer than 11.",
    },
    33: {
        "personal": "Love practiced until someone else can learn from it. Stay a person.",
        "bible": "Traditional age of the crucifixion. Teacher-count. Tradition, not proof.",
        "cipher": "Master 33. About 4.3% of random integers. The rarest master.",
    },
}

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "thirty": 30, "forty": 40, "fifty": 50, "seventy": 70,
    "hundred": 100, "thousand": 1000,
}


def _tone_wav(freqs: list[float], seconds: float = 0.22, volume: float = 0.18) -> bytes:
    rate = 22050
    n = int(rate * seconds)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        for i in range(n):
            t = i / rate
            fade = min(1.0, i / 180, (n - i) / 280)
            sample = 0.0
            for f in freqs:
                sample += math.sin(2 * math.pi * f * t)
            sample = sample / max(1, len(freqs))
            val = int(max(-1, min(1, sample * volume * fade)) * 32767)
            w.writeframes(struct.pack("<h", val))
    return buf.getvalue()


CHIME_WAV = {
    11: _tone_wav([523.25, 784.0], 0.28),
    22: _tone_wav([392.0, 587.33], 0.32),
    33: _tone_wav([329.63, 659.25, 987.77], 0.36),
}


def maybe_chime(n: int, tag: str = "") -> None:
    """Soft chime the first time a master lands for this input. Not on every rerun."""
    if n not in CHIME_WAV:
        return
    sig = (int(n), tag)
    if st.session_state.get("chime_sig") == sig:
        return
    st.session_state["chime_sig"] = sig
    st.caption({11: "✦ 11", 22: "✦ 22", 33: "✦ 33"}[int(n)] + " — master landing")
    try:
        st.audio(CHIME_WAV[int(n)], format="audio/wav")
    except Exception:
        pass


def lens_line(n: int, source: str = "personal") -> str:
    info = meaning(n)
    block = LENS.get(n) or LENS.get(reduce_number(n, False), {})
    line = block.get(source) or block.get("personal") or info.get("current") or info["light"]
    return line


def confidence_line(n: int) -> str:
    rate = BASE_RATE.get(n)
    if rate is None:
        folded = reduce_number(n, True)
        rate = BASE_RATE.get(folded)
        if rate is None:
            return "No base-rate for this value yet."
        return f"{n} is unusual as a raw stop. Folded {folded} lands in ~{rate:.1f}% of random draws. Unusual ≠ true."
    band = "common" if rate >= 9 else ("uncommon" if rate >= 5 else "rare in the funnel")
    return f"Funnel frequency ~{rate:.1f}% ({band}). Frequency is not meaning."


def remember_reading(kind: str, n: int, label: str) -> None:
    hist = st.session_state.setdefault("reading_hist", [])
    hist.append({"kind": kind, "n": int(n), "label": label})
    st.session_state["reading_hist"] = hist[-12:]


def show_thread(n: int) -> None:
    hist = st.session_state.get("reading_hist") or []
    hits = [h for h in hist if h["n"] == n]
    if len(hits) >= 2:
        labels = ", ".join(h["kind"] for h in hits[-4:])
        st.caption(f"Thread: {n} already showed up {len(hits)}× this session ({labels}).")


def render_depth(n: int, key: str, source: str = "personal") -> None:
    info = meaning(n)
    maybe_chime(n, key)
    exp_key = f"depth_{key}_{n}"
    with st.expander(f"{n} · {info['title']} — full current", expanded=False, key=exp_key):
        st.caption(info["keywords"])
        st.markdown(f"**{source} lens.** {lens_line(n, source)}")
        st.caption(confidence_line(n))
        show_thread(n)
        for label, line in depth_lines(n):
            if line:
                st.markdown(f"**{label}.** {line}")


def shelf_passages(extra=None):
    books = load_library(extra if extra is not None else st.session_state.get("extra_books") or [])
    rows = []
    for book in books:
        if book.get("id") == "example_book":
            continue
        for p in book.get("passages") or []:
            body = (p.get("en") or "").strip()
            if not body:
                continue
            rows.append({
                "book": book.get("title") or book.get("id"),
                "short": book.get("short") or book.get("id"),
                "ref": p.get("ref") or "",
                "title": p.get("title") or "",
                "en": body,
                "src": p.get("src") or "",
            })
    return rows


def raw_number_hits(needle: int, extra=None) -> list[dict]:
    token = str(int(needle))
    word_hits = {w for w, v in WORD_NUMBERS.items() if v == needle or str(v) == token}
    hits = []
    for row in shelf_passages(extra):
        blob = f"{row['en']} {row['src']} {row['title']}"
        digits = extract_digits(blob)
        words = set(re.findall(r"[A-Za-z]+", blob.lower()))
        if token in digits or token in blob or (word_hits & words):
            hits.append(row)
    return hits


def name_to_verses(name: str, extra=None) -> dict:
    prof = name_profile(name)
    target = prof["destiny"][1]
    matches = []
    for row in shelf_passages(extra):
        core = count_text(row["en"]).get("pythagorean")
        if core and core["reduced"] == target:
            matches.append({**row, "raw": core["raw"], "reduced": core["reduced"]})
    return {"n": target, "profile": prof, "matches": matches}


def eden_jump_points(center: int, span: int = 400) -> list[tuple[int, int, int]]:
    lo = max(0, int(center) - span)
    hi = int(center) + span
    prev = None
    jumps = []
    for y in range(lo, hi + 1):
        red = reduce_number(y, True)
        if prev is not None and red != prev:
            jumps.append((y, prev, red))
        prev = red
    return jumps


def _slug(text: str) -> str:
    first = (text.splitlines() or ["reading"])[0].strip() or "reading"
    clean = re.sub(r"[^A-Za-z0-9_\-]+", "_", first)[:40].strip("_")
    return clean or "reading"


def build_report(text: str, latin: list, scripts: list, dates: list, digits: str, birth_time: time | None = None, earth: dict | None = None, stamp: dict | None = None) -> str:
    lines = [
        "# NUMBERIN reading",
        f"Saved {(stamp or reading_stamp())['iso']}",
        "",
        f"Seal: {seed_sigil(text)}",
        "",
        f"Stamp: {(stamp or reading_stamp())['iso']}",
        "",
        "## Input",
        text,
        "",
    ]
    if latin:
        prof = name_profile(text)
        lines.append("## Name chart")
        lines.append(decode_voice(prof))
        lines.append("")
        extras = name_extras(prof)
        if extras["corner"]:
            c = extras["corner"]
            lines.append(f"- Cornerstone {c['letter']}={c['value']} ({meaning(c['value'])['title']})")
        if extras["cap"]:
            c = extras["cap"]
            lines.append(f"- Capstone {c['letter']}={c['value']} ({meaning(c['value'])['title']})")
        if extras["hidden"]:
            lines.append(f"- Hidden passion {extras['hidden']} ({meaning(extras['hidden'])['title']})")
        lines.append("- Intensity: " + ", ".join(f"{n}×{extras['counts'][n]}" for n in range(1, 10) if extras["counts"][n]))
        lines.append("")
        for label, pack in (
            ("Destiny / Expression", prof["destiny"]),
            ("Soul Urge", prof["soul"]),
            ("Personality", prof["personality"]),
        ):
            raw, red, steps = pack
            info = meaning(red)
            lines.append(f"### {label}: {red} — {info['title']}")
            lines.append(f"raw {raw} · {' → '.join(map(str, steps))}")
            for lab, line in depth_lines(red):
                if line:
                    lines.append(f"- **{lab}:** {line}")
            lines.append("")
    if digits:
        red, steps = reduce_trace(int(digits[:18]))
        lines.append("## Digit stream")
        lines.append(f"`{digits[:18]}` → {red} ({' → '.join(map(str, steps))})")
        omen = angel_read(digits) or angel_read(digits[:4])
        if omen:
            lines.append(omen)
        lines.append("")
    if dates:
        lines.append("## Dates")
        for d in dates[:8]:
            lp = life_path(d)
            info = meaning(lp["life_path"][1])
            lines.append(f"- {d.isoformat()} · Life Path {lp['life_path'][1]} — {info['title']}")
            lines.append(f"  {info.get('current', info['light'])}")
        lines.append("")
    if birth_time:
        hp = hour_profile(birth_time)
        info = meaning(hp["hour"][1])
        lines.append("## Birth time")
        lines.append(f"- Clock: {birth_time.strftime('%H:%M')}")
        lines.append(f"- Natal hour {hp['hour'][1]} — {info['title']}")
        lines.append(f"  {info.get('current', info['light'])}")
        if dates:
            when = datetime.combine(dates[0], birth_time, tzinfo=timezone.utc)
            m = moon_phase(when)
            lines.append(f"- Moon at birth (UTC clock): {m['name']} — {m['note']}")
        lines.append("")
    if earth:
        info = meaning(earth["earth_num"][0])
        lines.append("## Earth / coordinates")
        lines.append(f"- Place: {earth['place']}")
        lines.append(
            f"- Coordinates: {abs(earth['lat']):.4f}°{earth['lat_hemi']}, "
            f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}"
        )
        lines.append(
            f"- Earth number {earth['earth_num'][0]} — {info['title']}. "
            f"{info.get('current', info['light'])}"
        )
        lines.append(
            f"- Latitude number {earth['lat_num'][0]} · Longitude number {earth['lon_num'][0]}"
        )
        if earth["name"]["destiny"][1]:
            lines.append(
                f"- Place name Destiny {earth['name']['destiny'][1]} — "
                f"{meaning(earth['name']['destiny'][1])['title']}"
            )
        lines.append("")
    if scripts:
        lines.append("## Scripts")
        for r in scripts:
            info = meaning(r["reduced"])
            lines.append(f"- {r['name']}: raw {r['raw']} → {r['reduced']} — {info['title']}")
            lines.append(f"  {info.get('current', info['light'])}")
        lines.append("")
    lines.append("---")
    lines.append("Counting is local. The click you feel is the reading.")
    return "\n".join(lines)


_FONT_PATH = {"file": None}


def _font_file() -> str | None:
    if _FONT_PATH["file"] and os.path.exists(_FONT_PATH["file"]):
        return _FONT_PATH["file"]
    local = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    )
    for path in local:
        if os.path.exists(path):
            _FONT_PATH["file"] = path
            return path
    dest = "/tmp/NumberinSans.ttf"
    if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
        _FONT_PATH["file"] = dest
        return dest
    urls = (
        "https://github.com/dejavu-fonts/dejavu-fonts/raw/version_2_37/ttf/DejaVuSans.ttf",
        "https://cdn.jsdelivr.net/gh/dejavu-fonts/dejavu-fonts@version_2_37/ttf/DejaVuSans.ttf",
    )
    for url in urls:
        try:
            resp = requests.get(url, timeout=20)
            if resp.ok and len(resp.content) > 10_000:
                with open(dest, "wb") as handle:
                    handle.write(resp.content)
                _FONT_PATH["file"] = dest
                return dest
        except Exception:
            continue
    return None


def _font(size: int, bold: bool = False):
    path = _font_file()
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def build_photo(text: str, latin: list, scripts: list, dates: list, digits: str, birth_time: time | None = None, earth: dict | None = None, stamp: dict | None = None) -> bytes:
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), "#050506")
    draw = ImageDraw.Draw(img)
    gold = "#f5d76e"
    cyan = "#7ef6ff"
    cream = "#fff6d8"
    body_c = "#f0e2b0"

    brand_f = _font(86)
    name_f = _font(58)
    label_f = _font(36)
    num_f = _font(150)
    title_f = _font(48)
    body_f = _font(40)
    foot_f = _font(30)

    y = 56
    draw.text((W // 2, y), "NUMBERIN", font=brand_f, fill=gold, anchor="mt")
    y += 100
    draw.text((W // 2, y), seed_sigil(text), font=title_f, fill=cyan, anchor="mt")
    y += 70
    draw.line((64, y, W - 64, y), fill=gold, width=3)
    y += 36

    first = (text.splitlines() or [""])[0][:42]
    for wrapped in textwrap.wrap(first, 22)[:2]:
        draw.text((64, y), wrapped, font=name_f, fill=cream)
        y += 68
    y += 18

    blocks = []
    if latin:
        prof = name_profile(text)
        for label, pack in (
            ("DESTINY", prof["destiny"]),
            ("SOUL URGE", prof["soul"]),
            ("PERSONALITY", prof["personality"]),
        ):
            _raw, red, _steps = pack
            info = meaning(red)
            blocks.append((label, str(red), info["title"], info.get("current", info["light"])))
    if dates:
        d = dates[0]
        lp = life_path(d)
        info = meaning(lp["life_path"][1])
        blocks.append(
            (
                "LIFE PATH",
                str(lp["life_path"][1]),
                info["title"],
                f"{d.isoformat()} · {info.get('current', info['light'])}",
            )
        )
    if digits:
        red, _ = reduce_trace(int(digits[:18]))
        info = meaning(red)
        blocks.append(("DIGITS", str(red), info["title"], digits[:18]))
    if birth_time:
        hp = hour_profile(birth_time)
        info = meaning(hp["hour"][1])
        blocks.append(
            (
                "NATAL HOUR",
                str(hp["hour"][1]),
                info["title"],
                f"{birth_time.strftime('%H:%M')} · {info.get('current', info['light'])}",
            )
        )
    if earth:
        info = meaning(earth["earth_num"][0])
        blocks.append(
            (
                earth["place"].upper()[:18],
                str(earth["earth_num"][0]),
                info["title"],
                f"{abs(earth['lat']):.4f}°{earth['lat_hemi']}  {abs(earth['lon']):.4f}°{earth['lon_hemi']}",
            )
        )
    for r in scripts[:2]:
        info = meaning(r["reduced"])
        blocks.append((r["name"].upper()[:18], str(r["reduced"]), info["title"], info.get("current", info["light"])))

    for label, num, title, current in blocks[:4]:
        if y > H - 280:
            break
        draw.text((64, y), label, font=label_f, fill=cyan)
        y += 50
        draw.text((64, y), num, font=num_f, fill=gold)
        draw.text((300, y + 48), title, font=title_f, fill=cream)
        y += 160
        for wrapped in textwrap.wrap(current, 28)[:4]:
            draw.text((64, y), wrapped, font=body_f, fill=body_c)
            y += 48
        y += 28

    stamp_line = (stamp or reading_stamp())["iso"]
    if earth:
        stamp_line += f"  {abs(earth['lat']):.2f}{earth['lat_hemi']} {abs(earth['lon']):.2f}{earth['lon_hemi']}"
    draw.line((64, H - 120, W - 64, H - 120), fill=gold, width=2)
    draw.text((W // 2, H - 84), stamp_line, font=foot_f, fill=body_c, anchor="mt")
    draw.text((W // 2, H - 44), "the click you feel is the reading", font=foot_f, fill=cyan, anchor="mt")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def wipe_reading() -> None:
    st.session_state.payload = ""
    st.session_state.lang_pick = "Auto"
    st.session_state.know_time = False
    st.session_state.place_in = ""
    st.session_state.track = "Off"


if "payload" not in st.session_state:
    st.session_state.payload = ""
if "lang_pick" not in st.session_state:
    st.session_state.lang_pick = "Auto"
if "place_in" not in st.session_state:
    st.session_state.place_in = ""
if "know_time" not in st.session_state:
    st.session_state.know_time = False
if "track" not in st.session_state:
    st.session_state.track = "Off"

moon = moon_phase()
h1, h2, h3 = st.columns([3.2, 1.1, 1])
with h1:
    st.title("NUMBERIN")
    st.caption(
        "Type a letter, a name, a date, a verse, Hebrew, Greek, Coptic, Sanskrit, "
        "Arabic, Aramaic, Russian, Ukrainian, Georgian, Armenian, a phone number, or junk from your notes. "
        "Local math. Optional live lookups."
    )
with h2:
    st.write("")
    if st.button("New reading", type="primary", use_container_width=True):
        wipe_reading()
        st.rerun()
    st.caption("Clears the specimen. Starts a clean count.")
with h3:
    st.markdown(
        f'<div style="text-align:center">{moon_svg(moon["fraction"], 80)}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"{moon['name']} · {moon['illumination']*100:.0f}% · {moon['note']}")

with st.sidebar:
    if st.button("New reading", use_container_width=True, key="reset_side"):
        wipe_reading()
        st.rerun()
    st.header("Lenses")
    lang = st.selectbox(
        "Language / script",
        list(LANG_FILTER.keys()),
        key="lang_pick",
    )
    st.markdown("##### Tracks")
    track = st.selectbox("Play", ["Off"] + list(TRACKS.keys()), key="track")
    if track != "Off":
        vid = TRACKS[track]
        st.markdown(
            f'<iframe width="100%" height="160" src="https://www.youtube.com/embed/{vid}?rel=0" '
            f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
            unsafe_allow_html=True,
        )
        st.caption("Official upload. Use headphones.")
    live = st.toggle("Live lookups (Numbers API + Bible API)", value=True)
    as_of = ancient_date_input(
        "Personal cycles as of",
        date.today(),
        "as_of",
    )
    st.markdown("##### Birth (optional)")
    st.caption("Leave blank unless you want a natal chart. Nothing here is prefilled.")
    know_time = st.toggle("I know the birth time", key="know_time")
    birth_time_in = st.time_input("Birth time", value=None, disabled=not know_time)
    place_in = st.text_input("Birth place", key="place_in", placeholder="City, country")
    place_preview = geocode_place(place_in.strip()) if place_in.strip() else None
    if place_in.strip() and place_preview:
        st.caption(place_preview["label"])
        st.caption(
            f"{abs(place_preview['lat']):.4f}°{'N' if place_preview['lat'] >= 0 else 'S'}, "
            f"{abs(place_preview['lon']):.4f}°{'E' if place_preview['lon'] >= 0 else 'W'}"
        )
    elif place_in.strip():
        st.caption("Could not pin that place. Try City, State or City, Country.")
    moon_date = ancient_date_input(
        "Moon for date",
        date.today(),
        "moon_date",
    )
    st.markdown("---")
    st.markdown("### Moon of Eden")
    st.caption(
        "God's calendar is the moon. "
        f"{EDEN_LUNAR_YEARS:,} lunar years from Creation to Christ "
        f"≈ {eden_span()['solar_years']:,.0f} solar years "
        f"({LUNAR_YEAR_DAYS:.3f} d / {SOLAR_YEAR_DAYS} d)."
    )
    _eden_override = st.text_input(
        "Type any lunar-year count (no cap)",
        value="",
        placeholder="e.g. 26600, 5533, 100000",
        key="eden_lunar_override",
        help="Leave blank to use the slider below. Accepts any whole number.",
    )
    if _eden_override.strip():
        try:
            lunar_years = int(float(_eden_override.strip().replace(",", "")))
        except ValueError:
            st.warning("That isn't a number — using the slider value.")
            lunar_years = st.slider(
                "Lunar years from Creation",
                min_value=0,
                max_value=40_000,
                value=int(EDEN_LUNAR_YEARS),
                step=1,
                key="eden_lunar_slider",
            )
    else:
        lunar_years = st.slider(
            "Lunar years from Creation",
            min_value=0,
            max_value=40_000,
            value=int(EDEN_LUNAR_YEARS),
            step=1,
            key="eden_lunar_slider",
        )
    eden = eden_span(lunar_years)
    e1, e2 = st.columns(2)
    e1.metric("Solar equivalent", f"{eden['solar_years']:,.0f} yrs")
    e2.metric("Creation lands at", f"~{eden['creation_bc']:,} BC")
    st.caption(
        f"Lunar count {eden['lunar_number'][0]} → {eden['lunar_number'][1]} "
        f"({' → '.join(map(str, eden['lunar_number'][2]))}). "
        f"Solar count {eden['solar_number'][0]} → {eden['solar_number'][1]}."
    )
    st.caption(f"**eden lens.** {lens_line(eden['lunar_number'][1], 'bible')}  ·  {confidence_line(eden['lunar_number'][1])}")
    jumps = eden_jump_points(int(lunar_years), span=250)
    if jumps:
        st.caption("Seams in this window (reduced digit flips):")
        st.caption(" · ".join(f"{y:,}: {a}→{b}" for y, a, b in jumps[:12]))
    if st.button("Read the lunar era", use_container_width=True):
        st.session_state["lunar_read"] = eden
    st.markdown("---")
    st.markdown(
        "Counting is local (Pythagorean 3-cycle Life Path, master 11/22/33 kept, "
        "karmic 13/14/16/19 flagged). APIs only decorate."
    )

birth_default = date.today()

if moon_date != date.today():
    m2 = moon_phase(datetime(moon_date.year, moon_date.month, moon_date.day, 12, tzinfo=timezone.utc))
    st.sidebar.markdown(f"**Moon on {moon_date.isoformat()}:** {m2['name']} — {m2['note']}")

payload = st.text_area(
    "Drop anything",
    height=110,
    placeholder="Name\nMonth/Day/Year\nCity, Country",
    key="payload",
)

text = (payload or "").strip()
dates: list = []
times: list = []
digits = ""
birth_time = birth_time_in if know_time else None
earth = None
stamp = reading_stamp()
latin: list = []
scripts: list = []
script_text = text
bible_ref = None
place_label = place_in.strip() if place_in.strip() else None
lat = lon = None

if not text:
    st.info(
        "Waiting for a letter, a name, a date, or anything else. "
        "Tabs below still work — Patterns, Books, Gospels, and Calibration do not need this box."
    )
else:
    st.markdown(f'<div class="seal">{seed_sigil(text)}</div>', unsafe_allow_html=True)
    st.caption("Seal of this input — same text, same seal.")

    dates = detect_dates(text)
    times = detect_times(text)
    digits = extract_digits(text)
    birth_time = birth_time_in if know_time else (times[0] if times else None)

    place_guess = detect_place(text) or (place_in.strip() if place_in.strip() else None)
    coords_guess = detect_coords(text)
    place_label = place_guess
    if coords_guess:
        lat, lon = coords_guess
    geo = geocode_place(place_guess) if place_guess else None
    if geo:
        place_label = geo["label"]
        if lat is None or lon is None:
            lat, lon = geo["lat"], geo["lon"]
    earth = earth_profile(place_label, lat, lon) if (place_label and lat is not None and lon is not None) else None
    stamp_bits = [f"Stamped {stamp['iso']}"]
    if earth:
        stamp_bits.append(
            f"{earth['place']} · {abs(earth['lat']):.4f}°{earth['lat_hemi']}, "
            f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}"
        )
    st.caption(" · ".join(stamp_bits))

    bible_m = BIBLE_RE.search(text)
    bible_ref = f"{bible_m.group('book')} {bible_m.group('ch')}:{bible_m.group('vs')}" if bible_m else None
    script_text = text
    if lang not in ("Auto", "English (Latin)"):
        script_text = transliterate(text, lang)
    latin = letters_latin(text) if lang in ("Auto", "English (Latin)") else []
    native = script_readings(text)
    converted = script_readings(script_text) if script_text != text else []
    scripts = filter_scripts(converted or native, lang)
    if lang == "Auto":
        scripts = filter_scripts(native, lang)
    if lang not in ("Auto", "English (Latin)") and script_text != text:
        st.markdown(f"**{lang}:** `{script_text}`")
        st.caption("Latin letters moved into this script so the cipher can actually count.")

if text:
    slug = _slug(text)
    file_name_md = f"numberin_{slug}.md"
    file_name_png = f"numberin_{slug}.png"
    save_token = hashlib.sha256(
        f"{text}|{lang}|{stamp['iso']}|{place_label}|{lat}|{lon}".encode("utf-8")
    ).hexdigest()[:20]
    if st.session_state.get("_save_token") != save_token:
        st.session_state._save_token = save_token
        st.session_state._save_md = build_report(
            text, latin, scripts, dates, digits, birth_time, earth, stamp
        )
        st.session_state._save_png = build_photo(
            text, latin, scripts, dates, digits, birth_time, earth, stamp
        )
    save_md = st.session_state._save_md
    save_png = st.session_state._save_png
    save_l, save_r = st.columns(2)
    with save_l:
        st.download_button(
            "Save reading as file",
            data=save_md,
            file_name=file_name_md,
            mime="text/markdown",
            key="save_md_btn",
            use_container_width=True,
        )
        md_b64 = base64.b64encode(save_md.encode("utf-8") if isinstance(save_md, str) else save_md).decode("ascii")
        st.markdown(
            f'<a href="data:text/markdown;charset=utf-8;base64,{md_b64}" '
            f'download="{file_name_md}" target="_blank" rel="noopener" '
            f'style="display:block;margin-top:.4rem;padding:.7rem;text-align:center;'
            f'background:#071018;color:#7ef6ff;border:1.5px solid #00e5ff;'
            f'font-weight:800;text-decoration:none;border-radius:8px;">'
            f"Open / save file</a>",
            unsafe_allow_html=True,
        )
    with save_r:
        st.download_button(
            "Save reading as photo",
            data=save_png,
            file_name=file_name_png,
            mime="image/png",
            key="save_png_btn",
            use_container_width=True,
        )
        png_b64 = base64.b64encode(save_png).decode("ascii")
        st.markdown(
            f'<a href="data:image/png;base64,{png_b64}" '
            f'download="{file_name_png}" target="_blank" rel="noopener" '
            f'style="display:block;margin-top:.4rem;padding:.7rem;text-align:center;'
            f'background:#071018;color:#7ef6ff;border:1.5px solid #00e5ff;'
            f'font-weight:800;text-decoration:none;border-radius:8px;">'
            f"Open photo</a>",
            unsafe_allow_html=True,
        )
if text and isinstance(st.session_state.get("_save_png"), (bytes, bytearray)) and len(st.session_state._save_png) > 100:
    st.image(
        st.session_state._save_png,
        caption="Phone: tap and hold this picture → Add to Photos / Save Image",
        use_container_width=True,
    )

tab_decode, tab_chart, tab_ciphers, tab_moon, tab_pair, tab_look, tab_gospel, tab_books, tab_pat, tab_cal = st.tabs(
    ["Decode", "Body chart", "All ciphers", "Moon", "Compare", "Lookups", "Gospels", "Books", "Patterns", "Calibration"]
)

with tab_decode:
    if lang not in ("Auto", "English (Latin)"):
        st.subheader(f"{lang} decode")
        if scripts:
            for r in scripts:
                info = meaning(r["reduced"])
                st.write(
                    f"**{r['name']}** — raw `{r['raw']}` → **{r['reduced']}** · {info['title']}"
                )
                st.write(info.get("current", info["light"]))
                shown = " ".join(f"{ch}={v}" for ch, v in r["pairs"][:48])
                st.caption(shown)
                render_depth(r["reduced"], f"dec_lang_{r['name']}")
        else:
            st.warning(
                f"No {lang} letters counted. Type in that script, or keep English letters — "
                "they get converted automatically (Erin → Эрин / Εριν / ארין)."
            )
    st.subheader("Letter / name decode (Pythagorean)")
    if latin:
        prof = name_profile(text)
        letter_chips(prof["rows"])
        a, b, c = st.columns(3)
        for col, label, pack, note in (
            (a, "Destiny / Expression", prof["destiny"], "Every letter — the vehicle."),
            (b, "Soul Urge", prof["soul"], "Vowels — private hunger."),
            (c, "Personality", prof["personality"], "Consonants — the face the room meets."),
        ):
            raw, red, steps = pack
            info = meaning(red)
            col.metric(label, red)
            col.caption(f"{info['title']} · raw {raw} · {' → '.join(map(str, steps))}")
            col.write(info["light"])
            col.caption(note)
            if raw in KARMIC:
                col.warning(KARMIC_NOTE[raw])
            col.caption(info.get("shadow", ""))

        extras = name_extras(prof)
        st.markdown("##### The current of this name")
        st.write(decode_voice(prof))

        g1, g2, g3, g4 = st.columns(4)
        if extras["corner"]:
            c = extras["corner"]
            g1.metric("Cornerstone", f"{c['letter']} · {c['value']}")
            g1.caption(f"{meaning(c['value'])['title']} — how it enters.")
        if extras["cap"]:
            c = extras["cap"]
            g2.metric("Capstone", f"{c['letter']} · {c['value']}")
            g2.caption(f"{meaning(c['value'])['title']} — how it closes.")
        if extras["first_vowel"]:
            v = extras["first_vowel"]
            g3.metric("First vowel", f"{v['letter']} · {v['value']}")
            g3.caption("First private note.")
        if extras["hidden"]:
            g4.metric("Hidden passion", extras["hidden"])
            g4.caption(f"{meaning(extras['hidden'])['title']} — the repeat.")

        st.markdown("##### Intensity (how often each number lives in the name)")
        icols = st.columns(9)
        for n in range(1, 10):
            icols[n - 1].metric(str(n), extras["counts"].get(n, 0))
        missing = [str(n) for n in range(1, 10) if extras["counts"].get(n, 0) == 0]
        loud = [str(n) for n in range(1, 10) if extras["counts"].get(n, 0) >= 3]
        if missing:
            st.caption("Quiet / absent: " + ", ".join(missing) + " — not a hole. A lesson that arrives from outside the name.")
        if loud:
            st.caption("Loud: " + ", ".join(loud) + " — this voltage is the habit.")

        if extras["token_sums"]:
            st.markdown("##### Each word")
            for tok, (raw, red, steps) in extras["token_sums"].items():
                info = meaning(red)
                st.write(
                    f"**{tok}** — raw `{raw}` → **{red}** {info['title']} "
                    f"({' → '.join(map(str, steps))})"
                )
                st.caption(info.get("current", info["light"]))

        with st.expander("Letter by letter", expanded=False):
            for r in prof["rows"]:
                info = meaning(r["value"])
                kind = "vowel" if r["kind"] == "vowel" else "consonant"
                st.markdown(
                    f"**{r['letter']}** = {r['value']} ({kind}, {r['token']}) — "
                    f"{info['title']}. {info['light']}"
                )

        st.markdown("##### Full current")
        render_depth(prof["destiny"][1], "dec_dest")
        render_depth(prof["soul"][1], "dec_soul")
        render_depth(prof["personality"][1], "dec_pers")
        if extras["hidden"]:
            render_depth(extras["hidden"], "dec_hidden")
        if extras["corner"]:
            render_depth(extras["corner"]["value"], "dec_corner")
    else:
        st.write("No Latin letters in this specimen. Check **All ciphers** for other scripts.")

    if digits:
        raw_n = int(digits[:18])
        red, steps = reduce_trace(raw_n)
        st.subheader("Digit stream")
        st.write(f"`{digits[:18]}` → **{red}** ({' → '.join(map(str, steps))})")
        omen = angel_read(digits) or angel_read(digits[:4])
        if omen:
            st.warning(omen)
        for k in KARMIC:
            if k in steps or raw_n == k:
                st.info(KARMIC_NOTE[k])
        render_depth(red, "dec_digits")

    if dates:
        st.caption("Dates found: " + ", ".join(d.isoformat() for d in dates[:8]))
    if times:
        st.caption("Times found: " + ", ".join(t.strftime("%H:%M") for t in times[:8]))
    if earth:
        st.markdown("##### Earth")
        e1, e2, e3 = st.columns(3)
        e1.metric("Place", earth["place"].split(",")[0])
        e2.metric("Latitude", f"{abs(earth['lat']):.4f}°{earth['lat_hemi']}")
        e3.metric("Longitude", f"{abs(earth['lon']):.4f}°{earth['lon_hemi']}")
        e4, e5, e6 = st.columns(3)
        e4.metric("Earth number", earth["earth_num"][0])
        e4.write(meaning(earth["earth_num"][0])["light"])
        e5.metric("Lat number", earth["lat_num"][0])
        e6.metric("Lon number", earth["lon_num"][0])
        eplace = earth["name"]
        st.caption(
            f"Place-name Destiny {eplace['destiny'][1]} — {meaning(eplace['destiny'][1])['title']}. "
            f"{meaning(earth['earth_num'][0]).get('current', meaning(earth['earth_num'][0])['light'])}"
        )
        render_depth(earth["earth_num"][0], "dec_earth")
        render_depth(eplace["destiny"][1], "dec_place")

with tab_chart:
    name_line = st.text_input("Name to chart", value=text.split("\n")[0])
    use_date = ancient_date_input(
        "Birth date",
        dates[0] if dates else birth_default,
        "chart_d",
        max_value=date.today(),
    )
    use_time = st.time_input(
        "Birth time (optional)",
        value=birth_time or time(12, 0),
        key="chart_t",
    )
    has_time = st.checkbox("Use this birth time", value=bool(birth_time), key="chart_use_t")
    if name_line.strip():
        nm = name_profile(name_line)
        letter_chips(nm["rows"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Destiny", nm["destiny"][1])
        c1.write(meaning(nm["destiny"][1])["light"])
        c2.metric("Soul Urge", nm["soul"][1])
        c2.write(meaning(nm["soul"][1])["light"])
        c3.metric("Personality", nm["personality"][1])
        c3.write(meaning(nm["personality"][1])["light"])
        render_depth(nm["destiny"][1], "ch_dest")
        render_depth(nm["soul"][1], "ch_soul")
        render_depth(nm["personality"][1], "ch_pers")

    use_date = _as_date(use_date)
    lp = life_path(use_date)
    st.markdown("##### Date cycles (3-cycle method — month, day, year reduced separately)")
    d1, d2, d3 = st.columns(3)
    d1.metric("Life Path", lp["life_path"][1])
    d1.caption(" → ".join(map(str, lp["life_path"][2])))
    d1.write(meaning(lp["life_path"][1])["light"])
    d2.metric("Birthday", lp["birthday"][1])
    d2.write(meaning(lp["birthday"][1])["light"])
    d3.metric("Attitude (month+day)", lp["attitude"][1])
    d3.write(meaning(lp["attitude"][1])["light"])
    st.caption(
        f"{use_date.isoformat()} → month {lp['month'][1]} · day {lp['day'][1]} · year {lp['year'][1]}"
    )
    for pack in (lp["life_path"], lp["birthday"], lp["attitude"], lp["month"], lp["day"], lp["year"]):
        raw = pack[0]
        if raw in KARMIC:
            st.info(KARMIC_NOTE[raw])

    cy = personal_cycles(use_date, as_of)
    t1, t2, t3 = st.columns(3)
    t1.metric(f"Personal Year {as_of.year}", cy["year"][1])
    t1.write(meaning(cy["year"][1])["light"])
    t2.metric("Personal Month", cy["month"][1])
    t3.metric("Personal Day", cy["day"][1])
    render_depth(lp["life_path"][1], "ch_lp")
    render_depth(cy["year"][1], "ch_py")

    when_time = use_time if has_time else birth_time
    if when_time:
        hp = hour_profile(when_time)
        st.markdown("##### Natal hour")
        h1c, h2c, h3c = st.columns(3)
        h1c.metric("Clock", when_time.strftime("%H:%M"))
        h2c.metric("Hour number", hp["hour"][1])
        h2c.write(meaning(hp["hour"][1])["light"])
        h3c.metric("HHMM stamp", hp["stamp"][1])
        born_at = datetime.combine(use_date, when_time, tzinfo=timezone.utc)
        mb = moon_phase(born_at)
        st.caption(
            f"Moon at birth (using this clock as UTC): {mb['name']} · "
            f"{mb['illumination']*100:.0f}% — {mb['note']}"
        )
        render_depth(hp["hour"][1], "ch_hour")

with tab_ciphers:
    st.write("Same specimen, many temples. Disagreement is information.")
    if latin:
        cols = st.columns(3)
        for i, name in enumerate(LATIN_CIPHERS):
            res = run_latin_cipher(text, name)
            with cols[i % 3]:
                inf = meaning(res["reduced"])
                st.markdown(f"**{name}**")
                st.write(f"`{res['raw']}` → **{res['reduced']}** · {inf['title']}")
                st.caption(res["blurb"])
                st.caption(" → ".join(map(str, res["steps"])))
    if scripts:
        st.markdown("#### Detected scripts")
        for r in scripts:
            st.write(
                f"**{r['name']}** — raw `{r['raw']}` → **{r['reduced']}** "
                f"({' → '.join(map(str, r['steps']))})"
            )
            shown = " ".join(f"{ch}={v}" for ch, v in r["pairs"][:40])
            st.caption(shown)
            inf = meaning(r["reduced"])
            st.write(inf["current"] if "current" in inf else inf["light"])
            render_depth(r["reduced"], f"sc_{r['name']}")
    if not latin and not scripts:
        st.write("No mapped letters. Digit reduction lives on the Decode tab.")

with tab_moon:
    pick = ancient_date_input(
        "Phase for",
        moon_date,
        "moon_tab",
    )
    pick = _as_date(pick)
    m = moon_phase(datetime(pick.year, pick.month, pick.day, 12, tzinfo=timezone.utc))
    left, right = st.columns([1, 2])
    with left:
        st.markdown(moon_svg(m["fraction"], 140), unsafe_allow_html=True)
    with right:
        st.markdown(f"### {m['name']}")
        st.write(m["note"])
        st.caption(
            f"Age in cycle: {m['age_days']} days of {29.53:.2f} · illumination {m['illumination']*100:.0f}%"
        )
        st.write(
            "Numerology tie-in: the phase is a timing weather system. "
            "Read it next to Personal Day / Personal Month — new moon likes 1-work, "
            "full moon likes 9-work (close, offer, forgive)."
        )

    st.markdown("---")
    st.markdown("### Moon of Eden")
    st.write(
        "The moon is the older clock. A lunar year is twelve synodic months "
        f"({LUNAR_YEAR_DAYS:.3f} days). A Julian solar year is {SOLAR_YEAR_DAYS} days. "
        f"The Life of Adam and Eve / Gospel of Nicodemus count "
        f"{EDEN_LUNAR_YEARS:,} years from Creation to Christ — "
        "held here as lunar years, then folded into solar so the chart can speak."
    )
    era = st.session_state.get("lunar_read") or eden_span(st.session_state.get("eden_lunar_years", EDEN_LUNAR_YEARS))
    r1, r2, r3 = st.columns(3)
    r1.metric("Lunar years", f"{era['lunar_years']:,.0f}")
    r2.metric("Solar years", f"{era['solar_years']:,.0f}")
    r3.metric("Creation", f"~{era['creation_bc']:,} BC")
    n1, n2 = st.columns(2)
    n1.metric("Lunar number", era["lunar_number"][1])
    n1.caption(" → ".join(map(str, era["lunar_number"][2])))
    n1.write(meaning(era["lunar_number"][1])["light"])
    n2.metric("Solar number", era["solar_number"][1])
    n2.caption(" → ".join(map(str, era["solar_number"][2])))
    n2.write(meaning(era["solar_number"][1])["light"])
    render_depth(era["lunar_number"][1], "eden_lunar")
    render_depth(era["solar_number"][1], "eden_solar")
    st.caption(
        "Python dates cannot go before year 1 AD. Anything earlier is a count "
        "(lunar years / solar equivalent / BC label), not a calendar widget."
    )

with tab_pair:
    st.caption("Four counts: Life Path, Destiny, Soul Urge (vowels), Personality (consonants).")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    default_a = lines[0] if lines else ""
    default_b = lines[1] if len(lines) > 1 else ""

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### A")
        a_txt = st.text_input("A — name", value=default_a, key="pair_a_name")
        a_date = ancient_date_input(
            "A — birth",
            dates[0] if dates else birth_default,
            "pa",
            max_value=date.today(),
        )
    with c2:
        st.markdown("##### B")
        b_txt = st.text_input("B — name", value=default_b, key="pair_b_name")
        b_date = ancient_date_input(
            "B — birth",
            dates[1] if len(dates) > 1 else date.today(),
            "pb",
            max_value=date.today(),
        )

    if not a_txt.strip() or not b_txt.strip():
        st.info("Type a name in both A and B. Or put two names on two lines in the main box.")
    else:
        A = name_profile(a_txt)
        B = name_profile(b_txt)
        alp = life_path(a_date)["life_path"][1]
        blp = life_path(b_date)["life_path"][1]
        rows = [
            ("Life Path", alp, blp, "Date. The road."),
            ("Destiny", A["destiny"][1], B["destiny"][1], "Every letter. The vehicle."),
            ("Soul Urge", A["soul"][1], B["soul"][1], "Vowels. Private hunger."),
            ("Personality", A["personality"][1], B["personality"][1], "Consonants. The face the room meets."),
        ]
        for lab, av, bv, hint in rows:
            same = av == bv
            root_same = reduce_number(av, False) == reduce_number(bv, False)
            if same:
                note = "Same number — instant recognition. Watch the echo chamber."
            elif root_same:
                note = "Same root, different octave (master vs simple)."
            else:
                note = f"{meaning(av)['title']} meeting {meaning(bv)['title']}."
            st.markdown(f"##### {lab}")
            st.caption(hint)
            left, right = st.columns(2)
            left.metric("A", av)
            left.caption(meaning(av)["title"])
            right.metric("B", bv)
            right.caption(meaning(bv)["title"])
            st.write(note)
            render_depth(av, f"pair_a_{lab}")
            render_depth(bv, f"pair_b_{lab}")
            st.markdown("---")

with tab_look:
    st.write("Optional internet. Math still works if these fail.")
    if live and latin:
        core = run_latin_cipher(text, "Pythagorean")
        fact = fetch_number_fact(int(core["reduced"]))
        if fact:
            st.success(f"Numbers API on {core['reduced']}: {fact}")
        if core["raw"] != core["reduced"]:
            fact2 = fetch_number_fact(int(core["raw"]))
            if fact2:
                st.info(f"Numbers API on raw {core['raw']}: {fact2}")
    if live and bible_ref:
        verse = fetch_bible(bible_ref)
        if verse:
            st.markdown(f"**{verse['ref']}** · {verse['translation']}")
            st.write(verse["text"])
            body = run_latin_cipher(verse["text"], "Pythagorean")
            st.caption(f"Verse body Pythagorean raw {body['raw']} → {body['reduced']}")
        else:
            st.warning(f"Could not fetch `{bible_ref}`.")
    elif bible_ref:
        st.caption(f"Detected `{bible_ref}` — turn on live lookups to pull text.")
    else:
        st.caption("No Book chapter:verse pattern. Try `John 1:1`.")

    st.markdown("---")
    st.markdown(
        "This is a counting machine plus a correspondence board. "
        "Traditional Western meanings are short-form, not a priesthood. "
        "The click you feel is the reading."
    )

with tab_gospel:
    st.subheader("Gospels & Bible")
    st.caption(
        "Count the reference, the English body, and vault Greek / Hebrew. "
        "Type `John 1:1`, `John 1:1-18`, or `John 1` for a whole chapter. "
        "English Pythagorean is an overlay. Greek and Hebrew letter-numbers are the old systems."
    )
    g1, g2, g3 = st.columns([2, 1, 1])
    with g1:
        gospel_ref = st.text_input(
            "Reference",
            value=(bible_ref or "John 1:1"),
            placeholder="John 1:1  ·  John 1  ·  Matt 5:3-12",
            key="gospel_ref",
        )
    with g2:
        gospel_tr = st.selectbox(
            "Translation",
            list(TRANSLATIONS.keys()),
            format_func=lambda k: TRANSLATIONS[k],
            key="gospel_tr",
        )
    with g3:
        gospel_live = st.toggle("Fetch live", value=bool(live), key="gospel_live")
    vault_choice = st.selectbox("Vault verse", ["—"] + list(VAULT.keys()), key="gospel_vault")
    peri_choice = st.selectbox("Compare a scene", ["—"] + list(PERICOPES.keys()), key="gospel_peri")
    target = gospel_ref.strip()
    if vault_choice != "—":
        target = vault_choice

    parsed_g = parse_bible_ref(target) if target else None
    if not parsed_g:
        st.info("Try `John 3:16`, `Genesis 1:1`, or `Revelation 13:18`.")
    else:
        passage = collect_passage(parsed_g, gospel_tr, gospel_live)
        st.markdown(f"##### {parsed_g['label']}")
        st.caption(
            {"verse": "Verse", "range": "Range", "chapter": "Chapter dump"}[parsed_g["kind"]]
            + " · "
            + (" · ".join(passage["sources"]) or "reference only")
        )
        if passage["english"]:
            st.write(passage["english"])
        if passage["note"]:
            st.caption(passage["note"])
        if passage["greek"]:
            st.markdown("**Greek**")
            st.write(passage["greek"])
        if passage["hebrew"]:
            st.markdown("**Hebrew**")
            st.write(passage["hebrew"])

        counts = passage["counts"]
        items = list(counts["parts"].items())
        for chunk in [items[i:i + 4] for i in range(0, len(items), 4)]:
            cols = st.columns(len(chunk))
            for col, (name, val) in zip(cols, chunk):
                red = counts["reduced"][name]
                col.metric(name.replace("_", " "), f"{val} → {red}")
                note = bible_note(val) or bible_note(red)
                if note:
                    col.caption(note[:80] + ("…" if len(note) > 80 else ""))

        def _dump_body(label: str, body: str, key: str) -> None:
            pack = count_text(body)
            core = pack.get("pythagorean")
            scripts = pack.get("scripts") or []
            st.markdown(f"**{label}**")
            if core:
                st.caption(
                    f"Pythagorean {core['raw']} → {core['reduced']} · "
                    + meaning(core["reduced"])["title"]
                    + " · "
                    + " → ".join(map(str, core["steps"]))
                )
                render_depth(core["reduced"], key)
            for r in scripts:
                st.caption(f"{r['name']} {r['raw']} → {r['reduced']} · " + " → ".join(map(str, r["steps"])))

        if passage["english"]:
            _dump_body("English body", passage["english"], f"g_en_{parsed_g['label']}")
        if passage["greek"]:
            _dump_body("Greek body", passage["greek"], f"g_el_{parsed_g['label']}")
        if passage["hebrew"]:
            _dump_body("Hebrew body", passage["hebrew"], f"g_he_{parsed_g['label']}")

        if parsed_g["kind"] in {"chapter", "range"} and passage["verses"]:
            st.markdown("###### Verse-by-verse dump")
            for row in chapter_table(passage["verses"]):
                st.caption(
                    f"{row['ref']} · v{row['verse']}→{row['verse_reduced']} · "
                    f"{row['raw']}→{row['reduced']} {row['title']}"
                )
                st.write(row["text"])

    st.markdown("---")
    st.markdown("###### Names of power")
    name_pick = st.selectbox("Name", [n["label"] for n in NAMES_OF_POWER], key="gospel_name")
    item = next(n for n in NAMES_OF_POWER if n["label"] == name_pick)
    st.caption(f"{item['text']} — {item['note']}")
    pack_n = count_text(item["text"])
    if pack_n["scripts"]:
        r = pack_n["scripts"][0]
        st.metric(r["name"], f"{r['raw']} → {r['reduced']}")
    elif pack_n["pythagorean"]:
        r = pack_n["pythagorean"]
        st.metric("Pythagorean", f"{r['raw']} → {r['reduced']}")

    if peri_choice != "—":
        st.markdown(f"###### Scene · {peri_choice}")
        for ref in PERICOPES[peri_choice]:
            packed = collect_passage(parse_bible_ref(ref), gospel_tr, gospel_live)
            core = count_text(packed["english"]).get("pythagorean") if packed["english"] else None
            line = f"**{ref}**"
            if core:
                line += f" · {core['raw']}→{core['reduced']} {meaning(core['reduced'])['title']}"
            st.markdown(line)
            if packed["english"]:
                st.caption(packed["english"][:220] + ("…" if len(packed["english"]) > 220 else ""))

with tab_books:
    st.subheader("Books of knowledge")
    st.caption(
        "Any book can plug in. Drop a JSON file in `corpus/` or upload one here. "
        "Started with Bible, Nag Hammadi, and Pistis Sophia. "
        "Nag Hammadi English translations are mostly still under copyright — "
        "the shelf ships the library map plus public-domain Oxyrhynchus Thomas fragments. "
        "Paste a page you have the right to count."
    )
    if "extra_books" not in st.session_state:
        st.session_state.extra_books = []

    up = st.file_uploader("Upload a book JSON", type=["json"], key="book_upload")
    if up is not None and st.button("Add uploaded book", key="book_add_up"):
        try:
            book = parse_uploaded_json(up.read())
            book["origin"] = up.name
            st.session_state.extra_books.append(book)
            st.success(f"Shelved {book['title']} ({len(book['passages'])} passages).")
        except Exception as exc:
            st.error(str(exc))

    shelf = load_library(st.session_state.extra_books)
    titles = [f"{b['short']} · {b['title']}" for b in shelf]
    pick = st.selectbox("Shelf", titles, key="book_shelf")
    book = shelf[titles.index(pick)] if titles else None

    paste_title = st.text_input("Or paste a page — title", key="book_paste_title", placeholder="Thunder, stanza 1")
    paste_body = st.text_area("Page body", key="book_paste_body", height=120, placeholder="Any script. Greek and Hebrew count as themselves.")
    if st.button("Count pasted page", key="book_paste_go") and paste_body.strip():
        st.session_state.extra_books.append(passage_from_paste(paste_title, paste_body))
        st.rerun()

    q = st.text_input("Search the shelf", key="book_q", placeholder="Sophia  ·  Thomas 3  ·  thirteenth")
    if q.strip():
        hits = search_library(shelf, q.strip())
        st.caption(f"{len(hits)} hit(s)")
        for hit in hits[:20]:
            p = hit["passage"]
            st.markdown(f"**{hit['book']['short']} {p['ref']}** · {p['title']}")
            if p["en"]:
                st.caption(p["en"][:240] + ("…" if len(p["en"]) > 240 else ""))

    if book:
        st.markdown(f"##### {book['title']}")
        st.caption(
            " · ".join(
                x for x in [book.get("tradition"), book.get("edition"), book.get("source_language"), book.get("origin")]
                if x
            )
        )
        if book.get("note"):
            st.write(book["note"])
        refs = [p["ref"] + ((" — " + p["title"]) if p["title"] else "") for p in book.get("passages") or []]
        if refs:
            chosen = st.selectbox("Passage", refs, key=f"book_pass_{book['id']}")
            raw_ref = chosen.split(" — ", 1)[0]
            passage = find_passage(book, raw_ref)
        else:
            passage = None
            st.info("This book has no passages yet. Paste a page or add them to the JSON.")

        if book.get("numbers"):
            with st.expander("This book's number lore"):
                for k, v in book["numbers"].items():
                    st.markdown(f"**{k}** — {v}")
        if book.get("names"):
            with st.expander("Names this book cares about"):
                for n in book["names"]:
                    pack = count_text(n["text"])
                    core = pack.get("scripts") or []
                    pyth = pack.get("pythagorean")
                    tally = ""
                    if core:
                        tally = f"{core[0]['name']} {core[0]['raw']}→{core[0]['reduced']}"
                    elif pyth:
                        tally = f"Pythagorean {pyth['raw']}→{pyth['reduced']}"
                    st.markdown(f"**{n['label']}** · `{n['text']}` · {tally}")
                    if n.get("note"):
                        st.caption(n["note"])

        if passage:
            st.markdown(f"**{book['short']} {passage['ref']}** · {passage['title']}")
            if passage["note"]:
                st.caption(passage["note"])
            if passage["en"]:
                st.write(passage["en"])
                pack = count_text(passage["en"])
                if pack.get("pythagorean"):
                    core = pack["pythagorean"]
                    st.metric("English / Latin", f"{core['raw']} → {core['reduced']}")
                    st.caption(meaning(core["reduced"])["title"] + " · " + " → ".join(map(str, core["steps"])))
                    render_depth(core["reduced"], f"bk_{book['id']}_{passage['ref']}")
                    note = book_number_note(book, core["raw"]) or book_number_note(book, core["reduced"])
                    if note:
                        st.caption("Book board: " + note)
            else:
                st.info("Socket only — paste the page in the box above.")
            if passage["src"]:
                st.markdown("**Source-language line**")
                st.write(passage["src"])
                pack_s = count_text(passage["src"])
                for r in pack_s.get("scripts") or []:
                    st.caption(f"{r['name']} {r['raw']} → {r['reduced']} · " + " → ".join(map(str, r["steps"])))

with tab_pat:
    st.subheader("Pattern finder")
    st.caption(
        "Scans every passage on the shelf. "
        "A cluster is two or more passages that fold to the same number. "
        "A double layer is a number the text itself writes that also lands in the count. "
        "Cross-book clusters are the only ones worth a second look. "
        "Master-number rate is measured against the Calibration noise floor (~17% on random integers)."
    )
    if "extra_books" not in st.session_state:
        st.session_state.extra_books = []
    shelf = load_library(st.session_state.extra_books)
    report = scan_shelf(shelf)
    a, b, c, d = st.columns(4)
    a.metric("Passages counted", report["n"])
    b.metric("Clusters", len(report["clusters"]))
    c.metric("Cross-book echoes", sum(1 for e in report["echoes"] if e["shared"]))
    d.metric("Master landings", f"{len(report['masters'])} · {report['master_rate']*100:.0f}%")
    if report["master_rate"] <= 0.20:
        st.caption("Master rate is inside the random-integer noise band. Do not treat 11/22/33 as a find by itself.")
    else:
        st.caption("Master rate is above the ~17% noise floor. Still check that a second layer agrees.")

    want_cross = st.toggle("Only show patterns that jump books", value=True, key="pat_cross")
    focus = st.selectbox(
        "Lens",
        [
            "Clusters",
            "Raw digit",
            "Name to verse",
            "Blind challenge",
            "Double layer",
            "Book lore hits",
            "Word echoes",
            "Raw twins",
            "Masters",
        ],
        key="pat_lens",
    )

    def _show(row, extra=""):
        bits = [f"**{label_row(row)}**"]
        if row["reduced"] is not None:
            bits.append(f"{row['raw']}→{row['reduced']}")
            bits.append(meaning(row["reduced"])["title"])
        if extra:
            bits.append(extra)
        st.markdown(" · ".join(bits))
        if row["en"]:
            st.caption(row["en"][:220] + ("…" if len(row["en"]) > 220 else ""))

    if focus == "Raw digit":
        needle = st.number_input("Digit or number as written", min_value=1, max_value=1_000_000, value=7, step=1, key="raw_needle")
        hits = raw_number_hits(int(needle))
        st.caption(f"{len(hits)} passage(s) where {int(needle)} appears unreduced — in digits or a number-word.")
        if not hits:
            st.info("Nothing on the current shelf writes that number out loud.")
        for row in hits:
            st.markdown(f"**{row['short']} {row['ref']}** · {row['title']}")
            st.caption(row["en"][:280] + ("…" if len(row["en"]) > 280 else ""))

    elif focus == "Name to verse":
        who = st.text_input("Name", value="", key="name_verse_who", placeholder="Erin")
        if who.strip():
            pack = name_to_verses(who.strip())
            n = pack["n"]
            remember_reading("name", n, who.strip())
            st.metric("Destiny of that name", n)
            maybe_chime(n, "name_verse")
            st.caption(f"**personal lens.** {lens_line(n, 'personal')}")
            st.caption(confidence_line(n))
            show_thread(n)
            if not pack["matches"]:
                st.info("No shelf passage reduces to that Destiny yet. Add pages or try another name.")
            for row in pack["matches"]:
                st.markdown(f"**{row['short']} {row['ref']}** · {row['raw']}→{row['reduced']} · {row['title']}")
                st.caption(row["en"][:280] + ("…" if len(row["en"]) > 280 else ""))

    elif focus == "Blind challenge":
        st.caption(
            "Two passages. One contains the raw digit. One does not. "
            "Guess. The score is the only number in this app that can go down."
        )
        if "chal_score" not in st.session_state:
            st.session_state.chal_score = {"hit": 0, "n": 0}
        if st.button("New round", key="chal_new") or "chal_round" not in st.session_state:
            rows = shelf_passages()
            pool = []
            for probe in (7, 12, 3, 40, 1, 8, 4, 153, 11, 6, 9, 5):
                hs = raw_number_hits(probe)
                if hs:
                    pool.append((probe, hs))
            if pool and rows:
                needle, goods = random.choice(pool)
                good = random.choice(goods)
                bads = [r for r in rows if r["ref"] != good["ref"] or r["short"] != good["short"]]
                bads = [r for r in bads if str(needle) not in extract_digits(r["en"] + r["title"]) and str(needle) not in r["en"]]
                if bads:
                    bad = random.choice(bads)
                    cards = [good, bad]
                    random.shuffle(cards)
                    st.session_state.chal_round = {
                        "needle": needle,
                        "left": cards[0],
                        "right": cards[1],
                        "answer": "left" if cards[0] is good else "right",
                        "resolved": False,
                    }
        rnd = st.session_state.get("chal_round")
        if not rnd:
            st.warning("Need at least two passages on the shelf to run a round.")
        else:
            st.metric("Raw number in play", rnd["needle"])
            st.caption(confidence_line(int(rnd["needle"])) if int(rnd["needle"]) in BASE_RATE else confidence_line(reduce_number(int(rnd["needle"]), True)))
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Card A** · {rnd['left']['short']} {rnd['left']['ref']}")
                st.write(rnd["left"]["en"][:400])
            with c2:
                st.markdown(f"**Card B** · {rnd['right']['short']} {rnd['right']['ref']}")
                st.write(rnd["right"]["en"][:400])
            if not rnd["resolved"]:
                g1, g2 = st.columns(2)
                if g1.button("A is the real one", key="chal_a"):
                    ok = rnd["answer"] == "left"
                    st.session_state.chal_score["n"] += 1
                    st.session_state.chal_score["hit"] += int(ok)
                    rnd["resolved"] = True
                    rnd["ok"] = ok
                    st.session_state.chal_round = rnd
                    st.rerun()
                if g2.button("B is the real one", key="chal_b"):
                    ok = rnd["answer"] == "right"
                    st.session_state.chal_score["n"] += 1
                    st.session_state.chal_score["hit"] += int(ok)
                    rnd["resolved"] = True
                    rnd["ok"] = ok
                    st.session_state.chal_round = rnd
                    st.rerun()
            else:
                st.success("Correct." if rnd.get("ok") else "Miss. The other card held the raw digit.")
                sc = st.session_state.chal_score
                rate = (100.0 * sc["hit"] / sc["n"]) if sc["n"] else 0
                st.caption(f"Score {sc['hit']} / {sc['n']} · {rate:.0f}% vs 50% chance.")

    elif focus == "Clusters":
        shown = 0
        for cl in report["clusters"]:
            if want_cross and not cl["cross"]:
                continue
            shown += 1
            tag = "cross-book" if cl["cross"] else "same book"
            st.markdown(
                f"#### {cl['reduced']} · {cl['title']} · {cl['count']} passages · {cl['books']} book(s) · {tag}"
            )
            for row in cl["rows"]:
                _show(row)
        if not shown:
            st.info("No cluster survives that filter yet. Add books or turn the filter off.")

    elif focus == "Double layer":
        if not report["doubles"]:
            st.info("No passage yet has a written number that also lands in its own count.")
        for row in report["doubles"]:
            _show(row, extra="stated " + ", ".join(map(str, row["double"])))

    elif focus == "Book lore hits":
        if not report["lore"]:
            st.info("No passage reduction matches that book's own number lore.")
        for row in report["lore"]:
            notes = " · ".join(f"{h['n']}: {h['note']}" for h in row["lore_hits"])
            _show(row, extra=notes)

    elif focus == "Word echoes":
        shown = 0
        for echo in report["echoes"]:
            if want_cross and echo["a"]["book_id"] == echo["b"]["book_id"]:
                continue
            shown += 1
            same = " · same reduction" if echo["same_reduced"] else ""
            st.markdown(
                f"**{label_row(echo['a'])}** ↔ **{label_row(echo['b'])}** · "
                f"shared {', '.join(echo['shared'][:12])}{same}"
            )
            st.caption((echo["a"]["en"] or "")[:160])
            st.caption((echo["b"]["en"] or "")[:160])
        if not shown:
            st.info("No cross-book word echo of three+ content words yet.")

    elif focus == "Raw twins":
        shown = 0
        for twin in report["raw_twins"]:
            if want_cross and not twin["cross"]:
                continue
            shown += 1
            st.markdown(f"#### raw {twin['raw']} · {twin['count']} passages")
            for row in twin["rows"]:
                _show(row)
        if not shown:
            st.info("No shared raw totals across books. That is the rare one — keep the filter on.")

    else:
        if not report["masters"]:
            st.info("No 11/22/33 landings in the current shelf.")
        for row in report["masters"]:
            _show(row)

with tab_cal:
    st.subheader("Calibration — master-number base rate")
    st.caption(
        "Control group. Draw random integers, run each through `reduce_trace`, "
        "and count how often the funnel stops on 11, 22, or 33. "
        "That rate is the noise floor — not a reading."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        cal_n = st.number_input(
            "Samples",
            min_value=100,
            max_value=100_000,
            value=5_000,
            step=100,
            key="cal_n",
        )
    with c2:
        cal_lo = st.number_input(
            "Min value",
            min_value=1,
            max_value=1_000_000_000,
            value=1,
            step=1,
            key="cal_lo",
        )
    with c3:
        cal_hi = st.number_input(
            "Max value",
            min_value=1,
            max_value=1_000_000_000,
            value=999_999,
            step=1,
            key="cal_hi",
        )

    cal_keep = st.checkbox(
        "Keep masters (engine default — stop on 11 / 22 / 33)",
        value=True,
        key="cal_keep",
    )
    cal_seed = st.number_input(
        "Random seed (0 = fresh each run)",
        min_value=0,
        max_value=2_147_483_647,
        value=0,
        step=1,
        key="cal_seed",
    )

    if int(cal_hi) < int(cal_lo):
        st.error("Max value must be ≥ min value.")
    elif st.button("Run calibration", use_container_width=True, key="cal_run"):
        lo = int(cal_lo)
        hi = int(cal_hi)
        n = int(cal_n)
        if int(cal_seed):
            rng = random.Random(int(cal_seed))
        else:
            rng = random.Random()

        finals: dict[int, int] = {}
        master_final = 0
        master_anywhere = 0
        by_master = {11: 0, 22: 0, 33: 0}
        samples_preview = []

        for i in range(n):
            raw = rng.randint(lo, hi)
            reduced, steps = reduce_trace(raw, keep_masters=bool(cal_keep))
            finals[reduced] = finals.get(reduced, 0) + 1
            hit_final = reduced in (11, 22, 33)
            hit_any = any(s in (11, 22, 33) for s in steps)
            if hit_final:
                master_final += 1
                by_master[reduced] = by_master.get(reduced, 0) + 1
            if hit_any:
                master_anywhere += 1
            if i < 12:
                samples_preview.append((raw, steps, reduced))

        rate_final = 100.0 * master_final / n
        rate_any = 100.0 * master_anywhere / n

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Samples", f"{n:,}")
        m2.metric("Final 11/22/33", f"{master_final:,}")
        m3.metric("Hit rate (final)", f"{rate_final:.2f}%")
        m4.metric("Hit rate (anywhere in trace)", f"{rate_any:.2f}%")

        st.markdown("##### Split by master")
        s1, s2, s3 = st.columns(3)
        s1.metric("11", f"{by_master[11]:,}  ({100.0 * by_master[11] / n:.2f}%)")
        s2.metric("22", f"{by_master[22]:,}  ({100.0 * by_master[22] / n:.2f}%)")
        s3.metric("33", f"{by_master[33]:,}  ({100.0 * by_master[33] / n:.2f}%)")

        st.markdown("##### Final-value distribution")
        order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]
        rows = []
        for k in order:
            count = finals.get(k, 0)
            rows.append(
                {
                    "value": k,
                    "count": count,
                    "percent": round(100.0 * count / n, 3),
                }
            )
        extras = sorted(set(finals) - set(order))
        for k in extras:
            rows.append(
                {
                    "value": k,
                    "count": finals[k],
                    "percent": round(100.0 * finals[k] / n, 3),
                }
            )
        st.dataframe(rows, use_container_width=True, hide_index=True)

        st.markdown("##### First 12 draws")
        for raw, steps, reduced in samples_preview:
            trail = " → ".join(str(s) for s in steps)
            mark = "  ← master" if reduced in (11, 22, 33) else ""
            st.caption(f"`{raw}` → {trail}  ⇒ **{reduced}**{mark}")

        st.info(
            f"Range `{lo:,}`–`{hi:,}`, keep_masters={bool(cal_keep)}. "
            "If a number you care about lands near this rate, treat it as base-rate noise "
            "until a second independent funnel agrees."
        )
        st.session_state["cal_last"] = {
            "n": n,
            "lo": lo,
            "hi": hi,
            "keep": bool(cal_keep),
            "seed": int(cal_seed),
            "master_final": master_final,
            "rate_final": rate_final,
            "rate_any": rate_any,
            "by_master": by_master,
        }
