"""
Custom exception hierarchy for the orchestrator service.

All service-level exceptions inherit from OrchestratorError so
callers can catch a single base type when needed.
"""

from __future__ import annotations


class OrchestratorError(Exception):
    """Base exception for all orchestrator errors."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(message)
        self.detail = detail


# ── Guardrail Exceptions ──


class GuardrailViolation(OrchestratorError):
    """Raised when user input fails a guardrail check."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"Input blocked by guardrail: {reason}", detail=reason)
        self.reason = reason


# ── Adapter / Integration Exceptions ──


class AdapterError(OrchestratorError):
    """Raised when an external adapter call fails after retries."""

    def __init__(self, adapter_name: str, message: str) -> None:
        super().__init__(f"[{adapter_name}] {message}")
        self.adapter_name = adapter_name


class STTError(AdapterError):
    """Speech-to-Text adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("STT", message)


class TTSError(AdapterError):
    """Text-to-Speech adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("TTS", message)


class LLMError(AdapterError):
    """LLM adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("LLM", message)


class RAGError(AdapterError):
    """RAG API adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("RAG", message)


class FilterError(AdapterError):
    """Filter API adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("Filter", message)


class ModerationError(AdapterError):
    """OpenAI Moderation adapter failure."""

    def __init__(self, message: str) -> None:
        super().__init__("Moderation", message)


# ── Repository Exceptions ──


class RepositoryError(OrchestratorError):
    """Raised when a data persistence operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(f"[Repository] {message}")


# ── Validation Exceptions ──


class AudioValidationError(OrchestratorError):
    """Raised when the uploaded audio file fails validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
