"""
FastAPI application factory.

Lifespan:
    On startup  → Initialize adapters, repository, graph, and pipeline.
    On shutdown → Clean up resources.

This is the single composition root for the entire application.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.filter_adapter import FilterAdapter
from app.adapters.llm_adapter import OpenRouterLLMAdapter
from app.adapters.rag_adapter import RAGAdapter
from app.adapters.stt_adapter import SarvamSTTAdapter
from app.adapters.tts_adapter import SarvamTTSAdapter
from app.api.middleware import RequestIDMiddleware
from app.api.v1.router import router as v1_router
from app.common.logging import get_logger, setup_logging
from app.config import get_settings
from app.orchestration.graph import build_graph
from app.repositories.redis_repository import UpstashRedisChatHistoryRepository
from app.services.input_guardrails import InputGuardrails
from app.services.pipeline_coordinator import PipelineCoordinator

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize all singletons on startup, tear down on shutdown."""
    settings = get_settings()
    setup_logging(settings.log_level)

    logger.info("startup_begin", log_level=settings.log_level)

    # ── Repository (Upstash REST — chat history persistence) ──
    repository = UpstashRedisChatHistoryRepository(settings)

    # ── Adapters ──────────────────────────────────────────────
    stt_adapter = SarvamSTTAdapter(settings)
    tts_adapter = SarvamTTSAdapter(settings)
    rag_adapter = RAGAdapter(settings)
    filter_adapter = FilterAdapter(settings)
    llm_adapter = OpenRouterLLMAdapter(settings)

    # ── LangGraph (Guard → Planner → RAG/Filter → Synthesizer) ──
    compiled_graph = build_graph(
        llm=llm_adapter,
        rag=rag_adapter,
        filter_adapter=filter_adapter,
    )

    # ── Application Services ──────────────────────────────────
    guardrails = InputGuardrails()
    pipeline = PipelineCoordinator(
        stt=stt_adapter,
        tts=tts_adapter,
        repo=repository,
        guardrails=guardrails,
        compiled_graph=compiled_graph,
    )
    app.state.pipeline = pipeline

    logger.info("startup_complete", model=settings.llm_model)

    yield  # ── Application runs here ──

    logger.info("shutdown_complete")


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Orchestrator Service",
        description="FastAPI + LangGraph chat orchestration service",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Custom Middleware ─────────────────────────────────────
    app.add_middleware(RequestIDMiddleware)

    # ── CORS ──────────────────────────────────────────────────
    # Added last so it executes first (Starlette LIFO)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────
    app.include_router(v1_router, tags=["Chat"])

    return app


# ── Module-level app instance for Uvicorn ─────────────────────
app = create_app()
