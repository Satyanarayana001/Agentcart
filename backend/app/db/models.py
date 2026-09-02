from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.database import Base


class ProductDB(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


class PurchasePlanDB(Base):
    __tablename__ = "purchase_plans"

    plan_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    max_budget: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="INR",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    items: Mapped[list["PurchaseItemDB"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
    )


class PurchaseItemDB(Base):
    __tablename__ = "purchase_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("purchase_plans.plan_id"),
        nullable=False,
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    plan: Mapped["PurchasePlanDB"] = relationship(
        back_populates="items",
    )


class PaymentOrderDB(Base):
    __tablename__ = "payment_orders"

    payment_order_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    plan_id: Mapped[str] = mapped_column(
        ForeignKey("purchase_plans.plan_id"),
        nullable=False,
    )

    razorpay_order_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ORDER_CREATED",
    )

    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class AuditEventDB(Base):
    __tablename__ = "audit_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    plan_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    metadata_json: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="{}",
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class FulfillmentDB(Base):
    __tablename__ = "fulfillments"

    order_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey(
            "payment_orders.payment_order_id"
        ),
        primary_key=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PROCESSING",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

class NotificationDB(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    order_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    plan_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_read: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )