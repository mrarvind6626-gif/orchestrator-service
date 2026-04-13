"""
LangGraph state definition.
"""
from __future__ import annotations

import operator
from typing import Annotated, TypedDict

class OrchestratorState(TypedDict, total=False):
    """Shared state flowing through the LangGraph pipeline."""

    # ── Inputs ─────────────────────────────────────────
    session_id: str
    chat_history: list[dict]       
    current_query: str

    # ── Planner Output ─────────────────────────────────
    rag_query: str | None
    filter_query: str | None
    execution_path: str            # "rag" | "filter" | "hybrid"

    # ── Retrieval outputs ──────────────────────────────
    rag_results: list[dict]        
    filter_results: list[dict]     

    # ── Synthesis outputs ──────────────────────────────
    synthesized_response: str      
    sources: list[dict]            
    confidence: float | None       
    
    # ── Errors ─────────────────────────────────────────
    errors: Annotated[list[str], operator.add]
