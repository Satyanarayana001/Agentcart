from datetime import datetime

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    notification_id: str
    order_id: str
    plan_id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime


class UnreadCountResponse(BaseModel):
    unread_count: int