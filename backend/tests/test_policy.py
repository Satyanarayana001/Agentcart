from app.models.purchase_plan import (
    PurchaseItemModel,
    PurchasePlan,
)
from app.policies.policy_engine import policy_engine


def make_plan(
    product_id="hp_001",
    quantity=1,
    unit_price=4499,
    max_budget=5000,
):
    item = PurchaseItemModel(
        product_id=product_id,
        name="SoundMax Pro ANC",
        quantity=quantity,
        unit_price=unit_price,
    )

    return PurchasePlan(
        items=[item],
        max_budget=max_budget,
        currency="INR",
    )


def test_policy_allows_valid_purchase():
    plan = make_plan(
        quantity=1,
        unit_price=4499,
        max_budget=5000,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is True
    assert result.reason == (
        "All purchase policy checks passed."
    )


def test_policy_blocks_over_budget_purchase():
    plan = make_plan(
        quantity=1,
        unit_price=4499,
        max_budget=4000,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is False
    assert "exceeds" in result.reason
    assert "4000.00" in result.reason


def test_policy_blocks_missing_product():
    plan = make_plan(
        product_id="does_not_exist",
        quantity=1,
        unit_price=1000,
        max_budget=5000,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is False
    assert "no longer exists" in result.reason


def test_policy_blocks_insufficient_stock():
    plan = make_plan(
        product_id="hp_001",
        quantity=999,
        unit_price=4499,
        max_budget=5000000,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is False
    assert "Insufficient stock" in result.reason


def test_policy_blocks_price_change():
    plan = make_plan(
        product_id="hp_001",
        quantity=1,
        unit_price=1,
        max_budget=5000,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is False
    assert "Price changed" in result.reason


def test_policy_accepts_purchase_at_exact_budget():
    plan = make_plan(
        quantity=1,
        unit_price=4499,
        max_budget=4499,
    )

    result = policy_engine.validate(plan)

    assert result.allowed is True
    assert result.reason == (
        "All purchase policy checks passed."
    )