from dataclasses import dataclass

from app.models.purchase_plan import PurchasePlan
from app.services.catalog_service import catalog_service


@dataclass
class PolicyResult:
    allowed: bool
    reason: str


class PolicyEngine:
    def validate(self, plan: PurchasePlan) -> PolicyResult:
        if plan.subtotal > plan.max_budget:
            return PolicyResult(
                allowed=False,
                reason=(
                    f"Purchase total ₹{plan.subtotal:.2f} exceeds "
                    f"the maximum budget of ₹{plan.max_budget:.2f}."
                ),
            )

        for item in plan.items:
            product = catalog_service.get_product_by_id(item.product_id)

            if product is None:
                return PolicyResult(
                    allowed=False,
                    reason=f"Product '{item.product_id}' no longer exists.",
                )

            if product.stock < item.quantity:
                return PolicyResult(
                    allowed=False,
                    reason=(
                        f"Insufficient stock for '{product.name}'. "
                        f"Requested: {item.quantity}, "
                        f"Available: {product.stock}."
                    ),
                )

            if product.price != item.unit_price:
                return PolicyResult(
                    allowed=False,
                    reason=(
                        f"Price changed for '{product.name}'. "
                        f"Planned price: ₹{item.unit_price:.2f}, "
                        f"Current price: ₹{product.price:.2f}."
                    ),
                )

        return PolicyResult(
            allowed=True,
            reason="All purchase policy checks passed.",
        )


policy_engine = PolicyEngine()