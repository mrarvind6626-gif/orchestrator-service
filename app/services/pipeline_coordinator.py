"""
Pipeline Coordinator — the conductor of the entire chat pipeline.

Orchestrates:
    1. Audio → STT (if audio provided)
    2. Input guardrails (local + semantic)
    3. Fast-path check (greetings, etc.)
    4. Chat history retrieval
    5. LangGraph invocation
    6. TTS synthesis (audio returned inline as base64)
    7. Async chat history persistence
    8. Response assembly
"""

from __future__ import annotations

import asyncio
import base64
from dataclasses import dataclass, field

from app.adapters.base import STTAdapterBase, TTSAdapterBase
from app.common.exceptions import AudioValidationError, OrchestratorError
from app.common.logging import get_logger
from app.repositories.base import ChatHistoryRepository
from app.services.fast_path import check_fast_path
from app.services.input_guardrails import InputGuardrails

logger = get_logger(__name__)


@dataclass
class PipelineResult:
    """Final result returned by the pipeline coordinator."""

    answer: str
    session_id: str
    execution_path: str
    confidence: float | None = None
    sources: list[dict] = field(default_factory=list)
    audio_base64: str | None = None


class PipelineCoordinator:
    """
    Top-level service that wires together all subsystems.

    This is the ONLY class imported by the API layer.
    """

    def __init__(
        self,
        stt: STTAdapterBase,
        tts: TTSAdapterBase,
        repo: ChatHistoryRepository,
        guardrails: InputGuardrails,
        compiled_graph,  # LangGraph CompiledGraph
    ) -> None:
        self._stt = stt
        self._tts = tts
        self._repo = repo
        self._guardrails = guardrails
        self._graph = compiled_graph

    async def execute(
        self,
        session_id: str,
        text_query: str | None = None,
        audio_bytes: bytes | None = None,
        audio_content_type: str | None = None,
        language: str | None = None,
        receive_audio: bool = True,
    ) -> PipelineResult:
        """
        Run the full chat pipeline.

        Args:
            session_id:  Client-provided session identifier.
            text_query:  Text input (mutually exclusive with audio).
            audio_bytes: Raw audio bytes (mutually exclusive with text).
            audio_content_type: MIME type of the audio file.

        Returns:
            PipelineResult with answer, base64 audio, sources, etc.
        """
        logger.info("pipeline_start", session_id=session_id)

        detected_language = None

        # ── Step 1: Audio → Text via STT ──────────────────────
        if audio_bytes and not text_query:
            logger.info("stt_start", session_id=session_id)
            text_query, detected_language = await self._stt.transcribe(
                audio_bytes, audio_content_type or "audio/webm"
            )
            logger.info("stt_complete", transcript_preview=text_query[:100], detected_language=detected_language)

        if not text_query:
            raise AudioValidationError(
                "Either text_query or audio_file must be provided."
            )

        # ── Step 2: Input Guardrails ──────────────────────────
        await self._guardrails.validate(text_query)

        # ── Step 3: Fast-Path Check ───────────────────────────
        fast_result = check_fast_path(text_query, language=language or detected_language)
        if fast_result is not None:
            logger.info("fast_path_short_circuit", category=fast_result.category)
            audio_b64 = None
            if receive_audio:
                audio_b64 = await self._process_tts(fast_result.response, session_id, language or detected_language)
            asyncio.create_task(
                self._save_exchange(session_id, text_query, fast_result.response)
            )
            return PipelineResult(
                answer=fast_result.response,
                session_id=session_id,
                execution_path="fast_path",
                audio_base64=audio_b64,
            )

        # ── Step 4: Fetch Chat History ────────────────────────
        chat_history = await self._repo.get_history(session_id)

        # ── Step 5: Invoke LangGraph ──────────────────────────
        initial_state = {
            "session_id": session_id,
            "chat_history": chat_history,
            "current_query": text_query,
        }

        logger.info("langgraph_invoke_start", session_id=session_id)
        result_state = await self._graph.ainvoke(initial_state)
        logger.info(
            "langgraph_invoke_complete",
            execution_path=result_state.get("execution_path"),
        )

        synthesized = result_state.get("synthesized_response", "")
        execution_path = result_state.get("execution_path", "unknown")
        sources = result_state.get("sources", [])
        confidence = result_state.get("confidence")

        # ── Step 6: TTS → inline base64 ──────────────────────
        audio_b64 = None
        if receive_audio:
            audio_b64 = await self._process_tts(synthesized, session_id, language or detected_language)

        # ── Step 7: Async History Persistence ─────────────────
        asyncio.create_task(
            self._save_exchange(session_id, text_query, synthesized)
        )

        # ── Step 8: Assemble Response ─────────────────────────
        logger.info("pipeline_complete", session_id=session_id, path=execution_path)
        return PipelineResult(
            answer=synthesized,
            session_id=session_id,
            execution_path=execution_path,
            confidence=confidence,
            sources=sources,
            audio_base64=audio_b64,
        )

    # ── Private Helpers ───────────────────────────────────────

    async def _process_tts(
        self, text: str, session_id: str, language: str | None = None
    ) -> str | None:
        """
        Generate TTS audio and return it as a base64-encoded string.

        Audio is always handled in memory — no external storage used.
        Returns None if TTS fails (non-blocking).
        """
        try:
            audio_bytes = await self._tts.synthesize(text, language)
        except OrchestratorError:
            logger.warning("tts_failed_graceful", session_id=session_id)
            return None

        encoded = base64.b64encode(audio_bytes).decode("utf-8")
        logger.info("audio_inline", size_bytes=len(audio_bytes))
        return encoded

    async def _save_exchange(
        self, session_id: str, user_query: str, assistant_response: str
    ) -> None:
        """Fire-and-forget: append the user/assistant exchange to history."""
        try:
            messages = [
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": assistant_response},
            ]
            await self._repo.append_history(session_id, messages)
        except Exception as exc:
            # Never let a history-save failure crash the pipeline
            logger.error(
                "history_save_failed",
                session_id=session_id,
                error=str(exc),
            )
