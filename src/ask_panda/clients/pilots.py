"""Pilots client for PanDA."""

from typing import Any

from ask_panda.clients.base import BaseClient


class PilotsClient(BaseClient):
    """Client for querying PanDA pilots."""

    async def query(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Query pilots information.

        Args:
            query: Search query for pilots.
            **kwargs: Additional parameters.

        Returns:
            Pilots query results.
        """
        return {
            "query": query,
            "results": [],
            "source": "pilots",
            "message": "Pilots query executed",
        }

    async def get_pilot_status(self, site: str) -> dict[str, Any]:
        """Get pilot status for a site.

        Args:
            site: The site name.

        Returns:
            Pilot status information.
        """
        return {
            "site": site,
            "status": {},
            "source": "pilots",
        }

    async def get_pilot_jobs(self, site: str) -> dict[str, Any]:
        """Get pilot jobs for a site.

        Args:
            site: The site name.

        Returns:
            List of pilot jobs.
        """
        return {
            "site": site,
            "jobs": [],
            "source": "pilots",
        }
