"""Dev runner for the FastAPI app."""

import uvicorn


def main() -> None:
    uvicorn.run(
        "traider.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
