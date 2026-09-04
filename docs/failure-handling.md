# AgentCart Failure Handling

## 1. Philosophy

AgentCart treats failure as a normal part of agentic commerce.

The system should not turn uncertainty or an invalid state into an
unintended purchase.

The recovery principle is:

``` text
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

> **If a required validation fails, do not silently continue.**

![AgentCart Failure
Handling](assets/failure-handling-catalog-inquiry.png)

------------------------------------------------------------------------

## 2. Failure Categories

AgentCart handles or demonstrates boundaries for:

-   Catalog/category absence
-   Out-of-stock products
-   Invalid products
-   Invalid quantities
-   Budget violations
-   Customer rejection
-   Payment failures
-   Payment verification failures
-   Invalid orders
-   Invalid tracking transitions
-   API errors
-   AI response validation
-   Refresh/persistence scenarios

------------------------------------------------------------------------

## 3. Missing Catalog Category

### Scenario

The customer asks:

``` text
Is there any TV?
```

when TV is not represented in the current catalog.

### Expected Behavior

``` text
Customer Request
       ↓
Catalog Inquiry Detection
       ↓
CATALOG_INQUIRY
       ↓
Explain Unavailability
       ↓
Keep Customer in Catalog
```

The system must not:

-   Invent a TV
-   Select an unrelated product
-   Create a purchase plan
-   Show an approval gate
-   Initiate payment

The customer can choose an actually available catalog product instead.

------------------------------------------------------------------------

## 4. Out-of-Stock Product

### Scenario

A genuine requested product exists in the catalog but:

``` text
Stock = 0
```

### Expected Behavior

``` text
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

------------------------------------------------------------------------

## 5. Alternative Selection

The alternative-product flow considers available catalog products using
factors such as:

-   Same category
-   Similar price
-   Matching features
-   Availability

The customer explicitly chooses the replacement.

The backend then revalidates the selected product.

------------------------------------------------------------------------

## 6. Budget Preservation

The original customer budget remains authoritative.

Example:

``` text
Original request: Under ₹5000
Alternative:      ₹5799
```

The system must not automatically change:

``` text
₹5000 → ₹5799
```

Instead, the selected alternative is evaluated against the original
budget.

If the alternative fails the policy, the purchase cannot continue under
that plan.

------------------------------------------------------------------------

## 7. Invalid Product

If a product identifier does not correspond to a valid catalog product,
the backend rejects the request.

The system should never create a valid-looking purchase plan for a
nonexistent product.

------------------------------------------------------------------------

## 8. Invalid Quantity

The backend validates quantity before purchase progression.

Invalid examples include:

``` text
Quantity <= 0
```

and:

``` text
Requested quantity > available stock
```

The request must be rejected rather than allowing an invalid purchase to
proceed.

------------------------------------------------------------------------

## 9. Budget Violation

If:

``` text
price × quantity > maximum budget
```

the plan cannot pass policy validation.

The system must not:

-   Increase the budget automatically
-   Hide the violation
-   Continue directly to payment

The customer must change the request or choose a valid product.

------------------------------------------------------------------------

## 10. Customer Rejection

Human rejection is an intentional stop condition.

``` text
Purchase Plan
      ↓
Customer Rejects
      ↓
Purchase Stops
```

A rejected plan must not continue into the normal payment authorization
path.

The AI cannot override the customer's decision.

------------------------------------------------------------------------

## 11. Payment Failure

A payment attempt may fail.

The system distinguishes:

``` text
Payment Failed
```

from:

``` text
Payment Verified
```

A failed payment must not become a completed purchase merely because
checkout was opened.

------------------------------------------------------------------------

## 12. Payment Verification Failure

The backend performs payment verification before treating the
transaction as completed.

``` text
Payment Response
       ↓
Backend Verification
       ↓
Verification Failed
       ↓
Do Not Complete Purchase
```

An unverified payment must not be treated as successful fulfillment.

------------------------------------------------------------------------

## 13. Invalid Order

When an unknown order ID is requested, the backend should return a
not-found response rather than fabricated order information.

``` text
Unknown Order ID
       ↓
404 / Not Found
       ↓
Frontend Error State
```

------------------------------------------------------------------------

## 14. Tracking Eligibility Failure

Tracking depends on the order being eligible for fulfillment.

An order that has not reached the appropriate payment state must not be
treated as ready for fulfillment.

The tracking service validates eligibility before beginning or advancing
fulfillment.

------------------------------------------------------------------------

## 15. Invalid Tracking Transition

Tracking follows a fixed lifecycle:

``` text
PROCESSING
    ↓
SHIPPED
    ↓
OUT_FOR_DELIVERY
    ↓
DELIVERED
```

The system should not:

-   Skip arbitrary states
-   Move backwards without an explicit supported operation
-   Advance beyond `DELIVERED`

An invalid transition should return an error instead of corrupting the
lifecycle.

------------------------------------------------------------------------

## 16. Notification Integrity

Notifications originate from backend state transitions.

Example:

``` text
Tracking changes to SHIPPED
        ↓
Audit event recorded
        ↓
Shipped notification created
```

This keeps notifications connected to actual fulfillment state.

------------------------------------------------------------------------

## 17. AI Response Failure

The AI model is not treated as a trusted business-rule engine.

If an AI response is:

-   Invalid
-   Malformed
-   Missing required information
-   Inconsistent with the catalog

the backend validation boundary should prevent unsafe progression.

``` text
AI proposes
   ↓
Backend validates
   ↓
Only valid state continues
```

------------------------------------------------------------------------

## 18. API Failure

Frontend API requests are handled through a common request layer.

When the backend returns an error, the frontend can surface an
appropriate error state rather than assuming success.

Examples:

``` text
Unable to load order details.
Unable to load tracking.
Unable to update tracking.
Unable to process your request.
```

------------------------------------------------------------------------

## 19. Refresh and Persistence

Important transaction state is persisted in the backend database.

After refreshing the application, the system can reload important state
such as:

-   Orders
-   Payment information
-   Audit events
-   Tracking state
-   Notifications

This prevents temporary React state from becoming the only source of
transaction truth.

------------------------------------------------------------------------

## 20. Failure Matrix

  Scenario                      Expected Behavior
  ----------------------------- ---------------------------------------
  Catalog category absent       Return `CATALOG_INQUIRY`
  Product out of stock          Show alternatives
  Alternative selected          Revalidate product
  Alternative above budget      Reject under original budget
  Invalid product               Reject request
  Invalid quantity              Reject request
  Budget exceeded               Block purchase
  Customer rejects              Stop purchase
  Payment fails                 Do not complete purchase
  Payment unverified            Do not mark completed
  Unknown order                 Return not found
  Invalid tracking transition   Reject transition
  AI output invalid             Backend validation blocks progression
  API error                     Show frontend error state
  Page refresh                  Reload persisted state

------------------------------------------------------------------------

## 21. Failure-Handling Principle

The most important AgentCart rule is:

> **When the system cannot safely continue, it should stop rather than
> guess.**

This is especially important when AI is involved in a financial
workflow.

A bad recommendation can be corrected.

An unintended payment is much more consequential.

AgentCart therefore prioritizes:

``` text
Safety
  >
Silent automation
```
