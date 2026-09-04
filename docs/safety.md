# AgentCart Safety and Security

## 1. Purpose

AgentCart is designed around a central principle:

> **AI should assist with commerce without receiving unrestricted
> authority over money.**

The system separates:

-   AI reasoning
-   Deterministic policy enforcement
-   Human authorization
-   Payment execution
-   Payment verification
-   Fulfillment
-   Auditing

------------------------------------------------------------------------

## 2. Core Security Boundary

![AgentCart Money and Safety Boundary](assets/money-safety-boundary.png)

``` text
┌──────────────────────┐
│       AI Agent       │
│                      │
│ Understand request   │
│ Recommend product    │
│ Explain decision     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     Policy Layer     │
│                      │
│ Product              │
│ Stock                │
│ Quantity             │
│ Budget               │
│ Plan state            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Human Approval     │
│                      │
│ Explicit consent     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│       Payment        │
│    Razorpay Test     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Backend Verification │
└──────────────────────┘
```

This boundary is fundamental to AgentCart.

------------------------------------------------------------------------

## 3. AI Capability Boundary

The AI is allowed to:

-   Interpret natural-language requests
-   Extract purchasing constraints
-   Identify relevant catalog products
-   Recommend products
-   Help identify alternatives
-   Produce recommendation explanations

The AI is not granted unrestricted authority to:

-   Approve purchases
-   Override budget rules
-   Ignore stock constraints
-   Invent catalog products
-   Authorize payment
-   Mark payments as verified
-   Declare fulfillment completed

------------------------------------------------------------------------

## 4. Deterministic Backend Controls

The backend remains responsible for important commerce rules.

``` text
Product exists?
Quantity valid?
Stock sufficient?
Within budget?
Plan state valid?
Payment state valid?
```

AI output therefore enters a controlled validation layer before
financial actions occur.

------------------------------------------------------------------------

## 5. Catalog Integrity

AgentCart does not treat an AI product selection as sufficient evidence
that a product exists.

The selected product must correspond to the controlled catalog.

For:

``` text
Is there any TV?
```

the system can return:

``` text
CATALOG_INQUIRY
```

instead of forcing an unrelated product selection.

This prevents catalog hallucination from becoming a purchase action.

------------------------------------------------------------------------

## 6. Human-in-the-Loop Approval

The customer must explicitly approve the purchase plan.

``` text
AI Recommendation
       ↓
Purchase Plan
       ↓
Customer Review
       ↓
Customer Approval
       ↓
Payment Allowed
```

The customer can also reject the plan.

Rejection stops normal payment progression.

------------------------------------------------------------------------

## 7. No Silent Substitution

When a requested product is unavailable:

``` text
Unavailable
    ↓
Alternatives
    ↓
Customer Chooses
    ↓
Backend Revalidates
```

The agent does not silently select a replacement.

This preserves customer intent.

------------------------------------------------------------------------

## 8. No Silent Budget Increase

The maximum budget expressed by the customer is treated as a real
constraint.

Example:

``` text
Budget = ₹5000
Alternative = ₹5799
```

The system does not automatically convert:

``` text
₹5000 → ₹5799
```

The alternative must satisfy the existing policy constraints.

------------------------------------------------------------------------

## 9. Payment Security

AgentCart currently uses Razorpay Test Mode.

Sensitive credentials include:

``` text
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET
GROQ_API_KEY
```

Actual secret values must never be:

-   Hardcoded into source files
-   Sent to the frontend
-   Committed to Git
-   Included in README files
-   Shown in screenshots
-   Shown in recordings
-   Published in the repository

Local secrets belong in:

``` text
backend/.env
```

The repository should contain only placeholder configuration such as
`.env.example`.

------------------------------------------------------------------------

## 10. Payment Verification

A frontend payment response is not treated as sufficient proof of
payment.

``` text
Razorpay Checkout
       ↓
Payment identifiers
       ↓
Backend
       ↓
Payment verification
       ↓
Verified
       ↓
Purchase completion
```

The principle is:

``` text
Frontend payment success
          ≠
Backend verified payment
```

Only successful backend verification should enable purchase completion.

------------------------------------------------------------------------

## 11. Test Mode

The Buildathon implementation uses Razorpay Test Mode.

This allows demonstration of:

-   Payment-order creation
-   Checkout
-   Payment response
-   Backend verification
-   Purchase completion

without representing a real-money transaction.

The demo should clearly identify the payment flow as Test Mode.

------------------------------------------------------------------------

## 12. Auditability

Agentic commerce requires visibility into important actions.

AgentCart records significant lifecycle events.

Purchase events can include:

``` text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Fulfillment events can include:

``` text
FULFILLMENT_PROCESSING
FULFILLMENT_SHIPPED
FULFILLMENT_OUT_FOR_DELIVERY
FULFILLMENT_DELIVERED
```

This creates an inspectable transaction history.

------------------------------------------------------------------------

## 13. Explainability

AgentCart provides a visible:

``` text
Why this product?
```

section.

This connects:

``` text
Customer Request
       ↓
Recommendation
       ↓
Purchase Plan
```

The customer can therefore understand the recommendation before
authorizing it.

------------------------------------------------------------------------

## 14. Order and Fulfillment Boundaries

Payment completion and fulfillment tracking are separate concerns.

The current controlled lifecycle is:

``` text
PROCESSING
    ↓
SHIPPED
    ↓
OUT_FOR_DELIVERY
    ↓
DELIVERED
```

The fulfillment system is a Buildathon demonstration.

It is not represented as a live connection to a logistics provider.

------------------------------------------------------------------------

## 15. Demo Identity Boundary

The application uses a fictional demo customer:

``` text
Arjun Mehta
AC-DEMO-001
```

The login is intentionally lightweight for the Buildathon.

It should not be interpreted as:

-   Production authentication
-   Identity verification
-   Account recovery
-   Production authorization

A production deployment would require a complete authentication and
authorization system.

------------------------------------------------------------------------

## 16. Notification Integrity

Notifications are generated from backend state transitions.

Example:

``` text
Tracking changes to SHIPPED
        ↓
Audit event recorded
        ↓
Shipped notification created
```

The frontend is therefore not the authoritative source of fulfillment
state.

------------------------------------------------------------------------

## 17. Data Integrity

Important state is persisted in the backend database.

This includes:

-   Purchase plans
-   Payment orders
-   Orders
-   Audit events
-   Fulfillment state
-   Notifications

Persisted backend state allows important transaction information to
survive a frontend refresh.

------------------------------------------------------------------------

## 18. Docker and Secrets

The application is packaged as separate frontend and backend containers
for local deployment.

``` text
Frontend
   ↓
Backend
   ↓
External services
```

Secrets should be injected through environment configuration.

They should not be baked into frontend bundles or committed to source
control.

------------------------------------------------------------------------

## 19. Current Security Scope

AgentCart is a Buildathon implementation.

The current scope focuses on demonstrating:

``` text
AI
 ↓
Policy
 ↓
Human Approval
 ↓
Payment Verification
 ↓
Audit
```

It is not intended to represent a complete production security program.

------------------------------------------------------------------------

## 20. Production Security Requirements

Before using an AgentCart-like system with real customers and real
money, additional controls would be required.

### Authentication

-   Secure login
-   Session management
-   Account recovery
-   Appropriate multi-factor authentication

### Authorization

-   Customer-level data isolation
-   Role-based access control where appropriate
-   Server-side authorization checks

### Payment

-   Production payment configuration
-   Webhook verification
-   Idempotency
-   Replay protection
-   Robust payment-state reconciliation
-   Refund and cancellation workflows

### Infrastructure

-   HTTPS
-   Secure secret manager
-   Network controls
-   Rate limiting
-   Monitoring
-   Alerting
-   Secure structured logging

### Data

-   Production database
-   Backups
-   Encryption controls
-   Retention policies
-   Privacy controls

### Commerce

-   Inventory reservation
-   Concurrency protection
-   Real fulfillment integration
-   Operational recovery workflows

------------------------------------------------------------------------

## 21. Security Invariants

The following rules should remain true:

``` text
AI recommendation ≠ authorization
AI output ≠ business-rule validation
Missing catalog category ≠ invented product
Out-of-stock ≠ silent substitution
Alternative price ≠ automatic budget increase
Frontend payment success ≠ verified payment
Demo tracking ≠ real logistics
Demo login ≠ production authentication
```

------------------------------------------------------------------------

## 22. Safety Philosophy

AgentCart is built around **bounded agency**.

The goal is not:

``` text
Give AI complete control.
```

The goal is:

``` text
Give AI useful capabilities
while keeping high-impact actions
behind deterministic controls
and human authorization.
```

In short:

``` text
AI may recommend.
Backend must validate.
Human must approve.
Payment must be verified.
Important actions must be auditable.
```

That is the safety model at the heart of AgentCart.
