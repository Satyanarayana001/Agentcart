import json
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import (
    AuditEventDB,
    FulfillmentDB,
    PaymentOrderDB,
)

from app.services.notification_service import (
    notification_service,
)


TRACKING_STEPS = [
    {
        "status": "PROCESSING",
        "label": "Preparing",
        "description": (
            "Your order is being prepared."
        ),
    },
    {
        "status": "SHIPPED",
        "label": "Shipped",
        "description": (
            "Your order has been handed over for delivery."
        ),
    },
    {
        "status": "OUT_FOR_DELIVERY",
        "label": "Out for delivery",
        "description": (
            "Your order is on the way to you."
        ),
    },
    {
        "status": "DELIVERED",
        "label": "Delivered",
        "description": (
            "Your order has been delivered."
        ),
    },
]


class TrackingService:

    def _get_payment_order(
        self,
        db: Session,
        order_id: str,
    ):
        return (
            db.query(PaymentOrderDB)
            .filter(
                PaymentOrderDB.payment_order_id
                == order_id
            )
            .first()
        )


    def _get_fulfillment(
        self,
        db: Session,
        order_id: str,
    ):
        return (
            db.query(FulfillmentDB)
            .filter(
                FulfillmentDB.order_id
                == order_id
            )
            .first()
        )


    def _record_audit_event(
        self,
        db: Session,
        plan_id: str,
        event_type: str,
        message: str,
        metadata: dict,
    ):
        event = AuditEventDB(
            event_id=str(uuid.uuid4()),
            plan_id=plan_id,
            event_type=event_type,
            message=message,
            metadata_json=json.dumps(metadata),
            timestamp=datetime.utcnow(),
        )

        db.add(event)
        db.commit()


    def _ensure_fulfillment(
        self,
        db: Session,
        payment_order: PaymentOrderDB,
    ):
        fulfillment = self._get_fulfillment(
            db,
            payment_order.payment_order_id,
        )

        if fulfillment:
            return fulfillment

        if payment_order.status != "PAYMENT_VERIFIED":
            return None

        fulfillment = FulfillmentDB(
            order_id=payment_order.payment_order_id,
            status="PROCESSING",
            updated_at=datetime.utcnow(),
        )

        db.add(fulfillment)
        db.commit()
        db.refresh(fulfillment)

        # Audit event
        self._record_audit_event(
            db=db,
            plan_id=payment_order.plan_id,
            event_type="FULFILLMENT_PROCESSING",
            message=(
                "Order fulfillment started "
                "after successful payment."
            ),
            metadata={
                "payment_order_id": (
                    payment_order.payment_order_id
                ),
                "status": "PROCESSING",
            },
        )

        # Notification
        notification_service.create_notification(
            db=db,
            order_id=payment_order.payment_order_id,
            plan_id=payment_order.plan_id,
            title="Order is being prepared",
            message=(
                "Your order has been confirmed "
                "and is now being prepared."
            ),
            notification_type="ORDER_PROCESSING",
        )

        return fulfillment


    def get_tracking(
        self,
        db: Session,
        order_id: str,
    ):
        payment_order = self._get_payment_order(
            db,
            order_id,
        )

        if payment_order is None:
            return None

        fulfillment = self._ensure_fulfillment(
            db,
            payment_order,
        )

        if fulfillment is None:
            return {
                "order_id": order_id,
                "payment_status": payment_order.status,
                "fulfillment_status": "NOT_STARTED",
                "fulfillment_label": "Awaiting payment",
                "updated_at": None,
                "events": [],
            }

        current_index = next(
            (
                index
                for index, step in enumerate(
                    TRACKING_STEPS
                )
                if step["status"]
                == fulfillment.status
            ),
            0,
        )

        events = []

        for index, step in enumerate(
            TRACKING_STEPS
        ):
            events.append(
                {
                    "status": step["status"],
                    "label": step["label"],
                    "description": step["description"],
                    "completed": (
                        index <= current_index
                    ),
                    "current": (
                        index == current_index
                    ),
                    "timestamp": (
                        fulfillment.updated_at
                        if index == current_index
                        else None
                    ),
                }
            )

        current_step = TRACKING_STEPS[
            current_index
        ]

        return {
            "order_id": order_id,
            "payment_status": payment_order.status,
            "fulfillment_status": fulfillment.status,
            "fulfillment_label": current_step["label"],
            "updated_at": fulfillment.updated_at,
            "events": events,
        }


    def advance_tracking(
        self,
        db: Session,
        order_id: str,
    ):
        payment_order = self._get_payment_order(
            db,
            order_id,
        )

        if payment_order is None:
            raise ValueError(
                "Order not found."
            )

        if payment_order.status != "PAYMENT_VERIFIED":
            raise ValueError(
                "Tracking can start only after "
                "payment is verified."
            )

        fulfillment = self._ensure_fulfillment(
            db,
            payment_order,
        )

        if fulfillment is None:
            raise ValueError(
                "Fulfillment has not started."
            )

        current_index = next(
            (
                index
                for index, step in enumerate(
                    TRACKING_STEPS
                )
                if step["status"]
                == fulfillment.status
            ),
            0,
        )

        if current_index >= len(
            TRACKING_STEPS
        ) - 1:
            raise ValueError(
                "Order has already been delivered."
            )

        previous_status = fulfillment.status

        next_step = TRACKING_STEPS[
            current_index + 1
        ]

        fulfillment.status = next_step["status"]
        fulfillment.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(fulfillment)

        # Audit event
        self._record_audit_event(
            db=db,
            plan_id=payment_order.plan_id,
            event_type=(
                f"FULFILLMENT_{next_step['status']}"
            ),
            message=next_step["description"],
            metadata={
                "payment_order_id": (
                    payment_order.payment_order_id
                ),
                "previous_status": previous_status,
                "new_status": next_step["status"],
            },
        )

        # Notification
        notification_service.create_notification(
            db=db,
            order_id=payment_order.payment_order_id,
            plan_id=payment_order.plan_id,
            title=next_step["label"],
            message=next_step["description"],
            notification_type=(
                f"ORDER_{next_step['status']}"
            ),
        )

        return {
            "order_id": order_id,
            "previous_status": previous_status,
            "status": next_step["status"],
            "label": next_step["label"],
            "message": next_step["description"],
        }


tracking_service = TrackingService()