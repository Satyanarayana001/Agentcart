import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import NotificationDB


class NotificationService:

    def create_notification(
        self,
        db: Session,
        order_id: str,
        plan_id: str,
        title: str,
        message: str,
        notification_type: str,
    ):
        notification = NotificationDB(
            notification_id=str(uuid.uuid4()),
            order_id=order_id,
            plan_id=plan_id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            created_at=datetime.utcnow(),
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification


    def get_notifications(
        self,
        db: Session,
        unread_only: bool = False,
    ):
        query = db.query(NotificationDB)

        if unread_only:
            query = query.filter(
                NotificationDB.is_read.is_(False)
            )

        return (
            query
            .order_by(
                NotificationDB.created_at.desc()
            )
            .all()
        )


    def get_unread_count(
        self,
        db: Session,
    ):
        return (
            db.query(NotificationDB)
            .filter(
                NotificationDB.is_read.is_(False)
            )
            .count()
        )


    def mark_as_read(
        self,
        db: Session,
        notification_id: str,
    ):
        notification = (
            db.query(NotificationDB)
            .filter(
                NotificationDB.notification_id
                == notification_id
            )
            .first()
        )

        if notification is None:
            return None

        notification.is_read = True

        db.commit()
        db.refresh(notification)

        return notification


    def mark_all_as_read(
        self,
        db: Session,
    ):
        (
            db.query(NotificationDB)
            .filter(
                NotificationDB.is_read.is_(False)
            )
            .update(
                {
                    NotificationDB.is_read: True
                },
                synchronize_session=False,
            )
        )

        db.commit()


notification_service = NotificationService()