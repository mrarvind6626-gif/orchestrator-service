"""
Custom FastAPI middleware.

RequestIDMiddleware:
    Generates a unique request ID for every inbound request and binds
    it to structlog's context variables so it appears in all log entries
    for that request.  Also logs the request summary (method, path,
    status, duration).
"""

from __future__ import annotations

import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.common.logging import get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a unique request ID to every request and log request metrics."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
        start = time.perf_counter()

        # Bind request_id to structlog context for all loggers in this request
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            status = response.status_code if response else 500
            logger.info(
                "request_complete",
                method=request.method,
                path=str(request.url.path),
                status_code=status,
                duration_ms=duration_ms,
            )
            # Set the request ID on the response for traceability
            if response:
                response.headers["X-Request-ID"] = request_id
