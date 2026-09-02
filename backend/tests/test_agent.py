import json
from unittest.mock import patch

import pytest

from app.schemas.agent import AgentPurchaseRequest
from app.services.agent_service import agent_service


def test_ai_selects_valid_product():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "max_budget": 5000,
        "reason": "Selected ANC headphones within the user's budget.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy ANC headphones under ₹5000"
        )

        result = agent_service.process_purchase_request(
            request
        )

    assert result.plan_id is not None

    assert result.status == "AWAITING_APPROVAL"

    assert (
        "ANC headphones"
        in result.explanation
    )


def test_ai_rejects_invalid_product():
    ai_response = {
        "product_id": "fake_product_999",
        "quantity": 1,
        "max_budget": 5000,
        "reason": "Fake product.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy something"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "invalid product"
        in str(error.value).lower()
    )


def test_ai_rejects_missing_product_id():
    ai_response = {
        "quantity": 1,
        "max_budget": 5000,
        "reason": "No product selected.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy something"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "did not return a product id"
        in str(error.value).lower()
    )


def test_ai_rejects_invalid_json():
    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value="this is not valid json",
    ):
        request = AgentPurchaseRequest(
            request="Buy ANC headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "ai agent failed to process request"
        in str(error.value).lower()
    )


def test_ai_rejects_zero_quantity():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 0,
        "max_budget": 5000,
        "reason": "Invalid quantity.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy zero headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "invalid quantity"
        in str(error.value).lower()
    )


def test_ai_rejects_negative_quantity():
    ai_response = {
        "product_id": "hp_001",
        "quantity": -1,
        "max_budget": 5000,
        "reason": "Invalid quantity.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy negative headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "invalid quantity"
        in str(error.value).lower()
    )


def test_ai_rejects_quantity_above_stock():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 999999,
        "max_budget": 5000000,
        "reason": "Large quantity.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy many headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "exceeds available stock"
        in str(error.value).lower()
    )


def test_ai_rejects_invalid_budget():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "max_budget": "not-a-number",
        "reason": "Invalid budget.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "invalid budget"
        in str(error.value).lower()
    )


def test_ai_rejects_zero_budget():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "max_budget": 0,
        "reason": "Invalid budget.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy headphones"
        )

        with pytest.raises(ValueError) as error:
            agent_service.process_purchase_request(
                request
            )

    assert (
        "invalid budget"
        in str(error.value).lower()
    )


def test_ai_uses_product_price_when_budget_missing():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "reason": "Selected the product.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy SoundMax headphones"
        )

        result = agent_service.process_purchase_request(
            request
        )

    assert result.plan_id is not None

    assert result.status == "AWAITING_APPROVAL"


def test_ai_output_still_goes_through_policy_engine():
    ai_response = {
        "product_id": "hp_001",
        "quantity": 1,
        "max_budget": 1000,
        "reason": "Selected product.",
    }

    with patch(
        "app.services.agent_service.groq_adapter.analyze_purchase_request",
        return_value=json.dumps(ai_response),
    ):
        request = AgentPurchaseRequest(
            request="Buy headphones under ₹1000"
        )

        result = agent_service.process_purchase_request(
            request
        )

    assert result.plan_id is not None

    assert result.status == "BLOCKED"

    # The AgentPurchaseResponse contains the AI's explanation,
    # while the policy decision is stored on the purchase plan.
    from app.services.purchase_service import purchase_service

    plan = purchase_service.get_plan(result.plan_id)

    assert plan is not None
    assert plan.status.value == "BLOCKED"

    assert (
        "exceeds"
        in plan.explanation.lower()
    )