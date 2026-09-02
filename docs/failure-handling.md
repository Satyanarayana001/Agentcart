# AgentCart Failure Handling

## 1. Philosophy

AgentCart treats failure as a normal part of agentic commerce.

The system should not turn uncertainty or an invalid state into an unintended purchase.

The general recovery principle is:

```text
Detect
  ↓
Stop unsafe progression
  ↓
Explain
  ↓
Offer a valid recovery path
  ↓
Require customer action where necessary
```

The safest default is:

> **If a required validation fails, do not silently continue.**

---

# 2. Failure Categories

AgentCart currently handles or demonstrates failure boundaries for:

- Out-of-stock products
- Invalid products
- Invalid quantities
- Budget violations
- Customer rejection
- Payment failures
- Payment verification failures
- Invalid orders
- Invalid tracking transitions
- API errors
- AI response validation
- Refresh/persistence scenarios

---

# 3. Out-of-Stock Product

## Scenario

The customer requests a product that has:

```text
Stock = 0
```

The system must not proceed with a purchase for that product.

---

## Expected Behavior

```text
Requested Product
       ↓
Stock Check
       ↓
Unavailable
       ↓
Find Alternatives
       ↓
Show Alternatives
       ↓
Customer Chooses
       ↓
Revalidate
```

The customer is never silently moved to another product.

---

# 4. Alternative Selection

The alternative-product system searches the available catalog.

Alternatives can be ranked using:

- Same product category
- Similar price
- Matching features
- Availability

Up to three suitable alternatives can be presented.

The customer explicitly selects the replacement.

---

# 5. Budget Preservation

The original customer budget remains authoritative.

Example:

```text
Original request:
Under ₹5000

Alternative:
₹5799
```

The system must not automatically change:

```text
₹5000 → ₹5799
```

Instead, the selected alternative is revalidated against the original budget.

If it fails the policy, the purchase cannot continue under that plan.

---

# 6. Invalid Product

If a product identifier does not correspond to a valid catalog product, the backend rejects the request.

The system should not create a valid-looking purchase plan for a nonexistent product.

---

# 7. Invalid Quantity

The backend validates quantity before purchase progression.

Examples of invalid conditions include:

```text
Quantity <= 0
```

or:

```text
Requested quantity > available stock
```

The request must be rejected instead of allowing an invalid order.

---

# 8. Budget Violation

If:

```text
price × quantity > maximum budget
```

the plan cannot pass policy validation.

The system should not:

- Increase the budget automatically
- Hide the violation
- Continue directly to payment

The customer must change the request or choose a valid product.

---

# 9. Customer Rejection

Human rejection is an intentional stop condition.

Flow:

```text
Purchase Plan
      ↓
Customer Rejects
      ↓
Purchase Stops
```

The rejected plan must not proceed into the normal payment authorization path.

The AI cannot override the customer's decision.

---

# 10. Payment Failure

A payment attempt may fail.

The system must distinguish:

```text
Payment failed
```

from:

```text
Payment verified
```

A failed payment must not become a completed purchase merely because the checkout interface was opened.

The order/payment state remains available for inspection.

---

# 11. Payment Verification Failure

The backend performs payment verification before treating the transaction as completed.

Conceptually:

```text
Payment Response
       ↓
Backend Verification
       ↓
Verification Failed
       ↓
Do Not Complete Purchase
```

The system must not treat an unverified payment as successful fulfillment.

---

# 12. Invalid Order

When a customer opens an unknown order ID, the backend returns:

```text
404
Order not found.
```

The frontend can then display an appropriate error state.

This prevents fabricated order information from being shown.

---

# 13. Tracking Eligibility Failure

Tracking depends on the order being eligible for fulfillment.

An order that has not reached the appropriate payment state should not be treated as ready for fulfillment.

The tracking service validates payment eligibility before beginning or advancing fulfillment.

---

# 14. Invalid Tracking Transition

Tracking follows a fixed lifecycle:

```text
PROCESSING
     ↓
SHIPPED
     ↓
OUT_FOR_DELIVERY
     ↓
DELIVERED
```

The system should not skip arbitrary states or advance beyond:

```text
DELIVERED
```

If an invalid transition is requested, the backend returns an error rather than corrupting the lifecycle.

---

# 15. Notification Behavior

Notifications are generated from backend state transitions.

For example:

```text
PROCESSING
     ↓
Notification:
Order is being prepared
```

Then:

```text
SHIPPED
     ↓
Notification:
Shipped
```

Then:

```text
OUT_FOR_DELIVERY
     ↓
Notification:
Out for delivery
```

Then:

```text
DELIVERED
     ↓
Notification:
Delivered
```

This keeps notifications connected to actual application state.

---

# 16. AI Response Failure

The AI model is not treated as a trusted business-rule engine.

If an AI response is:

- Invalid
- Unstructured
- Missing required information
- Inconsistent with the catalog

the backend validation layer must prevent unsafe progression.

The AI can propose.

The backend decides whether the proposal is valid.

---

# 17. API Failure

Frontend API requests are handled through a common request layer.

When the backend returns an error, the frontend can surface an appropriate message rather than assuming success.

Examples:

```text
Unable to load order details.
Unable to load tracking.
Unable to update tracking.
```

---

# 18. Refresh and Persistence

Important transaction state is persisted in the backend database.

After refreshing the application, the system can reload:

- Order information
- Payment information
- Audit events
- Tracking state

This prevents the UI's temporary React state from becoming the only source of transaction truth.

---

# 19. Failure Matrix

| Scenario | Expected System Behavior |
|---|---|
| Product out of stock | Show alternatives |
| Alternative selected | Revalidate product |
| Alternative above budget | Reject under original budget |
| Invalid product | Reject request |
| Invalid quantity | Reject request |
| Budget exceeded | Block purchase |
| Customer rejects | Stop purchase |
| Payment fails | Do not complete purchase |
| Payment unverified | Do not mark completed |
| Unknown order | Return not found |
| Invalid tracking transition | Reject transition |
| AI output invalid | Backend validation blocks progression |
| API error | Show frontend error state |
| Page refresh | Reload persisted state |

---

# 20. Failure-Handling Principle

The most important AgentCart failure-handling rule is:

> **When the system cannot safely continue, it should stop rather than guess.**

This is especially important when AI is involved in a financial workflow.

A bad recommendation can be corrected.

An unintended payment is much more consequential.

AgentCart therefore prioritizes:

```text
Safety
  >
Silent automation
```
