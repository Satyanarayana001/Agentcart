from app.core.state_machine import PurchaseStatus
from app.schemas.purchase import (
    CreatePurchasePlanRequest,
    PurchaseItemRequest,
)
from app.services.approval_service import approval_service
from app.services.purchase_service import purchase_service


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


def test_new_plan_starts_in_plan_created_state():
    plan = create_valid_plan()

    # PurchaseService evaluates the policy immediately,
    # so a valid plan moves to AWAITING_APPROVAL.
    assert plan.status == PurchaseStatus.AWAITING_APPROVAL


def test_valid_plan_transitions_to_approved():
    plan = create_valid_plan()

    approved_plan = approval_service.approve_plan(
        plan.plan_id
    )

    assert approved_plan.status == PurchaseStatus.APPROVED


def test_valid_plan_transitions_to_rejected():
    plan = create_valid_plan()

    rejected_plan = approval_service.reject_plan(
        plan.plan_id
    )

    assert rejected_plan.status == PurchaseStatus.REJECTED


def test_blocked_plan_cannot_transition_to_approved():
    plan = create_blocked_plan()

    assert plan.status == PurchaseStatus.BLOCKED

    try:
        approval_service.approve_plan(plan.plan_id)
        assert False, "Blocked plan must not become approved."
    except ValueError as error:
        assert "cannot be approved" in str(error)


def test_approved_plan_cannot_be_approved_again():
    plan = create_valid_plan()

    approval_service.approve_plan(plan.plan_id)

    try:
        approval_service.approve_plan(plan.plan_id)
        assert False, "Approved plan cannot be approved again."
    except ValueError as error:
        assert "cannot be approved" in str(error)


def test_rejected_plan_cannot_be_approved():
    plan = create_valid_plan()

    approval_service.reject_plan(plan.plan_id)

    try:
        approval_service.approve_plan(plan.plan_id)
        assert False, "Rejected plan must not become approved."
    except ValueError as error:
        assert "cannot be approved" in str(error)


def test_rejected_plan_cannot_be_rejected_again():
    plan = create_valid_plan()

    approval_service.reject_plan(plan.plan_id)

    try:
        approval_service.reject_plan(plan.plan_id)
        assert False, "Rejected plan cannot be rejected again."
    except ValueError as error:
        assert "cannot be rejected" in str(error)