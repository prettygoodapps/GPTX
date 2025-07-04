"""
Unit tests for AI providers service.

This module tests the AIProviderService functionality including
credit verification, balance checking, and provider management.
"""

from unittest.mock import AsyncMock, patch

import pytest

from gptx.services.ai_providers import AIProviderService


class TestAIProviderService:
    """Test cases for AIProviderService."""

    @pytest.fixture
    def ai_service(self):
        """Create AIProviderService instance for testing."""
        return AIProviderService()

    def test_get_supported_providers(self, ai_service):
        """Test getting list of supported providers."""
        providers = ai_service.get_supported_providers()

        assert isinstance(providers, dict)
        assert "openai" in providers
        assert "anthropic" in providers
        assert "google" in providers

        for provider_id, info in providers.items():
            assert "name" in info
            assert "credit_unit" in info
            assert "available" in info
            assert isinstance(info["available"], bool)

    @pytest.mark.asyncio
    async def test_verify_credit_ownership_valid(self, ai_service):
        """Test valid credit ownership verification."""
        result = await ai_service.verify_credit_ownership(
            provider="openai", credit_amount=100.0, proof="valid_proof_12345"
        )

        assert result["valid"] is True
        assert result["provider"] == "openai"
        assert result["credit_amount"] == 100.0
        assert "verification_timestamp" in result
        assert "verification_id" in result

    @pytest.mark.asyncio
    async def test_verify_credit_ownership_invalid_provider(self, ai_service):
        """Test credit verification with invalid provider."""
        result = await ai_service.verify_credit_ownership(
            provider="invalid_provider", credit_amount=100.0, proof="valid_proof_12345"
        )

        assert result["valid"] is False
        assert "not supported" in result["error"]

    @pytest.mark.asyncio
    async def test_verify_credit_ownership_invalid_proof(self, ai_service):
        """Test credit verification with invalid proof."""
        result = await ai_service.verify_credit_ownership(
            provider="openai", credit_amount=100.0, proof="short"
        )

        assert result["valid"] is False
        assert "Invalid proof" in result["error"]

    @pytest.mark.asyncio
    async def test_verify_credit_ownership_invalid_amount(self, ai_service):
        """Test credit verification with invalid amount."""
        result = await ai_service.verify_credit_ownership(
            provider="openai", credit_amount=-10.0, proof="valid_proof_12345"
        )

        assert result["valid"] is False
        assert "must be positive" in result["error"]

    @pytest.mark.asyncio
    async def test_get_credit_balance(self, ai_service):
        """Test getting credit balance from provider."""
        result = await ai_service.get_credit_balance(
            provider="openai", api_key="test_key"
        )

        assert result["success"] is True
        assert result["provider"] == "openai"
        assert isinstance(result["balance"], float)
        assert result["unit"] == "tokens"

    @pytest.mark.asyncio
    async def test_restore_credits(self, ai_service):
        """Test restoring credits to user account."""
        result = await ai_service.restore_credits(
            provider="openai", credit_amount=50.0, user_identifier="test_user"
        )

        assert result["success"] is True
        assert result["provider"] == "openai"
        assert result["credits_restored"] == 50.0
        assert result["user_identifier"] == "test_user"
        assert "restoration_id" in result

    def test_calculate_carbon_footprint(self, ai_service):
        """Test carbon footprint calculation."""
        result = ai_service.calculate_carbon_footprint(
            provider="openai", credit_amount=1000.0
        )

        assert "estimated_carbon_kg" in result
        assert "estimated_carbon_tons" in result
        assert result["provider"] == "openai"
        assert result["credit_amount"] == 1000.0
        assert isinstance(result["estimated_carbon_kg"], float)

    @pytest.mark.asyncio
    async def test_health_check(self, ai_service):
        """Test provider health check."""
        result = await ai_service.health_check("openai")

        assert result["provider"] == "openai"
        assert result["status"] == "healthy"
        assert "api_available" in result
        assert "response_time_ms" in result
        assert "api_key_configured" in result
