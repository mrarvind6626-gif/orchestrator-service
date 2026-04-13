"""Unit tests for input guardrails."""

from __future__ import annotations

import pytest

from app.common.exceptions import GuardrailViolation
from app.services.input_guardrails import InputGuardrails


# Mocking the Moderation Adapter for unit tests
class MockModerationAdapter:
    async def check(self, text: str) -> dict:
        return {"flagged": False, "categories": {}}


@pytest.fixture
def guardrails() -> InputGuardrails:
    return InputGuardrails(MockModerationAdapter())


@pytest.mark.asyncio
async def test_guardrails_pass(guardrails: InputGuardrails, sample_normal_queries: list[str]) -> None:
    for query in sample_normal_queries:
        # Should not raise any exception
        await guardrails.validate(query)


@pytest.mark.asyncio
async def test_guardrails_prompt_injection(
    guardrails: InputGuardrails, sample_injection_queries: list[str]
) -> None:
    for query in sample_injection_queries:
        with pytest.raises(GuardrailViolation) as exc_info:
            await guardrails.validate(query)
        assert "cannot be processed" in exc_info.value.reason


@pytest.mark.asyncio
async def test_guardrails_profanity(guardrails: InputGuardrails) -> None:
    profane_queries = [
        "this is some bullshit",
        "fuck off",
        "you are a bitch",
    ]
    for query in profane_queries:
        with pytest.raises(GuardrailViolation) as exc_info:
            await guardrails.validate(query)
        assert "inappropriate language" in exc_info.value.reason
