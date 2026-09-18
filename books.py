"""Plug-in library for any book of knowledge.

JSON files in ./corpus/ are books. Runtime uploads and pasted pages
join them for the session. Counting still lives in engine.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bible_board import VAULT, count_text, fold_marks
from engine import meaning, reduce_trace

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
    if not isinstance(data, dict):
        raise ValueError("Book file must be a JSON object.")
    missing = [k for k in REQUIRED if k not in data]
    if missing:
        raise ValueError(f"Book missing fields: {', '.join(missing)}")
    book_id = str(data["id"]).strip()
    passages = [_clean_passage(p, book_id) for p in (data.get("passages") or [])]
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