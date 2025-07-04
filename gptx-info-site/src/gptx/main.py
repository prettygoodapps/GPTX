"""
GPTX Exchange - Main FastAPI Application.

This module contains the main FastAPI application with all routes,
middleware, and configuration for the GPTX Exchange platform.
"""

from pathlib import Path
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from gptx.core.config import settings
from gptx.core.database import Base, engine
from gptx.routers import carbon, exchange, tokens

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="GPTX Exchange",
    description="Decentralized AI Token Exchange with Carbon Offsetting",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Mount static files
static_path = Path(__file__).parent.parent.parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Templates
templates_path = Path(__file__).parent.parent.parent / "templates"
templates_path.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_path))

# Include routers
app.include_router(tokens.router, prefix="/api/tokens", tags=["tokens"])
app.include_router(exchange.router, prefix="/api/exchange", tags=["exchange"])
app.include_router(carbon.router, prefix="/api/carbon", tags=["carbon"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    """
    Serve the main landing page.

    Args:
        request: The incoming HTTP request

    Returns:
        HTMLResponse: The rendered landing page
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        Dict[str, str]: Health status and version information
    """
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/api/info")
async def api_info() -> Dict[str, Any]:
    """
    API information endpoint providing service metadata.

    Returns:
        Dict[str, Any]: API information including available endpoints
    """
    return {
        "name": "GPTX Exchange API",
        "version": "0.1.0",
        "description": "Decentralized AI Token Exchange with Carbon Offsetting",
        "endpoints": {
            "tokens": "/api/tokens",
            "exchange": "/api/exchange",
            "carbon": "/api/carbon",
        },
    }


def main() -> None:
    """
    Main entry point for running the application.

    This function starts the uvicorn server with the configured settings.
    """
    uvicorn.run(
        "gptx.main:app",
        host=settings.HOST,
        port=settings.port,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )


if __name__ == "__main__":
    main()
