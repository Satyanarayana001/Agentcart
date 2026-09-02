from uuid import uuid4
from unittest.mock import patch

from app.core.state_machine import PurchaseStatus
from app.schemas.payment import VerifyPaymentRequest
from app.schemas.purchase import (
    CreatePurchasePlanRequest,
    PurchaseItemRequest,
)
from app.services.payment_service import payment_service
from app.services.purchase_service import purchase_service


def create_razorpay_order_id():
    return f"order_test_{uuid4().hex}"


def create_approved_plan():
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

    plan = purchase_service.create_plan(request)

    assert plan.status == PurchaseStatus.AWAITING_APPROVAL

    from app.services.approval_service import approval_service

    return approval_service.approve_plan(plan.plan_id)


def test_payment_order_requires_approved_plan():
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

    plan = purchase_service.create_plan(request)

    assert plan.status == PurchaseStatus.AWAITING_APPROVAL

    try:
        payment_service.create_payment_order(
            plan.plan_id
        )

        assert False, (
            "Payment order should not be created "
            "before approval."
        )

    except ValueError as error:
        assert (
            "only be created for an approved"
            in str(error)
        )


def test_payment_order_can_be_retrieved_from_database():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    assert payment_order is not None
    assert (
        payment_order.razorpay_order_id
        == fake_order_id
    )
    assert payment_order.amount == 4499
    assert payment_order.status == "ORDER_CREATED"

    from app.services.payment_service import PaymentService

    fresh_service = PaymentService()

    recovered_order = fresh_service.get_payment_order(
        payment_order.payment_order_id
    )

    assert recovered_order is not None
    assert (
        recovered_order.payment_order_id
        == payment_order.payment_order_id
    )
    assert (
        recovered_order.razorpay_order_id
        == fake_order_id
    )
    assert recovered_order.amount == 4499
    assert recovered_order.status == "ORDER_CREATED"


def test_payment_verification_rejects_wrong_order_id():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    request = VerifyPaymentRequest(
        razorpay_order_id="wrong_order_id",
        razorpay_payment_id="pay_test_001",
        razorpay_signature="signature",
    )

    try:
        payment_service.verify_payment(
            payment_order.payment_order_id,
            request,
        )

        assert False, (
            "Verification should reject a mismatched "
            "Razorpay order ID."
        )

    except ValueError as error:
        assert (
            "does not match this payment order"
            in str(error)
        )


def test_payment_verification_rejects_invalid_signature():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    request = VerifyPaymentRequest(
        razorpay_order_id=fake_order_id,
        razorpay_payment_id="pay_test_002",
        razorpay_signature="invalid_signature",
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.verify_payment_signature",
        side_effect=ValueError(
            "Invalid payment signature."
        ),
    ):
        try:
            payment_service.verify_payment(
                payment_order.payment_order_id,
                request,
            )

            assert False, (
                "Invalid signatures must be rejected."
            )

        except ValueError as error:
            assert (
                "signature verification failed"
                in str(error)
            )


def test_payment_verification_marks_payment_verified():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    request = VerifyPaymentRequest(
        razorpay_order_id=fake_order_id,
        razorpay_payment_id="pay_test_004",
        razorpay_signature="valid_signature",
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.verify_payment_signature",
        return_value=None,
    ):
        verified_order = payment_service.verify_payment(
            payment_order.payment_order_id,
            request,
        )

    assert verified_order.status == "PAYMENT_VERIFIED"

    assert (
        verified_order.razorpay_payment_id
        == "pay_test_004"
    )


def test_verified_payment_is_persisted():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    request = VerifyPaymentRequest(
        razorpay_order_id=fake_order_id,
        razorpay_payment_id="pay_test_005",
        razorpay_signature="valid_signature",
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.verify_payment_signature",
        return_value=None,
    ):
        payment_service.verify_payment(
            payment_order.payment_order_id,
            request,
        )

    from app.services.payment_service import PaymentService

    fresh_service = PaymentService()

    recovered_order = fresh_service.get_payment_order(
        payment_order.payment_order_id
    )

    assert recovered_order is not None
    assert recovered_order.status == "PAYMENT_VERIFIED"
    assert (
        recovered_order.razorpay_payment_id
        == "pay_test_005"
    )


def test_payment_cannot_be_verified_twice():
    approved_plan = create_approved_plan()

    fake_order_id = create_razorpay_order_id()

    with patch(
        "app.services.payment_service.razorpay_adapter.create_order",
        return_value={"id": fake_order_id},
    ):
        payment_order = (
            payment_service.create_payment_order(
                approved_plan.plan_id
            )
        )

    request = VerifyPaymentRequest(
        razorpay_order_id=fake_order_id,
        razorpay_payment_id="pay_test_006",
        razorpay_signature="valid_signature",
    )

    with patch(
        "app.services.payment_service.razorpay_adapter.verify_payment_signature",
        return_value=None,
    ):
        payment_service.verify_payment(
            payment_order.payment_order_id,
            request,
        )

    try:
        payment_service.verify_payment(
            payment_order.payment_order_id,
            request,
        )

        assert False, (
            "A verified payment must not "
            "be verified again."
        )

    except ValueError as error:
        assert (
            "already been verified"
            in str(error)
        )


def test_missing_payment_order_is_rejected():
    request = VerifyPaymentRequest(
        razorpay_order_id="order_missing",
        razorpay_payment_id="pay_missing",
        razorpay_signature="signature",
    )

    try:
        payment_service.verify_payment(
            "missing-payment-order",
            request,
        )

        assert False, (
            "Missing payment orders must be rejected."
        )

    except ValueError as error:
        assert (
            "Payment order not found"
            in str(error)
        )