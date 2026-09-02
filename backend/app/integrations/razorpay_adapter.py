import razorpay

from app.config import settings


class RazorpayAdapter:
    def __init__(self):
        self.client = None

        if (
            settings.RAZORPAY_KEY_ID
            and settings.RAZORPAY_KEY_SECRET
        ):
            self.client = razorpay.Client(
                auth=(
                    settings.RAZORPAY_KEY_ID,
                    settings.RAZORPAY_KEY_SECRET,
                )
            )

    def is_configured(self) -> bool:
        return self.client is not None

    def create_order(
        self,
        amount: float,
        currency: str,
        receipt: str,
    ) -> dict:
        if not self.is_configured():
            raise ValueError(
                "Razorpay is not configured. "
                "Add test credentials to the .env file."
            )

        amount_in_smallest_unit = round(amount * 100)

        order_data = {
            "amount": amount_in_smallest_unit,
            "currency": currency,
            "receipt": receipt,
        }

        return self.client.order.create(
            data=order_data
        )

    def verify_payment_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> None:
        if not self.is_configured():
            raise ValueError(
                "Razorpay is not configured."
            )

        verification_data = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }

        self.client.utility.verify_payment_signature(
            verification_data
        )


razorpay_adapter = RazorpayAdapter()