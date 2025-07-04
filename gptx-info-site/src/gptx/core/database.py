"""
Database configuration and models for GPTX Exchange.

This module contains SQLAlchemy models and database configuration
for the GPTX Exchange platform with proper type hints and documentation.
"""

from datetime import datetime
from typing import Generator

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from gptx.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    ),
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class TokenWrapper(Base):
    """
    Model for tracking wrapped AI service credits.

    This table stores information about AI service credits that have been
    wrapped into GPTX tokens on the blockchain.
    """

    __tablename__ = "token_wrappers"

    id = Column(Integer, primary_key=True, index=True)
    user_address = Column(String, index=True, nullable=False)
    provider = Column(String, nullable=False)  # e.g., "openai", "anthropic"
    original_credits = Column(Float, nullable=False)
    wrapped_tokens = Column(Float, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Exchange(Base):
    """
    Model for tracking token exchanges.

    This table stores information about completed token trades
    between users on the GPTX Exchange platform.
    """

    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)
    seller_address = Column(String, index=True, nullable=False)
    buyer_address = Column(String, index=True, nullable=False)
    token_amount = Column(Float, nullable=False)
    price_per_token = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    transaction_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="completed")  # pending, completed, failed


class CarbonOffset(Base):
    """
    Model for tracking carbon offset purchases.

    This table stores information about carbon offsets purchased
    when GPTX tokens are retired from circulation.
    """

    __tablename__ = "carbon_offsets"

    id = Column(Integer, primary_key=True, index=True)
    user_address = Column(String, index=True, nullable=False)
    tokens_retired = Column(Float, nullable=False)
    carbon_credits_purchased = Column(Float, nullable=False)  # in tons CO2
    offset_provider = Column(String, nullable=False)
    offset_certificate_id = Column(String, unique=True)
    transaction_hash = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(Text)  # JSON string for additional data


class AIProvider(Base):
    """
    Model for supported AI service providers.

    This table stores configuration and metadata for AI service
    providers that can be wrapped into GPTX tokens.
    """

    __tablename__ = "ai_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "openai"
    display_name = Column(String, nullable=False)  # e.g., "OpenAI"
    is_active = Column(Boolean, default=True)
    api_endpoint = Column(String)
    conversion_rate = Column(Float, default=1.0)  # credits to GPTX token ratio
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.

    This function provides a database session for dependency injection
    in FastAPI endpoints with proper cleanup.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
