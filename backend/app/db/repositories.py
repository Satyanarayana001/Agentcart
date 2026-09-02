from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.database import SessionLocal
from app.db.models import (
    PaymentOrderDB,
    PurchaseItemDB,
    PurchasePlanDB,
)


class PurchasePlanRepository:

    def save(self, plan) -> None:
        db = SessionLocal()

        try:
            db_plan = PurchasePlanDB(
                plan_id=plan.plan_id,
                max_budget=plan.max_budget,
                currency=plan.currency,
                status=plan.status.value,
                explanation=getattr(
                    plan,
                    "explanation",
                    "",
                ),
                created_at=plan.created_at,
            )

            for item in plan.items:
                db_item = PurchaseItemDB(
                    plan_id=plan.plan_id,
                    product_id=item.product_id,
                    name=item.name,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )

                db_plan.items.append(db_item)

            db.add(db_plan)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def get(self, plan_id: str):
        db = SessionLocal()

        try:
            statement = (
                select(PurchasePlanDB)
                .options(
                    selectinload(
                        PurchasePlanDB.items
                    )
                )
                .where(
                    PurchasePlanDB.plan_id == plan_id
                )
            )

            return db.scalars(statement).first()

        finally:
            db.close()

    def update_status(
        self,
        plan_id: str,
        status: str,
    ) -> None:

        db = SessionLocal()

        try:
            db_plan = db.get(
                PurchasePlanDB,
                plan_id,
            )

            if db_plan is None:
                raise ValueError(
                    "Purchase plan database record "
                    "not found."
                )

            db_plan.status = status

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


class PaymentOrderRepository:

    def save(self, payment_order) -> None:
        db = SessionLocal()

        try:
            db_payment_order = PaymentOrderDB(
                payment_order_id=(
                    payment_order.payment_order_id
                ),
                plan_id=payment_order.plan_id,
                razorpay_order_id=(
                    payment_order.razorpay_order_id
                ),
                amount=payment_order.amount,
                currency=payment_order.currency,
                status=payment_order.status,
                razorpay_payment_id=(
                    payment_order.razorpay_payment_id
                ),
                created_at=payment_order.created_at,
            )

            db.add(db_payment_order)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def get(
        self,
        payment_order_id: str,
    ):
        db = SessionLocal()

        try:
            return db.get(
                PaymentOrderDB,
                payment_order_id,
            )

        finally:
            db.close()

    def update_status(
        self,
        payment_order_id: str,
        status: str,
        razorpay_payment_id: str | None = None,
    ) -> None:

        db = SessionLocal()

        try:
            db_payment_order = db.get(
                PaymentOrderDB,
                payment_order_id,
            )

            if db_payment_order is None:
                raise ValueError(
                    "Payment order database record "
                    "not found."
                )

            db_payment_order.status = status

            if razorpay_payment_id is not None:
                db_payment_order.razorpay_payment_id = (
                    razorpay_payment_id
                )

            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


purchase_plan_repository = (
    PurchasePlanRepository()
)

payment_order_repository = (
    PaymentOrderRepository()
)