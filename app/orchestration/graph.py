"""
LangGraph graph definition using Planner -> Concurrent RAG/Filter -> Synthesizer pattern.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, List

from langgraph.graph import END, START, StateGraph
from app.common.constants import ROUTER_SYSTEM_PROMPT
from app.common.constants import SYNTHESIS_SYSTEM_PROMPT
from app.adapters.base import (
    FilterAdapterBase,
    LLMAdapterBase,
    RAGAdapterBase,
)
from app.common.logging import get_logger
from app.orchestration.state import OrchestratorState

logger = get_logger(__name__)

# ═══════════════════════════════════════════════════════════════
#  Node Functions
# ═══════════════════════════════════════════════════════════════

def _build_planner_node(llm: LLMAdapterBase):
    async def planner_node(state: OrchestratorState) -> dict[str, Any]:
        """Analyzes the query and extracts specific sub-queries for RAG and Filter."""
        logger.info("planner_node_start", query=state["current_query"])
        
        try:
            messages = [
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                {"role": "user", "content": state["current_query"]},
            ]
            raw = await llm.chat_completion(messages, temperature=0.0, max_tokens=256)
            
            # Clean possible markdown block
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()

            plan = json.loads(cleaned)
            rag_query = plan.get("rag_query")
            filter_query = plan.get("filter_query")
            
            # Set the execution path for logging upstream
            path = "hybrid" if (rag_query and filter_query) else ("rag" if rag_query else ("filter" if filter_query else "unknown"))
            
            return {
                "rag_query": rag_query,
                "filter_query": filter_query,
                "execution_path": path
            }
            
        except Exception as e:
            logger.error("planner_error", error=str(e))
            return {"errors": [f"Planner Error: {str(e)}"]}

    return planner_node


def route_queries(state: OrchestratorState) -> List[str]:
    """Dynamically route to multiple destinations if necessary via Fan-Out."""
    if state.get("errors"):
        return [END]

    destinations = []
    if state.get("rag_query"):
        destinations.append("rag_node")
    if state.get("filter_query"):
        destinations.append("filter_node")
        
    return destinations if destinations else [END]


def _build_rag_node(rag: RAGAdapterBase):
    async def rag_node(state: OrchestratorState) -> dict[str, Any]:
        """Worker node performing semantic retrieval."""
        query = state.get("rag_query")
        if not query:
            return {}
            
        try:
            result = await rag.search(query, session_id=state.get("session_id"))
            results_dicts = [asdict(r) for r in result.results]
            return {"rag_results": results_dicts}
        except Exception as e:
            return {"errors": [f"RAG API Error: {str(e)}"]}

    return rag_node


def _build_filter_node(filter_adapter: FilterAdapterBase):
    async def filter_node(state: OrchestratorState) -> dict[str, Any]:
        """Worker node performing structured statistical filtering."""
        query = state.get("filter_query")
        if not query:
            return {}
            
        try:
            result = await filter_adapter.search(query)
            data_dicts = [asdict(r) for r in result.data]
            return {"filter_results": data_dicts}
        except Exception as e:
            return {"errors": [f"Filter API Error: {str(e)}"]}

    return filter_node


def _build_synthesizer_node(llm: LLMAdapterBase):
    async def synthesize_node(state: OrchestratorState) -> dict[str, Any]:
        """Synthesizes final answers based on aggregated data."""
        if state.get("errors") and not state.get("rag_results") and not state.get("filter_results"):
            return {"synthesized_response": "I'm sorry, I encountered an internal error and couldn't process your request."}
        
        # Build Context String
        context = f"Original Query: {state['current_query']}\n\n"
        
        rag_res = state.get("rag_results", [])
        if rag_res:
            context += f"Documentation Data (RAG):\n{json.dumps(rag_res, indent=2)}\n\n"
            
        filter_res = state.get("filter_results", [])
        if filter_res:
            context += f"Statistical/Structured Data (Filter):\n{json.dumps(filter_res, indent=2)}\n\n"

        history_str = _format_history(state.get("chat_history", []))
        if history_str:
            context += f"Chat History:\n{history_str}\n"

        messages = [
            {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
            {"role": "user", "content": context},
        ]
        
        try:
            response = await llm.chat_completion(messages)
            
            # Formats logic for generic downstream handlers
            sources = _merge_sources(rag_res, filter_res)
            confidence = _compute_confidence(rag_res, filter_res)
            
            return {
                "synthesized_response": response,
                "sources": sources,
                "confidence": confidence
            }
        except Exception as e:
            logger.error("synthesize_error", error=str(e))
            return {"synthesized_response": "Data was retrieved, but I failed to format it."}

    return synthesize_node

# ═══════════════════════════════════════════════════════════════
#  Graph Builder
# ═══════════════════════════════════════════════════════════════

def build_graph(
    llm: LLMAdapterBase,
    rag: RAGAdapterBase,
    filter_adapter: FilterAdapterBase,
):
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("planner", _build_planner_node(llm))
    workflow.add_node("rag_node", _build_rag_node(rag))
    workflow.add_node("filter_node", _build_filter_node(filter_adapter))
    workflow.add_node("synthesizer", _build_synthesizer_node(llm))

    workflow.add_edge(START, "planner")

    workflow.add_conditional_edges(
        "planner",
        route_queries,
        ["rag_node", "filter_node", END]
    )

    workflow.add_edge("rag_node", "synthesizer")
    workflow.add_edge("filter_node", "synthesizer")
    workflow.add_edge("synthesizer", END)

    compiled = workflow.compile()
    logger.info("langgraph_compiled_with_query_extraction_nodes")
    return compiled


# ═══════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════

def _format_history(history: list[dict]) -> str:
    if not history:
        return ""
    lines: list[str] = []
    for msg in history[-10:]:
        role = msg.get("role", "unknown").capitalize()
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)

def _merge_sources(rag_results: list[dict], filter_results: list[dict]) -> list[dict]:
    sources: list[dict] = []
    rank = 1

    for r in rag_results:
        sources.append({
            "rank": rank,
            "score": r.get("score", 0.0),
            "file_name": r.get("file_name", ""),
            "url": r.get("url", ""),
            "text_preview": r.get("text_preview", ""),
        })
        rank += 1

    for r in filter_results:
        sources.append({
            "rank": rank,
            "score": r.get("match_confidence", 0.0),
            "file_name": r.get("document_name", ""),
            "url": r.get("doc_url", ""),
            "text_preview": r.get("summary_text", ""),
        })
        rank += 1

    sources.sort(key=lambda s: s.get("score", 0.0), reverse=True)
    for i, s in enumerate(sources, 1):
        s["rank"] = i

    return sources

def _compute_confidence(rag_results: list[dict], filter_results: list[dict]) -> float | None:
    scores: list[float] = []
    for r in rag_results:
        if "score" in r:
            scores.append(float(r["score"]))
    for r in filter_results:
        if "match_confidence" in r:
            scores.append(float(r["match_confidence"]))

    if not scores:
        return None
    return round(sum(scores) / len(scores), 4)
