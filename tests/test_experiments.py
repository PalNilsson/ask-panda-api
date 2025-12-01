"""Tests for experiments."""


from ask_panda.experiments import AtlasExperiment, EpicExperiment, VeraRubinExperiment


class TestAtlasExperiment:
    """Tests for ATLAS experiment."""

    def test_initialization(self) -> None:
        """Test experiment initialization."""
        exp = AtlasExperiment()
        assert exp.name == "atlas"
        assert exp.config.experiment.name == "atlas"

    def test_custom_tools(self) -> None:
        """Test getting custom tools."""
        exp = AtlasExperiment()
        tools = exp.get_custom_tools()
        assert len(tools) > 0
        tool_names = [t["name"] for t in tools]
        assert "get_atlas_job_status" in tool_names

    def test_customize_prompt(self) -> None:
        """Test prompt customization."""
        exp = AtlasExperiment()
        customized = exp.customize_prompt("Additional context")
        assert "ATLAS" in customized
        assert "Additional context" in customized


class TestVeraRubinExperiment:
    """Tests for Vera Rubin experiment."""

    def test_initialization(self) -> None:
        """Test experiment initialization."""
        exp = VeraRubinExperiment()
        assert exp.name == "verarubin"
        assert exp.config.experiment.name == "verarubin"

    def test_custom_tools(self) -> None:
        """Test getting custom tools."""
        exp = VeraRubinExperiment()
        tools = exp.get_custom_tools()
        assert len(tools) > 0
        tool_names = [t["name"] for t in tools]
        assert "get_rubin_job_status" in tool_names
        assert "query_butler" in tool_names


class TestEpicExperiment:
    """Tests for ePIC experiment."""

    def test_initialization(self) -> None:
        """Test experiment initialization."""
        exp = EpicExperiment()
        assert exp.name == "epic"
        assert exp.config.experiment.name == "epic"

    def test_custom_tools(self) -> None:
        """Test getting custom tools."""
        exp = EpicExperiment()
        tools = exp.get_custom_tools()
        assert len(tools) > 0
        tool_names = [t["name"] for t in tools]
        assert "get_epic_job_status" in tool_names
        assert "list_simulation_campaigns" in tool_names
