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
and select the best matching product from the provided catalog.

You MUST NOT approve, reject, authorize, or execute a purchase.

USER REQUEST:
{user_request}

AVAILABLE CATALOG:
{product_context}

IMPORTANT RULES:

1. Select exactly ONE product from the catalog.
2. The product_id MUST exactly match one of the catalog IDs.
3. Never invent a product ID.
4. Select the product that best matches the user's request,
   even if that product is currently out of stock.
5. The backend will independently check availability and
   provide alternatives if the selected product is unavailable.
6. Extract the user's maximum budget if one is explicitly mentioned.
7. If the user did not specify a budget, use the selected
   product price multiplied by quantity.
8. If the user says "under", "below", "less than", or similar,
   use that number as max_budget.
9. If the user says "around", "approximately", or similar,
   use that number as max_budget.
10. If no quantity is mentioned, quantity must be 1.
11. Quantity must be a positive integer.
12. Do NOT change the user's budget to make the purchase fit.
13. Do NOT compare the product price against the budget to
    decide whether the purchase is allowed.
14. Budget enforcement is performed by AgentCart's backend
    policy engine.
15. Return ONLY valid JSON.

Example:

User:
Buy ANC headphones under 100

If the catalog contains:
ID: hp_001 | Name: SoundMax Pro ANC | Price: 4499 INR

Return:

{{
    "product_id": "hp_001",
    "quantity": 1,
    "max_budget": 100,
    "reason": "Selected SoundMax Pro ANC because it matches the headphone request."
}}

The fact that the product costs more than the user's budget
does NOT mean you should reject it.

The backend policy engine will determine whether the purchase
is allowed.

Return exactly this JSON structure:

{{
    "product_id": "selected product ID",
    "quantity": 1,
    "max_budget": number,
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
                            "Select only from the provided catalog. "
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
