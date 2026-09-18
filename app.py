"""NUMBERIN — Streamlit UI. Math lives in engine.py."""

from __future__ import annotations

import base64
import hashlib
import io
import os
import re
import textwrap
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
    name