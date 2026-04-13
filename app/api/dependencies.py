"""
FastAPI dependency injection.

Pulls initialized singletons from ``app.state`` (set during lifespan)
and exposes them via ``Depends()`` for clean endpoint signatures.
"""

from __future__ import annotations

from fastapi import Request

from app.services.pipeline_coordinator import PipelineCoordinator


def get_pipeline(request: Request) -> PipelineCoordinator:
    """Inject the PipelineCoordinator singleton."""
    return request.app.state.pipeline
