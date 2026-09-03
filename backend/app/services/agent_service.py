import json
import re

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

        # ---------------------------------------------------------
        # 1. BACKEND CATALOG CHECK
        #
        # Explicit product/category inquiries are checked against
        # the real catalog BEFORE asking the LLM to select anything.
        # ---------------------------------------------------------

        catalog_inquiry = self._check_catalog_inquiry(
            user_request=request.request,
            products=products,
        )

        if catalog_inquiry is not None:
            return catalog_inquiry

        # ---------------------------------------------------------
        # 2. PREPARE CATALOG CONTEXT FOR AI
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # 3. AI INTERPRETATION
        # ---------------------------------------------------------

        try:
            ai_response = groq_adapter.analyze_purchase_request(
                user_request=request.request,
                products=available_products,
            )

            decision = json.loads(ai_response)

        except Exception as error:
            raise ValueError(
                f"AI agent failed to process request: {error}"
            )

        # ---------------------------------------------------------
        # 4. AI CATALOG INQUIRY
        # ---------------------------------------------------------

        product_id = decision.get("product_id")

        if (
            product_id is None
            and decision.get("intent") == "CATALOG_INQUIRY"
        ):
            reason = decision.get("reason")

            explanation = (
                reason
                or "That product is not currently available "
                   "in the AgentCart catalog."
            )

            explanation = (
                f"{explanation} "
                "If you'd like anything else, you can choose "
                "from the products available below."
            )

            return AgentPurchaseResponse(
                plan_id=None,
                status="CATALOG_INQUIRY",
                explanation=explanation,
                selected_product=None,
                alternatives=[],
            )

        # ---------------------------------------------------------
        # 5. AI MUST RETURN A PRODUCT ID
        # ---------------------------------------------------------

        if not product_id:
            raise ValueError(
                "AI agent did not return a product ID."
            )

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

        # ---------------------------------------------------------
        # 6. SECOND BACKEND SAFETY CHECK
        #
        # Even if Groq ignores the prompt and selects an unrelated
        # product, the backend validates the selection.
        # ---------------------------------------------------------

        if not self._request_matches_selected_product(
            user_request=request.request,
            selected_product=selected_product,
        ):
            return AgentPurchaseResponse(
                plan_id=None,
                status="CATALOG_INQUIRY",
                explanation=(
                    "The product you're looking for is not "
                    "currently available in the AgentCart catalog. "
                    "If you'd like anything else, you can choose "
                    "from the products available below."
                ),
                selected_product=None,
                alternatives=[],
            )

        # ---------------------------------------------------------
        # 7. EXISTING PURCHASE FLOW
        # ---------------------------------------------------------

        quantity = decision.get("quantity", 1)
        max_budget = decision.get("max_budget")
        reason = decision.get("reason")

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError(
                "AI agent returned an invalid quantity."
            )

        if (
            selected_product.stock > 0
            and quantity > selected_product.stock
        ):
            raise ValueError(
                "Requested quantity exceeds available stock."
            )

        if quantity > 10:
            raise ValueError(
                "Requested quantity exceeds the maximum allowed quantity."
            )

        if max_budget is None:
            max_budget = selected_product.price * quantity

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

        # ---------------------------------------------------------
        # 8. OUT-OF-STOCK PRODUCT
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # 9. CREATE PURCHASE PLAN
        # ---------------------------------------------------------

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

    # =============================================================
    # BACKEND CATALOG INQUIRY CHECK
    # =============================================================

    def _check_catalog_inquiry(
        self,
        user_request: str,
        products,
    ) -> AgentPurchaseResponse | None:

        request_text = user_request.lower().strip()

        # Words that indicate the user is asking about availability
        # rather than directly purchasing something.
        inquiry_patterns = [
            r"\bis there\b",
            r"\bdo you have\b",
            r"\bdoes agentcart have\b",
            r"\bavailable\b",
            r"\bavailability\b",
            r"\bcan i get\b",
            r"\bcan you provide\b",
        ]

        is_inquiry = any(
            re.search(pattern, request_text)
            for pattern in inquiry_patterns
        )

        if not is_inquiry:
            return None

        # ---------------------------------------------------------
        # Build actual catalog vocabulary.
        # ---------------------------------------------------------

        catalog_categories = {
            product.category.lower()
            for product in products
            if product.category
        }

        catalog_names = [
            product.name.lower()
            for product in products
        ]

        # ---------------------------------------------------------
        # Known category aliases.
        #
        # These map natural user terminology to catalog categories.
        # ---------------------------------------------------------

        aliases = {
            "tv": {"tv", "television", "smart tv"},
            "television": {"tv", "television", "smart tv"},
            "headphone": {
                "headphone",
                "headphones",
                "headset",
                "earphone",
                "earphones",
            },
            "headphones": {
                "headphone",
                "headphones",
                "headset",
                "earphone",
                "earphones",
            },
            "earbuds": {
                "earbud",
                "earbuds",
                "earphone",
                "earphones",
            },
            "laptop": {
                "laptop",
                "notebook",
            },
            "phone": {
                "phone",
                "smartphone",
                "mobile",
            },
            "smartphone": {
                "phone",
                "smartphone",
                "mobile",
            },
            "tablet": {
                "tablet",
                "ipad",
            },
            "speaker": {
                "speaker",
                "speakers",
            },
            "camera": {
                "camera",
                "cameras",
            },
            "watch": {
                "watch",
                "smartwatch",
            },
            "keyboard": {
                "keyboard",
                "keyboards",
            },
            "mouse": {
                "mouse",
                "mice",
            },
            "monitor": {
                "monitor",
                "monitors",
                "display",
            },
        }

        # ---------------------------------------------------------
        # Find explicitly requested product/category terms.
        # ---------------------------------------------------------

        requested_terms = set()

        for alias_group in aliases.values():
            for term in alias_group:
                if re.search(
                    rf"\b{re.escape(term)}\b",
                    request_text,
                ):
                    requested_terms.add(term)

        # ---------------------------------------------------------
        # Check actual catalog categories.
        # ---------------------------------------------------------

        for term in requested_terms:

            # Direct category match.
            if term in catalog_categories:
                return None

            # Alias → category match.
            for category, category_aliases in aliases.items():
                if term in category_aliases:
                    if category in catalog_categories:
                        return None

        # ---------------------------------------------------------
        # Check exact catalog product names.
        # ---------------------------------------------------------

        for product_name in catalog_names:
            if product_name in request_text:
                return None

        # ---------------------------------------------------------
        # If an explicit product/category was requested but no
        # matching catalog entry exists, stop BEFORE Groq.
        # ---------------------------------------------------------

        if requested_terms:

            requested_display = next(
                iter(requested_terms)
            )

            return AgentPurchaseResponse(
                plan_id=None,
                status="CATALOG_INQUIRY",
                explanation=(
                    f"'{requested_display}' is not currently "
                    "available in the AgentCart catalog. "
                    "If you'd like anything else, you can choose "
                    "from the products available below."
                ),
                selected_product=None,
                alternatives=[],
            )

        return None

    # =============================================================
    # BACKEND PRODUCT MATCH VALIDATION
    # =============================================================

    def _request_matches_selected_product(
        self,
        user_request: str,
        selected_product,
    ) -> bool:

        request_text = user_request.lower()

        product_text = " ".join(
            [
                selected_product.name,
                selected_product.description,
                selected_product.category,
            ]
        ).lower()

        # Explicit category aliases.
        aliases = {
            "tv": {
                "tv",
                "television",
                "smart tv",
            },
            "headphones": {
                "headphone",
                "headphones",
                "headset",
                "earphone",
                "earphones",
            },
            "earbuds": {
                "earbud",
                "earbuds",
                "earphone",
                "earphones",
            },
            "laptop": {
                "laptop",
                "notebook",
            },
            "phone": {
                "phone",
                "smartphone",
                "mobile",
            },
            "tablet": {
                "tablet",
                "ipad",
            },
            "speaker": {
                "speaker",
                "speakers",
            },
            "camera": {
                "camera",
                "cameras",
            },
        }

        # If an explicit category appears in the request,
        # selected product must belong to that category.
        for category, terms in aliases.items():

            if any(
                re.search(
                    rf"\b{re.escape(term)}\b",
                    request_text,
                )
                for term in terms
            ):

                if category == "headphones":
                    return (
                        selected_product.category.lower()
                        == "headphones"
                    )

                if category == "earbuds":
                    return (
                        selected_product.category.lower()
                        == "headphones"
                        and any(
                            term in product_text
                            for term in terms
                        )
                    )

                return (
                    category
                    in product_text
                )

        # Generic overlap for natural requests.
        stop_words = {
            "i",
            "want",
            "need",
            "buy",
            "get",
            "please",
            "something",
            "anything",
            "to",
            "the",
            "a",
            "an",
            "for",
            "under",
            "below",
            "less",
            "than",
            "with",
            "and",
            "or",
            "is",
            "there",
            "any",
            "do",
            "you",
            "have",
            "available",
            "currently",
            "can",
            "me",
            "my",
            "in",
            "on",
            "at",
            "around",
            "approximately",
        }

        request_words = {
            word
            for word in re.findall(
                r"[a-z0-9]+",
                request_text,
            )
            if word not in stop_words
            and len(word) >= 3
            and not word.isdigit()
        }

        if not request_words:
            return True

        product_words = set(
            re.findall(
                r"[a-z0-9]+",
                product_text,
            )
        )

        if request_words.intersection(product_words):
            return True

        # Semantic shopping intent.
        if "music" in request_words or "listen" in request_words:
            return selected_product.category.lower() in {
                "headphones",
                "speaker",
            }

        return False

    # =============================================================
    # CREATE PLAN FROM EXPLICIT PRODUCT SELECTION
    # =============================================================

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

    # =============================================================
    # PURCHASE PLAN
    # =============================================================

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

    # =============================================================
    # ALTERNATIVES
    # =============================================================

    def _find_alternatives(
        self,
        selected_product,
        products,
        quantity: int,
    ) -> list[AgentAlternative]:

        candidates = []

        for product in products:

            if product.id == selected_product.id:
                continue

            if product.stock < quantity:
                continue

            score = 0

            if (
                product.category.lower()
                == selected_product.category.lower()
            ):
                score += 5

            price_difference = abs(
                product.price
                - selected_product.price
            )

            if price_difference <= 1000:
                score += 3
            elif price_difference <= 2000:
                score += 1

            for key, value in selected_product.features.items():
                if product.features.get(key) == value:
                    score += 1

            candidates.append(
                (score, product)
            )

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