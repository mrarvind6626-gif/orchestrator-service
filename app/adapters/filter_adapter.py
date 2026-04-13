"""
Filter (structured NLP search) external API adapter.

Calls the stateless Filter service with a query string.
"""

from __future__ import annotations

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.adapters.base import FilterAdapterBase, FilterRecord, FilterResponse
from app.common.exceptions import FilterError
from app.common.logging import get_logger
from app.config import Settings

logger = get_logger(__name__)


class FilterAdapter(FilterAdapterBase):
    """Concrete adapter for the external Filter search API."""

    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.filter_api_base_url.rstrip("/")
        self._timeout = httpx.Timeout(30.0, connect=10.0)

    async def search(self, query: str) -> FilterResponse:
        """Perform structured NLP search via the Filter API."""
        return await self._call_filter(query)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TransportError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_filter(self, query: str) -> FilterResponse:
        """Retryable Filter HTTP call."""
        url = f"{self._base_url}/api/query"
        payload = {"query": query}

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            data = response.json()
            records = [
                FilterRecord(
                    record_id=r.get("record_id", ""),
                    document_name=r.get("document_name", ""),
                    doc_url=r.get("doc_url", ""),
                    summary_text=r.get("summary_text", ""),
                    match_confidence=r.get("match_confidence", 0.0),
                )
                for r in data.get("data", [])
            ]

            logger.info("filter_search_success", record_count=len(records))
            return FilterResponse(status=data.get("status", "success"), data=records)

        except httpx.HTTPStatusError as exc:
            logger.error(
                "filter_http_error",
                status_code=exc.response.status_code,
                body=exc.response.text[:500],
            )
            raise
        except httpx.TransportError as exc:
            logger.error("filter_transport_error", error=str(exc))
            raise
        except Exception as exc:
            raise FilterError(f"Unexpected Filter error: {exc}") from exc
