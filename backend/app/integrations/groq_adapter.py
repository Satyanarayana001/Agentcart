from groq import Groq

from app.config import settings


class GroqAdapter:
    def __init__(self):
        self.client = None

        if settings.GROQ_API_KEY:
            self.client = Groq(
                api_key=settings.GROQ_API_KEY
            )

    def is_configured(self) -> bool:
        return self.client is not None

    def analyze_purchase_request(
        self,
        user_request: str,
        products: list[dict],
    ) -> str:

        if not self.is_configured():
            raise ValueError(
                "Groq is not configured. "
                "Add GROQ_API_KEY to the .env file."
            )

        product_context = "\n".join(
            [
                (
                    f"ID: {product['id']} | "
                    f"Name: {product['name']} | "
                    f"Description: {product['description']} | "
                    f"Price: {product['price']} INR | "
                    f"Stock: {product['stock']}"
                )
                for product in products
            ]
        )

        prompt = f"""
You are the AI decision layer for AgentCart.

Your job is ONLY to interpret the user's shopping request
against the provided catalog.

You MUST NOT approve, reject, authorize, or execute a purchase.

USER REQUEST:
{user_request}

AVAILABLE CATALOG:
{product_context}

IMPORTANT RULES:

1. First determine whether the user's requested product or
   product category is genuinely represented in the catalog.

2. If the user's requested product/category IS represented
   by a genuine catalog match, select the best matching
   product.

3. If the user's requested product/category is NOT represented
   in the catalog, DO NOT force a product selection.

4. For a request that has no genuine catalog match, return:

   "intent": "CATALOG_INQUIRY"
   "product_id": null
   "quantity": 1
   "max_budget": null

   The reason should briefly explain that the requested
   product or category is not currently available.

5. Never select an unrelated product as a substitute.

6. Never invent a product ID.

7. A product being out of stock does NOT mean it is absent
   from the catalog. If it genuinely matches the request,
   select it even if stock is insufficient.

8. The backend independently handles stock availability
   and alternatives.

9. When a genuine catalog match exists, return:

   "intent": "PRODUCT_REQUEST"
   "product_id": the exact catalog product ID
   "quantity": requested quantity
   "max_budget": requested budget
   "reason": short explanation

10. Extract the user's maximum budget if one is explicitly
    mentioned.

11. If the user did not specify a budget, use the selected
    product price multiplied by quantity.

12. If the user says "under", "below", "less than", or
    similar, use that number as max_budget.

13. If the user says "around", "approximately", or similar,
    use that number as max_budget.

14. If no quantity is mentioned, quantity must be 1.

15. Quantity must be a positive integer.

16. Do NOT change the user's budget to make the purchase fit.

17. Do NOT compare the product price against the budget to
    decide whether the purchase is allowed.

18. Budget enforcement is performed by AgentCart's backend
    policy engine.

19. Do NOT approve or reject purchases.

20. Return ONLY valid JSON.

Example 1:

User:
Buy ANC headphones under 5000

If the catalog contains:

ID: hp_001 | Name: SoundMax Pro ANC | Price: 4499 INR

Return:

{{
    "intent": "PRODUCT_REQUEST",
    "product_id": "hp_001",
    "quantity": 1,
    "max_budget": 5000,
    "reason": "Selected SoundMax Pro ANC because it matches the headphone request."
}}

Example 2:

User:
Is there any TV?

If the catalog contains headphones and speakers but
does not contain TVs:

Return:

{{
    "intent": "CATALOG_INQUIRY",
    "product_id": null,
    "quantity": 1,
    "max_budget": null,
    "reason": "TVs are not currently available in the AgentCart catalog."
}}

Example 3:

User:
Do you have a laptop?

If the catalog does not contain laptops:

Return:

{{
    "intent": "CATALOG_INQUIRY",
    "product_id": null,
    "quantity": 1,
    "max_budget": null,
    "reason": "Laptops are not currently available in the AgentCart catalog."
}}

Example 4:

User:
Do you have headphones?

If the catalog contains headphones:

Return a PRODUCT_REQUEST for the best genuine
headphone match.

Do NOT return CATALOG_INQUIRY when a genuine
catalog match exists.

Example 5:

User:
I want something to listen to music.

If the catalog contains headphones that genuinely
match this request:

Return a PRODUCT_REQUEST for the best matching
headphone product.

Do not return CATALOG_INQUIRY when a genuine
catalog match exists.

Return exactly this JSON structure:

{{
    "intent": "PRODUCT_REQUEST or CATALOG_INQUIRY",
    "product_id": "selected product ID or null",
    "quantity": 1,
    "max_budget": number or null,
    "reason": "short explanation"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a controlled shopping "
                            "interpretation assistant for AgentCart. "
                            "Only select products that genuinely "
                            "match the user's request and exist "
                            "in the provided catalog. "
                            "If no genuine catalog match exists, "
                            "return intent CATALOG_INQUIRY with "
                            "product_id null. "
                            "Never select an unrelated product as "
                            "a placeholder or substitute. "
                            "Never invent products or product IDs. "
                            "Extract the user's requested budget "
                            "without changing it. "
                            "Never approve or reject purchases. "
                            "Always return valid JSON."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0,
                response_format={
                    "type": "json_object"
                },
            )

        except Exception as error:
            raise ValueError(
                f"Groq request failed: {error}"
            )

        content = response.choices[0].message.content

        if not content:
            raise ValueError(
                "Groq returned an empty response."
            )

        return content


groq_adapter = GroqAdapter()