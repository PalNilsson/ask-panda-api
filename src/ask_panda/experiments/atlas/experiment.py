"""ATLAS experiment glue code."""

from typing import Any

from ask_panda.config.schemas import AgentConfig, ExperimentConfig


class AtlasExperiment:
    """ATLAS experiment-specific configuration and customization."""

    name = "atlas"
    description = "ATLAS experiment at CERN LHC"

    default_system_prompt = """You are an AI assistant specialized in helping users with the ATLAS experiment
at CERN's Large Hadron Collider. You have knowledge of:
- PanDA (Production and Distributed Analysis) workload management system
- ATLAS computing infrastructure and grid computing
- Data management with Rucio
- Job submission and monitoring
- ATLAS-specific workflows and procedures

Help users query PanDA, understand job statuses, troubleshoot issues, and navigate ATLAS computing resources."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize ATLAS experiment.

        Args:
            config: Optional agent configuration.
        """
        self.config = config or self._default_config()

    def _default_config(self) -> AgentConfig:
        """Get default configuration for ATLAS.

        Returns:
            Default agent configuration.
        """
        return AgentConfig(
            experiment=ExperimentConfig(
                name=self.name,
                description=self.description,
                custom_settings={
                    "panda_url": "https://bigpanda.cern.ch",
                    "rucio_account": "atlas",
                },
            ),
            system_prompt=self.default_system_prompt,
        )

    def get_custom_tools(self) -> list[dict[str, Any]]:
        """Get ATLAS-specific tools.

        Returns:
            List of tool definitions.
        """
        return [
            {
                "name": "get_atlas_job_status",
                "description": "Get the status of an ATLAS PanDA job",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "description": "The PanDA job ID"},
                    },
                    "required": ["job_id"],
                },
            },
            {
                "name": "search_atlas_datasets",
                "description": "Search for ATLAS datasets in Rucio",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {"type": "string", "description": "Dataset name pattern"},
                        "scope": {"type": "string", "description": "Rucio scope"},
                    },
                    "required": ["pattern"],
                },
            },
        ]

    def customize_prompt(self, base_prompt: str) -> str:
        """Customize prompt with ATLAS-specific context.

        Args:
            base_prompt: The base prompt to customize.

        Returns:
            Customized prompt.
        """
        return f"{self.default_system_prompt}\n\n{base_prompt}"
