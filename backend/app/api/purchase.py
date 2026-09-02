from fastapi import APIRouter, HTTPException

from app.schemas.purchase import (
    CreatePurchasePlanRequest,
    PurchaseItemResponse,
    PurchasePlanResponse,
)
from app.services.approval_service import approval_service
from app.services.purchase_service import purchase_service


router = APIRouter(
    prefix="/api/purchase",
    tags=["Purchase"],
)


def serialize_plan(plan) -> PurchasePlanResponse:
    return PurchasePlanResponse(
        plan_id=plan.plan_id,
        items=[
            PurchaseItemResponse(
                product_id=item.product_id,
                name=item.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in plan.items
        ],
        subtotal=plan.subtotal,
        currency=plan.currency,
        max_budget=plan.max_budget,
        status=plan.status.value,
        explanation=plan.explanation,
    )


@router.post(
    "/plans",
    response_model=PurchasePlanResponse,
)
def create_purchase_plan(
    request: CreatePurchasePlanRequest,
):
    try:
        plan = purchase_service.create_plan(request)
        return serialize_plan(plan)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.get(
    "/plans/{plan_id}",
    response_model=PurchasePlanResponse,
)
def get_purchase_plan(plan_id: str):
    plan = purchase_service.get_plan(plan_id)

    if plan is None:
        raise HTTPException(
            status_code=404,
            detail="Purchase plan not found.",
        )

    return serialize_plan(plan)


@router.post(
    "/plans/{plan_id}/approve",
    response_model=PurchasePlanResponse,
)
def approve_purchase_plan(plan_id: str):
    try:
        plan = approval_service.approve_plan(plan_id)
        return serialize_plan(plan)

    except ValueError as error:
        message = str(error)

        if message == "Purchase plan not found.":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )


@router.post(
    "/plans/{plan_id}/reject",
    response_model=PurchasePlanResponse,
)
def reject_purchase_plan(plan_id: str):
    try:
        plan = approval_service.reject_plan(plan_id)
        return serialize_plan(plan)

    except ValueError as error:
        message = str(error)

        if message == "Purchase plan not found.":
            raise HTTPException(
                status_code=404,
                detail=message,
            )

        raise HTTPException(
            status_code=400,
            detail=message,
        )