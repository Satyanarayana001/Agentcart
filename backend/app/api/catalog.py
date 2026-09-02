from fastapi import APIRouter, HTTPException

from app.schemas.product import Product
from app.services.catalog_service import catalog_service


router = APIRouter(
    prefix="/api/catalog",
    tags=["Catalog"]
)


@router.get("/products", response_model=list[Product])
def get_products():
    return catalog_service.get_all_products()


@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    product = catalog_service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.get("/search", response_model=list[Product])
def search_products(
    category: str | None = None,
    max_price: float | None = None,
    min_battery_hours: int | None = None,
    anc: bool | None = None,
):
    return catalog_service.search_products(
        category=category,
        max_price=max_price,
        min_battery_hours=min_battery_hours,
        anc=anc,
    )