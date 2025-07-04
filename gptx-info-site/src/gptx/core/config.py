"""
Configuration settings for GPTX Exchange.

This module contains all configuration settings using Pydantic Settings
for type-safe configuration management following 12-factor app principles.
"""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    All settings can be overridden via environment variables.
    Settings are validated using Pydantic for type safety.
    """

    # Application
    APP_NAME: str = "GPTX Exchange"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Railway deployment support
    @property
    def port(self) -> int:
        """Get port from Railway's PORT env var or fallback to default."""
        import os
        return int(os.getenv("PORT", self.PORT))

    # Database
    DATABASE_URL: str = "sqlite:///./gptx.db"

    # Blockchain
    WEB3_PROVIDER_URL: str = "http://127.0.0.1:8545"  # Local Ganache/Hardhat
    ETHEREUM_RPC_URL: Optional[str] = None
    CHAIN_ID: int = 1337  # Local development chain
    PRIVATE_KEY: Optional[str] = None
    ETHEREUM_PRIVATE_KEY: Optional[str] = None
    CONTRACT_ADDRESS: Optional[str] = None

    # Carbon Offset API
    CARBON_API_URL: str = "https://api.carbonoffset.example.com"
    CARBON_API_KEY: Optional[str] = None
    CARBON_OFFSET_PROVIDER: str = "climatetrade"
    CARBON_OFFSET_API_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # AI Service Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    # CORS Settings
    ALLOWED_ORIGINS: str = '["http://localhost:3000", "http://localhost:8000"]'

    class Config:
        """Pydantic configuration for settings."""

        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
