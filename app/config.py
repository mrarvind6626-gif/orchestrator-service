"""
Application settings loaded from environment variables.

Uses pydantic-settings for type-safe, validated configuration.
Fails fast on startup if required variables are missing.
"""

from __future__ import annotations

from urllib.parse import urlparse

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration — every external knob lives here."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── LLM (OpenRouter) ──────────────────────────────────────
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "openai/gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 2048

    # ── Sarvam AI (STT) ───────────────────────────────────────
    sarvam_api_key: str
    sarvam_stt_url: str = "https://api.sarvam.ai/speech-to-text"
    sarvam_stt_model: str = "saaras:v3"
    sarvam_stt_language: str = "auto"

    # ── Sarvam AI (TTS) ───────────────────────────────────────
    sarvam_tts_url: str = "https://api.sarvam.ai/text-to-speech"
    sarvam_tts_model: str = "bulbul:v3"
    sarvam_tts_language: str = "hi-IN"
    sarvam_tts_speaker: str = "shubh"

    # ── External APIs ─────────────────────────────────────────
    rag_api_base_url: str = "https://welcometofightclub-acpc-testing-5.hf.space"
    filter_api_base_url: str = "https://orchestrator-production-1d43.up.railway.app"

    # ── Upstash Redis ─────────────────────────────────────────
    upstash_redis_rest_url: str = "https://magical-vulture-85269.upstash.io"
    upstash_redis_rest_token: str = "gQAAAAAAAU0VAAIncDJhMWQxYTYzOGU4MTk0MWE3YWE3ZTY5Mzk3NjUzNDczMHAyODUyNjk"

    # ── Application Tuning ────────────────────────────────────
    chat_history_ttl_minutes: int = 30
    audio_max_size_mb: int = 5

    # ── CORS ──────────────────────────────────────────────────
    cors_allowed_origins: str = "*"

    # ── Logging ───────────────────────────────────────────────
    log_level: str = "INFO"

    # ── Adapter Resilience ────────────────────────────────────
    retry_max_attempts: int = 3
    retry_min_wait_seconds: float = 1.0
    retry_max_wait_seconds: float = 10.0

    @property
    def audio_max_size_bytes(self) -> int:
        return self.audio_max_size_mb * 1024 * 1024

    @property
    def upstash_redis_url(self) -> str:
        """Standard Redis URL for the LangGraph checkpointer (derived from REST credentials)."""
        host = urlparse(self.upstash_redis_rest_url).hostname
        return f"rediss://default:{self.upstash_redis_rest_token}@{host}:6379"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]


# ── Singleton accessor ────────────────────────────────────────
_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
