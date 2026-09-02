from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.tracking import (
    TrackingAdvanceResponse,
    TrackingResponse,
)
from app.services.tracking_service import (
    tracking_service,
)


router = APIRouter(
    prefix="/api/orders",
    tags=["Order Tracking"],
)


@router.get(
    "/{order_id}/tracking",
    response_model=TrackingResponse,
)
def get_tracking(
    order_id: str,
    db: Session = Depends(get_db),
):
    tracking = tracking_service.get_tracking(
        db,
        order_id,
    )

    if tracking is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found.",
        )

    return tracking


@router.post(
    "/{order_id}/tracking/advance",
    response_model=TrackingAdvanceResponse,
)
def advance_tracking(
    order_id: str,
    db: Session = Depends(get_db),
):
    try:
        return tracking_service.advance_tracking(
            db,
            order_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )