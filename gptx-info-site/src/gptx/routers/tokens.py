"""
Token management API endpoints.

This module provides API endpoints for wrapping AI service credits into GPTX tokens,
checking balances, and unwrapping tokens back to credits.
"""

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from gptx.core.database import AIProvider, TokenWrapper, get_db
from gptx.services.ai_providers import AIProviderService
from gptx.services.blockchain import BlockchainService

router = APIRouter()


class WrapCreditsRequest(BaseModel):
    """Request model for wrapping AI service credits into GPTX tokens."""

    provider: str
    credit_amount: float
    proof: str  # Simplified proof for POC


class WrapCreditsResponse(BaseModel):
    """Response model for successful credit wrapping."""

    transaction_hash: str
    tokens_issued: float
    message: str


class TokenBalance(BaseModel):
    """Response model for user token balance information."""

    user_address: str
    total_balance: float
    wrapped_credits: List[dict]


class ProviderInfo(BaseModel):
    """Response model for AI provider information."""

    name: str
    display_name: str
    is_active: bool
    conversion_rate: float


class UnwrapCreditsRequest(BaseModel):
    """Request model for unwrapping GPTX tokens back to credits."""

    provider: str
    token_amount: float


class UnwrapCreditsResponse(BaseModel):
    """Response model for successful token unwrapping."""

    message: str
    credits_restored: float
    provider: str
    transaction_hash: str


@router.get("/providers", response_model=List[ProviderInfo])
async def get_supported_providers(db: Session = Depends(get_db)) -> List[ProviderInfo]:
    """
    Get list of supported AI service providers.

    Args:
        db: Database session dependency

    Returns:
        List[ProviderInfo]: List of active AI service providers
    """
    providers = db.query(AIProvider).filter(AIProvider.is_active == True).all()
    return [
        ProviderInfo(
            name=p.name,
            display_name=p.display_name,
            is_active=p.is_active,
            conversion_rate=p.conversion_rate,
        )
        for p in providers
    ]


@router.post("/wrap", response_model=WrapCreditsResponse)
async def wrap_credits(
    request: WrapCreditsRequest,
    user_address: str,
    db: Session = Depends(get_db),
) -> WrapCreditsResponse:
    """
    Wrap AI service credits into GPTX tokens.

    This endpoint validates the user's AI service credits and creates
    corresponding GPTX tokens on the blockchain.

    Args:
        request: Credit wrapping request details
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        WrapCreditsResponse: Transaction details and tokens issued

    Raises:
        HTTPException: If provider is invalid, amount is invalid, or proof is insufficient
    """
    # Validate provider
    provider = (
        db.query(AIProvider)
        .filter(AIProvider.name == request.provider, AIProvider.is_active == True)
        .first()
    )

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider '{request.provider}' not supported",
        )

    # Validate credit amount
    if request.credit_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credit amount must be greater than 0",
        )

    # For POC: Simulate proof validation
    if not request.proof or len(request.proof) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid proof of credit ownership required",
        )

    try:
        # Initialize services
        blockchain_service = BlockchainService()
        ai_service = AIProviderService()

        # Verify credit ownership
        verification = await ai_service.verify_credit_ownership(
            request.provider, request.credit_amount, request.proof
        )

        if not verification.get("valid"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Credit verification failed: {verification.get('error')}",
            )

        # Calculate tokens to mint (using provider's conversion rate)
        tokens_to_mint = request.credit_amount * provider.conversion_rate

        # Create blockchain transaction
        tx_result = blockchain_service.wrap_credits_transaction(
            user_address, request.provider, request.credit_amount, request.proof
        )

        # Store in database
        wrapper = TokenWrapper(
            user_address=user_address,
            provider=request.provider,
            original_credits=request.credit_amount,
            wrapped_tokens=tokens_to_mint,
            transaction_hash=tx_result["transaction_hash"],
        )

        db.add(wrapper)
        db.commit()
        db.refresh(wrapper)

        return WrapCreditsResponse(
            transaction_hash=tx_result["transaction_hash"],
            tokens_issued=tokens_to_mint,
            message=f"Successfully wrapped {request.credit_amount} {request.provider} credits into {tokens_to_mint} GPTX tokens",
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to wrap credits: {str(e)}",
        )


@router.get("/balance/{user_address}", response_model=TokenBalance)
async def get_token_balance(
    user_address: str, db: Session = Depends(get_db)
) -> TokenBalance:
    """
    Get token balance and wrapped credits for a user.

    Args:
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        TokenBalance: User's total balance and detailed wrapped credits
    """
    # Get all wrapped credits for user
    wrapped_credits = (
        db.query(TokenWrapper)
        .filter(
            TokenWrapper.user_address == user_address, TokenWrapper.is_active == True
        )
        .all()
    )

    # Calculate total balance
    total_balance = sum(w.wrapped_tokens for w in wrapped_credits)

    # Format wrapped credits info
    credits_info = []
    for wrapper in wrapped_credits:
        credits_info.append(
            {
                "provider": wrapper.provider,
                "original_credits": wrapper.original_credits,
                "wrapped_tokens": wrapper.wrapped_tokens,
                "transaction_hash": wrapper.transaction_hash,
                "created_at": wrapper.created_at.isoformat(),
            }
        )

    return TokenBalance(
        user_address=user_address,
        total_balance=total_balance,
        wrapped_credits=credits_info,
    )


@router.post("/unwrap", response_model=UnwrapCreditsResponse)
async def unwrap_credits(
    request: UnwrapCreditsRequest,
    user_address: str,
    db: Session = Depends(get_db),
) -> UnwrapCreditsResponse:
    """
    Unwrap GPTX tokens back to AI service credits.

    This endpoint burns GPTX tokens and restores the equivalent
    AI service credits to the user's provider account.

    Args:
        request: Unwrapping request details
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        UnwrapCreditsResponse: Transaction details and credits restored

    Raises:
        HTTPException: If provider is invalid or insufficient tokens
    """
    # Validate provider
    provider_obj = (
        db.query(AIProvider)
        .filter(AIProvider.name == request.provider, AIProvider.is_active == True)
        .first()
    )

    if not provider_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Provider '{request.provider}' not supported",
        )

    # Check user's wrapped credits for this provider
    user_wrappers = (
        db.query(TokenWrapper)
        .filter(
            TokenWrapper.user_address == user_address,
            TokenWrapper.provider == request.provider,
            TokenWrapper.is_active == True,
        )
        .all()
    )

    total_wrapped = sum(w.wrapped_tokens for w in user_wrappers)

    if total_wrapped < request.token_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient wrapped tokens. Available: {total_wrapped}, Requested: {request.token_amount}",
        )

    try:
        # Initialize services
        blockchain_service = BlockchainService()
        ai_service = AIProviderService()

        # Calculate credits to restore
        credits_to_restore = request.token_amount / provider_obj.conversion_rate

        # Create blockchain transaction
        tx_result = blockchain_service.unwrap_credits_transaction(
            user_address, request.provider, request.token_amount
        )

        # Mark tokens as unwrapped (simplified - in production would be more complex)
        remaining_to_unwrap = request.token_amount
        for wrapper in user_wrappers:
            if remaining_to_unwrap <= 0:
                break

            if wrapper.wrapped_tokens <= remaining_to_unwrap:
                # Unwrap entire wrapper
                wrapper.is_active = False
                remaining_to_unwrap -= wrapper.wrapped_tokens
            else:
                # Partial unwrap - would need more complex logic in production
                wrapper.wrapped_tokens -= remaining_to_unwrap
                remaining_to_unwrap = 0

        # Restore credits to AI provider account
        restore_result = await ai_service.restore_credits(
            request.provider, credits_to_restore, user_address
        )

        db.commit()

        return UnwrapCreditsResponse(
            message=f"Successfully unwrapped {request.token_amount} GPTX tokens back to {credits_to_restore} {request.provider} credits",
            credits_restored=credits_to_restore,
            provider=request.provider,
            transaction_hash=tx_result["transaction_hash"],
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unwrap tokens: {str(e)}",
        )
