import json
from pathlib import Path

from app.schemas.product import Product


DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "db"
    / "data"
    / "products.json"
)


class CatalogService:

    def __init__(self):
        self.products = self._load_products()

    def _load_products(self) -> list[Product]:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [Product(**product) for product in data]

    def get_all_products(self) -> list[Product]:
        return self.products

    def get_product_by_id(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def search_products(
        self,
        category: str | None = None,
        max_price: float | None = None,
        min_battery_hours: int | None = None,
        anc: bool | None = None,
    ) -> list[Product]:

        results = self.products

        if category:
            results = [
                product
                for product in results
                if product.category.lower() == category.lower()
            ]

        if max_price is not None:
            results = [
                product
                for product in results
                if product.price <= max_price
            ]

        if min_battery_hours is not None:
            results = [
                product
                for product in results
                if product.features.get("battery_hours", 0)
                >= min_battery_hours
            ]

        if anc is not None:
            results = [
                product
                for product in results
                if product.features.get("anc") == anc
            ]

        return results


catalog_service = CatalogService()