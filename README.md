# 🛒 AgentCart

## Explainable AI-Powered Agentic Commerce

> **AgentCart turns a natural-language shopping request into a
> policy-checked, human-approved, auditable transaction.**

AgentCart is an **AI-powered agentic commerce platform** built for the
Razorpay AI Buildathon --- **Track 01: AI Growth & Agentic Commerce**.

The project explores a simple question:

> **How can AI make commerce easier without giving an AI unrestricted
> authority over a customer's money?**

A customer can express a shopping goal conversationally:

``` text
Buy wireless ANC headphones under ₹5000
```

AgentCart interprets the request, works against a controlled product
catalog, validates the resulting purchase against deterministic
policies, explains the recommendation, creates a purchase plan, and
waits for explicit customer approval.

Only after approval can the payment stage begin.

------------------------------------------------------------------------

## 🎯 Core Idea

AgentCart separates **intelligence** from **authority**.

``` text
Customer Intent
      ↓
AI Interpretation
      ↓
Catalog Validation
      ↓
Policy Validation
      ↓
Purchase Plan
      ↓
Human Approval
      ↓
Razorpay Test Payment
      ↓
Backend Payment Verification
      ↓
Order + Audit
      ↓
Tracking + Notifications
```

The key principle is:

> **The AI can recommend and prepare. It does not receive unrestricted
> authority to move money.**

------------------------------------------------------------------------

# 🎯 The Problem

Traditional e-commerce is optimized around search boxes, filters,
product pages, and checkout forms.

That works well when a customer already knows what they want. It creates
more friction when the customer has a goal instead of a specific SKU.

For example:

``` text
I need wireless ANC headphones under ₹5000.
```

A conventional workflow may require the customer to:

1.  Search for headphones.
2.  Filter for wireless products.
3.  Filter for ANC.
4.  Set a price limit.
5.  Compare products.
6.  Check stock.
7.  Select a product.
8.  Start checkout.
9.  Pay.

Agentic commerce can compress the **discovery and decision-support**
portion of that process into a conversation.

But financial actions require stronger controls.

An AI system must not be trusted to:

-   silently substitute a product;
-   override a customer's budget;
-   ignore stock constraints;
-   invent catalog products;
-   approve its own recommendation;
-   treat an unverified payment as successful.

AgentCart is designed around those boundaries.

------------------------------------------------------------------------

# 💡 The AgentCart Approach

AgentCart has three logical layers.

### 1. Intelligence

The AI interprets:

``` text
What does the customer want?
What product is relevant?
What constraints did the customer express?
Why is the product relevant?
```

### 2. Control

The backend determines:

``` text
Does the product exist?
Is the requested quantity valid?
Is sufficient stock available?
Is the purchase within budget?
Is the plan in a valid state?
Is payment verified?
```

### 3. Authorization

The customer determines:

``` text
Do I actually want to purchase this?
```

This separation is the foundation of the application.

------------------------------------------------------------------------

# ✨ Core Capabilities

## 1. Conversational Product Discovery

Customers can describe a shopping requirement using natural language.

Example:

``` text
Buy wireless ANC headphones under ₹5000
```

The request is interpreted into structured purchase intent and evaluated
against the catalog.

------------------------------------------------------------------------

## 2. AI-Powered Product Recommendation

AgentCart can recommend a catalog product based on:

-   product category;
-   requested features;
-   price;
-   stock;
-   quantity;
-   customer budget.

The recommendation is presented before payment.

------------------------------------------------------------------------

## 3. Explainable Recommendations

AgentCart exposes a visible:

``` text
Why this product?
```

explanation.

The customer can understand how the recommendation relates to the
original request before deciding whether to approve the purchase.

------------------------------------------------------------------------

## 4. Policy-Gated Purchasing

AI output is not treated as final authority.

The backend independently validates:

``` text
Product
   ↓
Quantity
   ↓
Stock
   ↓
Budget
   ↓
Purchase State
```

Only a valid purchase plan can proceed toward approval.

------------------------------------------------------------------------

## 5. Human Approval Gate

The system deliberately separates:

``` text
AI recommends this
```

from:

``` text
I approve this purchase
```

The customer must explicitly approve the purchase plan before the
payment-order stage.

------------------------------------------------------------------------

## 6. No Silent Substitution

AgentCart distinguishes two failure cases.

### Product absent from the catalog

For a request such as:

``` text
Is there any TV?
```

when TV is not represented in the catalog, AgentCart returns a catalog
inquiry instead of inventing an unrelated product.

``` text
CATALOG_INQUIRY
```

No purchase plan is created and no approval gate should appear.

The customer can instead choose from the products actually available in
the catalog.

### Product exists but is out of stock

If a genuine catalog match exists but has:

``` text
Stock = 0
```

AgentCart can find available alternatives.

``` text
Requested Product
       ↓
Out of Stock
       ↓
Available Alternatives
       ↓
Customer Chooses
       ↓
Backend Revalidates
```

The customer explicitly controls substitution.

------------------------------------------------------------------------

## 7. Budget Preservation

The original customer budget remains authoritative.

Example:

``` text
Original budget: ₹5000
Alternative:     ₹5799
```

AgentCart does not silently change:

``` text
₹5000 → ₹5799
```

The selected alternative must still pass the backend policy constraints.

------------------------------------------------------------------------

## 8. Razorpay Test-Mode Payments

AgentCart uses **Razorpay Test Mode** for the hackathon.

The intended lifecycle is:

``` text
Approved Plan
      ↓
Create Razorpay Order
      ↓
Checkout
      ↓
Payment Response
      ↓
Backend Verification
      ↓
Payment Verified
      ↓
Purchase Completed
```

A frontend payment response is not treated as sufficient proof of
successful payment.

------------------------------------------------------------------------

## 9. Orders

After successful payment verification, the application exposes persisted
order information.

Order history and order details can include:

-   Order ID;
-   Plan ID;
-   Product;
-   Quantity;
-   Amount;
-   Currency;
-   Status;
-   Razorpay order reference;
-   Razorpay payment reference;
-   AI recommendation explanation;
-   Audit information;
-   Tracking information.

------------------------------------------------------------------------

## 10. Fulfillment Tracking

The current tracking system is a controlled hackathon demonstration.

``` text
PROCESSING
    ↓
SHIPPED
    ↓
OUT_FOR_DELIVERY
    ↓
DELIVERED
```

The UI presents these as:

``` text
Preparing
    ↓
Shipped
    ↓
Out for delivery
    ↓
Delivered
```

This is **not presented as a real logistics-provider integration**.

------------------------------------------------------------------------

## 11. Notifications

Tracking transitions generate persisted in-app notifications.

Examples:

``` text
Order is being prepared
Shipped
Out for delivery
Delivered
```

The frontend periodically checks the unread notification count.

------------------------------------------------------------------------

## 12. Audit Trail

Important transaction lifecycle events are recorded.

A successful purchase can contain:

``` text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Fulfillment transitions can additionally produce:

``` text
FULFILLMENT_PROCESSING
FULFILLMENT_SHIPPED
FULFILLMENT_OUT_FOR_DELIVERY
FULFILLMENT_DELIVERED
```

This gives the transaction an inspectable lifecycle instead of only a
final success state.

------------------------------------------------------------------------

# 🧠 System Architecture

``` text
                         CUSTOMER
                            │
                            ▼
                 ┌──────────────────────┐
                 │    React Frontend    │
                 │       + Vite         │
                 ├──────────────────────┤
                 │ Demo Login           │
                 │ Commerce             │
                 │ Product Discovery    │
                 │ Purchase Plan        │
                 │ Approval Gate        │
                 │ Payment Gate         │
                 │ Orders               │
                 │ Tracking             │
                 │ Notifications        │
                 └──────────┬───────────┘
                            │ HTTP
                            ▼
                 ┌──────────────────────┐
                 │    FastAPI Backend   │
                 ├──────────────────────┤
                 │ Agent API            │
                 │ Catalog API          │
                 │ Purchase API         │
                 │ Payment API          │
                 │ Orders API           │
                 │ Tracking API         │
                 │ Notifications API    │
                 │ Audit API            │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐   ┌───────────┐
        │ SQLite  │    │  Groq   │   │ Razorpay  │
        │Database │    │   AI    │   │ Test Mode │
        └─────────┘    └─────────┘   └───────────┘
```

------------------------------------------------------------------------

# 🏗️ Technology Stack

  Layer                    Technology             Purpose
  ------------------------ ---------------------- ---------------------------------------
  Frontend                 React                  User interface
  Frontend tooling         Vite                   Development/build tooling
  Frontend communication   Fetch API              Backend communication
  Backend                  Python                 Application language
  API                      FastAPI                REST API framework
  Validation               Pydantic               Request/response validation
  ORM                      SQLAlchemy             Database access
  Database                 SQLite                 Local persistence
  AI                       Groq                   LLM inference
  AI model                 `openai/gpt-oss-20b`   Structured intent interpretation
  Payments                 Razorpay               Payment order, checkout, verification
  Infrastructure           Docker                 Containerization
  Orchestration            Docker Compose         Multi-service setup
  Web serving              Nginx                  Production frontend serving

------------------------------------------------------------------------

# 📁 Project Structure

``` text
agentcart/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── agent.py
│   │   │   ├── audit.py
│   │   │   ├── catalog.py
│   │   │   ├── notifications.py
│   │   │   ├── orders.py
│   │   │   ├── payment.py
│   │   │   ├── purchase.py
│   │   │   └── tracking.py
│   │   │
│   │   ├── db/
│   │   │   ├── data/
│   │   │   │   ├── images/
│   │   │   │   └── products.json
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── seed.py
│   │   │
│   │   ├── schemas/
│   │   └── services/
│   │       ├── agent_service.py
│   │       ├── groq_adapter.py
│   │       ├── notification_service.py
│   │       ├── order_service.py
│   │       └── tracking_service.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── AlternativeProducts.jsx
│   │   │   ├── ApprovalGate.jsx
│   │   │   ├── AuditTimeline.jsx
│   │   │   ├── DemoLogin.jsx
│   │   │   ├── NotificationCenter.jsx
│   │   │   ├── PaymentGate.jsx
│   │   │   ├── ProductDiscovery.jsx
│   │   │   └── PurchasePlan.jsx
│   │   ├── pages/
│   │   │   ├── CommercePage.jsx
│   │   │   ├── OrdersPage.jsx
│   │   │   └── OrderDetailsPage.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── Dockerfile
│   └── nginx.conf
│
├── docs/
│   ├── architecture.md
│   ├── demo-flow.md
│   ├── failure-handling.md
│   └── safety.md
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

------------------------------------------------------------------------

# 🔄 End-to-End Purchase Flow

``` text
1. Demo Login
       ↓
2. Customer describes requirement
       ↓
3. AI interprets request
       ↓
4. Catalog/product validation
       ↓
5. Stock + quantity + budget validation
       ↓
6. Purchase plan created
       ↓
7. Customer reviews explanation
       ↓
8. Customer approves
       ↓
9. Razorpay order created
       ↓
10. Razorpay Test Checkout
       ↓
11. Backend verifies payment
       ↓
12. Purchase completed
       ↓
13. Order available in history
       ↓
14. Fulfillment begins
       ↓
15. Tracking updates
       ↓
16. Notifications generated
       ↓
17. Audit trail updated
```

------------------------------------------------------------------------

# 🗃️ Data Model

Major database entities:

``` text
Product
PurchasePlan
PurchaseItem
PaymentOrder
AuditEvent
Fulfillment
Notification
```

Relationship concept:

``` text
Product
   │
   ▼
PurchaseItem
   │
   ▼
PurchasePlan
   │
   ├──────────────► AuditEvent
   │
   ▼
PaymentOrder
   │
   ▼
Fulfillment
   │
   └──────────────► Notification
```

Important state is persisted in SQLite so the backend remains the source
of transaction state after a frontend refresh.

------------------------------------------------------------------------

# 🧩 API Surface

### Agent

``` text
POST /api/agent/purchase
POST /api/agent/select-product
```

### Catalog

``` text
GET /api/catalog/products
GET /api/catalog/products/{product_id}
GET /api/catalog/search
```

### Purchase Plans

``` text
GET  /api/purchase/plans/{plan_id}
POST /api/purchase/plans/{plan_id}/approve
POST /api/purchase/plans/{plan_id}/reject
```

### Payments

``` text
POST /api/payment/plans/{plan_id}/orders
GET  /api/payment/orders/{payment_order_id}
POST /api/payment/orders/{payment_order_id}/verify
```

### Orders

``` text
GET /api/orders/
GET /api/orders/{order_id}
```

### Tracking

``` text
GET  /api/orders/{order_id}/tracking
POST /api/orders/{order_id}/tracking/advance
```

### Notifications

``` text
GET  /api/notifications/
GET  /api/notifications/unread-count
POST /api/notifications/{notification_id}/read
POST /api/notifications/read-all
```

### Audit

``` text
GET /api/audit/
GET /api/audit/plans/{plan_id}
```

------------------------------------------------------------------------

# 🧪 Verified Demo Scenarios

  Scenario                            Expected Result
  ----------------------------------- -----------------------------------------------
  Natural-language product request    AI recommendation/purchase plan
  `Is there any TV?`                  `CATALOG_INQUIRY`, no purchase plan
  Matching product with zero stock    Alternatives shown
  Customer selects alternative        Product is revalidated
  Alternative above original budget   Original budget remains enforced
  Customer rejects plan               Purchase stops
  Successful test payment             Backend verifies and completes purchase
  Tracking transition                 Fulfillment, audit, and notification update
  Page refresh                        Persisted state can be reloaded
  Docker startup                      Frontend and backend run as separate services

------------------------------------------------------------------------

# 🔒 Security Model

AgentCart follows a layered security model:

``` text
AI Boundary
     ↓
Backend Policy Boundary
     ↓
Human Authorization Boundary
     ↓
Payment Boundary
     ↓
Verification Boundary
     ↓
Audit Boundary
```

Core invariants:

``` text
AI recommendation ≠ authorization

AI output ≠ business-rule validation

Out-of-stock ≠ silent substitution

Alternative price ≠ automatic budget increase

Frontend payment success ≠ verified payment

Demo tracking ≠ real logistics

Demo login ≠ production authentication
```

------------------------------------------------------------------------

# 🔑 Environment Configuration

Create a local:

``` text
backend/.env
```

using `.env.example` as the template.

Expected variables:

``` env
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
GROQ_API_KEY=
```

Never commit or publish actual secret values.

Do not expose credentials in:

-   source code;
-   frontend bundles;
-   screenshots;
-   README files;
-   Git history;
-   demo recordings.

------------------------------------------------------------------------

# 🐳 Docker

Start the complete stack:

``` bash
docker compose up --build
```

Open:

``` text
Frontend:
http://localhost

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs
```

Check:

``` bash
docker compose ps
```

Stop:

``` bash
docker compose down
```

The SQLite database is persisted through the configured Docker volume
mapping.

------------------------------------------------------------------------

# 👤 Demo Identity

The hackathon UI uses a fictional demo customer:

``` text
Name:        Arjun Mehta
Customer ID: AC-DEMO-001
Phone:       +91 9876543210
Email:       arjun.mehta@demo.agentcart.ai
Account:     Demo Customer
Currency:    INR
Location:    Bengaluru, India
Payment:     Razorpay Test Mode
```

This is a frictionless hackathon identity and **not production
authentication**.

------------------------------------------------------------------------

# 🎬 Recommended Judge Demonstration

The strongest concise sequence is:

``` text
1. Login
2. Natural-language request
3. AI recommendation
4. "Why this product?"
5. Policy boundary
6. Human approval
7. Razorpay Test Mode
8. Backend payment verification
9. Order details
10. Audit trail
11. Tracking
12. Notifications
13. Out-of-stock recovery
14. Rejection
```

Primary request:

``` text
Buy wireless ANC headphones under ₹5000
```

Failure request:

``` text
Is there any TV?
```

------------------------------------------------------------------------

# 🚧 Current Scope vs Production Scope

## Current Hackathon Scope

-   Fictional demo customer
-   Controlled local catalog
-   SQLite persistence
-   Groq-based intent interpretation
-   Razorpay Test Mode
-   Human approval gate
-   Demo fulfillment tracking
-   Poll-based notification updates
-   Dockerized frontend/backend

## Production Evolution

A production deployment would additionally require:

-   strong authentication;
-   customer-level authorization and data isolation;
-   production database and backups;
-   secure secret management;
-   payment webhooks;
-   idempotency and replay protection;
-   inventory reservation and concurrency controls;
-   real logistics integration;
-   refunds/cancellations;
-   rate limiting;
-   monitoring and alerting;
-   structured logging;
-   stronger audit retention;
-   privacy and retention controls.

------------------------------------------------------------------------

# 🏆 Razorpay Track 01 Positioning

AgentCart is designed around:

``` text
Intent
  ↓
Discovery
  ↓
Recommendation
  ↓
Policy
  ↓
Approval
  ↓
Transaction
  ↓
Fulfillment
```

The project emphasizes five properties:

### Explainable

The customer can understand the recommendation.

### Bounded

The backend enforces commerce constraints.

### Gated

Human approval is required before payment.

### Auditable

Important lifecycle events are recorded.

### Recoverable

Unavailable products and rejected decisions have controlled recovery
paths.

------------------------------------------------------------------------

# 📚 Documentation

  -----------------------------------------------------------------------
  Document                            Purpose
  ----------------------------------- -----------------------------------
  `docs/architecture.md`              Technical architecture, components,
                                      data flow, APIs, and invariants

  `docs/demo-flow.md`                 Judge presentation script and
                                      demonstration checklist

  `docs/failure-handling.md`          Failure scenarios, expected
                                      behavior, and recovery paths

  `docs/safety.md`                    AI, payment, data, identity, and
                                      production security boundaries
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 📌 One-Line Summary

> **AgentCart is an explainable, policy-bounded, human-approved AI
> commerce agent that takes natural-language shopping intent through
> recommendation, validation, Razorpay test payment, order tracking,
> notifications, and an auditable transaction lifecycle.**

------------------------------------------------------------------------

## ⚠️ Hackathon Disclaimer

AgentCart is a hackathon implementation.

The current demonstration uses:

-   Razorpay Test Mode;
-   a fictional customer identity;
-   a controlled catalog;
-   simulated/controlled fulfillment tracking.

It is not presented as a production commerce or logistics system.
