"""API routes for Ask PanDA."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    """Request model for queries."""

    query: str
    experiment: str = "atlas"
    client_type: str | None = None


class QueryResponse(BaseModel):
    """Response model for queries."""

    query: str
    response: str
    experiment: str
    metadata: dict[str, Any] = {}


class ChatRequest(BaseModel):
    """Request model for chat."""

    message: str
    experiment: str = "atlas"
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Response model for chat."""

    message: str
    conversation_id: str
    experiment: str


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check API health status."""
    return HealthResponse(status="healthy", version="0.1.0")


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """Execute a query against PanDA services.

    Args:
        request: The query request.

    Returns:
        Query response with results.
    """
    # Placeholder implementation
    return QueryResponse(
        query=request.query,
        response=f"Query '{request.query}' processed for experiment '{request.experiment}'",
        experiment=request.experiment,
        metadata={"client_type": request.client_type or "auto"},
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Have a chat conversation with the assistant.

    Args:
        request: The chat request.

    Returns:
        Chat response.
    """
    import uuid

    conversation_id = request.conversation_id or str(uuid.uuid4())

    # Placeholder implementation
    return ChatResponse(
        message=f"I understand you're asking about: {request.message}",
        conversation_id=conversation_id,
        experiment=request.experiment,
    )


@router.get("/experiments")
async def list_experiments() -> dict[str, Any]:
    """List available experiments.

    Returns:
        Dictionary of available experiments.
    """
    return {
        "experiments": [
            {"name": "atlas", "description": "ATLAS experiment at CERN LHC"},
            {"name": "verarubin", "description": "Vera C. Rubin Observatory LSST"},
            {"name": "epic", "description": "ePIC detector at the Electron-Ion Collider"},
        ]
    }


@router.get("/experiments/{experiment}")
async def get_experiment(experiment: str) -> dict[str, Any]:
    """Get experiment details.

    Args:
        experiment: The experiment name.

    Returns:
        Experiment details.

    Raises:
        HTTPException: If experiment not found.
    """
    experiments = {
        "atlas": {
            "name": "atlas",
            "description": "ATLAS experiment at CERN LHC",
            "panda_url": "https://bigpanda.cern.ch",
        },
        "verarubin": {
            "name": "verarubin",
            "description": "Vera C. Rubin Observatory LSST",
            "panda_url": "https://panda.lsst.io",
        },
        "epic": {
            "name": "epic",
            "description": "ePIC detector at the Electron-Ion Collider",
            "panda_url": "https://panda.eic.io",
        },
    }

    if experiment not in experiments:
        raise HTTPException(status_code=404, detail=f"Experiment '{experiment}' not found")

    return experiments[experiment]
