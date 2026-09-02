from fastapi import APIRouter, HTTPException

from app.schemas.agent import (
    AgentProductSelectionRequest,
    AgentPurchaseRequest,
    AgentPurchaseResponse,
)
from app.services.agent_service import agent_service


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"],
)


@router.post(
    "/purchase",
    response_model=AgentPurchaseResponse,
)
def agent_purchase(
    request: AgentPurchaseRequest,
):
    try:
        return agent_service.process_purchase_request(
            request
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post(
    "/select-product",
    response_model=AgentPurchaseResponse,
)
def select_product(
    request: AgentProductSelectionRequest,
):
    try:
        return agent_service.create_plan_from_product(
            request
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )