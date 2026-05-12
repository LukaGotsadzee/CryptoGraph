"""
FastAPI application factory.

Creates and configures the CryptoGraph API application,
including router registration and health check endpoint.
"""

from fastapi import FastAPI

from app.api.routes_classical import router as classical_router
from app.api.routes_modern import router as modern_router
from app.api.routes_files import router as files_router
from app.api.schemas import HealthResponse


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        A configured FastAPI application instance with all routers
        registered and metadata for the Swagger UI.
    """
    app = FastAPI(
        title="CryptoGraph API",
        description=(
            "A cryptography toolbox API supporting classical ciphers "
            "(Caesar, Vigenère), SHA-256 hashing, RSA encryption/decryption, "
            "and RSA digital signatures."
        ),
        version="1.0.0",
    )

    # Register API routers
    app.include_router(classical_router)
    app.include_router(modern_router)
    app.include_router(files_router)

    # Health check endpoint
    @app.get("/health", response_model=HealthResponse, tags=["System"])
    async def health_check() -> HealthResponse:
        """Check if the API is running."""
        return HealthResponse()

    return app
