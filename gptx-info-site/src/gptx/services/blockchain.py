"""
Blockchain service for interacting with smart contracts.

This module provides services for blockchain interactions including
token wrapping, unwrapping, and retirement with proper type safety.
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

from eth_account import Account
from web3 import Web3

from gptx.core.config import settings


class BlockchainService:
    """
    Service for blockchain interactions.

    This service handles all blockchain-related operations including
    smart contract interactions, transaction management, and gas estimation.
    """

    def __init__(self) -> None:
        """Initialize the blockchain service with Web3 connection and contract setup."""
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
        self.chain_id = settings.CHAIN_ID
        self.private_key = settings.PRIVATE_KEY
        self.contract_address = settings.CONTRACT_ADDRESS

        # For POC: Use mock contract ABI
        self.contract_abi = self._get_mock_contract_abi()

        if self.contract_address and self.w3.is_connected():
            self.contract = self.w3.eth.contract(
                address=self.contract_address, abi=self.contract_abi
            )
        else:
            self.contract = None

    def _get_mock_contract_abi(self) -> list[Dict[str, Any]]:
        """
        Get mock contract ABI for POC.

        Returns:
            list[Dict[str, Any]]: Mock contract ABI definition
        """
        return [
            {
                "inputs": [
                    {"name": "provider", "type": "string"},
                    {"name": "creditAmount", "type": "uint256"},
                    {"name": "proof", "type": "bytes32"},
                ],
                "name": "wrapCredits",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"name": "provider", "type": "string"},
                    {"name": "tokenAmount", "type": "uint256"},
                ],
                "name": "unwrapCredits",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
            {
                "inputs": [
                    {"name": "tokenAmount", "type": "uint256"},
                    {"name": "reason", "type": "string"},
                ],
                "name": "retireTokens",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            },
        ]

    def is_connected(self) -> bool:
        """
        Check if connected to blockchain.

        Returns:
            bool: True if connected to blockchain, False otherwise
        """
        return self.w3.is_connected()

    def get_account_balance(self, address: str) -> float:
        """
        Get ETH balance for an address.

        Args:
            address: Ethereum address to check balance for

        Returns:
            float: ETH balance in ether units
        """
        if not self.w3.is_connected():
            return 0.0

        try:
            balance_wei = self.w3.eth.get_balance(address)
            return float(self.w3.from_wei(balance_wei, "ether"))
        except Exception:
            return 0.0

    def wrap_credits_transaction(
        self, user_address: str, provider: str, credit_amount: float, proof: str
    ) -> Dict[str, Any]:
        """
        Create a wrap credits transaction.

        This is a POC simulation. In production, this would create
        actual blockchain transactions.

        Args:
            user_address: User's Ethereum address
            provider: AI service provider identifier
            credit_amount: Amount of credits to wrap
            proof: Proof of credit ownership

        Returns:
            Dict[str, Any]: Transaction result with hash and details
        """
        # For POC: Simulate transaction without actual blockchain interaction
        transaction_hash = f"0x{hash(f'{user_address}{provider}{credit_amount}{datetime.utcnow()}') & 0xffffffffffffffffffffffffffffffffffffffff:040x}"

        return {
            "transaction_hash": transaction_hash,
            "status": "success",
            "gas_used": 150000,
            "block_number": 12345678,
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "user_address": user_address,
                "provider": provider,
                "credit_amount": credit_amount,
                "tokens_minted": credit_amount * 1.0,  # 1:1 ratio for POC
            },
        }

    def unwrap_credits_transaction(
        self, user_address: str, provider: str, token_amount: float
    ) -> Dict[str, Any]:
        """
        Create an unwrap credits transaction.

        This is a POC simulation. In production, this would create
        actual blockchain transactions to unwrap tokens back to credits.

        Args:
            user_address: User's Ethereum address
            provider: AI service provider identifier
            token_amount: Amount of tokens to unwrap

        Returns:
            Dict[str, Any]: Transaction result with hash and details
        """
        transaction_hash = f"0x{hash(f'{user_address}unwrap{provider}{token_amount}{datetime.utcnow()}') & 0xffffffffffffffffffffffffffffffffffffffff:040x}"

        return {
            "transaction_hash": transaction_hash,
            "status": "success",
            "gas_used": 120000,
            "block_number": 12345679,
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "user_address": user_address,
                "provider": provider,
                "token_amount": token_amount,
                "credits_restored": token_amount * 1.0,
            },
        }

    def retire_tokens_transaction(
        self, user_address: str, token_amount: float, reason: str
    ) -> Dict[str, Any]:
        """
        Create a retire tokens transaction.

        This is a POC simulation. In production, this would create
        actual blockchain transactions to retire tokens and trigger carbon offsets.

        Args:
            user_address: User's Ethereum address
            token_amount: Amount of tokens to retire
            reason: Reason for token retirement

        Returns:
            Dict[str, Any]: Transaction result with hash and details
        """
        transaction_hash = f"0x{hash(f'{user_address}retire{token_amount}{datetime.utcnow()}') & 0xffffffffffffffffffffffffffffffffffffffff:040x}"

        return {
            "transaction_hash": transaction_hash,
            "status": "success",
            "gas_used": 100000,
            "block_number": 12345680,
            "timestamp": datetime.utcnow().isoformat(),
            "details": {
                "user_address": user_address,
                "token_amount": token_amount,
                "reason": reason,
                "carbon_offset_triggered": True,
            },
        }

    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction receipt.

        This is a POC simulation. In production, this would retrieve
        actual transaction receipts from the blockchain.

        Args:
            tx_hash: Transaction hash to get receipt for

        Returns:
            Optional[Dict[str, Any]]: Transaction receipt or None if not found
        """
        # For POC: Return mock receipt
        return {
            "transactionHash": tx_hash,
            "status": 1,  # Success
            "blockNumber": 12345678,
            "gasUsed": 150000,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def estimate_gas_price(self) -> Dict[str, Any]:
        """
        Estimate current gas prices.

        Returns:
            Dict[str, Any]: Gas price estimates for different speeds with unit
        """
        if not self.w3.is_connected():
            # Return mock gas prices for POC
            return {"slow": 20.0, "standard": 25.0, "fast": 30.0, "unit": "gwei"}

        try:
            gas_price = self.w3.eth.gas_price
            gas_price_gwei = float(self.w3.from_wei(gas_price, "gwei"))

            return {
                "slow": gas_price_gwei * 0.8,
                "standard": gas_price_gwei,
                "fast": gas_price_gwei * 1.2,
                "unit": "gwei",
            }
        except Exception:
            return {"slow": 20.0, "standard": 25.0, "fast": 30.0, "unit": "gwei"}
