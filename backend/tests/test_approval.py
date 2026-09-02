from fastapi.testclient import TestClient

from app.core.state_machine import PurchaseStatus
from app.main import app
from app.schemas.purchase import (
    CreatePurchasePlanRequest,
    PurchaseItemRequest,
)
from app.services.approval_service import approval_service
from app.services.purchase_service import purchase_service


client = TestClient(app)


def create_valid_plan():
    request = CreatePurchasePlanRequest(
        items=[
            PurchaseItemRequest(
                product_id="hp_001",
                quantity=1,
            )
        ],
        max_budget=5000,
        currency="INR",
    )

    return purchase_service.create_plan(request)


def create_blocked_plan():
    request = CreatePurchasePlanRequest(
        items=[
            PurchaseItemRequest(
                product_id="hp_001",
                quantity=1,
            )
        ],
        max_budget=4000,
        currency="INR",
    )

    return purchase_service.create_plan(request)


def test_approve_plan():
    plan = create_valid_plan()

    assert plan.status == PurchaseStatus.AWAITING_APPROVAL

    approved_plan = approval_service.approve_plan(
        plan.plan_id
    )

    assert approved_plan.status == PurchaseStatus.APPROVED


def test_approve_plan_is_persisted():
    plan = create_valid_plan()

    approval_service.approve_plan(plan.plan_id)

    # Force a fresh service instance so the result
    # must come from SQLite rather than the current
    # in-memory object.
    from app.services.purchase_service import PurchaseService

    fresh_service = PurchaseService()

    recovered_plan = fresh_service.get_plan(
        plan.plan_id
    )

    assert recovered_plan is not None
    assert recovered_plan.status == PurchaseStatus.APPROVED


def test_reject_plan():
    plan = create_valid_plan()

    assert plan.status == PurchaseStatus.AWAITING_APPROVAL

    rejected_plan = approval_service.reject_plan(
        plan.plan_id
    )

    assert rejected_plan.status == PurchaseStatus.REJECTED


def test_reject_plan_is_persisted():
    plan = create_valid_plan()

    approval_service.reject_plan(plan.plan_id)

    from app.services.purchase_service import PurchaseService

    fresh_service = PurchaseService()

    recovered_plan = fresh_service.get_plan(
        plan.plan_id
    )

    assert recovered_plan is not None
    assert recovered_plan.status == PurchaseStatus.REJECTED


def test_blocked_plan_cannot_be_approved():
    plan = create_blocked_plan()

    assert plan.status == PurchaseStatus.BLOCKED

    try:
        approval_service.approve_plan(plan.plan_id)
        assert False, "Blocked plan should not be approved."
    except ValueError as error:
        assert (
            str(error)
            == "Blocked purchase plans cannot be approved."
        )


def test_approved_plan_cannot_be_approved_again():
    plan = create_valid_plan()

    approval_service.approve_plan(plan.plan_id)

    try:
        approval_service.approve_plan(plan.plan_id)
        assert False, (
            "An already approved plan should not "
            "be approved again."
        )
    except ValueError as error:
        assert "cannot be approved" in str(error)


def test_api_approve_plan():
    plan = create_valid_plan()

    response = client.post(
        f"/api/purchase/plans/{plan.plan_id}/approve"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["plan_id"] == plan.plan_id
    assert data["status"] == "APPROVED"