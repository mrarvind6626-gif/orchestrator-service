"""
API v1 router — all public HTTP endpoints.

Endpoints:
    POST /v1/chat   — Main chat pipeline (multipart/form-data)
    GET  /health    — ALB / monitoring health probe
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.dependencies import get_pipeline
from app.api.v1.schemas import ChatResponse, HealthResponse, SourceItem, SuggestedQuestionsResponse
from app.services.fast_path import get_suggested_questions
from app.common.constants import ALLOWED_AUDIO_CONTENT_TYPES, ALLOWED_AUDIO_EXTENSIONS
from app.common.exceptions import (
    AudioValidationError,
    GuardrailViolation,
    OrchestratorError,
)
from app.common.logging import get_logger
from app.config import get_settings
from app.services.pipeline_coordinator import PipelineCoordinator

logger = get_logger(__name__)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════
#  POST /v1/chat
# ═══════════════════════════════════════════════════════════════


@router.post(
    "/v1/chat",
    response_model=ChatResponse,
    summary="Chat pipeline",
    description="Accept text or audio, run through the orchestration pipeline, return synthesized response.",
)
async def chat(
    sessionId: str = Form(..., description="Client session identifier"),  # noqa: N803
    text_query: str | None = Form(None, description="Text query (optional if audio provided)"),
    audio_file: UploadFile | None = File(None, description="Audio file (WEBM/MP3/WAV/OGG/M4A, max 5MB)"),
    language: str | None = Form(None, description="Sarvam TTS language code: en-IN | hi-IN | gu-IN"),
    receive_audio: bool = Form(True, description="Whether to generate and return audio response"),
    pipeline: PipelineCoordinator = Depends(get_pipeline),
):
    """Main chat endpoint — multipart/form-data."""
    settings = get_settings()

    # ── Validate inputs ───────────────────────────────────────
    if not text_query and not audio_file:
        raise HTTPException(
            status_code=400,
            detail="Either 'text_query' or 'audio_file' must be provided.",
        )

    audio_bytes: bytes | None = None
    audio_content_type: str | None = None

    if audio_file:
        # Validate content type
        audio_content_type = audio_file.content_type or ""
        if audio_content_type not in ALLOWED_AUDIO_CONTENT_TYPES:
            # Fallback: check file extension
            _, ext = os.path.splitext(audio_file.filename or "")
            if ext.lower() not in ALLOWED_AUDIO_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Unsupported audio format: {audio_content_type}. "
                        f"Allowed: WEBM, MP3, WAV, OGG, M4A."
                    ),
                )

        # Read and validate size
        audio_bytes = await audio_file.read()
        if len(audio_bytes) > settings.audio_max_size_bytes:
            raise HTTPException(
                status_code=400,
                detail=f"Audio file exceeds the {settings.audio_max_size_mb}MB limit.",
            )

        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Audio file is empty.")

    # ── Execute pipeline ──────────────────────────────────────
    try:
        result = await pipeline.execute(
            session_id=sessionId,
            text_query=text_query,
            audio_bytes=audio_bytes,
            audio_content_type=audio_content_type,
            language=language,
            receive_audio=receive_audio,
        )
    except GuardrailViolation as exc:
        raise HTTPException(status_code=422, detail=exc.reason) from exc
    except AudioValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OrchestratorError as exc:
        logger.error("pipeline_error", error=str(exc), detail=exc.detail)
        raise HTTPException(status_code=502, detail="An internal processing error occurred.") from exc
    except Exception as exc:
        logger.exception("pipeline_unexpected_error")
        raise HTTPException(status_code=500, detail="Internal server error.") from exc

    # ── Build response ────────────────────────────────────────
    return ChatResponse(
        answer=result.answer,
        session_id=result.session_id,
        confidence=result.confidence,
        sources=[SourceItem(**s) for s in result.sources],
        audio_base64=result.audio_base64,
        execution_path=result.execution_path,
    )


# ═══════════════════════════════════════════════════════════════
#  GET /v1/suggested-questions
# ═══════════════════════════════════════════════════════════════


@router.get(
    "/v1/suggested-questions",
    response_model=SuggestedQuestionsResponse,
    summary="Suggested questions",
    description="Return the list of suggested questions shown as UI chips.",
)
async def suggested_questions():
    """Return pre-defined suggested questions for the chat UI (all three languages)."""
    return SuggestedQuestionsResponse(
        en=get_suggested_questions("en-IN"),
        hi=get_suggested_questions("hi-IN"),
        gu=get_suggested_questions("gu-IN"),
    )


# ═══════════════════════════════════════════════════════════════
#  GET /health
# ═══════════════════════════════════════════════════════════════


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Lightweight health probe for ALB / monitoring.",
)
async def health():
    """Return service health status."""
    return HealthResponse(status="healthy", version="1.0.0")
