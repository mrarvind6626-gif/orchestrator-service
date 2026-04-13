"""
LLM adapter using OpenRouter (OpenAI-compatible API).

Routes all LLM calls (router classification + synthesis) through
the OpenRouter gateway targeting ``openai/gpt-4o``.
"""

from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import LLMAdapterBase
from app.common.exceptions import LLMError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)


class OpenRouterLLMAdapter(LLMAdapterBase):
    """Concrete LLM adapter calling OpenRouter's chat/completions endpoint."""

    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.openrouter_base_url.rstrip("/")
        self._api_key = settings.openrouter_api_key
        self._model = settings.llm_model
        self._default_temperature = settings.llm_temperature
        self._default_max_tokens = settings.llm_max_tokens
        self._timeout = httpx.Timeout(60.0, connect=10.0)

    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send messages to OpenRouter and return the assistant's reply."""
        return await self._call_llm(
            messages,
            temperature=temperature or self._default_temperature,
            max_tokens=max_tokens or self._default_max_tokens,
        )

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_llm(
        self,
        messages: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Retryable LLM HTTP call."""
        url = f"{self._base_url}/chat/completions"
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orchestrator-service.internal",
            "X-Title": "Orchestrator Service",
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                raise LLMError("OpenRouter returned no choices")

            content = choices[0].get("message", {}).get("content", "").strip()
            if not content:
                raise LLMError("OpenRouter returned empty content")

            usage = data.get("usage", {})
            logger.info(
                "llm_completion_success",
                model=self._model,
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
            )
            return content

        except httpx.HTTPStatusError as exc:
            logger.error(
                "llm_http_error",
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("llm_transport_error", error=str(exc))
            raise
        except LLMError:
            raise
        except Exception as exc:
            raise LLMError(f"Unexpected LLM error: {exc}") from exc
