from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_purchase_plan_is_blocked_when_over_budget():
    response = client.post(
        "/api/purchase/plans",
        json={
            "items": [
                {
                    "product_id": "hp_001",
                    "quantity": 1,
                }
            ],
            "max_budget": 4000,
            "currency": "INR",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "BLOCKED"
    assert data["subtotal"] == 4499
    assert data["max_budget"] == 4000
    assert "exceeds" in data["explanation"]


def test_purchase_plan_is_allowed_when_within_budget():
    response = client.post(
        "/api/purchase/plans",
        json={
            "items": [
                {
                    "product_id": "hp_001",
                    "quantity": 1,
                }
            ],
            "max_budget": 5000,
            "currency": "INR",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "AWAITING_APPROVAL"
    assert data["subtotal"] == 4499
    assert data["max_budget"] == 5000


def test_purchase_plan_is_allowed_at_exact_budget():
    response = client.post(
        "/api/purchase/plans",
        json={
            "items": [
                {
                    "product_id": "hp_001",
                    "quantity": 1,
                }
            ],
            "max_budget": 4499,
            "currency": "INR",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "AWAITING_APPROVAL"
    assert data["subtotal"] == 4499
    assert data["max_budget"] == 4499


def test_purchase_plan_rejects_invalid_quantity():
    response = client.post(
        "/api/purchase/plans",
        json={
            "items": [
                {
                    "product_id": "hp_001",
                    "quantity": 0,
                }
            ],
            "max_budget": 5000,
            "currency": "INR",
        },
    )

    assert response.status_code == 422


def test_purchase_plan_rejects_missing_items():
    response = client.post(
        "/api/purchase/plans",
        json={
            "items": [],
            "max_budget": 5000,
            "currency": "INR",
        },
    )

    assert response.status_code == 422