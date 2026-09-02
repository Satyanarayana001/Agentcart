import json

from app.integrations.groq_adapter import groq_adapter
from app.schemas.agent import (
    AgentAlternative,
    AgentPurchaseRequest,
    AgentPurchaseResponse,
    AgentSelectedProduct,
    AgentProductSelectionRequest,
)
from app.schemas.purchase import (
    CreatePurchasePlanRequest,
    PurchaseItemRequest,
)
from app.services.catalog_service import catalog_service
from app.services.purchase_service import purchase_service


class AgentService:

    def process_purchase_request(
        self,
        request: AgentPurchaseRequest,
    ) -> AgentPurchaseResponse:

        products = catalog_service.get_all_products()

        if not products:
            raise ValueError(
                "No products available in the catalog."
            )

        # -----------------------------------------------------
        # Prepare catalog context for AI
        # -----------------------------------------------------

        available_products = []

        for product in products:
            available_products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "stock": product.stock,
                }
            )

        # -----------------------------------------------------
        # AI INTERPRETATION
        # -----------------------------------------------------

        try:
            ai_response = (
                groq_adapter.analyze_purchase_request(
                    user_request=request.request,
                    products=available_products,
                )
            )

            decision = json.loads(ai_response)

        except Exception as error:
            raise ValueError(
                f"AI agent failed to process request: {error}"
            )

        product_id = decision.get("product_id")
        quantity = decision.get("quantity", 1)
        max_budget = decision.get("max_budget")
        reason = decision.get("reason")

        if not product_id:
            raise ValueError(
                "AI agent did not return a product ID."
            )

        # -----------------------------------------------------
        # Validate selected product
        # -----------------------------------------------------

        selected_product = next(
            (
                product
                for product in products
                if product.id == product_id
            ),
            None,
        )

        if selected_product is None:
            raise ValueError(
                "AI agent selected an invalid product."
            )

        # -----------------------------------------------------
        # Validate quantity
        # -----------------------------------------------------

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                "AI agent returned an invalid quantity."
            )

        if selected_product.stock > 0 and quantity > selected_product.stock:
             raise ValueError(
        "Requested quantity exceeds available stock."
    )

        if quantity > 10:
            raise ValueError(
        "Requested quantity exceeds the maximum allowed quantity."
    )

        # -----------------------------------------------------
        # Validate budget
        # -----------------------------------------------------

        if max_budget is None:
            max_budget = (
                selected_product.price * quantity
            )

        try:
            max_budget = float(max_budget)

        except (TypeError, ValueError):
            raise ValueError(
                "AI agent returned an invalid budget."
            )

        if max_budget <= 0:
            raise ValueError(
                "AI agent returned an invalid budget."
            )

        # -----------------------------------------------------
        # AVAILABILITY CHECK
        #
        # AI identifies the requested product.
        # Backend decides whether it is available.
        # -----------------------------------------------------

        if selected_product.stock < quantity:

            alternatives = self._find_alternatives(
                selected_product=selected_product,
                products=products,
                quantity=quantity,
            )

            return AgentPurchaseResponse(
                status="ALTERNATIVES_REQUIRED",
                explanation=(
                    f"'{selected_product.name}' is currently "
                    "unavailable. Please choose an available "
                    "alternative to continue."
                ),
                selected_product=AgentSelectedProduct(
                    product_id=selected_product.id,
                    name=selected_product.name,
                    price=selected_product.price,
                    currency=selected_product.currency,
                    stock=selected_product.stock,
                    quantity=quantity,
                    max_budget=max_budget,

                ),
                alternatives=alternatives,
            )

        # -----------------------------------------------------
        # PRODUCT AVAILABLE
        # Create normal purchase plan.
        # -----------------------------------------------------

        return self._create_purchase_plan(
            product=selected_product,
            quantity=quantity,
            max_budget=max_budget,
            explanation=(
                reason
                or f"Selected '{selected_product.name}' "
                "based on the user's request."
            ),
        )

    # =========================================================
    # CREATE PLAN FROM USER-SELECTED PRODUCT
    # =========================================================

    def create_plan_from_product(
        self,
        request: AgentProductSelectionRequest,
    ) -> AgentPurchaseResponse:

        product = catalog_service.get_product_by_id(
            request.product_id
        )

        if product is None:
            raise ValueError(
                "Selected product was not found."
            )

        # Check stock again.
        #
        # This is important because the product could have
        # become unavailable after the alternatives were shown.
        if product.stock < request.quantity:
            raise ValueError(
                "Selected product is no longer available."
            )

        return self._create_purchase_plan(
            product=product,
            quantity=request.quantity,
            max_budget=request.max_budget,
            explanation=(
                f"Selected '{product.name}' "
                "from the available alternatives."
            ),
        )

    # =========================================================
    # PURCHASE PLAN CREATION
    # =========================================================

    def _create_purchase_plan(
        self,
        product,
        quantity: int,
        max_budget: float,
        explanation: str,
    ) -> AgentPurchaseResponse:

        purchase_request = CreatePurchasePlanRequest(
            items=[
                PurchaseItemRequest(
                    product_id=product.id,
                    quantity=quantity,
                )
            ],
            max_budget=max_budget,
            currency="INR",
        )

        plan = purchase_service.create_plan(
            request=purchase_request
        )

        return AgentPurchaseResponse(
            plan_id=plan.plan_id,
            status=plan.status.value,
            explanation=explanation,
        )

    # =========================================================
    # FIND AVAILABLE ALTERNATIVES
    # =========================================================

    def _find_alternatives(
        self,
        selected_product,
        products,
        quantity: int,
    ) -> list[AgentAlternative]:

        candidates = []

        for product in products:

            # Never recommend the unavailable product itself.
            if product.id == selected_product.id:
                continue

            # Alternative must have enough stock.
            if product.stock < quantity:
                continue

            score = 0

            # Same category is the strongest signal.
            if (
                product.category.lower()
                == selected_product.category.lower()
            ):
                score += 5

            # Similar price.
            price_difference = abs(
                product.price
                - selected_product.price
            )

            if price_difference <= 1000:
                score += 3

            elif price_difference <= 2000:
                score += 1

            # Match product features.
            for key, value in selected_product.features.items():

                if product.features.get(key) == value:
                    score += 1

            candidates.append(
                (
                    score,
                    product,
                )
            )

        # Highest score first.
        # Lower price breaks ties.
        candidates.sort(
            key=lambda item: (
                -item[0],
                item[1].price,
            )
        )

        alternatives = []

        for score, product in candidates[:3]:

            reason_parts = []

            if (
                product.category.lower()
                == selected_product.category.lower()
            ):
                reason_parts.append(
                    "same category"
                )

            if (
                abs(
                    product.price
                    - selected_product.price
                )
                <= 1000
            ):
                reason_parts.append(
                    "similar price"
                )

            if not reason_parts:
                reason_parts.append(
                    "available catalog option"
                )

            alternatives.append(
                AgentAlternative(
                    product_id=product.id,
                    name=product.name,
                    price=product.price,
                    currency=product.currency,
                    stock=product.stock,
                    description=product.description,
                    reason=", ".join(reason_parts),
                )
            )

        return alternatives


agent_service = AgentService()