"""Data client for PanDA."""

from typing import Any

from ask_panda.clients.base import BaseClient


class DataClient(BaseClient):
    """Client for querying PanDA data."""

    async def query(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Query data.

        Args:
            query: Search query for data.
            **kwargs: Additional parameters.

        Returns:
            Data query results.
        """
        return {
            "query": query,
            "results": [],
            "source": "data",
            "message": "Data query executed",
        }

    async def get_dataset(self, dataset_name: str) -> dict[str, Any]:
        """Get information about a dataset.

        Args:
            dataset_name: The dataset name.

        Returns:
            Dataset information.
        """
        return {
            "dataset_name": dataset_name,
            "info": {},
            "source": "data",
        }

    async def get_files(self, dataset_name: str) -> dict[str, Any]:
        """Get files in a dataset.

        Args:
            dataset_name: The dataset name.

        Returns:
            List of files in the dataset.
        """
        return {
            "dataset_name": dataset_name,
            "files": [],
            "source": "data",
        }
