"""Context memory for maintaining conversation context."""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Message:
    """A message in the conversation."""

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextMemory:
    """Memory for maintaining conversation context and history."""

    def __init__(self, max_messages: int = 100, max_tokens: int = 4000) -> None:
        """Initialize context memory.

        Args:
            max_messages: Maximum number of messages to retain.
            max_tokens: Maximum token count for context window.
        """
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self._messages: deque[Message] = deque(maxlen=max_messages)
        self._context: dict[str, Any] = {}

    def add_message(self, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Add a message to memory.

        Args:
            role: The role of the message sender (e.g., 'user', 'assistant').
            content: The message content.
            metadata: Optional metadata for the message.
        """
        message = Message(role=role, content=content, metadata=metadata or {})
        self._messages.append(message)

    def add_user_message(self, content: str, **kwargs: Any) -> None:
        """Add a user message.

        Args:
            content: The message content.
            **kwargs: Additional metadata.
        """
        self.add_message("user", content, kwargs)

    def add_assistant_message(self, content: str, **kwargs: Any) -> None:
        """Add an assistant message.

        Args:
            content: The message content.
            **kwargs: Additional metadata.
        """
        self.add_message("assistant", content, kwargs)

    def add_system_message(self, content: str, **kwargs: Any) -> None:
        """Add a system message.

        Args:
            content: The message content.
            **kwargs: Additional metadata.
        """
        self.add_message("system", content, kwargs)

    def get_messages(self, count: int | None = None) -> list[dict[str, Any]]:
        """Get messages from memory.

        Args:
            count: Number of recent messages to retrieve. If None, returns all.

        Returns:
            List of messages as dictionaries.
        """
        messages = list(self._messages)
        if count is not None:
            messages = messages[-count:]
        return [{"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in messages]

    def get_context(self) -> dict[str, Any]:
        """Get the current context.

        Returns:
            The context dictionary.
        """
        return self._context.copy()

    def set_context(self, key: str, value: Any) -> None:
        """Set a context value.

        Args:
            key: The context key.
            value: The context value.
        """
        self._context[key] = value

    def clear_context(self) -> None:
        """Clear the context."""
        self._context.clear()

    def clear_messages(self) -> None:
        """Clear all messages."""
        self._messages.clear()

    def clear(self) -> None:
        """Clear all memory (messages and context)."""
        self.clear_messages()
        self.clear_context()

    def to_chat_format(self) -> list[dict[str, str]]:
        """Convert messages to chat completion format.

        Returns:
            List of messages in OpenAI chat format.
        """
        return [{"role": m.role, "content": m.content} for m in self._messages]

    @property
    def message_count(self) -> int:
        """Get the number of messages in memory."""
        return len(self._messages)
