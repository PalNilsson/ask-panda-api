"""Client selector for routing queries to appropriate clients."""

from typing import Any

from ask_panda.clients.base import BaseClient
from ask_panda.clients.data import DataClient
from ask_panda.clients.docs import DocsClient
from ask_panda.clients.logs import LogsClient
from ask_panda.clients.maintenance import MaintenanceClient
from ask_panda.clients.pilots import PilotsClient
from ask_panda.config.schemas import ClientConfig


class ClientSelector:
    """Selector for routing queries to the appropriate domain client."""

    def __init__(self, config: ClientConfig) -> None:
        """Initialize the client selector.

        Args:
            config: Client configuration.
        """
        self.config = config
        self._clients: dict[str, BaseClient] = {}
        self._initialize_clients()

    def _initialize_clients(self) -> None:
        """Initialize enabled clients based on configuration."""
        base_url = self.config.base_url
        timeout = self.config.timeout

        if self.config.docs_enabled:
            self._clients["docs"] = DocsClient(base_url=base_url, timeout=timeout)
        if self.config.logs_enabled:
            self._clients["logs"] = LogsClient(base_url=base_url, timeout=timeout)
        if self.config.data_enabled:
            self._clients["data"] = DataClient(base_url=base_url, timeout=timeout)
        if self.config.pilots_enabled:
            self._clients["pilots"] = PilotsClient(base_url=base_url, timeout=timeout)
        if self.config.maintenance_enabled:
            self._clients["maintenance"] = MaintenanceClient(base_url=base_url, timeout=timeout)

    def get_client(self, client_type: str) -> BaseClient | None:
        """Get a client by type.

        Args:
            client_type: The type of client to retrieve.

        Returns:
            The client instance or None if not found/enabled.
        """
        return self._clients.get(client_type)

    def get_available_clients(self) -> list[str]:
        """Get list of available client types.

        Returns:
            List of available client type names.
        """
        return list(self._clients.keys())

    async def route_query(self, query: str, client_type: str | None = None, **kwargs: Any) -> dict[str, Any]:
        """Route a query to the appropriate client.

        Args:
            query: The query string.
            client_type: Specific client type to use, or None for auto-selection.
            **kwargs: Additional query parameters.

        Returns:
            Query results.

        Raises:
            ValueError: If no appropriate client is available.
        """
        if client_type:
            client = self.get_client(client_type)
            if client is None:
                raise ValueError(f"Client '{client_type}' is not available")
            async with client:
                return await client.query(query, **kwargs)

        # Auto-select based on query content (simple keyword matching)
        client_type = self._auto_select_client(query)
        client = self.get_client(client_type)
        if client is None:
            raise ValueError("No appropriate client available for the query")
        async with client:
            return await client.query(query, **kwargs)

    def _auto_select_client(self, query: str) -> str:
        """Automatically select a client based on query content.

        Args:
            query: The query string.

        Returns:
            The selected client type.
        """
        query_lower = query.lower()

        # Simple keyword-based routing
        if any(kw in query_lower for kw in ["doc", "documentation", "how to", "guide", "manual"]):
            return "docs"
        if any(kw in query_lower for kw in ["log", "error", "output", "stderr", "stdout"]):
            return "logs"
        if any(kw in query_lower for kw in ["data", "dataset", "file", "rucio"]):
            return "data"
        if any(kw in query_lower for kw in ["pilot", "harvester", "site"]):
            return "pilots"
        if any(kw in query_lower for kw in ["maintenance", "downtime", "status"]):
            return "maintenance"

        # Default to docs
        return "docs"
