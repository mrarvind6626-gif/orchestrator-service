"""
LangGraph state definition.

The ``messages`` field uses the ``add_messages`` reducer so that the
Redis checkpointer can implicitly manage conversation history —
each invocation only needs to send the new user message and the
reducer merges it with the persisted history.
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class OrchestratorState(TypedDict, total=False):
    """Shared state flowing through the LangGraph pipeline."""

    # ── Conversation (managed by checkpointer) ────────────
    messages: Annotated[list, add_messages]

    # ── Session metadata ──────────────────────────────────
    session_id: str
    current_query: str

    # ── Guard node output (safety + relevance in one call) ──
    guard_verdict: str             # "pass" | "unsafe" | "off_topic"

    # ── Planner output ────────────────────────────────────
    rag_query: str | None
    filter_query: str | None
    execution_path: str            # "rag" | "filter" | "hybrid" | "guardrail_blocked"

    # ── Retrieval outputs ─────────────────────────────────
    rag_results: list[dict]
    filter_results: list[dict]

    # ── Synthesis outputs ─────────────────────────────────
    synthesized_response: str
    sources: list[dict]
    confidence: float | None

    # ── Errors (accumulated across concurrent nodes) ──────
    errors: Annotated[list[str], operator.add]
