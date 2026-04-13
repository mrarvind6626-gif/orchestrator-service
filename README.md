# Orchestrator Service

A production-grade, highly robust backend orchestration service built with **FastAPI** and **LangGraph**. It acts as the backbone for the conversational UI, handling audio ingestion, speech-to-text, safety guardrails, intent routing, hybrid retrieval (Semantic RAG + Structured Filtering), and final text-to-audio synthesis.

## Features

- **Layered Architecture:** Strict separation of API, Services, Orchestration, Adapters, and Data Persistence.
- **Fast-Path Resolution:** Instantly answers trivial queries (greetings, farewells) with zero LLM latency.
- **Robust Guardrails:** Multi-layered input protection using local offline checks (regex + `better_profanity`) and OpenAI's semantic Moderation API.
- **Agentic Routing:** Uses GPT-4o via LangGraph to intelligently route queries to `rag`, `filter`, or a concurrent `hybrid` execution path.
- **Optimized Audio Delivery:** Generates real-time audio using Sarvam AI. Returns Base64 strings for tiny payloads (<500KB) and S3 presigned URLs for large files to conserve memory.
- **Stateless & Scalable:** Uses DynamoDB for ephemeral session storage with native TTL auto-deletion.
- **Production-Ready Hooks:** Includes structured JSON logging to `stdout` (via `structlog` & CloudWatch), robust retry mechanisms via `tenacity`, and multi-stage Docker builds.

---

## 🛠 Prerequisites & Environment Setup

This service requires a `.env` file at the root. Copy the template and fill in the secrets:

```bash
cp .env.example .env
```

Ensure you have credentials for:
- OpenRouter (LLM)
- Sarvam AI (STT & TTS)
- OpenAI (Moderation)
- AWS (S3 & DynamoDB)

### Database Setup

Before running the application, create the DynamoDB table:

```bash
docker compose run --rm app python -m scripts.create_dynamodb_table
```

---

## 🚀 Deployment (AWS EC2 / Docker)

The service is configured for direct deployment on an AWS EC2 instance using Docker Compose.

It deploys:
1. The **FastAPI Application** (port 8000 internally).
2. An **Nginx Reverse Proxy** (port 80 externally) handling CORS and HTTP routing.

**Build and Start:**
```bash
docker compose build
docker compose up -d
```

Logs are configured to stream directly to AWS CloudWatch using the `awslogs` driver. Make sure your EC2 instance profile has the necessary permissions.

---

## 📡 API Overview

The service exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/v1/chat` | Main conversational pipeline. Accepts `multipart/form-data` (`sessionId`, `text_query`, `audio_file`). |
| `POST` | `/v1/session/clear` | **Beacon API**: Immediately deletes session history. |
| `GET` | `/health` | Lightweight HTTP 200 health probe for load balancers. |

---

## 🧹 Hybrid Chat Retention & Beacon API

Chat history is ephemeral and stored in DynamoDB.

1. **Passive Cleanup (TTL):** Every message extends the session's `expires_at` timestamp by 30 minutes. DynamoDB automatically purges expired rows.
2. **Active Cleanup (Beacon API):** Frontend clients should actively notify the backend when the user leaves.

### 📋 Frontend Setup for Beacon API

Add this vanilla JavaScript snippet to your frontend to cleanly wipe the session history when the user closes the tab or navigates away. `navigator.sendBeacon` is a reliable way to fire a fire-and-forget payload during the page unload lifecycle.

```javascript
// Function to clear chat history on tab close
function wipeChatSession() {
  const sessionId = sessionStorage.getItem("activeSessionId");
  if (!sessionId) return;

  const url = "http://<YOUR_EC2_IP_OR_DOMAIN>/v1/session/clear";

  // sendBeacon takes a USVString, Blob, ArrayBuffer, or FormData.
  // Using Blob allows us to send application/json.
  const payload = new Blob(
    [JSON.stringify({ sessionId: sessionId })],
    { type: "application/json" }
  );

  navigator.sendBeacon(url, payload);
}

// Bind to both pagehide and beforeunload for maximum reliability across browsers
window.addEventListener("pagehide", wipeChatSession, { capture: true });
window.addEventListener("beforeunload", wipeChatSession, { capture: true });
```
