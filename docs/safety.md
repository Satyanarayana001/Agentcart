# AgentCart Safety and Security

## 1. Purpose

AgentCart is designed around a central principle:

> **AI should assist with commerce without receiving unrestricted authority over money.**

The system therefore separates:

- AI reasoning
- Deterministic policy enforcement
- Human authorization
- Payment execution
- Payment verification
- Fulfillment
- Auditing

---

# 2. Core Security Boundary

The central AgentCart boundary is:

```text
┌──────────────────────┐
│      AI Agent        │
│                      │
│ Understand request   │
│ Recommend product    │
│ Explain decision     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    Policy Layer      │
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

This boundary is fundamental to the application design.

---

# 3. AI Capability Boundary

The AI is allowed to:

- Interpret natural-language requests
- Identify relevant purchasing constraints
- Recommend products
- Help identify alternatives
- Generate purchase-plan explanations

The AI is not granted unrestricted authority to:

- Approve purchases
- Override budget rules
- Ignore stock constraints
- Authorize payment
- Mark payments as verified
- Declare fulfillment completed

This is an intentional capability boundary.

---

# 4. Deterministic Backend Controls

The backend remains responsible for enforcing important commerce rules.

Examples include:

```text
Product exists?
Quantity valid?
Stock sufficient?
Within budget?
Plan state valid?
Payment state valid?
```

The model's output therefore enters a controlled validation layer before financial actions occur.

---

# 5. Human-in-the-Loop Approval

The customer must explicitly approve the purchase plan.

The flow is:

```text
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

Rejection stops the normal payment progression.

---

# 6. No Silent Substitution

When a requested product is unavailable, AgentCart does not silently select a replacement.

Instead:

```text
Unavailable
    ↓
Alternatives
    ↓
Customer chooses
    ↓
Backend revalidates
```

This preserves customer intent and avoids unexpected purchases.

---

# 7. No Silent Budget Increase

The customer's maximum budget is treated as a real constraint.

For example:

```text
Budget = ₹5000
Alternative = ₹5799
```

The system does not automatically convert:

```text
₹5000 → ₹5799
```

The alternative must satisfy the existing plan constraints.

---

# 8. Payment Security

AgentCart currently uses Razorpay Test Mode.

Payment secrets must remain outside the frontend and source repository.

Sensitive credentials include:

```text
RAZORPAY_KEY_SECRET
GROQ_API_KEY
```

These values must never be:

- Hardcoded into source files
- Sent to the frontend
- Included in screenshots
- Added to README files
- Committed to Git
- Shared in public repositories

---

# 9. Environment Variables

The backend expects environment configuration such as:

```env
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
GROQ_API_KEY=
```

Local secrets belong in:

```text
backend/.env
```

The repository's ignore rules are intended to prevent local environment files from being committed.

`.env.example` contains placeholders rather than actual credentials.

---

# 10. Payment Verification

A frontend payment response is not treated as sufficient proof of payment.

The expected security flow is:

```text
Razorpay Checkout
       ↓
Payment identifiers
       ↓
Backend
       ↓
Signature / payment verification
       ↓
Verified
       ↓
Purchase completion
```

The backend is responsible for deciding whether the payment can be considered verified.

Only after successful verification should the purchase lifecycle move into the completed state.

---

# 11. Test Mode

The hackathon implementation uses Razorpay Test Mode.

This allows the application to demonstrate:

- Payment-order creation
- Checkout
- Payment response
- Backend verification
- Purchase completion

without using real customer money.

The demo should clearly identify payment as test-mode behavior.

---

# 12. Auditability

Agentic commerce requires visibility into important actions.

AgentCart records significant lifecycle events.

Example:

```text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Fulfillment events are also recorded.

This creates an inspectable history of the transaction.

---

# 13. Explainability

AgentCart provides a visible:

```text
Why this product?
```

section.

This helps the customer understand the relationship between:

```text
Customer request
       ↓
Product recommendation
       ↓
Purchase plan
```

The system therefore does not hide the recommendation behind an opaque checkout step.

---

# 14. Order and Fulfillment Boundaries

The application separates payment completion from fulfillment tracking.

The tracking lifecycle is:

```text
PROCESSING
     ↓
SHIPPED
     ↓
OUT_FOR_DELIVERY
     ↓
DELIVERED
```

The current fulfillment system is a controlled hackathon demo.

It is not represented as a live connection to a real logistics provider.

---

# 15. Demo Identity Boundary

The current application uses a fictional demo customer:

```text
Arjun Mehta
AC-DEMO-001
```

The login is intentionally lightweight for the hackathon.

It should not be interpreted as:

- Production authentication
- Identity verification
- Account recovery
- Authorization for real users

A production version would require a complete authentication and authorization system.

---

# 16. Notification Integrity

Notifications are generated from backend state transitions.

For example:

```text
Tracking changes to SHIPPED
        ↓
Audit event recorded
        ↓
Shipped notification created
```

This avoids making the frontend the authoritative source for fulfillment state.

---

# 17. Data Integrity

Important state is persisted in the backend database.

This includes:

- Purchase plans
- Payment orders
- Audit events
- Fulfillment state
- Notifications
- Orders

This allows the application to recover important state after a page refresh.

---

# 18. Docker and Secrets

The application is packaged as separate frontend and backend containers.

```text
Frontend
   ↓
Backend
   ↓
External services
```

Secrets should be injected through environment configuration.

They should not be baked into Docker images or committed to source control.

---

# 19. Current Security Scope

AgentCart is a hackathon implementation.

The current scope intentionally focuses on demonstrating the core safety architecture:

```text
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

---

# 20. Production Security Requirements

Before using a system like AgentCart for real customers and real money, additional controls would be required.

These include:

### Authentication

- Secure login
- Session management
- Account recovery
- Multi-factor authentication where appropriate

### Authorization

- User-level data isolation
- Role-based access control
- Server-side authorization checks

### Payment

- Production payment configuration
- Webhook verification
- Idempotency
- Replay protection
- Robust payment-state reconciliation

### Infrastructure

- HTTPS
- Secure secret manager
- Network controls
- Rate limiting
- Monitoring
- Alerting
- Secure logging

### Data

- Production database
- Backups
- Encryption controls
- Retention policies
- Privacy controls

### Commerce

- Inventory reservation
- Concurrency protection
- Real fulfillment integration
- Refund/cancellation workflows

---

# 21. Security Invariants

The following rules should remain true throughout the application:

```text
AI recommendation ≠ authorization

AI output ≠ business-rule validation

Out-of-stock ≠ silent substitution

Alternative price ≠ automatic budget increase

Frontend payment success ≠ verified payment

Demo tracking ≠ real logistics

Demo login ≠ production authentication
```

---

# 22. Safety Philosophy

AgentCart is built around **bounded agency**.

The goal is not to remove humans from every commerce decision.

The goal is to automate the parts where AI provides value while preserving control over high-impact actions.

In short:

```text
AI may recommend.
Backend must validate.
Human must approve.
Payment must be verified.
Important actions must be auditable.
```

That is the safety model at the heart of AgentCart.
