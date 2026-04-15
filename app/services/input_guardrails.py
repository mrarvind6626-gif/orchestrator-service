"""
Input guardrails — local pre-pipeline content moderation.

Tier 0 — O(1) Set Lookups (instant):
    BAD_WORDS_SET: Exact + token + phrase scan for abusive terms.

Tier 1 — Local Pattern Matching (near-instant):
    Regex patterns for prompt-injection attempts +
    ``better_profanity`` for broad offline toxicity filtering.

LLM-level safety AND topicality checking is handled by the guard node
inside the LangGraph pipeline (single gpt-4o-mini call).
"""

from __future__ import annotations

import re

from better_profanity import profanity

from app.common.constants import (
    BAD_WORD_RESPONSE,
    BAD_WORDS_SET,
    PROMPT_INJECTION_PATTERNS,
    _BAD_WORD_PHRASES,
)
from app.common.exceptions import GuardrailViolation
from app.common.logging import get_logger

logger = get_logger(__name__)

# ── Initialize profanity filter at module load ────────────────────────────────
profanity.load_censor_words()

# ── Pre-compile injection patterns ───────────────────────────────────────────
_INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.IGNORECASE) for p in PROMPT_INJECTION_PATTERNS
]


class InputGuardrails:
    """Pre-pipeline input guardrail system (local checks only, zero I/O)."""

    async def validate(self, text: str) -> None:
        """
        Run the full pre-pipeline guardrail check.
        Raises ``GuardrailViolation`` on failure.
        """
        self._check_bad_words_set(text)
        self._check_prompt_injection(text)
        self._check_profanity(text)
        logger.info("guardrails_passed")

    # ── Tier 0 ────────────────────────────────────────────────────────────────

    @staticmethod
    def _check_bad_words_set(text: str) -> None:
        normalized = re.sub(r"\s+", " ", text.strip().lower())

        if normalized in BAD_WORDS_SET:
            logger.warning("guardrail_bad_word_exact", preview=text[:80])
            raise GuardrailViolation(BAD_WORD_RESPONSE)

        tokens = set(normalized.split())
        overlap = tokens & BAD_WORDS_SET
        if overlap:
            logger.warning("guardrail_bad_word_token", matches=list(overlap)[:3])
            raise GuardrailViolation(BAD_WORD_RESPONSE)

        for phrase in _BAD_WORD_PHRASES:
            if phrase in normalized:
                logger.warning("guardrail_bad_phrase", phrase=phrase)
                raise GuardrailViolation(BAD_WORD_RESPONSE)

    # ── Tier 1 ────────────────────────────────────────────────────────────────

    @staticmethod
    def _check_prompt_injection(text: str) -> None:
        for pattern in _INJECTION_PATTERNS:
            if pattern.search(text):
                logger.warning(
                    "guardrail_injection_blocked",
                    pattern=pattern.pattern,
                    text_preview=text[:100],
                )
                raise GuardrailViolation(
                    "Your message contains content that cannot be processed. "
                    "Please rephrase your query."
                )

    @staticmethod
    def _check_profanity(text: str) -> None:
        if profanity.contains_profanity(text):
            logger.warning("guardrail_profanity_blocked", text_preview=text[:100])
            raise GuardrailViolation(
                "Your message contains inappropriate language. "
                "Please rephrase your query."
            )
