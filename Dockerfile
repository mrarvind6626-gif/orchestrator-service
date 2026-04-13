# ══════════════════════════════════════════════════════════════
#  Stage 1: Dependencies
# ══════════════════════════════════════════════════════════════
FROM python:3.12-slim AS builder

WORKDIR /build

# Install system deps needed for some Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ══════════════════════════════════════════════════════════════
#  Stage 2: Production Runtime
# ══════════════════════════════════════════════════════════════
FROM python:3.12-slim AS runtime

# Security: run as non-root
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/

# Copy NeMo Guardrails config (Colang flows + model config)
COPY core/ ./core/

# Ensure the user owns the app directory
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run with extended keep-alive for long GenAI requests
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--timeout-keep-alive", "75", \
     "--workers", "1", \
     "--log-level", "warning"]
