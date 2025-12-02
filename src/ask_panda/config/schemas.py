"""Pydantic schemas for configuration."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ModelProvider(str, Enum):
    """Supported model providers."""

    OPENAI = "openai"
    OLLAMA = "ollama"


class ModelConfig(BaseModel):
    """Configuration for the language model."""

    provider: ModelProvider = Field(default=ModelProvider.OPENAI, description="Model provider")
    model_name: str = Field(default="gpt-4", description="Name of the model to use")
    api_key: str | None = Field(default=None, description="API key for the model provider")
    base_url: str | None = Field(default=None, description="Base URL for the model API")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature for sampling")
    max_tokens: int = Field(default=4096, gt=0, description="Maximum tokens in response")


class ClientConfig(BaseModel):
    """Configuration for domain clients."""

    docs_enabled: bool = Field(default=True, description="Enable documentation client")
    logs_enabled: bool = Field(default=True, description="Enable logs client")
    data_enabled: bool = Field(default=True, description="Enable data client")
    pilots_enabled: bool = Field(default=True, description="Enable pilots client")
    maintenance_enabled: bool = Field(default=True, description="Enable maintenance client")
    base_url: str | None = Field(default="http://bigpanda.cern.ch", description="Base URL for PanDA services")
    timeout: int = Field(default=30, gt=0, description="Request timeout in seconds")


class ExperimentConfig(BaseModel):
    """Configuration for a specific experiment."""

    name: str = Field(..., description="Name of the experiment (e.g., atlas, verarubin, epic)")
    description: str = Field(default="", description="Description of the experiment")
    custom_settings: dict[str, Any] = Field(default_factory=dict, description="Custom experiment settings")


class ServerConfig(BaseModel):
    """Configuration for the API server."""

    host: str = Field(default="0.0.0.0", description="Host to bind the server to")
    port: int = Field(default=8000, gt=0, le=65535, description="Port to bind the server to")
    debug: bool = Field(default=False, description="Enable debug mode")
    cors_origins: list[str] = Field(default=["*"], description="Allowed CORS origins")


class AgentConfig(BaseModel):
    """Main configuration for the Ask PanDA agent."""

    model: ModelConfig = Field(default_factory=ModelConfig, description="Model configuration")
    clients: ClientConfig = Field(default_factory=ClientConfig, description="Clients configuration")
    experiment: ExperimentConfig = Field(..., description="Experiment configuration")
    server: ServerConfig = Field(default_factory=ServerConfig, description="Server configuration")
    system_prompt: str = Field(
        default="You are a helpful assistant for PanDA workflows.",
        description="System prompt for the agent",
    )
