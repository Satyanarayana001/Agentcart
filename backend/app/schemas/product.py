from typing import Any

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    currency: str
    features: dict[str, Any]
    stock: int
    description: str
    compatible_products: list[str]

    image_url: str | None = None
    rating: float | None = None
    review_count: int | None = None