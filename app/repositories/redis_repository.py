"""
Upstash Redis implementation of ChatHistoryRepository.

Storage layout:
    Key:   chat_history:{session_id}   (Redis List)
    Items: JSON-encoded message dicts, one per list element
    Size:  Capped at 10 items (5 user + 5 assistant exchanges) via LTRIM

Each append does three commands:
    RPUSH  key  <json_message>  ...   — add new messages to the tail
    LTRIM  key  -10  -1               — trim to the last 10 elements
    EXPIRE key  <ttl_seconds>         — slide the TTL window forward
"""

from __future__ import annotations

import json

from upstash_redis.asyncio import Redis

from app.common.exceptions import RepositoryError
from app.common.logging import get_logger
from app.config import Settings
from app.repositories.base import ChatHistoryRepository

logger = get_logger(__name__)

# Maximum number of individual messages kept per session (5 pairs × 2).
_MAX_MESSAGES: int = 10


class UpstashRedisChatHistoryRepository(ChatHistoryRepository):
    """Chat-history repository backed by Upstash Redis (REST API, async)."""

    def __init__(self, settings: Settings) -> None:
        self._redis = Redis(
            url=settings.upstash_redis_rest_url,
            token=settings.upstash_redis_rest_token,
        )
        self._ttl_seconds: int = settings.chat_history_ttl_minutes * 60

    # ── Public Interface ──────────────────────────────────────

    async def get_history(self, session_id: str) -> list[dict]:
        """Return all stored messages for the session (up to 10)."""
        key = self._key(session_id)
        try:
            raw_items: list[str] = await self._redis.lrange(key, 0, -1)
            if not raw_items:
                logger.info("no_history_found", session_id=session_id)
                return []

            history = [json.loads(item) for item in raw_items]
            logger.info(
                "history_retrieved",
                session_id=session_id,
                message_count=len(history),
            )
            return history

        except Exception as exc:
            logger.error("get_history_failed", session_id=session_id, error=str(exc))
            raise RepositoryError(f"Failed to retrieve history: {exc}") from exc

    async def append_history(
        self, session_id: str, messages: list[dict]
    ) -> None:
        """
        Append messages to the session list, cap at 10, and refresh TTL.

        Uses RPUSH → LTRIM → EXPIRE so the list never exceeds _MAX_MESSAGES.
        """
        key = self._key(session_id)
        try:
            # Push each message individually as a JSON string.
            for msg in messages:
                await self._redis.rpush(key, json.dumps(msg))

            # Trim to the last _MAX_MESSAGES entries.
            await self._redis.ltrim(key, -_MAX_MESSAGES, -1)

            # Slide the TTL window forward on every write.
            await self._redis.expire(key, self._ttl_seconds)

            logger.info(
                "history_appended",
                session_id=session_id,
                new_messages=len(messages),
            )

        except RepositoryError:
            raise
        except Exception as exc:
            logger.error("append_history_failed", session_id=session_id, error=str(exc))
            raise RepositoryError(f"Failed to append history: {exc}") from exc

    # ── Private Helpers ───────────────────────────────────────

    @staticmethod
    def _key(session_id: str) -> str:
        return f"chat_history:{session_id}"
