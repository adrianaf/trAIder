"""Health and version endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from traider import __version__

router = APIRouter(tags=["meta"])


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)