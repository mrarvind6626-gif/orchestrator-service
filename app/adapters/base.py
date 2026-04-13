"""
Abstract base classes for all external adapters.

LangGraph nodes and services depend on these interfaces — never on
concrete implementations — so that adapters can be swapped without
touching the orchestration logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# ── Result Data Classes ───────────────────────────────────────


@dataclass(frozen=True)
class RAGResult:
    """A single result from the RAG search API."""
    rank: int
    score: float
    file_name: str
    url: str
    text_preview: str


@dataclass(frozen=True)
class RAGResponse:
    """Full response from the RAG adapter."""
    status: str
    results: list[RAGResult] = field(default_factory=list)


@dataclass(frozen=True)
class FilterRecord:
    """A single result from the Filter API."""
    record_id: str
    document_name: str
    doc_url: str
    summary_text: str
    match_confidence: float


@dataclass(frozen=True)
class FilterResponse:
    """Full response from the Filter adapter."""
    status: str
    data: list[FilterRecord] = field(default_factory=list)


# ── Abstract Interfaces ──────────────────────────────────────


class STTAdapterBase(ABC):
    """Speech-to-Text adapter interface."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, content_type: str) -> tuple[str, str]:
        """Convert audio bytes to text. Returns tuple of (transcript_string, language_code)."""
        ...


class TTSAdapterBase(ABC):
    """Text-to-Speech adapter interface."""

    @abstractmethod
    async def synthesize(self, text: str, language: str | None = None) -> bytes:
        """Convert text to audio bytes (WAV/MP3). If language is provided, override default."""
        ...


class RAGAdapterBase(ABC):
    """RAG (Retrieval-Augmented Generation) search adapter interface."""

    @abstractmethod
    async def search(self, query: str) -> RAGResponse:
        """Perform semantic vector search."""
        ...


class FilterAdapterBase(ABC):
    """Structured filter/NLP search adapter interface."""

    @abstractmethod
    async def search(self, query: str) -> FilterResponse:
        """Perform structured database query."""
        ...


class LLMAdapterBase(ABC):
    """LLM chat-completion adapter interface."""

    @abstractmethod
    async def chat_completion(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Send messages and return the assistant's reply text."""
        ...


class ModerationAdapterBase(ABC):
    """Content moderation adapter interface."""

    @abstractmethod
    async def check(self, text: str) -> dict:
        """
        Check text for harmful content.
        Returns a dict with keys:  flagged (bool), categories (dict).
        """
        ...
