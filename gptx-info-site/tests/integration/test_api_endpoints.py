"""
Integration tests for GPTX Exchange API endpoints.

This module tests the complete API functionality including
token wrapping, trading, and carbon offsetting workflows.
"""

import pytest
from fastapi.testclient import TestClient

from gptx.core.database import AIProvider


class TestTokenEndpoints:
    """Integration tests for token management endpoints."""

    def test_get_providers(self, client: TestClient, test_db):
        """Test getting supported AI providers."""
        # Add a test provider
        provider = AIProvider(
            name="test_provider",
            display_name="Test Provider",
            is_active=True,
            conversion_rate=1.0,
        )
        test_db.add(provider)
        test_db.commit()

        response = client.get("/api/tokens/providers")
        assert response.status_code == 200

        providers = response.json()
        assert len(providers) >= 1

        test_provider = next(
            (p for p in providers if p["name"] == "test_provider"), None
        )
        assert test_provider is not None
        assert test_provider["display_name"] == "Test Provider"

    def test_wrap_credits_flow(self, client: TestClient, test_db, sample_user_address):
        """Test the complete credit wrapping flow."""
        # Add a test provider
        provider = AIProvider(
            name="openai", display_name="OpenAI", is_active=True, conversion_rate=1.0
        )
        test_db.add(provider)
        test_db.commit()

        # Test wrapping credits
        wrap_request = {
            "provider": "openai",
            "credit_amount": 100.0,
            "proof": "test_proof_12345",
        }

        response = client.post(
            f"/api/tokens/wrap?user_address={sample_user_address}", json=wrap_request
        )

        assert response.status_code == 200
        result = response.json()

        assert "transaction_hash" in result
        assert result["tokens_issued"] == 100.0
        assert "Successfully wrapped" in result["message"]

    def test_get_balance(self, client: TestClient, sample_user_address):
        """Test getting user token balance."""
        response = client.get(f"/api/tokens/balance/{sample_user_address}")
        assert response.status_code == 200

        balance = response.json()
        assert "user_address" in balance
        assert "total_balance" in balance
        assert "wrapped_credits" in balance
        assert balance["user_address"] == sample_user_address


class TestExchangeEndpoints:
    """Integration tests for exchange endpoints."""

    def test_get_orders(self, client: TestClient):
        """Test getting active trading orders."""
        response = client.get("/api/exchange/orders")
        assert response.status_code == 200

        orders = response.json()
        assert isinstance(orders, list)
        # Should have mock orders in POC
        assert len(orders) >= 0

    def test_execute_trade(self, client: TestClient, sample_user_address):
        """Test executing a trade."""
        trade_request = {"order_id": 1, "token_amount": 50.0}

        response = client.post(
            f"/api/exchange/trade?buyer_address={sample_user_address}",
            json=trade_request,
        )

        assert response.status_code == 200
        result = response.json()

        assert "transaction_hash" in result
        assert "Successfully traded" in result["message"]
        assert "trade_details" in result

    def test_get_trade_history(self, client: TestClient, sample_user_address):
        """Test getting trade history."""
        response = client.get(f"/api/exchange/history/{sample_user_address}")
        assert response.status_code == 200

        history = response.json()
        assert "user_address" in history
        assert "trade_count" in history
        assert "trades" in history

    def test_get_exchange_stats(self, client: TestClient):
        """Test getting exchange statistics."""
        response = client.get("/api/exchange/stats")
        assert response.status_code == 200

        stats = response.json()
        assert "total_trades" in stats
        assert "total_volume" in stats
        assert "total_value" in stats
        assert "recent_trades" in stats


class TestCarbonEndpoints:
    """Integration tests for carbon offset endpoints."""

    def test_retire_tokens(self, client: TestClient, test_db, sample_user_address):
        """Test retiring tokens for carbon offset."""
        # First need to have some tokens - add a mock wrapper
        from gptx.core.database import TokenWrapper

        wrapper = TokenWrapper(
            user_address=sample_user_address,
            provider="openai",
            original_credits=100.0,
            wrapped_tokens=100.0,
            transaction_hash="0x123456789",
            is_active=True,
        )
        test_db.add(wrapper)
        test_db.commit()

        retire_request = {
            "token_amount": 25.0,
            "reason": "Environmental sustainability test",
        }

        response = client.post(
            f"/api/carbon/retire?user_address={sample_user_address}",
            json=retire_request,
        )

        assert response.status_code == 200
        result = response.json()

        assert "transaction_hash" in result
        assert result["tokens_retired"] == 25.0
        assert result["carbon_credits_purchased"] > 0
        assert "certificate_id" in result

    def test_get_offset_history(self, client: TestClient, sample_user_address):
        """Test getting carbon offset history."""
        response = client.get(f"/api/carbon/history/{sample_user_address}")
        assert response.status_code == 200

        history = response.json()
        assert isinstance(history, list)

    def test_get_carbon_stats(self, client: TestClient):
        """Test getting carbon offset statistics."""
        response = client.get("/api/carbon/stats")
        assert response.status_code == 200

        stats = response.json()
        assert "total_offsets" in stats
        assert "total_tokens_retired" in stats
        assert "total_carbon_credits_purchased" in stats
        assert "environmental_impact" in stats
        assert "recent_offsets" in stats


class TestHealthEndpoints:
    """Integration tests for health and info endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        health = response.json()
        assert health["status"] == "healthy"
        assert "version" in health

    def test_api_info(self, client: TestClient):
        """Test API info endpoint."""
        response = client.get("/api/info")
        assert response.status_code == 200

        info = response.json()
        assert "name" in info
        assert "version" in info
        assert "endpoints" in info
        assert "tokens" in info["endpoints"]
        assert "exchange" in info["endpoints"]
        assert "carbon" in info["endpoints"]

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestErrorHandling:
    """Integration tests for error handling."""

    def test_invalid_provider(self, client: TestClient, sample_user_address):
        """Test error handling for invalid provider."""
        wrap_request = {
            "provider": "invalid_provider",
            "credit_amount": 100.0,
            "proof": "test_proof_12345",
        }

        response = client.post(
            f"/api/tokens/wrap?user_address={sample_user_address}", json=wrap_request
        )

        assert response.status_code == 400
        assert "not supported" in response.json()["detail"]

    def test_invalid_token_amount(self, client: TestClient, sample_user_address):
        """Test error handling for invalid token amounts."""
        trade_request = {
            "order_id": 1,
            "token_amount": -10.0,  # Invalid negative amount
        }

        response = client.post(
            f"/api/exchange/trade?buyer_address={sample_user_address}",
            json=trade_request,
        )

        assert response.status_code == 400
        assert "greater than 0" in response.json()["detail"]

    def test_nonexistent_certificate(self, client: TestClient):
        """Test error handling for nonexistent certificate."""
        response = client.get("/api/carbon/certificate/nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
