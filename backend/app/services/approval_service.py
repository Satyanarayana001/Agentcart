from app.audit.audit_service import audit_service
from app.core.state_machine import PurchaseStatus
from app.db.repositories import purchase_plan_repository
from app.services.purchase_service import purchase_service


class ApprovalService:

    def approve_plan(self, plan_id: str):
        plan = purchase_service.get_plan(plan_id)

        if plan is None:
            raise ValueError(
                "Purchase plan not found."
            )

        if plan.status == PurchaseStatus.BLOCKED:
            audit_service.log_event(
                event_type="INVALID_ACTION_ATTEMPTED",
                plan_id=plan_id,
                message=(
                    "Attempted to approve a "
                    "blocked purchase plan."
                ),
                metadata={
                    "current_status": plan.status.value,
                    "attempted_action": "APPROVE",
                },
            )

            raise ValueError(
                "Blocked purchase plans cannot be approved."
            )

        if plan.status != PurchaseStatus.AWAITING_APPROVAL:
            audit_service.log_event(
                event_type="INVALID_ACTION_ATTEMPTED",
                plan_id=plan_id,
                message=(
                    "Attempted an invalid approval action."
                ),
                metadata={
                    "current_status": plan.status.value,
                    "attempted_action": "APPROVE",
                },
            )

            raise ValueError(
                "Purchase plan cannot be approved from "
                f"status '{plan.status.value}'."
            )

        # Update the domain object.
        plan.status = PurchaseStatus.APPROVED

        # Persist the state transition to SQLite.
        purchase_plan_repository.update_status(
            plan_id=plan.plan_id,
            status=plan.status.value,
        )

        audit_service.log_event(
            event_type="PLAN_APPROVED",
            plan_id=plan.plan_id,
            message=(
                "Purchase plan explicitly approved."
            ),
            metadata={
                "previous_status": "AWAITING_APPROVAL",
                "new_status": "APPROVED",
                "subtotal": plan.subtotal,
                "currency": plan.currency,
            },
        )

        return plan

    def reject_plan(self, plan_id: str):
        plan = purchase_service.get_plan(plan_id)

        if plan is None:
            raise ValueError(
                "Purchase plan not found."
            )

        if plan.status != PurchaseStatus.AWAITING_APPROVAL:
            audit_service.log_event(
                event_type="INVALID_ACTION_ATTEMPTED",
                plan_id=plan_id,
                message=(
                    "Attempted an invalid rejection action."
                ),
                metadata={
                    "current_status": plan.status.value,
                    "attempted_action": "REJECT",
                },
            )

            raise ValueError(
                "Purchase plan cannot be rejected from "
                f"status '{plan.status.value}'."
            )

        # Update the domain object.
        plan.status = PurchaseStatus.REJECTED

        # Persist the state transition to SQLite.
        purchase_plan_repository.update_status(
            plan_id=plan.plan_id,
            status=plan.status.value,
        )

        audit_service.log_event(
            event_type="PLAN_REJECTED",
            plan_id=plan.plan_id,
            message=(
                "Purchase plan explicitly rejected."
            ),
            metadata={
                "previous_status": "AWAITING_APPROVAL",
                "new_status": "REJECTED",
                "subtotal": plan.subtotal,
                "currency": plan.currency,
            },
        )

        return plan


approval_service = ApprovalService()