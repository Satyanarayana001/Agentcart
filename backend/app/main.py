from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router as agent_router
from app.api.audit import router as audit_router
from app.api.catalog import router as catalog_router
from app.api.payment import router as payment_router
from app.api.purchase import router as purchase_router
from app.api.orders import router as orders_router
from app.api.tracking import router as tracking_router
from app.api.notifications import (
    router as notifications_router,
)
from app.db.seed import init_database
from pathlib import Path
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="AgentCart API",
    description="Explainable, bounded, and approval-gated AI commerce system",
    version="1.0.0",
)
init_database()


IMAGES_DIR = (
    Path(__file__).resolve().parent
    / "db"
    / "data"
    / "images"
)

app.mount(
    "/static/images",
    StaticFiles(directory=IMAGES_DIR),
    name="product-images",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(catalog_router)
app.include_router(purchase_router)
app.include_router(agent_router)
app.include_router(audit_router)
app.include_router(payment_router)
app.include_router(orders_router)
app.include_router(tracking_router)
app.include_router(notifications_router)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AgentCart API",
    }