# AgentCart Safety and Security

## 1. Purpose

AgentCart is designed around a central principle:

> **AI should assist with commerce without receiving unrestricted
> authority over money.**

The system therefore separates:

-   AI reasoning;
-   deterministic policy enforcement;
-   human authorization;
-   payment execution;
-   payment verification;
-   fulfillment;
-   auditing.

------------------------------------------------------------------------

# 2. Core Security Boundary

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
│    Human Approval    │
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

# 3. AI Capability Boundary

The AI is allowed to:

-   interpret natural-language requests;
-   extract purchasing constraints;
-   identify relevant catalog products;
-   recommend products;
-   help identify alternatives;
-   produce recommendation explanations.

The AI is not granted unrestricted authority to:

-   approve purchases;
-   override budget rules;
-   ignore stock constraints;
-   invent catalog products;
-   authorize payment;
-   mark payments as verified;
-   declare fulfillment completed.

This is an intentional capability boundary.

------------------------------------------------------------------------

# 4. Deterministic Backend Controls

The backend remains responsible for important commerce rules.

Examples:

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

# 5. Catalog Integrity

AgentCart does not treat the AI's product selection as sufficient
evidence that a product exists.

The selected product must correspond to the controlled catalog.

For a category that is not represented, such as:

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

# 6. Human-in-the-Loop Approval

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

# 7. No Silent Substitution

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

# 8. No Silent Budget Increase

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

# 9. Payment Security

AgentCart currently uses Razorpay Test Mode.

Sensitive credentials include:

``` text
RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET
GROQ_API_KEY
```

Actual secret values must never be:

-   hardcoded into source files;
-   sent to the frontend;
-   committed to Git;
-   included in README files;
-   shown in screenshots;
-   shown in recordings;
-   published in the repository.

Local secrets belong in:

``` text
backend/.env
```

and the repository should contain only placeholder configuration such as
`.env.example`.

------------------------------------------------------------------------

# 10. Payment Verification

A frontend payment response is not treated as sufficient proof of
payment.

The intended boundary is:

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

# 11. Test Mode

The hackathon implementation uses Razorpay Test Mode.

This allows the demonstration of:

-   payment-order creation;
-   checkout;
-   payment response;
-   backend verification;
-   purchase completion;

without representing a real-money transaction.

The demo should clearly identify the payment flow as Test Mode.

------------------------------------------------------------------------

# 12. Auditability

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

# 13. Explainability

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

# 14. Order and Fulfillment Boundaries

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

The fulfillment system is a hackathon demonstration.

It is not represented as a live connection to a logistics provider.

------------------------------------------------------------------------

# 15. Demo Identity Boundary

The application uses a fictional demo customer.

``` text
Arjun Mehta
AC-DEMO-001
```

The login is intentionally lightweight for the hackathon.

It should not be interpreted as:

-   production authentication;
-   identity verification;
-   account recovery;
-   production authorization.

A production deployment would require a complete authentication and
authorization system.

------------------------------------------------------------------------

# 16. Notification Integrity

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

# 17. Data Integrity

Important state is persisted in the backend database.

This includes:

-   purchase plans;
-   payment orders;
-   orders;
-   audit events;
-   fulfillment state;
-   notifications.

Persisted backend state allows important transaction information to
survive a frontend refresh.

------------------------------------------------------------------------

# 18. Docker and Secrets

The application is packaged as separate frontend and backend containers.

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

# 19. Current Security Scope

AgentCart is a hackathon implementation.

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

# 20. Production Security Requirements

Before using an AgentCart-like system with real customers and real
money, additional controls would be required.

## Authentication

-   secure login;
-   session management;
-   account recovery;
-   appropriate multi-factor authentication.

## Authorization

-   customer-level data isolation;
-   role-based access control where appropriate;
-   server-side authorization checks.

## Payment

-   production payment configuration;
-   webhook verification;
-   idempotency;
-   replay protection;
-   robust payment-state reconciliation;
-   refund and cancellation workflows.

## Infrastructure

-   HTTPS;
-   secure secret manager;
-   network controls;
-   rate limiting;
-   monitoring;
-   alerting;
-   secure structured logging.

## Data

-   production database;
-   backups;
-   encryption controls;
-   retention policies;
-   privacy controls.

## Commerce

-   inventory reservation;
-   concurrency protection;
-   real fulfillment integration;
-   operational recovery workflows.

------------------------------------------------------------------------

# 21. Security Invariants

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

# 22. Safety Philosophy

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
