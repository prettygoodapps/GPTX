"""
Logging configuration for GPTX Exchange.

This module provides structured logging configuration with proper
formatting and log levels for the GPTX Exchange platform.
"""

import logging
import sys
from typing import Any, Dict

from gptx.core.config import settings


def setup_logging() -> None:
    """
    Configure application logging.

    Sets up structured logging with appropriate formatters and handlers
    based on the environment configuration.
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Configure specific loggers
    loggers_config = {
        "uvicorn": logging.INFO,
        "uvicorn.error": logging.INFO,
        "uvicorn.access": logging.INFO,
        "sqlalchemy.engine": logging.WARNING,
        "httpx": logging.WARNING,
    }

    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class StructuredLogger:
    """
    Structured logger for consistent log formatting.

    Provides methods for logging with structured data and consistent
    formatting across the application.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize structured logger.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs: Any) -> None:
        """
        Log info message with structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        extra_data = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.info(full_message)

    def error(self, message: str, **kwargs: Any) -> None:
        """
        Log error message with structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        extra_data = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.error(full_message)

    def warning(self, message: str, **kwargs: Any) -> None:
        """
        Log warning message with structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        extra_data = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.warning(full_message)

    def debug(self, message: str, **kwargs: Any) -> None:
        """
        Log debug message with structured data.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        extra_data = " | ".join(f"{k}={v}" for k, v in kwargs.items())
        full_message = f"{message} | {extra_data}" if extra_data else message
        self.logger.debug(full_message)
