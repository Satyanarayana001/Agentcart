# 🛒 AgentCart

## Explainable AI-Powered Agentic Commerce

> **AgentCart turns a natural-language shopping request into a policy-checked, human-approved, auditable transaction.**

AgentCart is an **AI-powered agentic commerce platform** built for the Razorpay AI Buildathon — **Track 01: AI Growth & Agentic Commerce**.

The idea is simple:

A customer should not need to navigate a traditional e-commerce workflow just to explain what they want.

Instead, they can tell an AI agent:

```text
Buy wireless ANC headphones under ₹5000
```

AgentCart understands the request, identifies a suitable product from its catalog, checks availability and purchasing constraints, explains the recommendation, creates a purchase plan, and waits for the customer to explicitly approve it.

Only after approval can the payment flow begin.

The central design principle is:

```text
┌──────────────────┐
│   Customer Need  │
└────────┬─────────┘
         ↓
┌──────────────────┐
│    AI Agent      │
│ Understand +     │
│ Recommend        │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Policy Engine   │
│ Budget + Stock + │
│ Quantity + State │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Human Approval   │
│ Explicit consent │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Razorpay Payment │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Payment Verify   │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Order + Audit    │
└────────┬─────────┘
         ↓
┌──────────────────┐
│ Tracking +       │
│ Notifications    │
└──────────────────┘
```

The important distinction is:

> **The AI can recommend and prepare. It does not get unrestricted authority to move money.**

---

# 🎯 The Problem

Traditional e-commerce is optimized around screens, filters, search boxes, and checkout forms.

That works well for deterministic shopping, but it creates friction when the customer has a goal rather than a specific SKU.

For example:

```text
"I need wireless ANC headphones,
under ₹5000, preferably with good battery life."
```

A conventional flow requires the customer to:

1. Search for headphones.
2. Apply a wireless filter.
3. Apply an ANC filter.
4. Set a price limit.
5. Compare products.
6. Check stock.
7. Select a product.
8. Start checkout.
9. Pay.

An agentic commerce system can compress the **discovery and decision-support** portion of this process into a conversation.

However, giving an AI unrestricted purchasing authority introduces a different problem:

### What happens if the AI:

- chooses an unavailable product?
- selects a product above the customer's budget?
- silently substitutes a product?
- misinterprets quantity?
- makes an incorrect recommendation?
- attempts to proceed without customer approval?
- receives a payment response that has not been verified?

AgentCart is designed around these exact boundaries.

---

# 💡 The AgentCart Approach

AgentCart separates **intelligence** from **authority**.

The AI is responsible for understanding the customer's intent and helping construct a purchase decision.

The backend is responsible for enforcing business rules.

The customer remains responsible for approving the financial action.

This produces three distinct layers:

### 1. Intelligence

The AI understands:

```text
What does the customer want?
What product best matches the request?
Why is that product relevant?
```

### 2. Control

The backend determines:

```text
Does the product exist?
Is it in stock?
Is the quantity valid?
Is it within budget?
Is the purchase plan in a valid state?
```

### 3. Authorization

The customer determines:

```text
Do I actually want to purchase this?
```

That separation is the foundation of AgentCart.

---

# ✨ What AgentCart Does

## 1. Conversational Product Discovery

The customer interacts with AgentCart using natural language.

Example:

```text
Buy wireless ANC headphones under ₹5000
```

The request is processed by the AI layer and converted into structured purchase intent.

The agent then works with the product catalog to identify an appropriate product.

---

## 2. AI-Powered Product Recommendation

AgentCart does not simply return a search result.

It creates a purchase recommendation.

The recommendation takes into account:

- Product category
- Requested features
- Price
- Availability
- Quantity
- Customer budget

The selected product is displayed to the customer before payment.

---

## 3. Explainable AI Decision

The system provides a visible:

```text
Why this product?
```

explanation.

For example:

```text
Selected because it matches the requested ANC and wireless
requirements while remaining within the ₹5000 budget.
```

The customer can therefore understand the recommendation before approving it.

---

# 🛡️ 4. Policy-Gated Purchasing

The AI's recommendation is **not** automatically considered valid.

The backend performs policy validation.

Conceptually:

```text
AI Recommendation
       ↓
Product Validation
       ↓
Stock Validation
       ↓
Quantity Validation
       ↓
Budget Validation
       ↓
Purchase Plan
```

This means business rules remain enforceable even if the AI produces an unexpected response.

---

# 👤 5. Human Approval Gate

This is one of the most important parts of AgentCart.

The system intentionally separates:

```text
"AI recommends this"
```

from:

```text
"I approve this purchase"
```

The customer must explicitly approve the purchase plan.

Only then can the payment order be created.

This prevents the AI recommendation layer from becoming an unrestricted payment authority.

---

# 🔄 6. Intelligent Out-of-Stock Recovery

AgentCart also demonstrates how an agentic commerce system can fail gracefully.

One catalog product is intentionally configured as unavailable for testing.

When the requested product has:

```text
Stock = 0
```

AgentCart does not silently purchase another product.

Instead:

```text
Requested product
       ↓
Out of stock
       ↓
Search available catalog
       ↓
Rank alternatives
       ↓
Show alternatives
       ↓
Customer chooses
       ↓
Validate selected alternative
       ↓
Continue only if valid
```

The customer remains in control of substitution.

### Budget is preserved

If the original request is:

```text
Maximum budget = ₹5000
```

and an alternative costs:

```text
₹5799
```

AgentCart does **not** silently increase the budget.

The original constraint remains authoritative.

---

# 💳 7. Razorpay Payment Integration

AgentCart integrates Razorpay for the transaction stage.

The current implementation uses **Razorpay Test Mode**.

Payment only becomes available after:

```text
Purchase Plan
      ↓
Policy Validation
      ↓
Human Approval
```

The conceptual lifecycle is:

```text
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

The system does not treat a frontend payment response as sufficient proof of successful payment.

---

# 🔐 8. Backend Payment Verification

Payment verification happens at the backend boundary.

The frontend provides the payment identifiers received from the checkout process.

The backend verifies the payment before treating the transaction as completed.

This is important because:

```text
Frontend says "success"
```

is not equivalent to:

```text
Backend has verified payment
```

Only the verified state can move the transaction into the completed purchase lifecycle.

---

# 📦 9. Order Management

After a successful purchase, AgentCart creates a persistent order record.

Customers can access:

### Order History

A list of previous transactions containing information such as:

- Order ID
- Product
- Quantity
- Amount
- Currency
- Status
- Creation time

### Order Details

A dedicated order view containing:

- Purchase summary
- AI recommendation explanation
- Security boundary
- Transaction details
- Razorpay references
- Audit timeline
- Delivery tracking

---

# 🚚 10. Order Tracking

AgentCart includes a post-purchase fulfillment lifecycle.

```text
PROCESSING
    ↓
SHIPPED
    ↓
OUT_FOR_DELIVERY
    ↓
DELIVERED
```

The interface presents these states as a customer-friendly timeline:

```text
Preparing
    ↓
Shipped
    ↓
Out for delivery
    ↓
Delivered
```

The tracking lifecycle is a **controlled hackathon demo flow**.

It is not presented as a real logistics-provider integration.

---

# 🔔 11. In-App Notifications

Order state changes generate notifications.

For example:

```text
Order is being prepared
```

then:

```text
Shipped
```

then:

```text
Out for delivery
```

then:

```text
Delivered
```

Notifications are persisted in the database and can be marked as read individually or all at once.

The frontend periodically checks the unread count so that the navigation header can surface new activity.

---

# 🧾 12. Audit Trail

Agentic commerce needs more than a final:

```text
Payment successful
```

It needs an understandable history of how the transaction reached that state.

AgentCart therefore records significant lifecycle events.

A successful transaction can contain:

```text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Fulfillment transitions can additionally create events such as:

```text
FULFILLMENT_PROCESSING
FULFILLMENT_SHIPPED
FULFILLMENT_OUT_FOR_DELIVERY
FULFILLMENT_DELIVERED
```

This provides an auditable sequence of important state changes.

---

# 🧠 System Architecture

AgentCart uses a React frontend and FastAPI backend with a service-oriented internal structure.

```text
                         CUSTOMER
                            │
                            ▼
                ┌──────────────────────┐
                │    React Frontend    │
                │      + Vite          │
                ├──────────────────────┤
                │ Commerce             │
                │ Product Discovery    │
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
                │ Audit API             │
                └──────────┬───────────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             ▼             ▼              ▼
        ┌─────────┐   ┌─────────┐   ┌───────────┐
        │ SQLite  │   │  Groq   │   │ Razorpay  │
        │         │   │   AI    │   │ Test Mode │
        └─────────┘   └─────────┘   └───────────┘
```

---

# 🏗️ Technology Stack

## Frontend

| Technology | Purpose |
|---|---|
| React | User interface |
| Vite | Frontend build tooling |
| JavaScript | Application logic |
| CSS | Product interface and responsive styling |
| Fetch API | Backend communication |

## Backend

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| Pydantic | Request/response validation |
| SQLite | Local persistence |

## AI

| Technology | Purpose |
|---|---|
| Groq | LLM inference |
| `openai/gpt-oss-20b` | Agent reasoning / structured intent |

## Payments

| Technology | Purpose |
|---|---|
| Razorpay | Payment order + checkout + verification |
| Razorpay Test Mode | Safe hackathon transactions |

## Infrastructure

| Technology | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |
| Nginx | Production frontend serving |

---

# 📁 Project Structure

```text
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
│   │   │   │   └── products.json
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── seed.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── notification.py
│   │   │   ├── order.py
│   │   │   └── tracking.py
│   │   │
│   │   └── services/
│   │       ├── agent_service.py
│   │       ├── groq_adapter.py
│   │       ├── notification_service.py
│   │       ├── order_service.py
│   │       └── tracking_service.py
│   │
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
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
│   │   │
│   │   ├── pages/
│   │   │   ├── CommercePage.jsx
│   │   │   ├── OrderDetailsPage.jsx
│   │   │   └── OrdersPage.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── Dockerfile
│   └── nginx.conf
│
├── docs/
│   ├── architecture.md
│   ├── demoflow.md
│   ├── failure-handling.md
│   └── safety.md
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 🔄 End-to-End Purchase Flow

The complete normal transaction can be represented as:

```text
1. Demo Login
       ↓
2. Customer describes requirement
       ↓
3. AI interprets request
       ↓
4. Product is selected
       ↓
5. Backend validates product
       ↓
6. Backend validates stock
       ↓
7. Backend validates budget
       ↓
8. Purchase plan created
       ↓
9. Customer reviews explanation
       ↓
10. Customer approves
       ↓
11. Razorpay order created
       ↓
12. Razorpay Test Checkout
       ↓
13. Backend verifies payment
       ↓
14. Purchase completed
       ↓
15. Order available in history
       ↓
16. Fulfillment begins
       ↓
17. Tracking updates
       ↓
18. Notifications generated
       ↓
19. Audit trail updated
```

---

# 🗃️ Data Model

AgentCart currently maintains database entities for the major parts of the transaction lifecycle.

```text
Product
   │
   │ referenced by
   ▼
Purchase Item
   │
   ▼
Purchase Plan
   │
   ▼
Payment Order
   │
   ▼
Fulfillment
```

Additional records:

```text
Purchase Plan ───────► Audit Events
Payment Order ───────► Notifications
```

The major database entities are:

- `products`
- `purchase_plans`
- `purchase_items`
- `payment_orders`
- `audit_events`
- `fulfillments`
- `notifications`

---

# 🧩 API Surface

The backend exposes separate API areas for each responsibility.

## Agent

```text
POST /api/agent/purchase
POST /api/agent/select-product
```

Used for natural-language purchase requests and explicit alternative/product selection.

## Catalog

```text
GET /api/catalog/products
GET /api/catalog/products/{product_id}
GET /api/catalog/search
```

Used for product discovery.

## Purchase Plans

```text
GET  /api/purchase/plans/{plan_id}
POST /api/purchase/plans/{plan_id}/approve
POST /api/purchase/plans/{plan_id}/reject
```

Used for purchase-plan inspection and human authorization.

## Payments

```text
POST /api/payment/plans/{plan_id}/orders
GET  /api/payment/orders/{payment_order_id}
POST /api/payment/orders/{payment_order_id}/verify
```

Used for payment-order creation and verification.

## Orders

```text
GET /api/orders/
GET /api/orders/{order_id}
```

Used for order history and order details.

## Tracking

```text
GET  /api/orders/{order_id}/tracking
POST /api/orders/{order_id}/tracking/advance
```

Used for the demo fulfillment lifecycle.

## Notifications

```text
GET  /api/notifications/
GET  /api/notifications/unread-count
POST /api/notifications/{notification_id}/read
POST /api/notifications/read-all
```

## Audit

```text
GET /api/audit/
GET /api/audit/plans/{plan_id}
```

---

# 🧪 Reliability and Failure Scenarios

AgentCart was built around the idea that a strong agentic-commerce demo should demonstrate failure handling rather than only the happy path.

The verified local scenarios include:

### Normal Purchase

```text
Request
→ Recommendation
→ Policy Validation
→ Approval
→ Payment
→ Verification
→ Completion
```

### Out-of-Stock Recovery

```text
Unavailable Product
→ Alternatives
→ Customer Selection
→ Revalidation
```

### Purchase Rejection

```text
Purchase Plan
→ Customer Rejects
→ Purchase Stops
```

### Tracking Lifecycle

```text
Preparing
→ Shipped
→ Out for Delivery
→ Delivered
```

### Refresh Persistence

Order information, audit history, and tracking state can be reloaded from the backend after refreshing the application.

---

# 🔒 Security Model

AgentCart follows a layered security model.

## AI Boundary

The model is treated as an intelligent input/decision layer, not as a trusted business-rule engine.

## Backend Boundary

The backend validates:

- Product
- Quantity
- Stock
- Budget
- Purchase state
- Payment state

## Human Boundary

The customer explicitly approves the transaction.

## Payment Boundary

Payment is verified on the backend before the purchase is considered completed.

## Secret Boundary

Sensitive credentials are provided through environment variables.

Secrets must never be hardcoded or committed.

The repository ignores local `.env` files.

---

# 🔑 Environment Configuration

Create:

```text
backend/.env
```

using `.env.example` as a template.

Required variables:

```env
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
GROQ_API_KEY=
```

### Important

Never commit:

```text
backend/.env
```

Never expose:

```text
RAZORPAY_KEY_SECRET
GROQ_API_KEY
```

in frontend code, screenshots, README files, GitHub commits, or demo recordings.

---

# 🐳 Docker

AgentCart is containerized as two services:

```text
agentcart-frontend
        +
agentcart-backend
```

The frontend is built using Node/Vite and served by Nginx.

The backend runs FastAPI with Uvicorn.

Start the stack:

```bash
docker compose up --build
```

Open:

```text
http://localhost
```

Backend:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

Stop:

```bash
docker compose down
```

---

# 👤 Demo Identity

The current hackathon UI uses a fictional demo customer:

```text
Name:
Arjun Mehta

Customer ID:
AC-DEMO-001

Phone:
+91 9876543210

Email:
arjun.mehta@demo.agentcart.ai

Account:
Demo Customer

Currency:
INR

Location:
Bengaluru, India

Payment:
Razorpay Test Mode
```

The login is intentionally designed as a frictionless hackathon demo and is **not production authentication**.

---

# 🎬 Recommended Judge Demonstration

A concise demonstration should follow this sequence:

```text
1. Login
2. Enter natural-language purchase request
3. Show AI recommendation
4. Show "Why this product?"
5. Show policy validation
6. Show security boundary
7. Approve purchase
8. Complete Razorpay Test Mode payment
9. Show successful audit trail
10. Open order details
11. Show tracking
12. Advance tracking
13. Show notification
14. Demonstrate out-of-stock recovery
15. Demonstrate rejection
```

Recommended request:

```text
Buy wireless ANC headphones under ₹5000
```

The detailed demo script is available in:

```text
docs/demoflow.md
```

---

# 📚 Documentation

AgentCart includes dedicated documentation for the most important system concerns.

### Architecture

```text
docs/architecture.md
```

Explains the technical architecture, services, data flow, APIs, and system boundaries.

### Demo Flow

```text
docs/demoflow.md
```

Contains the recommended judge presentation and demonstration sequence.

### Failure Handling

```text
docs/failure-handling.md
```

Documents out-of-stock handling, rejection, payment failures, invalid states, and tracking failures.

### Safety

```text
docs/safety.md
```

Explains AI boundaries, human approval, payment security, secret handling, and production considerations.

---

# 🏆 Razorpay AI Buildathon Positioning

AgentCart is designed for:

## Track 01 — AI Growth & Agentic Commerce

The project explores a future where AI agents can participate directly in commerce.

Instead of treating the AI as a chatbot sitting beside an existing shopping experience, AgentCart makes the agent part of the purchasing workflow:

```text
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

The project specifically focuses on the challenge of making this workflow:

### Explainable

The customer can understand why a product was recommended.

### Bounded

The backend enforces budget, stock, quantity, and lifecycle constraints.

### Gated

Human approval is required before payment.

### Auditable

Important transaction state transitions are recorded.

### Recoverable

The system demonstrates graceful handling of unavailable products and rejected decisions.

---

# 🚧 Current Scope vs Production Scope

AgentCart is a hackathon implementation designed to demonstrate the core agentic-commerce architecture.

Some components are intentionally simplified.

## Current Hackathon Implementation

- Fictional demo customer
- Local catalog
- SQLite persistence
- Razorpay Test Mode
- Demo fulfillment tracking
- Controlled tracking advancement
- Poll-based unread notification updates

## Production Evolution

A production deployment would additionally require:

- Strong authentication
- Authorization and customer isolation
- Production database
- Persistent cloud storage
- Secure secret management
- Payment webhooks
- Idempotency controls
- Inventory reservation
- Real logistics integration
- Rate limiting
- Monitoring and alerting
- Structured logging
- Abuse prevention
- Stronger audit retention
- Production-grade session management

These are deliberately outside the current hackathon scope.

---

# 📈 Future Evolution

The architecture can be extended toward a more complete agentic-commerce platform.

Potential next steps include:

```text
Multi-merchant catalog
        ↓
Agent-readable product feeds
        ↓
Merchant-specific policies
        ↓
Personalized preferences
        ↓
Upsell / cross-sell intelligence
        ↓
Campaign-aware recommendations
        ↓
Real fulfillment integrations
        ↓
Production-grade agent authorization
```

The existing separation between:

```text
AI
Policy
Human Approval
Payment
```

provides the foundation for those extensions.

---

# 🧭 Design Principles

AgentCart follows five core principles.

## 1. AI should assist, not silently act

The customer should understand what the agent intends to purchase.

## 2. Business rules belong in the backend

AI output is not a replacement for deterministic policy enforcement.

## 3. Money actions need an explicit boundary

Payment should require a clear authorization step.

## 4. Failure should be visible and recoverable

When something cannot proceed, the system should explain why and provide a valid next step.

## 5. Important actions should be auditable

A transaction should have a traceable lifecycle rather than only a final success state.

---

# 📊 Example Successful Transaction

A representative successful purchase looks like:

```text
Customer Request
────────────────────────────────────
Buy wireless ANC headphones under ₹5000

AI Recommendation
────────────────────────────────────
SoundMax Pro ANC
₹4,499
In stock

Policy
────────────────────────────────────
Budget: ₹5,000
Price:  ₹4,499
Stock:  Available
Result: PASS

Human Approval
────────────────────────────────────
Approved

Payment
────────────────────────────────────
Razorpay Test Mode
Result: VERIFIED

Purchase
────────────────────────────────────
Status: COMPLETED

Audit
────────────────────────────────────
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED

Fulfillment
────────────────────────────────────
PROCESSING
→ SHIPPED
→ OUT_FOR_DELIVERY
→ DELIVERED
```

---

# ⚠️ Demo and Security Disclaimer

AgentCart is a hackathon project.

The current implementation uses:

- Razorpay Test Mode
- A fictional demo customer
- A local/demo catalog
- Demo fulfillment tracking

No real customer identity or real-world delivery operation is represented by the demo.

Never commit or publish actual API secrets.

---

# 🧑‍💻 Development Status

The core application flow has been implemented and locally reliability-tested.

Verified scenarios:

- ✅ Normal purchase success
- ✅ AI recommendation and explanation
- ✅ Policy validation
- ✅ Human approval gate
- ✅ Razorpay Test Mode payment
- ✅ Payment verification
- ✅ Order history
- ✅ Order details
- ✅ Audit trail
- ✅ Out-of-stock recovery
- ✅ Customer-selected alternatives
- ✅ Purchase rejection
- ✅ Tracking lifecycle
- ✅ In-app notifications
- ✅ Refresh persistence
- ✅ Dockerized frontend/backend

---

# 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>

# Enter the project
cd agentcart

# Configure backend secrets
# Create backend/.env using .env.example

# Start the application
docker compose up --build
```

Then open:

```text
http://localhost
```

API documentation:

```text
http://localhost:8000/docs
```

---

# 📌 One-Line Summary

> **AgentCart is an explainable, policy-bounded, human-approved AI commerce agent that takes a natural-language shopping request from intent to Razorpay payment, order tracking, notifications, and an auditable transaction lifecycle.**

---

## License

This project was created as a hackathon project.
