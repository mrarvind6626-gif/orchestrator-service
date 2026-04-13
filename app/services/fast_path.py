"""
Fast-path resolver for trivial and frequently-asked queries.

Priority order:
  1. Small talk  — O(1) set lookup  (greetings, farewells, chitchat)
  2. ACPC FAQ    — O(1) dict lookup (common ACPC questions answered directly)
  3. Regex       — compiled pattern match (partial greeting/gratitude/farewell)

Any match short-circuits the full LangGraph pipeline for zero-latency replies.
"""

from __future__ import annotations

import random
import re
import unicodedata
from dataclasses import dataclass

from app.common.constants import (
    FAREWELL_PATTERNS,
    FAST_PATH_RESPONSES,
    GRATITUDE_PATTERNS,
    GREETING_PATTERNS,
    SMALL_TALK_RESPONSES,
    SMALL_TALK_SET,
)
from app.common.faq_data import (
    ACPC_FAQ_DICT,
    ACPC_FAQ_DICT_GU,
    ACPC_FAQ_DICT_HI,
    SUGGESTED_QUESTIONS,
    SUGGESTED_QUESTIONS_GU,
    SUGGESTED_QUESTIONS_HI,
)

# Language code → FAQ dict / suggested questions list
_FAQ_BY_LANG: dict[str, dict[str, str]] = {
    "en-IN": ACPC_FAQ_DICT,
    "hi-IN": ACPC_FAQ_DICT_HI,
    "gu-IN": ACPC_FAQ_DICT_GU,
}

_SUGGESTIONS_BY_LANG: dict[str, list[str]] = {
    "en-IN": SUGGESTED_QUESTIONS,
    "hi-IN": SUGGESTED_QUESTIONS_HI,
    "gu-IN": SUGGESTED_QUESTIONS_GU,
}
from app.common.logging import get_logger

logger = get_logger(__name__)


# ── Pre-compile regex patterns at module load ─────────────────────────────────

_COMPILED_PATTERNS: list[tuple[str, re.Pattern]] = []

for _category, _patterns in [
    ("greeting", GREETING_PATTERNS),
    ("gratitude", GRATITUDE_PATTERNS),
    ("farewell", FAREWELL_PATTERNS),
]:
    for _p in _patterns:
        _COMPILED_PATTERNS.append((_category, re.compile(_p, re.IGNORECASE)))


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class FastPathResult:
    """Result of a fast-path match."""
    matched: bool
    category: str   # "small_talk" | "faq" | "greeting" | "gratitude" | "farewell"
    response: str


# ── Internal helpers ──────────────────────────────────────────────────────────

def _normalize(text: str) -> str:
    """Lowercase, replace punctuation/symbols with spaces, collapse whitespace.

    Uses unicodedata.category so that Indic combining marks (Mn/Mc)
    like Gujarati ુ ં ે and Devanagari ि ी ं are preserved.
    """
    text = "".join(
        " " if unicodedata.category(c)[0] in ("P", "S") else c
        for c in text.lower()
    )
    return re.sub(r"\s+", " ", text.strip())


def _check_small_talk(normalized: str) -> FastPathResult | None:
    """O(1) set lookup against SMALL_TALK_SET."""
    if normalized in SMALL_TALK_SET:
        reply = random.choice(SMALL_TALK_RESPONSES)
        logger.info("fast_path_small_talk", query=normalized)
        return FastPathResult(matched=True, category="small_talk", response=reply)
    return None


def _check_faq(normalized: str, language: str | None = None) -> FastPathResult | None:
    """O(1) dict lookup against the language-appropriate FAQ dict."""
    faq_dict = _FAQ_BY_LANG.get(language or "en-IN", ACPC_FAQ_DICT)
    answer = faq_dict.get(normalized)
    if answer is not None:
        logger.info("fast_path_faq", query=normalized, language=language)
        return FastPathResult(matched=True, category="faq", response=answer)
    return None


def _check_regex(normalized: str) -> FastPathResult | None:
    """Compiled regex match for partial greeting/gratitude/farewell patterns."""
    for category, pattern in _COMPILED_PATTERNS:
        if pattern.match(normalized):
            response = FAST_PATH_RESPONSES.get(category, "")
            logger.info("fast_path_regex", category=category, query=normalized)
            return FastPathResult(matched=True, category=category, response=response)
    return None


# ── Public API ────────────────────────────────────────────────────────────────

def check_fast_path(query: str, language: str | None = None) -> FastPathResult | None:
    """
    Test the query against all fast-path checks in priority order.

    Returns a ``FastPathResult`` if matched, otherwise ``None``.
    The caller should short-circuit the pipeline when a result is returned.

    Args:
        query:    The raw user query.
        language: Sarvam language code (``en-IN`` | ``hi-IN`` | ``gu-IN``).
                  When provided, FAQ lookup uses the matching language dict so
                  answers are returned in the requested language.

    Priority:
        1. Small talk set  (O(1)) — pure chitchat / greetings / farewells
        2. ACPC FAQ dict   (O(1)) — language-specific FAQ with direct answers
        3. Regex patterns         — partial / variant greeting/gratitude/farewell
    """
    if not query or not query.strip():
        return None

    normalized = _normalize(query)

    # 1. Small talk (O(1))
    result = _check_small_talk(normalized)
    if result is not None:
        return result

    # 2. ACPC FAQ — use language-specific dict
    result = _check_faq(normalized, language)
    if result is not None:
        return result

    # 3. Regex fallback
    result = _check_regex(normalized)
    if result is not None:
        return result

    return None


def get_suggested_questions(language: str | None = None) -> list[str]:
    """Return the suggested questions for the given language (defaults to English)."""
    return list(_SUGGESTIONS_BY_LANG.get(language or "en-IN", SUGGESTED_QUESTIONS))
