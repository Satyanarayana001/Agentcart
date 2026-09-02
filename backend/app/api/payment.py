from fastapi import APIRouter, HTTPException

from app.schemas.payment import (
    CreatePaymentOrderResponse,
    PaymentVerificationResponse,
    VerifyPaymentRequest,
)
from app.services.payment_service import payment_service


router = APIRouter(
    prefix="/api/payment",
    tags=["Payment"],
)


@router.post(
    "/plans/{plan_id}/orders",
    response_model=CreatePaymentOrderResponse,
)
def create_payment_order(plan_id: str):
    try:
        payment_order = payment_service.create_payment_order(
            plan_id
        )

        return CreatePaymentOrderResponse(
            payment_order_id=payment_order.payment_order_id,
            razorpay_order_id=payment_order.razorpay_order_id,
            plan_id=payment_order.plan_id,
            amount=payment_order.amount,
            currency=payment_order.currency,
            status=payment_order.status,
            message="Razorpay payment order created successfully.",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.get(
    "/orders/{payment_order_id}",
    response_model=CreatePaymentOrderResponse,
)
def get_payment_order(payment_order_id: str):
    payment_order = payment_service.get_payment_order(
        payment_order_id
    )

    if payment_order is None:
        raise HTTPException(
            status_code=404,
            detail="Payment order not found.",
        )

    return CreatePaymentOrderResponse(
        payment_order_id=payment_order.payment_order_id,
        razorpay_order_id=payment_order.razorpay_order_id,
        plan_id=payment_order.plan_id,
        amount=payment_order.amount,
        currency=payment_order.currency,
        status=payment_order.status,
        message="Payment order retrieved successfully.",
    )


@router.post(
    "/orders/{payment_order_id}/verify",
    response_model=PaymentVerificationResponse,
)
def verify_payment(
    payment_order_id: str,
    request: VerifyPaymentRequest,
):
    try:
        payment_order = payment_service.verify_payment(
            payment_order_id=payment_order_id,
            request=request,
        )

        return PaymentVerificationResponse(
            payment_order_id=payment_order.payment_order_id,
            razorpay_payment_id=(
                payment_order.razorpay_payment_id
            ),
            status=payment_order.status,
            message="Payment verified successfully.",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )