"""FastAPI application factory."""

from fastapi import FastAPI

from traider import __version__
from traider.api.routes import health


def create_app() -> FastAPI:
    app = FastAPI(
        title="trAIder API",
        version=__version__,
        description="Personal AI-powered swing-trading advisor.",
    )
    app.include_router(health.router)
    return app


app = create_app()
