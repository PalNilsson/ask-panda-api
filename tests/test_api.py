"""Tests for API routes."""

import pytest
from fastapi.testclient import TestClient

from ask_panda.api.app import create_app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestQueryEndpoint:
    """Tests for query endpoint."""

    def test_query(self, client: TestClient) -> None:
        """Test query endpoint."""
        response = client.post(
            "/api/v1/query",
            json={"query": "Test query", "experiment": "atlas"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "Test query"
        assert data["experiment"] == "atlas"

    def test_query_default_experiment(self, client: TestClient) -> None:
        """Test query with default experiment."""
        response = client.post(
            "/api/v1/query",
            json={"query": "Test query"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["experiment"] == "atlas"


class TestChatEndpoint:
    """Tests for chat endpoint."""

    def test_chat(self, client: TestClient) -> None:
        """Test chat endpoint."""
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello", "experiment": "atlas"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "conversation_id" in data

    def test_chat_with_conversation_id(self, client: TestClient) -> None:
        """Test chat with existing conversation."""
        response = client.post(
            "/api/v1/chat",
            json={
                "message": "Hello",
                "experiment": "atlas",
                "conversation_id": "test-123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["conversation_id"] == "test-123"


class TestExperimentsEndpoint:
    """Tests for experiments endpoint."""

    def test_list_experiments(self, client: TestClient) -> None:
        """Test listing experiments."""
        response = client.get("/api/v1/experiments")
        assert response.status_code == 200
        data = response.json()
        assert "experiments" in data
        names = [e["name"] for e in data["experiments"]]
        assert "atlas" in names
        assert "verarubin" in names
        assert "epic" in names

    def test_get_experiment(self, client: TestClient) -> None:
        """Test getting experiment details."""
        response = client.get("/api/v1/experiments/atlas")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "atlas"

    def test_get_experiment_not_found(self, client: TestClient) -> None:
        """Test getting non-existent experiment."""
        response = client.get("/api/v1/experiments/unknown")
        assert response.status_code == 404
