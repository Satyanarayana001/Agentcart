from fastapi.testclient import TestClient

from app.main import app
from app.services.catalog_service import catalog_service


client = TestClient(app)


def test_catalog_returns_products():
    products = catalog_service.get_all_products()

    assert len(products) > 0


def test_get_existing_product():
    product = catalog_service.get_product_by_id("hp_001")

    assert product is not None
    assert product.id == "hp_001"
    assert product.name == "SoundMax Pro ANC"
    assert product.price == 4499


def test_get_nonexistent_product():
    product = catalog_service.get_product_by_id(
        "does_not_exist"
    )

    assert product is None


def test_search_by_category():
    results = catalog_service.search_products(
        category="headphones"
    )

    assert len(results) > 0

    for product in results:
        assert product.category.lower() == "headphones"


def test_search_by_max_price():
    results = catalog_service.search_products(
        max_price=5000
    )

    assert len(results) > 0

    for product in results:
        assert product.price <= 5000


def test_search_by_anc():
    results = catalog_service.search_products(
        anc=True
    )

    assert len(results) > 0

    for product in results:
        assert product.features.get("anc") is True


def test_search_combined_filters():
    results = catalog_service.search_products(
        category="headphones",
        max_price=5000,
        anc=True,
    )

    for product in results:
        assert product.category.lower() == "headphones"
        assert product.price <= 5000
        assert product.features.get("anc") is True


def test_catalog_api_returns_products():
    response = client.get(
        "/api/catalog/products"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_catalog_api_get_product():
    response = client.get(
        "/api/catalog/products/hp_001"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "hp_001"
    assert data["name"] == "SoundMax Pro ANC"
    assert data["price"] == 4499


def test_catalog_api_product_not_found():
    response = client.get(
        "/api/catalog/products/does_not_exist"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_catalog_api_search():
    response = client.get(
        "/api/catalog/search",
        params={
            "max_price": 5000,
            "anc": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for product in data:
        assert product["price"] <= 5000
        assert product["features"]["anc"] is True