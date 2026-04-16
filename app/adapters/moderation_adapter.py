"""
OpenRouter moderation adapter (Guardrails Layer 2).

Uses OpenRouter's chat-completion endpoint with openai/gpt-4o-mini to
classify whether a message contains harmful content.  The model returns a
structured JSON verdict that matches the same interface expected by
InputGuardrails, so no other code needs to change.

Model choice — openai/gpt-4o-mini:
    Fast, low-cost, and accurate enough for binary safety classification.
    Already routed through OpenRouter, so no separate API key is needed.
"""

from __future__ import annotations

import json

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import ModerationAdapterBase
from app.common.exceptions import ModerationError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)

_MODERATION_SYSTEM_PROMPT = (
    "You are a content safety classifier for an official government education portal.\n"
    "Analyze the user message and return ONLY a JSON object — no markdown, no extra text.\n\n"
    "Required format:\n"
    '{"flagged": <true|false>, "categories": {"hate": <bool>, "violence": <bool>, '
    '"sexual": <bool>, "self_harm": <bool>, "harassment": <bool>}}\n\n'
    "Rules:\n"
    "- Set flagged=true ONLY for genuinely harmful, abusive, violence, or dangerous content.\n"
    "- If the message contains ANY words related to 'admission', 'cutoff', 'rank', 'college', "
    "or 'documents', you MUST set flagged=false NO MATTER WHAT.\n"
    "- Do not flag queries with missing context or informal academic questions.\n"
    "- Respond with the JSON object and nothing else."
)


class OpenRouterModerationAdapter(ModerationAdapterBase):
    """Content moderation via OpenRouter chat-completion (gpt-4o-mini)."""

    def __init__(self, settings: Settings) -> None:
        self._url = f"{settings.openrouter_base_url.rstrip('/')}/chat/completions"
        self._api_key = settings.openrouter_api_key
        self._timeout = httpx.Timeout(15.0, connect=5.0)

    async def check(self, text: str) -> dict:
        """
        Classify text for harmful content.

        Returns:
            {"flagged": bool, "categories": {"hate": bool, "violence": bool, ...}}
        """
        return await self._call_moderation(text)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_moderation(self, text: str) -> dict:
        """Retryable moderation call via OpenRouter chat completions."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": _MODERATION_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            "temperature": 0.0,
            "max_tokens": 128,
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(self._url, json=payload, headers=headers)
                response.raise_for_status()

            raw = response.json()
            content = raw["choices"][0]["message"]["content"].strip()

            # Strip accidental markdown fences if the model adds them
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                content = content.rsplit("```", 1)[0]

            verdict = json.loads(content)
            flagged = bool(verdict.get("flagged", False))
            categories = verdict.get("categories", {})

            logger.info("moderation_check", flagged=flagged)
            return {"flagged": flagged, "categories": categories}

        except (json.JSONDecodeError, KeyError) as exc:
            # If the model returns unparseable output, fail open (don't block user).
            logger.error("moderation_parse_error", error=str(exc))
            return {"flagged": False, "categories": {}}
        except httpx.HTTPStatusError as exc:
            logger.error(
                "moderation_http_error",
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("moderation_transport_error", error=str(exc))
            raise
        except Exception as exc:
            raise ModerationError(f"Unexpected moderation error: {exc}") from exc
