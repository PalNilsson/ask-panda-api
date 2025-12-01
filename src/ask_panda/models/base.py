"""Base model class for language model backends."""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any

from ask_panda.config.schemas import ModelConfig


class BaseModel(ABC):
    """Base class for language model backends."""

    def __init__(self, config: ModelConfig) -> None:
        """Initialize the model.

        Args:
            config: Model configuration.
        """
        self.config = config

    @abstractmethod
    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a response from the model.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Returns:
            The generated response text.
        """
        ...

    @abstractmethod
    async def generate_stream(self, messages: list[dict[str, str]], **kwargs: Any) -> AsyncGenerator[str, None]:
        """Generate a streaming response from the model.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Yields:
            Chunks of the generated response text.
        """
        ...

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate embeddings for text.

        Args:
            text: The text to embed.

        Returns:
            The embedding vector.
        """
        ...
