from datetime import datetime

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: str
    name: str
    quantity: int
    unit_price: float
    total_price: float


class OrderSummaryResponse(BaseModel):
    order_id: str
    plan_id: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    item_count: int
    primary_product: str


class OrderDetailResponse(BaseModel):
    order_id: str
    plan_id: str

    amount: float
    currency: str

    status: str

    razorpay_order_id: str
    razorpay_payment_id: str | None = None

    created_at: datetime

    items: list[OrderItemResponse]

    plan_status: str
    plan_explanation: str