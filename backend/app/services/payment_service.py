from app.audit.audit_service import audit_service
from app.core.state_machine import PurchaseStatus
from app.db.repositories import (
    payment_order_repository,
    purchase_plan_repository,
)
from app.integrations.razorpay_adapter import razorpay_adapter
from app.models.order import PaymentOrder
from app.schemas.payment import VerifyPaymentRequest
from app.services.purchase_service import purchase_service


class PaymentService:

    def create_payment_order(
        self,
        plan_id: str,
    ) -> PaymentOrder:

        plan = purchase_service.get_plan(plan_id)

        if plan is None:
            raise ValueError(
                "Purchase plan not found."
            )

        if plan.status != PurchaseStatus.APPROVED:

            audit_service.log_event(
                event_type="PAYMENT_ATTEMPT_BLOCKED",
                plan_id=plan_id,
                message=(
                    "Payment order creation attempted "
                    "before approval."
                ),
                metadata={
                    "current_status": plan.status.value,
                    "required_status": "APPROVED",
                },
            )

            raise ValueError(
                "Payment can only be created for "
                "an approved purchase plan."
            )

        if not razorpay_adapter.is_configured():

            audit_service.log_event(
                event_type="PAYMENT_CONFIGURATION_ERROR",
                plan_id=plan_id,
                message=(
                    "Payment order creation failed because "
                    "Razorpay is not configured."
                ),
                metadata={
                    "reason": "Missing Razorpay credentials.",
                },
            )

            raise ValueError(
                "Razorpay is not configured. "
                "Add test credentials to the .env file."
            )

        try:

            razorpay_order = razorpay_adapter.create_order(
                amount=plan.subtotal,
                currency=plan.currency,
                receipt=f"plan_{plan.plan_id[:20]}",
            )

        except Exception as error:

            audit_service.log_event(
                event_type="PAYMENT_ORDER_FAILED",
                plan_id=plan_id,
                message=(
                    "Razorpay payment order creation failed."
                ),
                metadata={
                    "error": str(error),
                },
            )

            raise ValueError(
                f"Failed to create Razorpay payment order: {error}"
            )

        payment_order = PaymentOrder(
            plan_id=plan.plan_id,
            razorpay_order_id=razorpay_order["id"],
            amount=plan.subtotal,
            currency=plan.currency,
        )

        payment_order_repository.save(
            payment_order
        )

        audit_service.log_event(
            event_type="PAYMENT_ORDER_CREATED",
            plan_id=plan_id,
            message=(
                "Razorpay payment order created successfully."
            ),
            metadata={
                "payment_order_id": (
                    payment_order.payment_order_id
                ),
                "razorpay_order_id": (
                    payment_order.razorpay_order_id
                ),
                "amount": payment_order.amount,
                "currency": payment_order.currency,
            },
        )

        return payment_order

    def get_payment_order(
        self,
        payment_order_id: str,
    ) -> PaymentOrder | None:

        db_payment_order = (
            payment_order_repository.get(
                payment_order_id
            )
        )

        if db_payment_order is None:
            return None

        return PaymentOrder(
            plan_id=db_payment_order.plan_id,
            razorpay_order_id=(
                db_payment_order.razorpay_order_id
            ),
            amount=db_payment_order.amount,
            currency=db_payment_order.currency,
            payment_order_id=(
                db_payment_order.payment_order_id
            ),
            status=db_payment_order.status,
            razorpay_payment_id=(
                db_payment_order.razorpay_payment_id
            ),
            created_at=db_payment_order.created_at,
        )

    def verify_payment(
        self,
        payment_order_id: str,
        request: VerifyPaymentRequest,
    ) -> PaymentOrder:

        payment_order = self.get_payment_order(
            payment_order_id
        )

        if payment_order is None:
            raise ValueError(
                "Payment order not found."
            )

        if (
            payment_order.razorpay_order_id
            != request.razorpay_order_id
        ):
            raise ValueError(
                "Razorpay order ID does not match "
                "this payment order."
            )

        if payment_order.status == "PAYMENT_VERIFIED":
            raise ValueError(
                "Payment has already been verified."
            )

        try:

            razorpay_adapter.verify_payment_signature(
                razorpay_order_id=(
                    payment_order.razorpay_order_id
                ),
                razorpay_payment_id=(
                    request.razorpay_payment_id
                ),
                razorpay_signature=(
                    request.razorpay_signature
                ),
            )

        except Exception as error:

            audit_service.log_event(
                event_type="PAYMENT_VERIFICATION_FAILED",
                plan_id=payment_order.plan_id,
                message=(
                    "Razorpay payment signature "
                    "verification failed."
                ),
                metadata={
                    "payment_order_id": payment_order_id,
                    "razorpay_order_id": (
                        request.razorpay_order_id
                    ),
                    "error": str(error),
                },
            )

            raise ValueError(
                f"Payment signature verification failed: {error}"
            )

        # -------------------------------------------------
        # Payment verification succeeded.
        # -------------------------------------------------

        payment_order.status = "PAYMENT_VERIFIED"

        payment_order.razorpay_payment_id = (
            request.razorpay_payment_id
        )

        payment_order_repository.update_status(
            payment_order_id=(
                payment_order.payment_order_id
            ),
            status=payment_order.status,
            razorpay_payment_id=(
                payment_order.razorpay_payment_id
            ),
        )

        audit_service.log_event(
            event_type="PAYMENT_VERIFIED",
            plan_id=payment_order.plan_id,
            message=(
                "Razorpay payment verified successfully."
            ),
            metadata={
                "payment_order_id": (
                    payment_order.payment_order_id
                ),
                "razorpay_order_id": (
                    payment_order.razorpay_order_id
                ),
                "razorpay_payment_id": (
                    payment_order.razorpay_payment_id
                ),
            },
        )

        # -------------------------------------------------
        # Complete the purchase plan.
        # -------------------------------------------------

        purchase_plan_repository.update_status(
            plan_id=payment_order.plan_id,
            status=PurchaseStatus.COMPLETED.value,
        )

        audit_service.log_event(
            event_type="PURCHASE_COMPLETED",
            plan_id=payment_order.plan_id,
            message=(
                "Purchase completed after successful "
                "Razorpay payment verification."
            ),
            metadata={
                "previous_status": (
                    PurchaseStatus.APPROVED.value
                ),
                "new_status": (
                    PurchaseStatus.COMPLETED.value
                ),
                "payment_order_id": (
                    payment_order.payment_order_id
                ),
                "razorpay_order_id": (
                    payment_order.razorpay_order_id
                ),
                "razorpay_payment_id": (
                    payment_order.razorpay_payment_id
                ),
                "amount": payment_order.amount,
                "currency": payment_order.currency,
            },
        )

        return payment_order


payment_service = PaymentService()
