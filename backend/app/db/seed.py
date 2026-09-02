from app.db.database import Base, engine
from app.db.models import (
    AuditEventDB,
    FulfillmentDB,
    PaymentOrderDB,
    ProductDB,
    PurchaseItemDB,
    PurchasePlanDB,
    NotificationDB,

)


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("AgentCart database initialized successfully.")