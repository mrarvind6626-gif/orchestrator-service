"""
Abstract repository interface for chat history storage.

Concrete implementations (Upstash Redis, PostgreSQL, etc.) must
implement every method defined here.  This keeps the service layer
completely decoupled from the storage technology.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ChatHistoryRepository(ABC):
    """Abstract interface for session chat history persistence."""

    @abstractmethod
    async def get_history(self, session_id: str) -> list[dict]:
        """
        Retrieve the chat history for a given session.

        Returns an empty list if no history exists.
        """
        ...

    @abstractmethod
    async def append_history(
        self, session_id: str, messages: list[dict]
    ) -> None:
        """
        Append new messages to the session's chat history.

        Implementations must cap the list at 10 messages (5 exchanges)
        and refresh the TTL on every write.
        """
        ...
