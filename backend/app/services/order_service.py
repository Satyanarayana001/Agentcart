from sqlalchemy.orm import Session

from app.db.models import (
    PaymentOrderDB,
    PurchasePlanDB,
)


class OrderService:

    def get_orders(
        self,
        db: Session,
    ) -> list[dict]:

        payment_orders = (
            db.query(PaymentOrderDB)
            .order_by(
                PaymentOrderDB.created_at.desc()
            )
            .all()
        )

        orders = []

        for payment_order in payment_orders:

            plan = (
                db.query(PurchasePlanDB)
                .filter(
                    PurchasePlanDB.plan_id
                    == payment_order.plan_id
                )
                .first()
            )

            if plan is None:
                continue

            items = plan.items

            primary_product = (
                items[0].name
                if items
                else "Unknown product"
            )

            orders.append(
                {
                    "order_id": payment_order.payment_order_id,
                    "plan_id": plan.plan_id,
                    "amount": payment_order.amount,
                    "currency": payment_order.currency,
                    "status": payment_order.status,
                    "created_at": payment_order.created_at,
                    "item_count": len(items),
                    "primary_product": primary_product,
                }
            )

        return orders


    def get_order(
        self,
        db: Session,
        order_id: str,
    ) -> dict | None:

        payment_order = (
            db.query(PaymentOrderDB)
            .filter(
                PaymentOrderDB.payment_order_id
                == order_id
            )
            .first()
        )

        if payment_order is None:
            return None

        plan = (
            db.query(PurchasePlanDB)
            .filter(
                PurchasePlanDB.plan_id
                == payment_order.plan_id
            )
            .first()
        )

        if plan is None:
            return None

        items = []

        for item in plan.items:

            total_price = (
                item.unit_price
                * item.quantity
            )

            items.append(
                {
                    "product_id": item.product_id,
                    "name": item.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": total_price,
                }
            )

        plan_status = (
            plan.status.value
            if hasattr(plan.status, "value")
            else str(plan.status)
        )

        return {
            "order_id": payment_order.payment_order_id,
            "plan_id": plan.plan_id,
            "amount": payment_order.amount,
            "currency": payment_order.currency,
            "status": payment_order.status,
            "razorpay_order_id": (
                payment_order.razorpay_order_id
            ),
            "razorpay_payment_id": (
                payment_order.razorpay_payment_id
            ),
            "created_at": payment_order.created_at,
            "items": items,
            "plan_status": plan_status,
            "plan_explanation": plan.explanation,
        }


# IMPORTANT:
# This is the object imported by app.api.orders.
order_service = OrderService()