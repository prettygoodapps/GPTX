"""Test database setup and configuration."""

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from gptx.core.database import Base, SessionLocal, engine


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session for testing.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_database_setup() -> None:
    """
    Test if database components can be imported and initialized.
    """
    assert Base is not None
    assert engine is not None
    assert SessionLocal is not None
    assert get_db is not None
