from app.audit.audit_service import audit_service
from app.core.state_machine import PurchaseStatus
from app.db.repositories import purchase_plan_repository
from app.models.purchase_plan import PurchaseItemModel, PurchasePlan
from app.policies.policy_engine import policy_engine
from app.schemas.purchase import CreatePurchasePlanRequest
from app.services.catalog_service import catalog_service


class PurchaseService:

    def create_plan(
        self,
        request: CreatePurchasePlanRequest,
    ) -> PurchasePlan:

        items: list[PurchaseItemModel] = []

        for requested_item in request.items:

            product = catalog_service.get_product_by_id(
                requested_item.product_id
            )

            if product is None:
                raise ValueError(
                    f"Product '{requested_item.product_id}' not found."
                )

            items.append(
                PurchaseItemModel(
                    product_id=product.id,
                    name=product.name,
                    quantity=requested_item.quantity,
                    unit_price=product.price,
                )
            )

        plan = PurchasePlan(
            items=items,
            max_budget=request.max_budget,
            currency=request.currency,
        )

        policy_result = policy_engine.validate(plan)

        if policy_result.allowed:
            plan.status = PurchaseStatus.AWAITING_APPROVAL
        else:
            plan.status = PurchaseStatus.BLOCKED

        plan.explanation = policy_result.reason

        # Persist the complete purchase plan.
        purchase_plan_repository.save(plan)

        audit_service.log_event(
            event_type="PLAN_CREATED",
            plan_id=plan.plan_id,
            message="Purchase plan created.",
            metadata={
                "subtotal": plan.subtotal,
                "max_budget": plan.max_budget,
                "currency": plan.currency,
                "item_count": len(plan.items),
            },
        )

        if policy_result.allowed:

            audit_service.log_event(
                event_type="POLICY_VALIDATED",
                plan_id=plan.plan_id,
                message=(
                    "Purchase plan passed all policy checks."
                ),
                metadata={
                    "subtotal": plan.subtotal,
                    "max_budget": plan.max_budget,
                    "result": "ALLOWED",
                },
            )

        else:

            audit_service.log_event(
                event_type="PLAN_BLOCKED",
                plan_id=plan.plan_id,
                message=(
                    "Purchase plan was blocked by policy."
                ),
                metadata={
                    "subtotal": plan.subtotal,
                    "max_budget": plan.max_budget,
                    "result": "BLOCKED",
                    "reason": policy_result.reason,
                },
            )

        return plan

    def get_plan(
        self,
        plan_id: str,
    ) -> PurchasePlan | None:

        # SQLite is the source of truth.
        db_plan = purchase_plan_repository.get(plan_id)

        if db_plan is None:
            return None

        items = [
            PurchaseItemModel(
                product_id=item.product_id,
                name=item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in db_plan.items
        ]

        plan = PurchasePlan(
            items=items,
            max_budget=db_plan.max_budget,
            currency=db_plan.currency,
            plan_id=db_plan.plan_id,
            status=PurchaseStatus(db_plan.status),
            created_at=db_plan.created_at,
        )

        plan.explanation = db_plan.explanation

        return plan


purchase_service = PurchaseService()