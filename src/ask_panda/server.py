"""Main server module for running the Ask PanDA agent."""

import argparse
import os
from typing import Any

import uvicorn

from ask_panda.api.app import create_app
from ask_panda.clients.selection import ClientSelector
from ask_panda.config.schemas import (
    AgentConfig,
    ClientConfig,
    ExperimentConfig,
    ModelConfig,
    ModelProvider,
    ServerConfig,
)
from ask_panda.experiments import AtlasExperiment, EpicExperiment, VeraRubinExperiment
from ask_panda.models import BaseModel, OllamaModel, OpenAIModel
from ask_panda.tools import ContextMemory, VectorStore


class Agent:
    """The main Ask PanDA agent."""

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the agent.

        Args:
            config: Agent configuration.
        """
        self.config = config
        self.model = self._create_model()
        self.client_selector = ClientSelector(config.clients)
        self.memory = ContextMemory()
        self.vector_store = VectorStore()

        # Add system prompt to memory
        self.memory.add_system_message(config.system_prompt)

    def _create_model(self) -> BaseModel:
        """Create the language model based on configuration.

        Returns:
            The configured language model.
        """
        if self.config.model.provider == ModelProvider.OLLAMA:
            return OllamaModel(self.config.model)
        return OpenAIModel(self.config.model)

    async def query(self, query: str, **kwargs: Any) -> dict[str, Any]:
        """Process a query.

        Args:
            query: The user query.
            **kwargs: Additional parameters.

        Returns:
            Query response.
        """
        # Add user message to memory
        self.memory.add_user_message(query)

        # Route to appropriate client
        client_type = kwargs.get("client_type")
        client_result = await self.client_selector.route_query(query, client_type)

        # Generate response using the model
        messages = self.memory.to_chat_format()
        messages.append({"role": "user", "content": f"Based on this data: {client_result}\n\nAnswer: {query}"})

        response = await self.model.generate(messages)

        # Add assistant response to memory
        self.memory.add_assistant_message(response)

        return {
            "query": query,
            "response": response,
            "client_data": client_result,
            "experiment": self.config.experiment.name,
        }

    async def chat(self, message: str) -> str:
        """Process a chat message.

        Args:
            message: The user message.

        Returns:
            Assistant response.
        """
        self.memory.add_user_message(message)
        messages = self.memory.to_chat_format()
        response = await self.model.generate(messages)
        self.memory.add_assistant_message(response)
        return response


def get_experiment_config(experiment_name: str) -> AgentConfig:
    """Get configuration for a specific experiment.

    Args:
        experiment_name: Name of the experiment.

    Returns:
        Agent configuration for the experiment.

    Raises:
        ValueError: If experiment is not recognized.
    """
    experiments = {
        "atlas": AtlasExperiment,
        "verarubin": VeraRubinExperiment,
        "epic": EpicExperiment,
    }

    experiment_class = experiments.get(experiment_name.lower())
    if experiment_class is None:
        raise ValueError(f"Unknown experiment: {experiment_name}")

    experiment = experiment_class()
    return experiment.config


def create_agent_from_env() -> Agent:
    """Create an agent from environment variables.

    Returns:
        Configured agent.
    """
    experiment = os.getenv("EXPERIMENT", "atlas")
    model_provider = os.getenv("MODEL_PROVIDER", "openai")
    model_name = os.getenv("MODEL_NAME", "gpt-4")
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
    base_url = os.getenv("MODEL_BASE_URL")

    config = AgentConfig(
        model=ModelConfig(
            provider=ModelProvider(model_provider),
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
        ),
        clients=ClientConfig(),
        experiment=ExperimentConfig(name=experiment, description=f"{experiment} experiment"),
    )

    return Agent(config)


def main() -> None:
    """Main entry point for running the server."""
    parser = argparse.ArgumentParser(description="Ask PanDA API Server")
    parser.add_argument(
        "--experiment",
        "-e",
        default=os.getenv("EXPERIMENT", "atlas"),
        choices=["atlas", "verarubin", "epic"],
        help="Experiment to run (default: atlas)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=int(os.getenv("PORT", "8000")),
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=os.getenv("DEBUG", "false").lower() == "true",
        help="Enable debug mode",
    )

    args = parser.parse_args()

    print(f"Starting Ask PanDA API Server for {args.experiment} experiment")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Debug: {args.debug}")

    server_config = ServerConfig(host=args.host, port=args.port, debug=args.debug)
    app = create_app(server_config)

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
