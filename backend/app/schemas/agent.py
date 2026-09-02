from pydantic import BaseModel, Field


class AgentPurchaseRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=3,
        description="Natural language purchase request from the user.",
    )


class AgentAlternative(BaseModel):
    product_id: str
    name: str
    price: float
    currency: str
    stock: int
    description: str
    reason: str


class AgentSelectedProduct(BaseModel):
    product_id: str
    name: str
    price: float
    currency: str
    stock: int
    quantity: int
    max_budget: float


class AgentPurchaseResponse(BaseModel):
    plan_id: str | None = None
    status: str
    explanation: str

    selected_product: AgentSelectedProduct | None = None

    alternatives: list[AgentAlternative] = Field(
        default_factory=list
    )


class AgentProductSelectionRequest(BaseModel):
    product_id: str
    quantity: int = Field(
        default=1,
        gt=0,
        le=10,
    )
    max_budget: float = Field(
        gt=0,
    )