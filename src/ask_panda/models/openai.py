"""OpenAI model backend."""

from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncOpenAI

from ask_panda.config.schemas import ModelConfig
from ask_panda.models.base import BaseModel


class OpenAIModel(BaseModel):
    """OpenAI model backend."""

    def __init__(self, config: ModelConfig) -> None:
        """Initialize the OpenAI model.

        Args:
            config: Model configuration.
        """
        super().__init__(config)
        self._client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

    async def generate(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """Generate a response from OpenAI.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Returns:
            The generated response text.
        """
        response = await self._client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,  # type: ignore[arg-type]
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
        )
        content = response.choices[0].message.content
        return content if content is not None else ""

    async def generate_stream(self, messages: list[dict[str, str]], **kwargs: Any) -> AsyncGenerator[str, None]:
        """Generate a streaming response from OpenAI.

        Args:
            messages: List of messages in chat format.
            **kwargs: Additional generation parameters.

        Yields:
            Chunks of the generated response text.
        """
        stream = await self._client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,  # type: ignore[arg-type]
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def embed(self, text: str) -> list[float]:
        """Generate embeddings using OpenAI.

        Args:
            text: The text to embed.

        Returns:
            The embedding vector.
        """
        response = await self._client.embeddings.create(
            model="text-embedding-ada-002",
            input=text,
        )
        return response.data[0].embedding
