"""
Pydantic request / response schemas for the v1 API.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Response Sub-models ───────────────────────────────────────


class SourceItem(BaseModel):
    """A single document source in the chat response."""

    rank: int = Field(..., description="Relevance rank (1 = most relevant)")
    score: float = Field(..., description="Relevance/confidence score")
    file_name: str = Field(..., description="Source document filename")
    url: str = Field(..., description="URL to the source document")
    text_preview: str = Field(..., description="Preview snippet of the source content")


# ── Chat Response ─────────────────────────────────────────────


class ChatResponse(BaseModel):
    """Response payload for POST /v1/chat."""

    answer: str = Field(..., description="The synthesized conversational response")
    session_id: str = Field(..., description="Session identifier")
    confidence: float | None = Field(None, description="Overall confidence score")
    sources: list[SourceItem] = Field(
        default_factory=list, description="Ranked source documents"
    )
    audio_base64: str | None = Field(
        None, description="Base64-encoded audio response"
    )
    execution_path: str = Field(
        ..., description="Pipeline path taken: fast_path | rag | filter | hybrid"
    )


# ── Suggested Questions ───────────────────────────────────────


class SuggestedQuestionsResponse(BaseModel):
    """Response payload for GET /v1/suggested-questions.

    All three language sets are returned at once so the frontend can switch
    languages without an additional round-trip.
    """

    en: list[str] = Field(..., description="Suggested questions in English")
    hi: list[str] = Field(..., description="Suggested questions in Hindi")
    gu: list[str] = Field(..., description="Suggested questions in Gujarati")


# ── Health ────────────────────────────────────────────────────


class HealthResponse(BaseModel):
    """Response payload for GET /health."""

    status: str = Field("healthy", description="Service health status")
    version: str = Field("1.0.0", description="Service version")
