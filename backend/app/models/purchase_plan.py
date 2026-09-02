from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.core.state_machine import PurchaseStatus


@dataclass
class PurchaseItemModel:
    product_id: str
    name: str
    quantity: int
    unit_price: float

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class PurchasePlan:
    items: list[PurchaseItemModel]
    max_budget: float
    currency: str = "INR"

    plan_id: str = field(default_factory=lambda: str(uuid4()))
    status: PurchaseStatus = PurchaseStatus.PLAN_CREATED
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def subtotal(self) -> float:
        return sum(item.total_price for item in self.items)