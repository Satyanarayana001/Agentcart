import json

from sqlalchemy import select

from app.audit.events import AuditEvent
from app.db.database import SessionLocal
from app.db.models import AuditEventDB


class AuditService:

    def log_event(
        self,
        event_type: str,
        plan_id: str,
        message: str,
        metadata: dict | None = None,
    ) -> AuditEvent:

        event = AuditEvent(
            event_type=event_type,
            plan_id=plan_id,
            message=message,
            metadata=metadata or {},
        )

        db = SessionLocal()

        try:
            db_event = AuditEventDB(
                event_id=event.event_id,
                plan_id=event.plan_id,
                event_type=event.event_type,
                message=event.message,
                metadata_json=json.dumps(event.metadata),
                timestamp=event.timestamp,
            )

            db.add(db_event)
            db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        return event

    def get_events_for_plan(
        self,
        plan_id: str,
    ) -> list[AuditEvent]:

        db = SessionLocal()

        try:
            statement = (
                select(AuditEventDB)
                .where(
                    AuditEventDB.plan_id == plan_id
                )
                .order_by(
                    AuditEventDB.timestamp
                )
            )

            db_events = db.scalars(statement).all()

            return [
                AuditEvent(
                    event_type=db_event.event_type,
                    plan_id=db_event.plan_id,
                    message=db_event.message,
                    metadata=json.loads(
                        db_event.metadata_json
                    ),
                    event_id=db_event.event_id,
                    timestamp=db_event.timestamp,
                )
                for db_event in db_events
            ]

        finally:
            db.close()

    def get_all_events(self) -> list[AuditEvent]:

        db = SessionLocal()

        try:
            statement = (
                select(AuditEventDB)
                .order_by(
                    AuditEventDB.timestamp
                )
            )

            db_events = db.scalars(statement).all()

            return [
                AuditEvent(
                    event_type=db_event.event_type,
                    plan_id=db_event.plan_id,
                    message=db_event.message,
                    metadata=json.loads(
                        db_event.metadata_json
                    ),
                    event_id=db_event.event_id,
                    timestamp=db_event.timestamp,
                )
                for db_event in db_events
            ]

        finally:
            db.close()


audit_service = AuditService()