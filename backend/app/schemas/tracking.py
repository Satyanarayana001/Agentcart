from datetime import datetime

from pydantic import BaseModel


class TrackingEventResponse(BaseModel):
    status: str
    label: str
    description: str
    completed: bool
    current: bool
    timestamp: datetime | None = None


class TrackingResponse(BaseModel):
    order_id: str
    payment_status: str
    fulfillment_status: str
    fulfillment_label: str
    updated_at: datetime | None = None
    events: list[TrackingEventResponse]


class TrackingAdvanceResponse(BaseModel):
    order_id: str
    previous_status: str
    status: str
    label: str
    message: str