# ask-panda-api

A flexible API for building smart assistants that query, analyze, and interact with PanDA workflows across multiple experiments.

## Overview

Ask PanDA API provides a unified interface for building AI-powered assistants that can help users interact with PanDA (Production and Distributed Analysis) workload management systems. It supports multiple experiments including ATLAS, Vera C. Rubin Observatory, and ePIC.

## Project Structure

```
ask-panda-api/
├── pyproject.toml              # Project configuration
├── docker/                     # Docker configurations
│   ├── atlas-server.Dockerfile
│   ├── verarubin-server.Dockerfile
│   └── epic-server.Dockerfile
├── src/ask_panda/              # Core package
│   ├── server.py               # Agent runner using config schemas
│   ├── config/                 # Configuration schemas
│   │   └── schemas.py
│   ├── clients/                # Domain logic clients
│   │   ├── docs.py             # Documentation client
│   │   ├── logs.py             # Logs client
│   │   ├── data.py             # Data client
│   │   ├── pilots.py           # Pilots client
│   │   ├── maintenance.py      # Maintenance client
│   │   └── selection.py        # Client selector
│   ├── tools/                  # Utility tools
│   │   ├── vector_store.py     # Vector store for embeddings
│   │   └── context_memory.py   # Context memory for conversations
│   ├── models/                 # LLM backends
│   │   ├── openai.py           # OpenAI backend
│   │   └── ollama.py           # Ollama backend
│   ├── experiments/            # Experiment-specific configurations
│   │   ├── atlas/              # ATLAS experiment
│   │   ├── verarubin/          # Vera Rubin experiment
│   │   └── epic/               # ePIC experiment
│   ├── api/                    # REST API interface
│   │   ├── app.py
│   │   └── routes.py
│   └── cli/                    # Command-line interface
│       └── main.py
├── mcp/                        # MCP server examples
│   ├── panda_server.py
│   └── docs_server.py
├── streamlit-ui/               # Streamlit web interface
│   └── app.py
└── tests/                      # Test suite
```

## Installation

### From source

```bash
git clone https://github.com/PalNilsson/ask-panda-api.git
cd ask-panda-api
pip install -e .
```

### With development dependencies

```bash
pip install -e ".[dev]"
```

### With all extras

```bash
pip install -e ".[all]"
```

## Quick Start

### Using the CLI

```bash
# Ask a question
ask-panda query "What is the status of my job?" --experiment atlas

# Start interactive chat
ask-panda chat --experiment atlas

# Start the API server
ask-panda serve --port 8000 --experiment atlas

# List available experiments
ask-panda list-experiments
```

### Using the API

```python
import asyncio
from ask_panda.server import Agent
from ask_panda.config import AgentConfig, ExperimentConfig

# Create configuration
config = AgentConfig(
    experiment=ExperimentConfig(name="atlas", description="ATLAS experiment")
)

# Create agent
agent = Agent(config)

# Query the agent
async def main():
    result = await agent.query("What is the status of job 123?")
    print(result)

asyncio.run(main())
```

### Using Docker

```bash
# Build and run ATLAS server
docker build -f docker/atlas-server.Dockerfile -t ask-panda-atlas .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ask-panda-atlas

# Build and run Vera Rubin server
docker build -f docker/verarubin-server.Dockerfile -t ask-panda-verarubin .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ask-panda-verarubin
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EXPERIMENT` | Default experiment | `atlas` |
| `MODEL_PROVIDER` | LLM provider (openai/ollama) | `openai` |
| `MODEL_NAME` | Model name | `gpt-4` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `MODEL_BASE_URL` | Custom model API URL | - |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `false` |

### Supported Experiments

- **ATLAS**: ATLAS experiment at CERN's Large Hadron Collider
- **Vera Rubin**: Vera C. Rubin Observatory Legacy Survey of Space and Time (LSST)
- **ePIC**: ePIC detector at the Electron-Ion Collider (EIC)

## Development

### Running Tests

```bash
pytest
```

### Running Linter

```bash
ruff check src tests
```

### Type Checking

```bash
mypy src
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/query` | POST | Execute a query |
| `/api/v1/chat` | POST | Chat with the assistant |
| `/api/v1/experiments` | GET | List experiments |
| `/api/v1/experiments/{name}` | GET | Get experiment details |

## License

Apache License 2.0
