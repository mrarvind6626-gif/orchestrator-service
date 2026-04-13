"""Unit test for the Pipeline Coordinator."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock

from app.services.pipeline_coordinator import PipelineCoordinator
from app.services.input_guardrails import InputGuardrails
from app.config import Settings


class MockSTT:
    async def transcribe(self, audio_bytes: bytes, content_type: str) -> tuple[str, str]:
        return "Test audio query", "hi-IN"

class MockTTS:
    async def synthesize(self, text: str, language: str | None = None) -> bytes:
        return b"fake_audio_bytes_under_500kb"

class MockS3:
    async def upload_audio(self, *args, **kwargs) -> str:
        return "https://s3.amazonaws.com/test/presigned"

class MockRepo:
    async def get_history(self, session_id: str) -> list[dict]:
        return []
    async def append_history(self, session_id: str, messages: list[dict]) -> None:
        pass


@pytest.fixture
def coordinator():
    settings = Settings(
        openrouter_api_key="test",
        sarvam_api_key="test",
        openai_api_key="test",
        rag_api_base_url="http://rag",
        filter_api_base_url="http://filter",
        aws_s3_bucket_name="test"
    )
    guardrails = AsyncMock(spec=InputGuardrails)
    graph = AsyncMock()
    graph.ainvoke.return_value = {
        "execution_path": "rag",
        "synthesized_response": "Graph Answer",
        "sources": [],
        "confidence": 0.8
    }

    return PipelineCoordinator(
        settings=settings,
        stt=MockSTT(),
        tts=MockTTS(),
        s3=MockS3(),
        repo=MockRepo(),
        guardrails=guardrails,
        compiled_graph=graph
    )


@pytest.mark.asyncio
async def test_coordinator_text_flow(coordinator):
    result = await coordinator.execute(
        session_id="session-1",
        text_query="Test query"
    )

    assert result.execution_path == "rag"
    assert result.answer == "Graph Answer"
    assert result.session_id == "session-1"
    # Audio is under 500KB (it's fake bytes) so it returns base64
    assert result.audio_base64 is not None
    assert result.audio_url is None

@pytest.mark.asyncio
async def test_coordinator_fast_path(coordinator):
    result = await coordinator.execute(
        session_id="session-2",
        text_query="hi"
    )
    
    assert result.execution_path == "fast_path"
    assert "Hello" in result.answer
