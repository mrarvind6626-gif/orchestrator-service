"""
RAG (semantic search) external API adapter.

Calls the stateless RAG service with a single query string.
"""

from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import RAGAdapterBase, RAGResponse, RAGResult
from app.common.exceptions import RAGError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)


class RAGAdapter(RAGAdapterBase):
    """Concrete adapter for the external RAG search API."""

    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.rag_api_base_url.rstrip("/")
        self._timeout = httpx.Timeout(30.0, connect=10.0)

    async def search(self, query: str, session_id: str | None = None) -> RAGResponse:
        """Perform semantic vector search via the RAG API."""
        return await self._call_rag(query, session_id)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_rag(self, query: str, session_id: str | None = None) -> RAGResponse:
        """Retryable RAG HTTP call."""
        url = f"{self._base_url}/api/retrieve"
        payload: dict = {
            "query": query,
            "top_k": 5
        }

        logger.info("rag_request", url=url, payload=payload)

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            data = response.json()
            logger.info(
                "rag_response",
                status_code=response.status_code,
                chunk_count=len(data.get("chunks", [])),
            )

            results = []
            for idx, chunk in enumerate(data.get("chunks", []), start=1):
                meta = chunk.get("metadata", {})
                results.append(
                    RAGResult(
                        rank=idx,
                        score=chunk.get("score", 0.0),
                        file_name=meta.get("file_name", ""),
                        url=meta.get("url", ""),
                        text_preview=chunk.get("text", ""),
                    )
                )

            logger.info("rag_search_success", result_count=len(results))
            return RAGResponse(status="success", results=results)

        except httpx.HTTPStatusError as exc:
            logger.error(
                "rag_http_error",
                url=url,
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("rag_transport_error", url=url, error=str(exc))
            raise
        except Exception as exc:
            raise RAGError(f"Unexpected RAG error: {exc}") from exc
