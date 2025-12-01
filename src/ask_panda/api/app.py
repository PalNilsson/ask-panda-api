"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ask_panda.api.routes import router
from ask_panda.config.schemas import ServerConfig


def create_app(config: ServerConfig | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        config: Optional server configuration.

    Returns:
        Configured FastAPI application.
    """
    config = config or ServerConfig()

    app = FastAPI(
        title="Ask PanDA API",
        description="A flexible API for building smart assistants for PanDA workflows",
        version="0.1.0",
        debug=config.debug,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router, prefix="/api/v1")

    return app
