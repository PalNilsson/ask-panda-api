"""ePIC experiment glue code."""

from typing import Any

from ask_panda.config.schemas import AgentConfig, ExperimentConfig


class EpicExperiment:
    """ePIC experiment-specific configuration and customization."""

    name = "epic"
    description = "ePIC detector at the Electron-Ion Collider (EIC)"

    default_system_prompt = """You are an AI assistant specialized in helping users with the ePIC experiment
at the Electron-Ion Collider (EIC). You have knowledge of:
- PanDA workload management system for ePIC simulations and analysis
- EIC computing infrastructure
- ePIC detector simulations and reconstruction
- Data management and storage systems
- ePIC-specific workflows and procedures

Help users query PanDA, understand job statuses, troubleshoot issues, and navigate ePIC computing resources."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize ePIC experiment.

        Args:
            config: Optional agent configuration.
        """
        self.config = config or self._default_config()

    def _default_config(self) -> AgentConfig:
        """Get default configuration for ePIC.

        Returns:
            Default agent configuration.
        """
        return AgentConfig(
            experiment=ExperimentConfig(
                name=self.name,
                description=self.description,
                custom_settings={
                    "panda_url": "https://panda.eic.io",
                    "simulation_version": "latest",
                },
            ),
            system_prompt=self.default_system_prompt,
        )

    def get_custom_tools(self) -> list[dict[str, Any]]:
        """Get ePIC-specific tools.

        Returns:
            List of tool definitions.
        """
        return [
            {
                "name": "get_epic_job_status",
                "description": "Get the status of an ePIC PanDA job",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "description": "The PanDA job ID"},
                    },
                    "required": ["job_id"],
                },
            },
            {
                "name": "list_simulation_campaigns",
                "description": "List ePIC simulation campaigns",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "description": "Filter by campaign status"},
                    },
                },
            },
        ]

    def customize_prompt(self, base_prompt: str) -> str:
        """Customize prompt with ePIC-specific context.

        Args:
            base_prompt: The base prompt to customize.

        Returns:
            Customized prompt.
        """
        return f"{self.default_system_prompt}\n\n{base_prompt}"
