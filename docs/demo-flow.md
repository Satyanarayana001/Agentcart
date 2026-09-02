# AgentCart Demo Flow

## 1. Demo Objective

The AgentCart demo should communicate one central idea:

> **An AI agent can make commerce dramatically easier without receiving unrestricted authority over the customer's money.**

The demonstration should therefore show both:

1. The intelligent path — understanding a request and completing a purchase.
2. The controlled path — handling failure, requiring approval, and maintaining an audit trail.

---

# 2. Demo Environment

Start the application using the final local/Docker setup.

Expected endpoints:

```text
Frontend
http://localhost

Backend
http://localhost:8000

Swagger
http://localhost:8000/docs
```

Use Razorpay Test Mode.

Do not display secret environment variables during the demo.

---

# 3. Demo Customer

Use the fictional demo customer:

```text
Name:
Arjun Mehta

Customer ID:
AC-DEMO-001

Phone:
+91 9876543210

Email:
arjun.mehta@demo.agentcart.ai

Location:
Bengaluru, India

Account:
Demo Customer

Payment:
Razorpay Test Mode
```

The login exists to provide a clean hackathon demonstration and is not production authentication.

---

# 4. Recommended Primary Scenario

Use the following request:

```text
Buy wireless ANC headphones under ₹5000
```

This scenario demonstrates:

- Natural-language intent
- AI recommendation
- Product information
- Budget validation
- Human approval
- Razorpay payment
- Payment verification
- Order creation
- Audit trail

---

# 5. Demo Script

## Step 1 — Introduce AgentCart

Start on the login screen.

Say:

> AgentCart is an AI-powered commerce agent. Instead of manually searching through an e-commerce site, the customer can describe what they want. The agent finds and prepares a purchase, but payment is always behind a human approval gate.

Continue using the demo account.

---

## Step 2 — Submit a Natural-Language Request

Enter:

```text
Buy wireless ANC headphones under ₹5000
```

Submit the request.

Explain:

> The customer is expressing a goal, not selecting a specific SKU. AgentCart uses AI to understand the intent and identify a suitable catalog product.

---

## Step 3 — Show the Recommendation

Show the selected product.

A representative product is:

```text
SoundMax Pro ANC
₹4,499
In stock
```

Point out:

- Product image/details
- Price
- Availability
- Requested features
- Purchase plan

---

# 6. Show "Why This Product?"

Open the explanation.

Explain:

> The recommendation is not hidden inside the agent. The customer can see why the product matches the request.

The explanation should connect the recommendation to the customer's requirements and budget.

---

# 7. Show the Policy Boundary

Highlight:

```text
AI decision
     ↓
Policy check
     ↓
Your approval
     ↓
Payment
```

Say:

> This is the critical control boundary. The AI can recommend the product, but it cannot authorize the customer's payment.

---

# 8. Show the Purchase Plan

Point out:

- Product
- Quantity
- Unit price
- Total
- Maximum budget
- Explanation
- Policy status

For the example:

```text
Product:
SoundMax Pro ANC

Price:
₹4,499

Budget:
₹5,000

Result:
Within budget
```

---

# 9. Human Approval

Click the explicit approval action.

Explain:

> This action is performed by the customer, not by the AI.

The backend changes the plan into an approved state.

The payment flow is now allowed to continue.

---

# 10. Razorpay Test Payment

Proceed to the Razorpay Test Mode checkout.

Complete the test payment.

Important:

- Use Test Mode.
- Do not use real payment credentials.
- Do not claim that real money was transferred.

After checkout, the backend verifies the payment.

---

# 11. Show the Successful Purchase

After successful verification, show the order.

A representative transaction may be:

```text
Amount:
₹4,499

Status:
Completed
```

Then open the order details.

---

# 12. Show the Audit Trail

Open the audit timeline.

A successful transaction should show events similar to:

```text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Say:

> The system doesn't only remember the final result. It records the important decisions and state transitions that led to it.

This is especially relevant for agentic commerce.

---

# 13. Show Order Details

Point out:

```text
Order ID
Plan ID
Amount
Payment status
Razorpay Order ID
Razorpay Payment ID
```

Then show the AI explanation and security boundary again.

---

# 14. Demonstrate Tracking

Open the tracking section.

The demo lifecycle is:

```text
Preparing
    ↓
Shipped
    ↓
Out for delivery
    ↓
Delivered
```

Advance the tracking state.

After each transition, show:

- Current tracking state
- Completed states
- Audit update
- Notification

---

# 15. Demonstrate Notifications

Open the notification center.

Show messages such as:

```text
Order is being prepared
Shipped
Out for delivery
Delivered
```

Explain:

> Notifications are generated when the backend changes fulfillment state.

---

# 16. Demonstrate Out-of-Stock Recovery

This is the recommended failure demonstration.

Use the intentionally unavailable catalog product.

The system should identify that:

```text
Requested product
=
Out of stock
```

Instead of silently choosing another product, AgentCart displays available alternatives.

Explain:

> An agent should not silently substitute something the customer did not choose.

---

# 17. Customer Selects an Alternative

Show the alternatives.

The customer explicitly chooses one.

The system then revalidates:

```text
Product
Stock
Quantity
Budget
```

Only a valid alternative can continue.

---

# 18. Demonstrate Budget Preservation

Use the scenario where an alternative is above the original budget.

Example:

```text
Original budget:
₹5000

Alternative:
₹5799
```

Explain:

> AgentCart does not silently raise the customer's budget just because the AI found another product.

The backend retains the original constraint.

---

# 19. Demonstrate Rejection

Create another purchase plan.

Instead of approving it, reject the plan.

Show:

```text
Purchase Plan
      ↓
Customer Rejects
      ↓
Purchase Stops
```

Explain:

> The customer's rejection is authoritative. The AI recommendation cannot override it.

---

# 20. Suggested 5-Minute Presentation

## 0:00–0:30

Problem + concept.

> Shopping intent is often conversational, but payment must remain controlled.

## 0:30–1:15

Natural-language request.

```text
Buy wireless ANC headphones under ₹5000
```

Show recommendation.

## 1:15–1:45

Show:

```text
Why this product?
```

and the security boundary.

## 1:45–2:30

Approve and complete Razorpay Test Mode payment.

## 2:30–3:00

Show order details and audit trail.

## 3:00–3:45

Show tracking and notifications.

## 3:45–4:30

Demonstrate out-of-stock recovery.

## 4:30–5:00

Demonstrate rejection and close.

---

# 21. Recommended Closing Statement

Finish with:

> AgentCart makes AI commerce actionable without making it uncontrolled. The agent understands the customer's intent, recommends and prepares the purchase, the backend enforces the policies, the customer approves the financial action, and the complete lifecycle remains auditable.

---

# 22. Demo Checklist

Before the final presentation:

### Application

- [ ] Frontend loads
- [ ] Backend is healthy
- [ ] Login works
- [ ] Catalog loads

### AI

- [ ] Natural-language request works
- [ ] Recommendation appears
- [ ] Explanation appears

### Policy

- [ ] Budget validation works
- [ ] Stock validation works
- [ ] Quantity validation works
- [ ] Approval gate works

### Payment

- [ ] Razorpay Test Mode works
- [ ] Payment verification works
- [ ] Purchase completion works

### Post-purchase

- [ ] Order history works
- [ ] Order details work
- [ ] Audit timeline works
- [ ] Tracking works
- [ ] Notifications work

### Failure handling

- [ ] Out-of-stock recovery works
- [ ] Alternative selection works
- [ ] Rejection works
- [ ] Original budget remains enforced

### Demo hygiene

- [ ] No API secrets visible
- [ ] No `.env` displayed
- [ ] Test Mode clearly identified
- [ ] Demo tracking described as simulated
