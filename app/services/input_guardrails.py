"""
Input guardrails — three-tiered content moderation pipeline.

Tier 0 — O(1) Set Lookups (local, instant):
    • BAD_WORDS_SET: Exact-match + token scan + phrase scan for known
      abusive/profane/threatening terms.  Raises GuardrailViolation immediately.

Tier 1 — Local Pattern Matching (local, near-instant):
    • Regex patterns for prompt-injection attempts.
    • ``better_profanity`` library for broad offline toxicity filtering.

Tier 2 — Semantic Guardrails (remote, async):
    • NeMo Guardrails (if installed and configured) for LLM-aware topicality
      and intent-based safety checking.  Falls back gracefully if unavailable.
    • OpenAI Moderation API for content safety (violence, hate, sexual, etc.).

Execution order: Tier 0 → Tier 1 → Tier 2a (NeMo) → Tier 2b (Moderation).
Any tier that fires raises ``GuardrailViolation`` — the pipeline stops there.
"""

from __future__ import annotations

import asyncio
import os
import re

from better_profanity import profanity

from app.adapters.base import ModerationAdapterBase
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

# ── NeMo Guardrails — module-level lazy singleton ─────────────────────────────
# NeMo is initialised once on first use (not at import time) to avoid blocking
# startup if the library or config is unavailable.
_nemo_rails = None
_nemo_init_done: bool = False
_nemo_init_lock: asyncio.Lock | None = None

# Path to the NeMo Colang config directory.
# Override via NEMO_CONFIG_PATH env var for Docker / custom deployments.
_HERE = os.path.dirname(os.path.abspath(__file__))
_NEMO_CONFIG_PATH: str = os.getenv(
    "NEMO_CONFIG_PATH",
    os.path.normpath(os.path.join(_HERE, "..", "..", "core", "nemo_config")),
)

# Phrases that indicate NeMo has blocked the message
_NEMO_BLOCK_INDICATORS: tuple[str, ...] = (
    "i cannot",
    "i can't",
    "i'm not able to",
    "not able to help with that",
    "i'm sorry, but i can't",
    "i should not",
    "i shouldn't",
    "i'm specifically designed",
    "i'm designed to help only",
)


async def _init_nemo() -> None:
    """Lazy-initialise NeMo Guardrails (called once, thread-safe via asyncio.Lock)."""
    global _nemo_rails, _nemo_init_done, _nemo_init_lock

    # Create the lock on first call (must happen inside a running event loop)
    if _nemo_init_lock is None:
        _nemo_init_lock = asyncio.Lock()

    async with _nemo_init_lock:
        if _nemo_init_done:
            return

        try:
            from nemoguardrails import LLMRails, RailsConfig  # type: ignore[import]

            if not os.path.isdir(_NEMO_CONFIG_PATH):
                logger.warning(
                    "nemo_config_not_found",
                    path=_NEMO_CONFIG_PATH,
                    hint="Set NEMO_CONFIG_PATH env var or create the directory.",
                )
                return

            # ── Bridge OpenRouter credentials into NeMo's OpenAI client ──────
            # NeMo uses the OpenAI SDK internally.  OpenRouter is OpenAI-compatible,
            # so we set OPENAI_API_KEY / OPENAI_API_BASE from the OpenRouter env vars
            # before NeMo loads — this way no separate OpenAI key is needed.
            # Force-set (not setdefault) to override any placeholder values in .env.
            openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
            openrouter_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            if openrouter_key:
                os.environ["OPENAI_API_KEY"] = openrouter_key
                os.environ["OPENAI_API_BASE"] = openrouter_url
                logger.info("nemo_using_openrouter", base_url=openrouter_url)

            config = RailsConfig.from_path(_NEMO_CONFIG_PATH)
            _nemo_rails = LLMRails(config)
            logger.info("nemo_guardrails_initialized", config_path=_NEMO_CONFIG_PATH)

        except ImportError:
            logger.warning(
                "nemo_guardrails_not_installed",
                hint="pip install nemoguardrails",
            )
        except Exception:
            logger.exception("nemo_guardrails_init_failed")
        finally:
            _nemo_init_done = True  # Don't retry even on failure


# ── InputGuardrails class ─────────────────────────────────────────────────────

class InputGuardrails:
    """Three-tiered input guardrail system."""

    def __init__(self, moderation_adapter: ModerationAdapterBase) -> None:
        self._moderation = moderation_adapter

    async def validate(self, text: str) -> None:
        """
        Run the full guardrail pipeline. Raises ``GuardrailViolation`` on failure.

        Designed to raise rather than return a boolean so callers cannot
        accidentally ignore the result.
        """
        # ── Tier 0: O(1) bad words set (fastest, no I/O) ─────────────────────
        self._check_bad_words_set(text)

        # ── Tier 1: Local pattern matching (still no I/O) ─────────────────────
        self._check_prompt_injection(text)
        self._check_profanity(text)

        # ── Tier 2a: NeMo Guardrails (semantic topicality) ────────────────────
        await self._check_nemo(text)

        # ── Tier 2b: OpenAI Moderation API (semantic safety) ─────────────────
        await self._check_moderation_api(text)

        logger.info("guardrails_passed")

    # ── Tier 0: Bad Words Set ─────────────────────────────────────────────────

    @staticmethod
    def _check_bad_words_set(text: str) -> None:
        """
        O(1) bad-word detection using BAD_WORDS_SET from constants.

        Three checks in order:
          1. Full normalised exact match
          2. Token-level scan (each whitespace-separated word)
          3. Multi-word phrase substring scan
        """
        normalized = re.sub(r"\s+", " ", text.strip().lower())

        # Full exact match
        if normalized in BAD_WORDS_SET:
            logger.warning("guardrail_bad_word_exact", preview=text[:80])
            raise GuardrailViolation(BAD_WORD_RESPONSE)

        # Token scan
        tokens = set(normalized.split())
        overlap = tokens & BAD_WORDS_SET
        if overlap:
            logger.warning("guardrail_bad_word_token", matches=list(overlap)[:3])
            raise GuardrailViolation(BAD_WORD_RESPONSE)

        # Multi-word phrase scan
        for phrase in _BAD_WORD_PHRASES:
            if phrase in normalized:
                logger.warning("guardrail_bad_phrase", phrase=phrase)
                raise GuardrailViolation(BAD_WORD_RESPONSE)

    # ── Tier 1: Prompt Injection ──────────────────────────────────────────────

    @staticmethod
    def _check_prompt_injection(text: str) -> None:
        """Scan text against known prompt-injection regex patterns."""
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

    # ── Tier 1: Profanity Library ─────────────────────────────────────────────

    @staticmethod
    def _check_profanity(text: str) -> None:
        """Scan text for profanity using better_profanity."""
        if profanity.contains_profanity(text):
            logger.warning("guardrail_profanity_blocked", text_preview=text[:100])
            raise GuardrailViolation(
                "Your message contains inappropriate language. "
                "Please rephrase your query."
            )

    # ── Tier 2a: NeMo Guardrails ──────────────────────────────────────────────

    @staticmethod
    async def _check_nemo(text: str) -> None:
        """
        Run the message through NeMo Guardrails for topicality and LLM-aware safety.

        If NeMo is not installed or configured, this is a no-op (fail-open).
        If NeMo blocks the message, raises GuardrailViolation.
        """
        global _nemo_rails

        if not _nemo_init_done:
            await _init_nemo()

        if _nemo_rails is None:
            return  # NeMo unavailable — passthrough

        try:
            response = await _nemo_rails.generate_async(
                messages=[{"role": "user", "content": text}]
            )

            bot_message = (
                response.get("content", "")
                if isinstance(response, dict)
                else str(response)
            )

            if any(indicator in bot_message.lower() for indicator in _NEMO_BLOCK_INDICATORS):
                logger.info("guardrail_nemo_blocked", preview=text[:80])
                raise GuardrailViolation(
                    "I'm designed to help with ACPC Gujarat admissions queries only. "
                    "Please ask me about admission processes, college information, "
                    "merit ranks, or cut-offs!"
                )

        except GuardrailViolation:
            raise
        except Exception:
            # NeMo failure must never block the user — fail open.
            logger.exception("nemo_check_failed_passthrough")

    # ── Tier 2b: OpenAI / OpenRouter Moderation API ───────────────────────────

    async def _check_moderation_api(self, text: str) -> None:
        """Call the Moderation API for semantic content safety analysis."""
        try:
            result = await self._moderation.check(text)
            if result.get("flagged", False):
                flagged_categories = [
                    cat for cat, flagged in result.get("categories", {}).items()
                    if flagged
                ]
                logger.warning(
                    "guardrail_moderation_blocked",
                    categories=flagged_categories,
                    text_preview=text[:100],
                )
                raise GuardrailViolation(
                    "Your message has been flagged by our content safety system. "
                    "Please rephrase your query."
                )
        except GuardrailViolation:
            raise
        except Exception as exc:
            # If the moderation API is down, LOG but do NOT block the user.
            # Deliberate fail-open: a moderation outage must not take down chat.
            logger.error("guardrail_moderation_api_error", error=str(exc))
