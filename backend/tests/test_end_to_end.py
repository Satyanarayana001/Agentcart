import json
from unittest.mock import patch
from uuid import uuid4

from app.core.state_machine import PurchaseStatus
from app.schemas.agent import AgentPurchaseRequest
from app.schemas.payment import VerifyPaymentRequest
from app.services.agent_service import agent_service
from app.services.approval_service import approval_service
from app.services.payment_service import payment_service
from app.services.purchase_service import purchase_service


def test_complete_agentcart_purchase_flow():

    # ---------------------------------------------------------
    # 1. AI receives the user's natural-language request
    # ---------------------------------------------------------

    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "max_budget": 5000,
        "reason": (
            "Selected SoundMax Pro ANC because "
            "it matches the request and budget."
        ),
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        agent_request = AgentPurchaseRequest(
            request="Buy ANC headphones under ₹5000"
        )

        agent_result = (
            agent_service.process_purchase_request(
                agent_request
            )
        )

    # ---------------------------------------------------------
    # 2. AI creates a purchase plan
    # ---------------------------------------------------------

    assert agent_result.plan_id is not None

    assert (
        agent_result.status
        == PurchaseStatus.AWAITING_APPROVAL.value
    )

    plan = purchase_service.get_plan(
        agent_result.plan_id
    )

    assert plan is not None

    assert (
        plan.status
        == PurchaseStatus.AWAITING_APPROVAL
    )

    assert plan.subtotal == 4499
    assert plan.max_budget == 5000

    assert len(plan.items) == 1

    assert (
        plan.items[0].product_id
        == "hp_001"
    )

    # ---------------------------------------------------------
    # 3. Human explicitly approves the purchase
    # ---------------------------------------------------------

    approved_plan = approval_service.approve_plan(
        plan.plan_id
    )

    assert (
        approved_plan.status
        == PurchaseStatus.APPROVED
    )

    fresh_plan = purchase_service.get_plan(
        plan.plan_id
    )

    assert fresh_plan is not None

    assert (
        fresh_plan.status
        == PurchaseStatus.APPROVED
    )

    # ---------------------------------------------------------
    # 4. Create Razorpay payment order
    # ---------------------------------------------------------

    fake_razorpay_order_id = (
        f"order_e2e_test_{uuid4().hex}"
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={
            "id": fake_razorpay_order_id,
        },
    ):
        payment_order = (
            payment_service.create_payment_order(
                plan.plan_id
            )
        )

    assert payment_order is not None

    assert (
        payment_order.razorpay_order_id
        == fake_razorpay_order_id
    )

    assert payment_order.amount == 4499
    assert payment_order.currency == "INR"

    assert (
        payment_order.status
        == "ORDER_CREATED"
    )

    # ---------------------------------------------------------
    # 5. Verify payment signature
    # ---------------------------------------------------------

    verify_request = VerifyPaymentRequest(
        razorpay_order_id=fake_razorpay_order_id,
        razorpay_payment_id="pay_e2e_test_001",
        razorpay_signature="valid_test_signature",
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.verify_payment_signature",
        return_value=None,
    ):
        verified_payment = (
            payment_service.verify_payment(
                payment_order.payment_order_id,
                verify_request,
            )
        )

    assert (
        verified_payment.status
        == "PAYMENT_VERIFIED"
    )

    assert (
        verified_payment.razorpay_payment_id
        == "pay_e2e_test_001"
    )

    # ---------------------------------------------------------
    # 6. Verify purchase plan is now COMPLETED
    # ---------------------------------------------------------

    completed_plan = purchase_service.get_plan(
        plan.plan_id
    )

    assert completed_plan is not None

    assert (
        completed_plan.status
        == PurchaseStatus.COMPLETED
    )

    # ---------------------------------------------------------
    # 7. Verify payment persisted after service restart
    # ---------------------------------------------------------

    from app.services.payment_service import PaymentService

    fresh_payment_service = PaymentService()

    recovered_payment = (
        fresh_payment_service.get_payment_order(
            payment_order.payment_order_id
        )
    )

    assert recovered_payment is not None

    assert (
        recovered_payment.status
        == "PAYMENT_VERIFIED"
    )

    assert (
        recovered_payment.razorpay_payment_id
        == "pay_e2e_test_001"
    )

    # ---------------------------------------------------------
    # 8. Verify completed plan persists after reload
    # ---------------------------------------------------------

    recovered_plan = purchase_service.get_plan(
        plan.plan_id
    )

    assert recovered_plan is not None

    assert (
        recovered_plan.status
        == PurchaseStatus.COMPLETED
    )

    # ---------------------------------------------------------
    # 9. Verify complete audit trail
    # ---------------------------------------------------------

    from app.audit.audit_service import audit_service

    events = audit_service.get_events_for_plan(
        plan.plan_id
    )

    event_types = [
        event.event_type
        for event in events
    ]

    assert "PLAN_CREATED" in event_types
    assert "POLICY_VALIDATED" in event_types
    assert "PLAN_APPROVED" in event_types
    assert "PAYMENT_ORDER_CREATED" in event_types
    assert "PAYMENT_VERIFIED" in event_types
    assert "PURCHASE_COMPLETED" in event_types

    # ---------------------------------------------------------
    # 10. Verify chronological order
    # ---------------------------------------------------------

    assert event_types.index(
        "PLAN_CREATED"
    ) < event_types.index(
        "POLICY_VALIDATED"
    )

    assert event_types.index(
        "POLICY_VALIDATED"
    ) < event_types.index(
        "PLAN_APPROVED"
    )

    assert event_types.index(
        "PLAN_APPROVED"
    ) < event_types.index(
        "PAYMENT_ORDER_CREATED"
    )

    assert event_types.index(
        "PAYMENT_ORDER_CREATED"
    ) < event_types.index(
        "PAYMENT_VERIFIED"
    )

    assert event_types.index(
        "PAYMENT_VERIFIED"
    ) < event_types.index(
        "PURCHASE_COMPLETED"
    )
