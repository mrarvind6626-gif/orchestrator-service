"""
Standalone test script for NeMo Guardrails — Allowlist / Catch-All strategy.

This script:
  1. Loads the OPENAI_API_KEY securely from a .env file (never hardcoded).
  2. Initialises NeMo Guardrails from the config directory (config.yml + rails.co).
  3. Runs two test queries:
       a) A valid ACPC admission query  -> should PASS (on-topic)
       b) An off-topic query            -> should be BLOCKED (catch-all fires)

HOW IT WORKS:
  - NeMo reads config.yml to know which LLM to use (gpt-4o-mini via OpenAI).
  - NeMo reads rails.co to load the intent definitions and flows.
  - For each user message, NeMo's internal LLM classifies the intent.
  - If the intent matches "ask acpc admission", the "allow acpc queries" flow
    fires and returns the on-topic bot response.
  - If the intent does NOT match any defined intent, the catch-all flow
    fires (via the `user ...` wildcard) and returns the hardcoded refusal.

USAGE:
  1. Ensure your .env file has OPENAI_API_KEY set:
       OPENAI_API_KEY=sk-...
  2. Install dependencies:
       pip install nemoguardrails python-dotenv
  3. Run from the orchestrator-service directory:
       python app_nemo_test.py

NOTE: This script is for testing/demonstration only.  In production, NeMo is
      invoked via InputGuardrails._check_nemo() in app/services/input_guardrails.py.
"""

from __future__ import annotations

import asyncio
import os
import sys

# ---------------------------------------------------------------------------
# 1. LOAD API KEY SECURELY FROM .env
# ---------------------------------------------------------------------------
# We use python-dotenv to read OPENAI_API_KEY from the .env file.
# The key is NEVER hardcoded in source code.
#
# If the project uses OPENROUTER_API_KEY instead of OPENAI_API_KEY, we bridge
# it automatically (same pattern as input_guardrails.py).
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is required.  Install with: pip install python-dotenv")
    sys.exit(1)

# Load .env from the orchestrator-service root directory
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path)

# Bridge: if OPENROUTER_API_KEY is set, ALWAYS map it to OPENAI_API_KEY.
# This overwrites any placeholder "sk-xxxxxxxxxxxx" value that may exist in .env.
# NeMo's internal LangChain client reads OPENAI_API_KEY and OPENAI_API_BASE.
openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
openrouter_url = os.getenv("OPENROUTER_BASE_URL", "")
if openrouter_key:
    os.environ["OPENAI_API_KEY"] = openrouter_key
    print(f"[bridge] Mapped OPENROUTER_API_KEY -> OPENAI_API_KEY")
if openrouter_url:
    os.environ["OPENAI_API_BASE"] = openrouter_url
    print(f"[bridge] Mapped OPENROUTER_BASE_URL -> OPENAI_API_BASE ({openrouter_url})")

# Validate that we have an API key
api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key:
    print(
        "ERROR: No API key found.\n"
        "Set OPENAI_API_KEY or OPENROUTER_API_KEY in your .env file.\n"
        "Example .env:\n"
        "  OPENAI_API_KEY=sk-..."
    )
    sys.exit(1)

print(f"[ok] API key loaded (ends with ...{api_key[-4:]})")

# ---------------------------------------------------------------------------
# 2. INITIALISE NEMO GUARDRAILS
# ---------------------------------------------------------------------------
# RailsConfig.from_path() reads ALL .yml and .co files from the directory.
# LLMRails wraps the config into a callable guardrail engine.
# ---------------------------------------------------------------------------
try:
    from nemoguardrails import LLMRails, RailsConfig
except ImportError:
    print(
        "ERROR: nemoguardrails is not installed.\n"
        "Install with: pip install nemoguardrails"
    )
    sys.exit(1)

# Path to the config directory containing config.yml and rails.co
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core", "nemo_config")

if not os.path.isdir(CONFIG_DIR):
    print(f"ERROR: Config directory not found: {CONFIG_DIR}")
    sys.exit(1)

print(f"[ok] Loading NeMo config from: {CONFIG_DIR}")

config = RailsConfig.from_path(CONFIG_DIR)
rails = LLMRails(config)

print("[ok] NeMo Guardrails initialised successfully\n")

# ---------------------------------------------------------------------------
# Phrases that indicate NeMo has blocked the message (same as input_guardrails.py)
# ---------------------------------------------------------------------------
BLOCK_INDICATORS = (
    "i cannot",
    "i can't",
    "i'm not able to",
    "not able to help with that",
    "i'm sorry, but i can't",
    "i should not",
    "i shouldn't",
    "i'm specifically designed",
    "i'm designed to help only",
)


# ---------------------------------------------------------------------------
# 3. TEST FUNCTION
# ---------------------------------------------------------------------------
async def test_query(query: str, expected_result: str) -> None:
    """
    Send a query through NeMo Guardrails and check whether it was allowed or blocked.

    Args:
        query:           The user message to test.
        expected_result: "PASS" if the query should be allowed, "BLOCK" if it should be refused.
    """
    print(f"{'=' * 70}")
    print(f"  QUERY:    {query}")
    print(f"  EXPECTED: {expected_result}")
    print(f"{'=' * 70}")

    # Send the message through NeMo Guardrails
    response = await rails.generate_async(
        messages=[{"role": "user", "content": query}]
    )

    # Extract the bot's response text
    bot_message = (
        response.get("content", "")
        if isinstance(response, dict)
        else str(response)
    )

    # Determine if the response indicates a block
    is_blocked = any(indicator in bot_message.lower() for indicator in BLOCK_INDICATORS)
    actual_result = "BLOCK" if is_blocked else "PASS"

    # Print results
    print(f"  RESPONSE: {bot_message}")
    print(f"  ACTUAL:   {actual_result}")

    if actual_result == expected_result:
        print(f"  STATUS:   CORRECT\n")
    else:
        print(f"  STATUS:   MISMATCH (expected {expected_result}, got {actual_result})\n")


# ---------------------------------------------------------------------------
# 4. RUN TEST QUERIES
# ---------------------------------------------------------------------------
async def main() -> None:
    """Run two test queries: one on-topic, one off-topic."""

    print("=" * 70)
    print("  NeMo Guardrails — Allowlist / Catch-All Test")
    print("  Strategy: Only ACPC admission queries are allowed.")
    print("            Everything else is caught by the wildcard flow.")
    print("=" * 70)
    print()

    # ── Test 1: Valid ACPC admission query (should PASS) ─────────────────
    # This query clearly relates to ACPC Gujarat admissions.
    # NeMo should classify it as the "ask acpc admission" intent.
    # The "allow acpc queries" flow should fire, returning the on-topic response.
    await test_query(
        query="What is the cut-off rank for computer engineering at LD College?",
        expected_result="PASS",
    )

    # ── Test 2: Off-topic query (should be BLOCKED) ──────────────────────
    # This query is about cooking — completely unrelated to ACPC admissions.
    # NeMo should NOT classify it as "ask acpc admission".
    # The catch-all flow (`user ...`) should fire, returning the refusal string.
    await test_query(
        query="How do I make paneer butter masala at home?",
        expected_result="BLOCK",
    )

    print("=" * 70)
    print("  Tests complete.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
