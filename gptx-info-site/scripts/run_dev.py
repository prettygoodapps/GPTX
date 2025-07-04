#!/usr/bin/env python3
"""
Development server startup script for GPTX Exchange.

This script initializes the database and starts the development server
with proper configuration for the refactored project structure.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import uvicorn

from gptx.core.config import settings
from gptx.core.database import AIProvider, Base, SessionLocal, engine


def init_database() -> None:
    """
    Initialize database with default data.

    Creates all tables and populates with default AI providers
    if they don't already exist.
    """
    print("🔧 Initializing database...")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Add default AI providers
    db = SessionLocal()
    try:
        # Check if providers already exist
        existing_providers = db.query(AIProvider).count()

        if existing_providers == 0:
            providers = [
                AIProvider(
                    name="openai",
                    display_name="OpenAI",
                    is_active=True,
                    api_endpoint="https://api.openai.com/v1",
                    conversion_rate=1.0,
                ),
                AIProvider(
                    name="anthropic",
                    display_name="Anthropic",
                    is_active=True,
                    api_endpoint="https://api.anthropic.com/v1",
                    conversion_rate=1.0,
                ),
                AIProvider(
                    name="google",
                    display_name="Google AI",
                    is_active=True,
                    api_endpoint="https://generativelanguage.googleapis.com/v1",
                    conversion_rate=1.0,
                ),
            ]

            for provider in providers:
                db.add(provider)

            db.commit()
            print("✅ Default AI providers added to database")
        else:
            print("✅ Database already initialized")

    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


def main() -> None:
    """
    Main startup function for development server.

    Initializes the database and starts the uvicorn development server
    with hot reloading enabled.
    """
    print("🚀 Starting GPTX Exchange (Development Mode)...")
    print(f"📊 Environment: {'Development' if settings.DEBUG else 'Production'}")
    print(f"🌐 Host: {settings.HOST}:{settings.PORT}")

    # Initialize database
    init_database()

    print("✅ GPTX Exchange is ready!")
    print(f"🔗 API Documentation: http://{settings.HOST}:{settings.PORT}/api/docs")
    print(f"🏠 Homepage: http://{settings.HOST}:{settings.PORT}/")

    # Start the server
    uvicorn.run(
        "gptx.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )


if __name__ == "__main__":
    main()
