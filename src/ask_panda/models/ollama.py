"""Ollama model backend."""

from collections.abc import AsyncGenerator
from typing import Any

import ollama

from ask_panda.config.schemas import ModelConfig
from ask_panda.models.base import BaseModel


class OllamaModel(BaseModel):
    """Ollama model backend."""

    def __init__(self, config: ModelConfig) -> None:
        """Initialize the Ollama model.

        Args:
            config: Model configuration.
        """
        super().__init__(config)
        self._client = ollama.AsyncClient(host=config.base_url)

    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a response from Ollama.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Returns:
            The generated response text.
        """
        response = await self._client.chat(
            model=self.config.model_name,
            messages=messages,  # type: ignore[arg-type]
            options={
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
            },
        )
        return response["message"]["content"]

    async def generate_stream(self, messages: list[dict[str, str]], **kwargs: Any) -> AsyncGenerator[str, None]:
        """Generate a streaming response from Ollama.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Yields:
            Chunks of the generated response text.
        """
        stream = await self._client.chat(
            model=self.config.model_name,
            messages=messages,  # type: ignore[arg-type]
            options={
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
            },
            stream=True,
        )
        async for chunk in stream:
            if chunk["message"]["content"]:
                yield chunk["message"]["content"]

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings using Ollama.

        Args:
            text: The text to embed.

        Returns:
            The embedding vector.
        """
        response = await self._client.embeddings(
            model=self.config.model_name,
            prompt=text,
        )
        return response["embedding"]
