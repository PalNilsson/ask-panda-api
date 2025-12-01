"""Tests for configuration schemas."""

import pytest
from pydantic import ValidationError

from ask_panda.config.schemas import (
    AgentConfig,
    ClientConfig,
    ExperimentConfig,
    ModelConfig,
    ModelProvider,
    ServerConfig,
)


class TestModelConfig:
    """Tests for ModelConfig."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ModelConfig()
        assert config.provider == ModelProvider.OPENAI
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 4096

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = ModelConfig(
            provider=ModelProvider.OLLAMA,
            model_name="llama2",
            temperature=0.5,
            max_tokens=2048,
        )
        assert config.provider == ModelProvider.OLLAMA
        assert config.model_name == "llama2"
        assert config.temperature == 0.5
        assert config.max_tokens == 2048

    def test_temperature_validation(self) -> None:
        """Test temperature validation."""
        with pytest.raises(ValidationError):
            ModelConfig(temperature=-0.1)
        with pytest.raises(ValidationError):
            ModelConfig(temperature=2.1)


class TestClientConfig:
    """Tests for ClientConfig."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ClientConfig()
        assert config.docs_enabled is True
        assert config.logs_enabled is True
        assert config.data_enabled is True
        assert config.pilots_enabled is True
        assert config.maintenance_enabled is True
        assert config.timeout == 30


class TestExperimentConfig:
    """Tests for ExperimentConfig."""

    def test_required_name(self) -> None:
        """Test that name is required."""
        with pytest.raises(ValidationError):
            ExperimentConfig()  # type: ignore[call-arg]

    def test_with_name(self) -> None:
        """Test configuration with name."""
        config = ExperimentConfig(name="atlas")
        assert config.name == "atlas"
        assert config.description == ""


class TestServerConfig:
    """Tests for ServerConfig."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = ServerConfig()
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.debug is False

    def test_port_validation(self) -> None:
        """Test port validation."""
        with pytest.raises(ValidationError):
            ServerConfig(port=0)
        with pytest.raises(ValidationError):
            ServerConfig(port=70000)


class TestAgentConfig:
    """Tests for AgentConfig."""

    def test_minimal_config(self) -> None:
        """Test minimal configuration."""
        config = AgentConfig(experiment=ExperimentConfig(name="atlas"))
        assert config.experiment.name == "atlas"
        assert config.model.provider == ModelProvider.OPENAI

    def test_full_config(self) -> None:
        """Test full configuration."""
        config = AgentConfig(
            model=ModelConfig(provider=ModelProvider.OLLAMA, model_name="llama2"),
            clients=ClientConfig(docs_enabled=False),
            experiment=ExperimentConfig(name="verarubin", description="LSST"),
            server=ServerConfig(port=9000),
            system_prompt="Custom prompt",
        )
        assert config.model.provider == ModelProvider.OLLAMA
        assert config.clients.docs_enabled is False
        assert config.experiment.name == "verarubin"
        assert config.server.port == 9000
        assert config.system_prompt == "Custom prompt"
