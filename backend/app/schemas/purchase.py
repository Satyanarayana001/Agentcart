from pydantic import BaseModel, Field


class PurchaseItemRequest(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, le=10)


class CreatePurchasePlanRequest(BaseModel):
    items: list[PurchaseItemRequest] = Field(min_length=1)
    max_budget: float = Field(gt=0)
    currency: str = "INR"


class PurchaseItemResponse(BaseModel):
    product_id: str
    name: str
    quantity: int
    unit_price: float
    total_price: float


class PurchasePlanResponse(BaseModel):
    plan_id: str
    items: list[PurchaseItemResponse]
    subtotal: float
    currency: str
    max_budget: float
    status: str
    explanation: str