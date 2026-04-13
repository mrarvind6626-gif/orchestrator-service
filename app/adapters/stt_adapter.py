"""
Sarvam AI Speech-to-Text adapter (saaras:v3).

Uses multipart/form-data as required by the Sarvam STT API.
"""

from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import STTAdapterBase
from app.common.exceptions import STTError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)


class SarvamSTTAdapter(STTAdapterBase):
    """Concrete STT adapter calling Sarvam AI saaras:v3."""

    def __init__(self, settings: Settings) -> None:
        self._url = settings.sarvam_stt_url
        self._api_key = settings.sarvam_api_key
        self._model = settings.sarvam_stt_model
        self._language = settings.sarvam_stt_language
        self._timeout = httpx.Timeout(30.0, connect=10.0)
        self._max_attempts = settings.retry_max_attempts
        self._min_wait = settings.retry_min_wait_seconds
        self._max_wait = settings.retry_max_wait_seconds

    async def transcribe(self, audio_bytes: bytes, content_type: str) -> tuple[str, str]:
        """Send audio to Sarvam STT and return the transcript and language code."""
        return await self._call_stt(audio_bytes, content_type)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_stt(self, audio_bytes: bytes, content_type: str) -> tuple[str, str]:
        """Retryable STT HTTP call."""
        # Determine file extension from content type
        ext_map = {
            "audio/webm": "audio.webm",
            "audio/mp3": "audio.mp3",
            "audio/mpeg": "audio.mp3",
            "audio/wav": "audio.wav",
            "audio/x-wav": "audio.wav",
            "audio/ogg": "audio.ogg",
            "audio/m4a": "audio.m4a",
            "audio/x-m4a": "audio.m4a",
            "audio/mp4": "audio.m4a",
        }
        filename = ext_map.get(content_type, "audio.webm")

        sarvam_language_code = "unknown" if self._language.lower() == "auto" else self._language

        if self._language.lower() == "auto":
            logger.info("STT mode: AUTO (language will be inferred)")
        else:
            logger.info("STT mode: MANUAL", language=self._language)

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    self._url,
                    headers={"api-subscription-key": self._api_key},
                    files={"file": (filename, audio_bytes, content_type)},
                    data={
                        "model": self._model,
                        "mode": "transcribe",
                        "language_code": sarvam_language_code,
                    },
                )
                response.raise_for_status()

            payload = response.json()
            transcript = payload.get("transcript", "").strip()
            detected_lang = payload.get("language_code", "unknown")

            if not transcript:
                raise STTError("Sarvam STT returned an empty transcript")

            logger.info(
                "stt_success",
                transcript_length=len(transcript),
                language=detected_lang,
            )
            return transcript, detected_lang

        except httpx.HTTPStatusError as exc:
            logger.error(
                "stt_http_error",
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("stt_transport_error", error=str(exc))
            raise
        except STTError:
            raise
        except Exception as exc:
            raise STTError(f"Unexpected STT error: {exc}") from exc
