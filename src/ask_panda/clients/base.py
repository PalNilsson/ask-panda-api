"""Base client class for domain logic."""

from abc import ABC, abstractmethod
from typing import Any

import httpx


class BaseClient(ABC):
    """Base class for all domain clients."""

    def __init__(self, base_url: str | None = None, timeout: int = 30) -> None:
        """Initialize the base client.

        Args:
            base_url: Base URL for the service.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "BaseClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._client

    @abstractmethod
    async def query(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Execute a query against the service.

        Args:
            query: The query string.
            **kwargs: Additional query parameters.

        Returns:
            Query results as a dictionary.
        """
        ...
