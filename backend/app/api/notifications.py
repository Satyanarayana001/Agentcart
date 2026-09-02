from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.notification import (
    NotificationResponse,
    UnreadCountResponse,
)
from app.services.notification_service import (
    notification_service,
)


router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"],
)


@router.get(
    "/",
    response_model=list[NotificationResponse],
)
def get_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
):
    return notification_service.get_notifications(
        db,
        unread_only=unread_only,
    )


@router.get(
    "/unread-count",
    response_model=UnreadCountResponse,
)
def get_unread_count(
    db: Session = Depends(get_db),
):
    return {
        "unread_count": (
            notification_service.get_unread_count(db)
        )
    }


@router.post(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
):
    notification = (
        notification_service.mark_as_read(
            db,
            notification_id,
        )
    )

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found.",
        )

    return notification


@router.post(
    "/read-all",
)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
):
    notification_service.mark_all_as_read(db)

    return {
        "status": "success",
        "message": "All notifications marked as read.",
    }