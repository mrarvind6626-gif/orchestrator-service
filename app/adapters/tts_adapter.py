"""
Sarvam AI Text-to-Speech adapter (bulbul:v3).

Sends a JSON POST and extracts the base64 audio from the ``audios`` array.
"""

from __future__ import annotations

import base64

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import TTSAdapterBase
from app.common.exceptions import TTSError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)


class SarvamTTSAdapter(TTSAdapterBase):
    """Concrete TTS adapter calling Sarvam AI bulbul:v3."""

    def __init__(self, settings: Settings) -> None:
        self._url = settings.sarvam_tts_url
        self._api_key = settings.sarvam_api_key
        self._model = settings.sarvam_tts_model
        self._language = settings.sarvam_tts_language
        self._speaker = settings.sarvam_tts_speaker
        self._timeout = httpx.Timeout(30.0, connect=10.0)

    async def synthesize(self, text: str, language: str | None = None) -> bytes:
        """Convert text to audio bytes via Sarvam TTS."""
        return await self._call_tts(text, language)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_tts(self, text: str, language: str | None = None) -> bytes:
        """Retryable TTS HTTP call."""
        target_language = language if language else self._language
        payload = {
            "text": text,
            "target_language_code": target_language,
            "model": self._model,
            "speaker": self._speaker,
            "pace": 1.0,
            "output_audio_codec": "wav",
        }

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    self._url,
                    headers={
                        "api-subscription-key": self._api_key,
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )
                response.raise_for_status()

            data = response.json()
            audios = data.get("audios")

            if not audios or not audios[0]:
                raise TTSError("Sarvam TTS returned no audio data")

            audio_bytes = base64.b64decode(audios[0])
            logger.info(
                "tts_success",
                text_length=len(text),
                audio_bytes=len(audio_bytes),
            )
            return audio_bytes

        except httpx.HTTPStatusError as exc:
            logger.error(
                "tts_http_error",
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("tts_transport_error", error=str(exc))
            raise
        except TTSError:
            raise
        except Exception as exc:
            raise TTSError(f"Unexpected TTS error: {exc}") from exc
