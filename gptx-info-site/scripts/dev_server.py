#!/usr/bin/env python3
"""
Development server script for GPTX Exchange.

This script starts the FastAPI development server with hot reload
and proper configuration for local development.
"""

import os
import sys
from pathlib import Path

import uvicorn

# Add src to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def main() -> None:
    """Start the development server."""
    # Set development environment
    os.environ.setdefault("ENVIRONMENT", "development")

    # Start uvicorn with hot reload
    uvicorn.run(
        "gptx.main:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        reload_dirs=[str(src_path)],
        log_level="info",
    )


if __name__ == "__main__":
    main()
