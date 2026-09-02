from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.order import (
    OrderDetailResponse,
    OrderSummaryResponse,
)
from app.services.order_service import order_service


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"],
)


@router.get(
    "/",
    response_model=list[OrderSummaryResponse],
)
def get_orders(
    db: Session = Depends(get_db),
):
    return order_service.get_orders(db)


@router.get(
    "/{order_id}",
    response_model=OrderDetailResponse,
)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    order = order_service.get_order(
        db,
        order_id,
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found.",
        )

    return order