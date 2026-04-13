"""Unit tests for the orchestration LangGraph."""

from __future__ import annotations

import pytest

from app.adapters.base import RAGResponse, RAGResult, FilterResponse, FilterRecord
from app.orchestration.graph import build_graph


class MockLLMAdapter:
    async def chat_completion(self, messages: list[dict], **kwargs) -> str:
        # If executing planner prompt:
        if "query planner" in messages[0]["content"].lower():
            return '{"rag_query": "semantic query", "filter_query": "structured query"}'
        
        # If executing synthesis prompt
        return "This is the synthesized final response."


class MockRAGAdapter:
    async def search(self, query: str, top_k: int = 3) -> RAGResponse:
        return RAGResponse(
            status="success",
            results=[
                RAGResult(rank=1, score=0.9, file_name="doc.pdf", url="http://x", text_preview="Semantic data")
            ]
        )


class MockFilterAdapter:
    async def search(self, query: str) -> FilterResponse:
        return FilterResponse(
            status="success",
            data=[
                FilterRecord(record_id="123", document_name="doc2.pdf", doc_url="http://y", summary_text="Structured data", match_confidence=0.95)
            ]
        )


@pytest.fixture
def compiled_graph():
    return build_graph(MockLLMAdapter(), MockRAGAdapter(), MockFilterAdapter())


@pytest.mark.asyncio
async def test_graph_concurrent_routing(compiled_graph):
    initial_state = {
        "session_id": "test-123",
        "chat_history": [],
        "current_query": "Show me Rank 2 requirements for the Sales department."
    }

    result = await compiled_graph.ainvoke(initial_state)

    assert result["rag_query"] == "semantic query"
    assert result["filter_query"] == "structured query"
    assert result["execution_path"] == "hybrid"
    
    assert len(result["rag_results"]) == 1
    assert len(result["filter_results"]) == 1
    assert result["synthesized_response"] == "This is the synthesized final response."
    
    # Confidence should be average of RAG (0.9) and Filter (0.95)
    assert result["confidence"] == 0.925
    # Sources should be merged and reranked
    assert len(result["sources"]) == 2
    assert result["sources"][0]["score"] == 0.95
    assert result["sources"][0]["rank"] == 1
    assert result["sources"][1]["score"] == 0.9
    assert result["sources"][1]["rank"] == 2
