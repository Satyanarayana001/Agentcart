# AgentCart Architecture

## 1. Purpose

AgentCart is an AI-powered agentic commerce application that converts a customer's natural-language shopping request into a validated and explainable purchase plan.

The architecture deliberately separates:

- AI interpretation and recommendation
- Deterministic business-policy validation
- Human authorization
- Payment processing
- Payment verification
- Order management
- Fulfillment tracking
- Notifications
- Audit logging

The central security and control boundary is:

```text
AI Decision
     ↓
Policy Check
     ↓
Human Approval
     ↓
Payment
     ↓
Payment Verification
     ↓
Order / Fulfillment
```

The AI is therefore an intelligent decision-support component, not an unrestricted financial authority.

---

# 2. High-Level Architecture

```text
                         ┌─────────────────────┐
                         │      Customer       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React Frontend    │
                         │      + Vite         │
                         ├─────────────────────┤
                         │ Demo Login           │
                         │ Commerce             │
                         │ Product Discovery    │
                         │ Purchase Plan        │
                         │ Approval Gate        │
                         │ Payment Gate         │
                         │ Orders               │
                         │ Order Details        │
                         │ Tracking             │
                         │ Notifications        │
                         └──────────┬──────────┘
                                    │ HTTP
                                    ▼
                 ┌─────────────────────────────────────┐
                 │           FastAPI Backend            │
                 ├─────────────────────────────────────┤
                 │ Agent API                            │
                 │ Catalog API                          │
                 │ Purchase API                         │
                 │ Payment API                          │
                 │ Orders API                           │
                 │ Tracking API                         │
                 │ Notifications API                    │
                 │ Audit API                             │
                 └───────────────┬─────────────────────┘
                                 │
             ┌───────────────────┼────────────────────┐
             │                   │                    │
             ▼                   ▼                    ▼
      ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
      │   SQLite    │     │    Groq     │     │  Razorpay    │
      │  Database   │     │     AI      │     │  Test Mode   │
      └─────────────┘     └─────────────┘     └──────────────┘
```

---

# 3. Frontend Architecture

The frontend is a React/Vite application.

```text
frontend/src/
│
├── api/
│   └── client.js
│
├── components/
│   ├── AlternativeProducts.jsx
│   ├── ApprovalGate.jsx
│   ├── AuditTimeline.jsx
│   ├── DemoLogin.jsx
│   ├── NotificationCenter.jsx
│   ├── PaymentGate.jsx
│   ├── ProductDiscovery.jsx
│   └── PurchasePlan.jsx
│
├── pages/
│   ├── CommercePage.jsx
│   ├── OrdersPage.jsx
│   └── OrderDetailsPage.jsx
│
├── App.jsx
├── App.css
└── index.css
```

### Application navigation

The application contains three primary page states:

```text
Shop
  ↓
Orders
  ↓
Order Details
```

The commerce page contains the active purchasing workflow.

---

# 4. Backend Architecture

The backend uses FastAPI with a separation between API routes, schemas, database models, and service logic.

```text
backend/app/
│
├── api/
│   ├── agent.py
│   ├── audit.py
│   ├── catalog.py
│   ├── notifications.py
│   ├── orders.py
│   ├── payment.py
│   ├── purchase.py
│   └── tracking.py
│
├── db/
│   ├── database.py
│   ├── models.py
│   ├── seed.py
│   └── data/
│       └── products.json
│
├── schemas/
│   ├── notification.py
│   ├── order.py
│   └── tracking.py
│
└── services/
    ├── agent_service.py
    ├── groq_adapter.py
    ├── notification_service.py
    ├── order_service.py
    └── tracking_service.py
```

The API layer handles HTTP requests and responses.

The service layer contains business behavior.

The database layer provides persistence.

---

# 5. Natural-Language Agent Flow

A customer can submit a request such as:

```text
Buy wireless ANC headphones under ₹5000
```

The flow is:

```text
Customer Request
       ↓
Agent API
       ↓
Groq Adapter
       ↓
Structured AI Intent
       ↓
Agent Service
       ↓
Catalog / Policy Validation
       ↓
Purchase Plan
```

The AI model is used to interpret the request and produce structured information.

The backend does not blindly trust the model output.

---

# 6. Catalog Layer

The product catalog is backed by:

```text
backend/app/db/data/products.json
```

The current demo catalog contains products with information including:

- Product ID
- Product name
- Description
- Price
- Stock
- Relevant product attributes

The catalog layer supports:

```text
Get products
Get product
Search products
```

The catalog is also used when finding alternatives for unavailable products.

---

# 7. Alternative Product Selection

When the requested product is unavailable, the agent service searches for suitable available alternatives.

The conceptual process is:

```text
Requested Product
       ↓
Check Stock
       ↓
Unavailable
       ↓
Find Available Catalog Products
       ↓
Rank Similar Products
       ↓
Return Alternatives
       ↓
Customer Chooses
       ↓
Revalidate Selected Product
```

The customer must explicitly choose the alternative.

The backend preserves the original budget instead of automatically increasing it.

---

# 8. Purchase Plan Layer

The purchase plan is the intermediate representation between recommendation and payment.

A plan contains information such as:

- Plan ID
- Maximum budget
- Currency
- Status
- Explanation
- Product items
- Quantity
- Unit price

The plan creates a controlled boundary before money movement.

---

# 9. Policy Validation

The backend validates the proposed purchase.

Conceptually:

```text
Product exists?
       ↓
Quantity valid?
       ↓
Enough stock?
       ↓
Within budget?
       ↓
Plan state valid?
       ↓
Continue
```

This prevents an AI recommendation from bypassing deterministic commerce rules.

---

# 10. Human Approval Layer

Human approval is an explicit state transition.

```text
PLAN_CREATED
      ↓
POLICY_VALIDATED
      ↓
PLAN_APPROVED
```

Payment-order creation occurs after approval.

This creates a clear separation between:

```text
AI recommendation
```

and:

```text
Customer authorization
```

---

# 11. Payment Layer

The payment API integrates Razorpay Test Mode.

The expected lifecycle is:

```text
Approved Plan
      ↓
Create Razorpay Order
      ↓
Razorpay Checkout
      ↓
Payment Response
      ↓
Backend Verification
      ↓
Payment Verified
      ↓
Purchase Completed
```

The frontend payment result is not treated as the final source of truth.

---

# 12. Payment Verification Boundary

The backend verifies payment before completing the purchase.

This is important because:

```text
Frontend:
"Payment succeeded"
```

must not automatically become:

```text
Backend:
"Purchase completed"
```

Instead:

```text
Payment Response
       ↓
Backend Verification
       ↓
Verified
       ↓
Complete Purchase
```

Only the verified state should enable the successful purchase lifecycle.

---

# 13. Database Model

The current database contains the following major entities:

```text
Product
PurchasePlan
PurchaseItem
PaymentOrder
AuditEvent
Fulfillment
Notification
```

The primary relationship chain is:

```text
PurchasePlan
      │
      ├── PurchaseItems
      │
      └── PaymentOrder
              │
              └── Fulfillment
```

Audit events and notifications reference the relevant plan/order identifiers.

---

# 14. Order Management

The order service exposes:

```text
GET /api/orders/
GET /api/orders/{order_id}
```

The order history is generated from persisted payment/order records.

Order details include:

- Order ID
- Plan ID
- Amount
- Currency
- Status
- Razorpay order ID
- Razorpay payment ID
- Created timestamp
- Items
- Plan explanation
- Plan status

---

# 15. Fulfillment Tracking

After payment verification, an order can enter the demo fulfillment lifecycle.

```text
PROCESSING
     ↓
SHIPPED
     ↓
OUT_FOR_DELIVERY
     ↓
DELIVERED
```

The tracking service:

1. Validates order/payment eligibility.
2. Creates fulfillment state when appropriate.
3. Advances the fulfillment state.
4. Records an audit event.
5. Creates a notification.

The tracking system is intentionally a controlled hackathon demonstration and is not a real courier integration.

---

# 16. Notification System

Notifications are stored in the database.

Each notification contains:

```text
notification_id
order_id
plan_id
title
message
notification_type
is_read
created_at
```

A tracking transition generates a notification.

For example:

```text
PROCESSING
     ↓
"Order is being prepared"

SHIPPED
     ↓
"Shipped"

OUT_FOR_DELIVERY
     ↓
"Out for delivery"

DELIVERED
     ↓
"Delivered"
```

The frontend periodically retrieves the unread count and can open the notification center to inspect notifications.

---

# 17. Audit System

The audit system records important lifecycle events.

A successful purchase can generate:

```text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Fulfillment transitions can generate:

```text
FULFILLMENT_PROCESSING
FULFILLMENT_SHIPPED
FULFILLMENT_OUT_FOR_DELIVERY
FULFILLMENT_DELIVERED
```

The audit timeline is therefore a chronological record of significant state changes.

---

# 18. API Boundaries

## Agent API

```text
POST /api/agent/purchase
POST /api/agent/select-product
```

## Catalog API

```text
GET /api/catalog/products
GET /api/catalog/products/{product_id}
GET /api/catalog/search
```

## Purchase API

```text
GET  /api/purchase/plans/{plan_id}
POST /api/purchase/plans/{plan_id}/approve
POST /api/purchase/plans/{plan_id}/reject
```

## Payment API

```text
POST /api/payment/plans/{plan_id}/orders
GET  /api/payment/orders/{payment_order_id}
POST /api/payment/orders/{payment_order_id}/verify
```

## Orders API

```text
GET /api/orders/
GET /api/orders/{order_id}
```

## Tracking API

```text
GET  /api/orders/{order_id}/tracking
POST /api/orders/{order_id}/tracking/advance
```

## Notifications API

```text
GET  /api/notifications/
GET  /api/notifications/unread-count
POST /api/notifications/{notification_id}/read
POST /api/notifications/read-all
```

## Audit API

```text
GET /api/audit/
GET /api/audit/plans/{plan_id}
```

---

# 19. End-to-End Data Flow

```text
Customer
   │
   │ Natural-language request
   ▼
Agent API
   │
   ▼
Groq AI
   │
   ▼
Agent Service
   │
   ├──────────────► Catalog
   │
   └──────────────► Policy Validation
                       │
                       ▼
                 Purchase Plan
                       │
                       ▼
                Human Approval
                       │
                       ▼
                 Payment API
                       │
                       ▼
                   Razorpay
                       │
                       ▼
              Backend Verification
                       │
                       ▼
                 Purchase Complete
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
           Orders              Audit
             │
             ▼
         Fulfillment
             │
       ┌─────┴─────┐
       ▼           ▼
    Tracking   Notifications
```

---

# 20. Docker Architecture

AgentCart is packaged as two Docker services.

```text
docker compose
      │
      ├── agentcart-frontend
      │       └── Nginx
      │           └── React production build
      │
      └── agentcart-backend
              └── FastAPI
                  └── Uvicorn
```

The frontend is built in a Node.js build stage and served using Nginx.

The backend runs independently as a Python service.

---

# 21. Architectural Invariants

The following rules are fundamental to AgentCart:

### Invariant 1

AI recommendation does not equal purchase authorization.

### Invariant 2

Business rules are enforced by the backend.

### Invariant 3

Out-of-stock products are not silently substituted.

### Invariant 4

Customer budget is not silently increased.

### Invariant 5

Payment is gated behind human approval.

### Invariant 6

Payment must be verified before purchase completion.

### Invariant 7

Important lifecycle transitions are auditable.

### Invariant 8

Fulfillment notifications originate from backend state transitions.

---

# 22. Design Philosophy

AgentCart is intentionally designed around **bounded agency**.

The goal is not:

```text
Give AI complete control.
```

The goal is:

```text
Give AI useful capabilities
while keeping high-impact actions
behind deterministic controls and human authorization.
```

This architecture allows AgentCart to demonstrate an agentic-commerce experience without treating the AI model itself as a trusted financial authority.
