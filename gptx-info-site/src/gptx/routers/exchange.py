"""
Token exchange API endpoints.

This module provides API endpoints for trading GPTX tokens between users,
managing orders, and viewing trade history and statistics.
"""

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from gptx.core.database import Exchange, TokenWrapper, get_db

router = APIRouter()


class CreateOrderRequest(BaseModel):
    """Request model for creating a new trading order."""

    token_amount: float
    price_per_token: float
    order_type: str  # "sell" or "buy"


class ExecuteTradeRequest(BaseModel):
    """Request model for executing a trade."""

    order_id: int
    token_amount: float


class OrderInfo(BaseModel):
    """Response model for trading order information."""

    id: int
    seller_address: str
    token_amount: float
    price_per_token: float
    total_price: float
    created_at: str
    status: str


class TradeResponse(BaseModel):
    """Response model for successful trade execution."""

    transaction_hash: str
    message: str
    trade_details: Dict[str, Any]


@router.get("/orders", response_model=List[OrderInfo])
async def get_active_orders(db: Session = Depends(get_db)) -> List[OrderInfo]:
    """
    Get all active sell orders.

    This is a POC implementation that returns mock orders.
    In production, this would query a real order book system.

    Args:
        db: Database session dependency

    Returns:
        List[OrderInfo]: List of active trading orders
    """
    # For POC: Return mock orders since we don't have a full order book system
    mock_orders = [
        OrderInfo(
            id=1,
            seller_address="0x1234567890123456789012345678901234567890",
            token_amount=100.0,
            price_per_token=0.95,
            total_price=95.0,
            created_at=datetime.utcnow().isoformat(),
            status="active",
        ),
        OrderInfo(
            id=2,
            seller_address="0x2345678901234567890123456789012345678901",
            token_amount=250.0,
            price_per_token=0.98,
            total_price=245.0,
            created_at=datetime.utcnow().isoformat(),
            status="active",
        ),
    ]

    return mock_orders


@router.post("/trade", response_model=TradeResponse)
async def execute_trade(
    request: ExecuteTradeRequest,
    buyer_address: str,
    db: Session = Depends(get_db),
) -> TradeResponse:
    """
    Execute a trade between buyer and seller.

    This endpoint processes a trade request, validates the transaction,
    and records the completed trade in the database.

    Args:
        request: Trade execution request details
        buyer_address: Buyer's Ethereum address
        db: Database session dependency

    Returns:
        TradeResponse: Transaction details and trade information

    Raises:
        HTTPException: If token amount is invalid or trade execution fails
    """
    # For POC: Simulate trade execution
    # In production, this would involve complex order matching and blockchain transactions

    if request.token_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token amount must be greater than 0",
        )

    try:
        # Mock seller address and price for POC
        seller_address = "0x1234567890123456789012345678901234567890"
        price_per_token = 0.95
        total_price = request.token_amount * price_per_token

        # Generate mock transaction hash
        transaction_hash = f"0x{hash(f'{buyer_address}{seller_address}{request.token_amount}{datetime.utcnow()}') & 0xffffffffffffffffffffffffffffffffffffffff:040x}"

        # Store trade in database
        trade = Exchange(
            seller_address=seller_address,
            buyer_address=buyer_address,
            token_amount=request.token_amount,
            price_per_token=price_per_token,
            total_price=total_price,
            transaction_hash=transaction_hash,
            status="completed",
        )

        db.add(trade)
        db.commit()
        db.refresh(trade)

        return TradeResponse(
            transaction_hash=transaction_hash,
            message=f"Successfully traded {request.token_amount} GPTX tokens",
            trade_details={
                "buyer": buyer_address,
                "seller": seller_address,
                "token_amount": request.token_amount,
                "price_per_token": price_per_token,
                "total_price": total_price,
                "timestamp": trade.created_at.isoformat(),
            },
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute trade: {str(e)}",
        )


@router.get("/history/{user_address}")
async def get_trade_history(
    user_address: str, db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get trade history for a user.

    Args:
        user_address: User's Ethereum address
        db: Database session dependency

    Returns:
        Dict[str, Any]: User's complete trade history with statistics
    """
    trades = (
        db.query(Exchange)
        .filter(
            (Exchange.buyer_address == user_address)
            | (Exchange.seller_address == user_address)
        )
        .order_by(Exchange.created_at.desc())
        .all()
    )

    history = []
    for trade in trades:
        history.append(
            {
                "id": trade.id,
                "type": "buy" if trade.buyer_address == user_address else "sell",
                "counterparty": (
                    trade.seller_address
                    if trade.buyer_address == user_address
                    else trade.buyer_address
                ),
                "token_amount": trade.token_amount,
                "price_per_token": trade.price_per_token,
                "total_price": trade.total_price,
                "transaction_hash": trade.transaction_hash,
                "created_at": trade.created_at.isoformat(),
                "status": trade.status,
            }
        )

    return {
        "user_address": user_address,
        "trade_count": len(history),
        "trades": history,
    }


@router.get("/stats")
async def get_exchange_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get exchange statistics.

    Args:
        db: Database session dependency

    Returns:
        Dict[str, Any]: Exchange statistics including volume and recent trades
    """
    # Get total trades
    total_trades = db.query(Exchange).count()

    # Get total volume
    total_volume = db.query(func.sum(Exchange.token_amount)).scalar() or 0

    # Get total value traded
    total_value = db.query(func.sum(Exchange.total_price)).scalar() or 0

    # Get recent trades
    recent_trades = (
        db.query(Exchange).order_by(Exchange.created_at.desc()).limit(10).all()
    )

    return {
        "total_trades": total_trades,
        "total_volume": float(total_volume),
        "total_value": float(total_value),
        "recent_trades": [
            {
                "token_amount": trade.token_amount,
                "price_per_token": trade.price_per_token,
                "created_at": trade.created_at.isoformat(),
            }
            for trade in recent_trades
        ],
    }
