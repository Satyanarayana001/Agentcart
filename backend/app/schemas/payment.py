from pydantic import BaseModel


class CreatePaymentOrderResponse(BaseModel):
    payment_order_id: str
    razorpay_order_id: str
    plan_id: str
    amount: float
    currency: str
    status: str
    message: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentVerificationResponse(BaseModel):
    payment_order_id: str
    razorpay_payment_id: str
    status: str
    message: str