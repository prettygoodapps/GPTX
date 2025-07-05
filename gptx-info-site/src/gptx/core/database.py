from datetime import datetime, timezone
from typing import Generator, Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

from gptx.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False}
        if "sqlite" in settings.DATABASE_URL
        else {}
    ),
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create base class for models
class Base(DeclarativeBase):
    pass


class TokenWrapper(Base):
    """
    Model for tracking wrapped AI service credits.

    This table stores information about AI service credits that have been
    wrapped into GPTX tokens on the blockchain.
    """

    __tablename__ = "token_wrappers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_address: Mapped[str] = mapped_column(
        String, index=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g., "openai", "anthropic"
    original_credits: Mapped[float] = mapped_column(Float, nullable=False)
    wrapped_tokens: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_hash: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Exchange(Base):
    """
    Model for tracking token exchanges.

    This table stores information about completed token trades
    between users on the GPTX Exchange platform.
    """

    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    seller_address: Mapped[str] = mapped_column(
        String, index=True, nullable=False
    )
    buyer_address: Mapped[str] = mapped_column(
        String, index=True, nullable=False
    )
    token_amount: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_token: Mapped[float] = mapped_column(Float, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_hash: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    status: Mapped[str] = mapped_column(
        String, default="completed"
    )  # pending, completed, failed


class CarbonOffset(Base):
    """
    Model for tracking carbon offset purchases.

    This table stores information about carbon offsets purchased
    when GPTX tokens are retired from circulation.
    """

    __tablename__ = "carbon_offsets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_address: Mapped[str] = mapped_column(
        String, index=True, nullable=False
    )
    tokens_retired: Mapped[float] = mapped_column(Float, nullable=False)
    carbon_credits_purchased: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # in tons CO2
    offset_provider: Mapped[str] = mapped_column(String, nullable=False)
    offset_certificate_id: Mapped[Optional[str]] = mapped_column(
        String, unique=True
    )
    transaction_hash: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    additional_data: Mapped[Optional[str]] = mapped_column(
        Text
    )  # JSON string for additional data


class AIProvider(Base):
    """
    Model for supported AI service providers.

    This table stores configuration and metadata for AI service
    providers that can be wrapped into GPTX tokens.
    """

    __tablename__ = "ai_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )  # e.g., "openai"
    display_name: Mapped[str] = mapped_column(
        String, nullable=False
    )  # e.g., "OpenAI"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    api_endpoint: Mapped[Optional[str]] = mapped_column(String)
    conversion_rate: Mapped[float] = mapped_column(
        Float, default=1.0
    )  # credits to GPTX token ratio
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


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