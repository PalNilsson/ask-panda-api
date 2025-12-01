"""Vera Rubin experiment glue code."""

from typing import Any

from ask_panda.config.schemas import AgentConfig, ExperimentConfig


class VeraRubinExperiment:
    """Vera Rubin Observatory experiment-specific configuration and customization."""

    name = "verarubin"
    description = "Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST)"

    default_system_prompt = """You are an AI assistant specialized in helping users with the Vera C. Rubin Observatory
and its Legacy Survey of Space and Time (LSST). You have knowledge of:
- PanDA workload management system for Rubin data processing
- Rubin Science Platform and data access
- LSST Data Management pipelines
- Butler data repository system
- Rubin-specific workflows and procedures

Help users query PanDA, understand job statuses, troubleshoot issues, and navigate Rubin computing resources."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize Vera Rubin experiment.

        Args:
            config: Optional agent configuration.
        """
        self.config = config or self._default_config()

    def _default_config(self) -> AgentConfig:
        """Get default configuration for Vera Rubin.

        Returns:
            Default agent configuration.
        """
        return AgentConfig(
            experiment=ExperimentConfig(
                name=self.name,
                description=self.description,
                custom_settings={
                    "panda_url": "https://panda.lsst.io",
                    "butler_repo": "/repo/main",
                },
            ),
            system_prompt=self.default_system_prompt,
        )

    def get_custom_tools(self) -> list[dict[str, Any]]:
        """Get Vera Rubin-specific tools.

        Returns:
            List of tool definitions.
        """
        return [
            {
                "name": "get_rubin_job_status",
                "description": "Get the status of a Rubin PanDA job",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "description": "The PanDA job ID"},
                    },
                    "required": ["job_id"],
                },
            },
            {
                "name": "query_butler",
                "description": "Query the Butler data repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "collection": {"type": "string", "description": "Collection name"},
                        "data_type": {"type": "string", "description": "Data type to query"},
                    },
                    "required": ["collection"],
                },
            },
        ]

    def customize_prompt(self, base_prompt: str) -> str:
        """Customize prompt with Vera Rubin-specific context.

        Args:
            base_prompt: The base prompt to customize.

        Returns:
            Customized prompt.
        """
        return f"{self.default_system_prompt}\n\n{base_prompt}"
