"""
Pytest configuration and shared fixtures for GPTX Exchange tests.

This module provides common test fixtures and configuration
for the entire test suite.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gptx.core.database import Base, get_db
from gptx.main import app


@pytest.fixture
def test_db():
    """
    Create a test database session.

    Yields:
        Session: SQLAlchemy test database session
    """
    # Create test database engine
    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """
    Create a test client with test database.

    Args:
        test_db: Test database session fixture

    Returns:
        TestClient: FastAPI test client
    """

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_address():
    """
    Provide a sample Ethereum address for testing.

    Returns:
        str: Sample Ethereum address
    """
    return "0x1234567890123456789012345678901234567890"


@pytest.fixture
def sample_provider():
    """
    Provide sample AI provider data for testing.

    Returns:
        dict: Sample provider configuration
    """
    return {
        "name": "openai",
        "display_name": "OpenAI",
        "is_active": True,
        "conversion_rate": 1.0,
    }
