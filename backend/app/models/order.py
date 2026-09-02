from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class PaymentOrder:
    plan_id: str
    razorpay_order_id: str
    amount: float
    currency: str

    payment_order_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    status: str = "ORDER_CREATED"

    razorpay_payment_id: str | None = None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )