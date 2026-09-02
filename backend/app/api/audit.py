from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from app.audit.audit_service import audit_service
from app.services.purchase_service import purchase_service


router = APIRouter(
    prefix="/api/audit",
    tags=["Audit"],
)


@router.get("/plans/{plan_id}")
def get_plan_audit_history(plan_id: str):
    plan = purchase_service.get_plan(plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase plan not found.",
        )

    events = audit_service.get_events_for_plan(plan_id)

    return {
        "plan_id": plan_id,
        "event_count": len(events),
        "events": [
            {
                **asdict(event),
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ],
    }


@router.get("/")
def get_all_audit_events():
    events = audit_service.get_all_events()

    return {
        "event_count": len(events),
        "events": [
            {
                **asdict(event),
                "timestamp": event.timestamp.isoformat(),
            }
            for event in events
        ],
    }