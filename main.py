"""
CryptoGraph — Application entry point.

Creates the FastAPI application, mounts the static frontend files,
and configures the root route to serve the web UI.

Usage:
    uvicorn main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.main import create_app

# Create the FastAPI application
app: FastAPI = create_app()

# Path to static files directory
STATIC_DIR = Path(__file__).parent / "static"

# Mount static files (CSS, JS, images) at /static
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Serve index.html at the root URL
    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        """Serve the frontend index.html at the root URL."""
        return FileResponse(str(STATIC_DIR / "index.html"))
