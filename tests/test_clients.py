"""Tests for clients."""


from ask_panda.clients.selection import ClientSelector
from ask_panda.config.schemas import ClientConfig


class TestClientSelector:
    """Tests for ClientSelector."""

    def test_initialization(self) -> None:
        """Test client selector initialization."""
        config = ClientConfig()
        selector = ClientSelector(config)
        available = selector.get_available_clients()
        assert "docs" in available
        assert "logs" in available
        assert "data" in available
        assert "pilots" in available
        assert "maintenance" in available

    def test_disabled_clients(self) -> None:
        """Test with disabled clients."""
        config = ClientConfig(docs_enabled=False, logs_enabled=False)
        selector = ClientSelector(config)
        available = selector.get_available_clients()
        assert "docs" not in available
        assert "logs" not in available
        assert "data" in available

    def test_get_client(self) -> None:
        """Test getting a specific client."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client = selector.get_client("docs")
        assert client is not None

    def test_get_client_not_found(self) -> None:
        """Test getting non-existent client."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client = selector.get_client("nonexistent")
        assert client is None

    def test_auto_select_docs(self) -> None:
        """Test auto-selection for documentation queries."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client_type = selector._auto_select_client("How do I use the documentation?")
        assert client_type == "docs"

    def test_auto_select_logs(self) -> None:
        """Test auto-selection for log queries."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client_type = selector._auto_select_client("Show me the error logs")
        assert client_type == "logs"

    def test_auto_select_data(self) -> None:
        """Test auto-selection for data queries."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client_type = selector._auto_select_client("Find dataset mc16_13TeV")
        assert client_type == "data"

    def test_auto_select_pilots(self) -> None:
        """Test auto-selection for pilot queries."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client_type = selector._auto_select_client("What is the pilot status?")
        assert client_type == "pilots"

    def test_auto_select_maintenance(self) -> None:
        """Test auto-selection for maintenance queries."""
        config = ClientConfig()
        selector = ClientSelector(config)
        client_type = selector._auto_select_client("Is there any maintenance scheduled?")
        assert client_type == "maintenance"
