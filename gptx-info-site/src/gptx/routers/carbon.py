"""
Carbon offset API endpoints.

This module provides API endpoints for retiring GPTX tokens to purchase
carbon offsets, viewing offset history, and accessing offset certificates.
"""

import json
from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from gptx.core.database import CarbonOffset, TokenWrapper, get_db
from gptx.services.blockchain import BlockchainService

router = APIRouter()


class RetireTokensRequest(BaseModel):
    """Request model for retiring tokens to purchase carbon offsets."""

    token_amount: float
    reason: str = "Carbon offset retirement"


class CarbonOffsetResponse(BaseModel):
    """Response model for successful carbon offset purchase."""

    transaction_hash: str
    tokens_retired: float
    carbon_credits_purchased: float
    offset_provider: str
    certificate_id: str
    message: str


class OffsetInfo(BaseModel):
    """Response model for carbon offset information."""

    id: int
    user_address: str
    tokens_retired: float
    carbon_credits_purchased: float
    offset_provider: str
    certificate_id: str
    created_at: str


@router.post("/retire", response_model=CarbonOffsetResponse)
async def retire_tokens_for_offset(
    request: RetireTokensRequest,
    user_address: str,
    db: Session = Depends(get_db),
) -> CarbonOffsetResponse:
    """
    Retire GPTX tokens and purchase carbon offsets.

    This endpoint burns GPTX tokens from the user's balance and
    purchases equivalent carbon offset credits.

    Args:
        request: Token retirement request details
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        CarbonOffsetResponse: Transaction details and offset certificate

    Raises:
        HTTPException: If token amount is invalid or insufficient balance
    """
    if request.token_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token amount must be greater than 0",
        )

    # Check if user has enough tokens
    user_wrappers = (
        db.query(TokenWrapper)
        .filter(
            TokenWrapper.user_address == user_address,
            TokenWrapper.is_active.is_(True)
        )
        .all()
    )

    total_balance = sum(w.wrapped_tokens for w in user_wrappers)

    if total_balance < request.token_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Insufficient token balance. Available: {total_balance}, "
                f"Requested: {request.token_amount}"
            ),
        )

    try:
        # Initialize blockchain service
        blockchain_service = BlockchainService()

        # For POC: Simulate carbon offset calculation
        # Assume 1 GPTX token = 0.001 tons CO2 offset (configurable in production)
        carbon_credits_purchased = request.token_amount * 0.001

        # Mock offset provider and certificate
        offset_provider = "GreenCarbon Solutions"
        certificate_id = (
            f"GCS-{datetime.utcnow().strftime('%Y%m%d')}-"
            f"{hash(user_address + str(request.token_amount)) & 0xffff:04x}"
        )

        # Create blockchain transaction for token retirement
        tx_result = blockchain_service.retire_tokens_transaction(
            user_address, request.token_amount, request.reason
        )

        # Store carbon offset record
        offset_record = CarbonOffset(
            user_address=user_address,
            tokens_retired=request.token_amount,
            carbon_credits_purchased=carbon_credits_purchased,
            offset_provider=offset_provider,
            offset_certificate_id=certificate_id,
            transaction_hash=tx_result["transaction_hash"],
            metadata=json.dumps(
                {
                    "reason": request.reason,
                    "offset_rate": 0.001,
                    "provider_details": {
                        "name": offset_provider,
                        "verification": "Gold Standard",
                        "project_type": "Renewable Energy",
                    },
                }
            ),
        )

        db.add(offset_record)

        # Mark tokens as retired (simplified - burn tokens from user's balance)
        remaining_to_retire = request.token_amount
        for wrapper in user_wrappers:
            if remaining_to_retire <= 0:
                break

            if wrapper.wrapped_tokens <= remaining_to_retire:
                # Retire entire wrapper
                remaining_to_retire -= wrapper.wrapped_tokens
                wrapper.is_active = False
            else:
                # Partial retirement
                wrapper.wrapped_tokens -= remaining_to_retire
                remaining_to_retire = 0

        db.commit()
        db.refresh(offset_record)

        return CarbonOffsetResponse(
            transaction_hash=tx_result["transaction_hash"],
            tokens_retired=request.token_amount,
            carbon_credits_purchased=carbon_credits_purchased,
            offset_provider=offset_provider,
            certificate_id=certificate_id,
            message=(
                f"Successfully retired {request.token_amount} GPTX tokens "
                f"and purchased {carbon_credits_purchased} tons CO2 offset"
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retire tokens and purchase offset: {str(e)}",
        )


@router.get("/history/{user_address}", response_model=List[OffsetInfo])
async def get_offset_history(
    user_address: str, db: Session = Depends(get_db)
) -> List[OffsetInfo]:
    """
    Get carbon offset history for a user.

    Args:
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        List[OffsetInfo]: User's complete carbon offset history
    """
    offsets = (
        db.query(CarbonOffset)
        .filter(CarbonOffset.user_address == user_address)
        .order_by(CarbonOffset.created_at.desc())
        .all()
    )

    return [
        OffsetInfo(
            id=offset.id,
            user_address=offset.user_address,
            tokens_retired=offset.tokens_retired,
            carbon_credits_purchased=offset.carbon_credits_purchased,
            offset_provider=offset.offset_provider,
            certificate_id=offset.offset_certificate_id,
            created_at=offset.created_at.isoformat(),
        )
        for offset in offsets
    ]


@router.get("/stats")
async def get_carbon_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get overall carbon offset statistics.

    Args:
        db: Database session dependency

    Returns:
        Dict[str, Any]: Platform-wide carbon offset statistics and
            environmental impact
    """
    # Total offsets
    total_offsets = db.query(CarbonOffset).count()

    # Total tokens retired
    total_tokens_retired = (
        db.query(CarbonOffset)
        .with_entities(func.sum(CarbonOffset.tokens_retired))
        .scalar()
        or 0
    )

    # Total carbon credits purchased
    total_carbon_credits = (
        db.query(CarbonOffset)
        .with_entities(func.sum(CarbonOffset.carbon_credits_purchased))
        .scalar()
        or 0
    )

    # Get recent offsets
    recent_offsets = (
        db.query(CarbonOffset)
        .order_by(CarbonOffset.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_offsets": total_offsets,
        "total_tokens_retired": float(total_tokens_retired),
        "total_carbon_credits_purchased": float(total_carbon_credits),
        "environmental_impact": {
            "co2_offset_tons": float(total_carbon_credits),
            "equivalent_trees_planted": int(
                float(total_carbon_credits) * 40
            ),  # Rough estimate
            "equivalent_cars_removed": int(
                float(total_carbon_credits) / 4.6
            ),  # Average car emissions per year
        },
        "recent_offsets": [
            {
                "tokens_retired": offset.tokens_retired,
                "carbon_credits": offset.carbon_credits_purchased,
                "provider": offset.offset_provider,
                "created_at": offset.created_at.isoformat(),
            }
            for offset in recent_offsets
        ],
    }


@router.get("/certificate/{certificate_id}")
async def get_offset_certificate(
    certificate_id: str, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get details of a specific carbon offset certificate.

    Args:
        certificate_id: Unique certificate identifier
        db: Database session dependency

    Returns:
        Dict[str, Any]: Complete certificate details and verification
            information

    Raises:
        HTTPException: If certificate is not found
    """
    offset = (
        db.query(CarbonOffset)
        .filter(CarbonOffset.offset_certificate_id == certificate_id)
        .first()
    )

    if not offset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )

    metadata = json.loads(offset.metadata) if offset.metadata else {}

    return {
        "certificate_id": offset.offset_certificate_id,
        "user_address": offset.user_address,
        "tokens_retired": offset.tokens_retired,
        "carbon_credits_purchased": offset.carbon_credits_purchased,
        "offset_provider": offset.offset_provider,
        "transaction_hash": offset.transaction_hash,
        "created_at": offset.created_at.isoformat(),
        "metadata": metadata,
        "verification_url": (
            f"https://registry.goldstandard.org/projects/{certificate_id}"
        ),  # Mock URL
        "status": "verified",
    }
