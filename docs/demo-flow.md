# AgentCart Demo Flow

## 1. Demo Objective

The AgentCart demo should communicate one central idea:

> **An AI agent can make commerce dramatically easier without receiving
> unrestricted authority over the customer's money.**

The presentation should demonstrate both:

1.  the intelligent path --- understanding intent and preparing a
    purchase;
2.  the controlled path --- handling failure, requiring approval,
    verifying payment, and maintaining an audit trail.

------------------------------------------------------------------------

# 2. Demo Environment

Use the final local or Docker setup.

``` text
Frontend
http://localhost

Backend
http://localhost:8000

Swagger
http://localhost:8000/docs
```

Payment mode:

``` text
Razorpay Test Mode
```

Do not display:

-   API keys;
-   `.env` files;
-   secret values;
-   private credentials.

------------------------------------------------------------------------

# 3. Demo Customer

Use the fictional demo identity configured by the application:

``` text
Name:        Arjun Mehta
Customer ID: AC-DEMO-001
Phone:       +91 9876543210
Email:       arjun.mehta@demo.agentcart.ai
Location:    Bengaluru, India
Account:     Demo Customer
Payment:     Razorpay Test Mode
```

This is a frictionless hackathon identity and is not production
authentication.

------------------------------------------------------------------------

# 4. Primary Scenario

Use:

``` text
Buy wireless ANC headphones under ₹5000
```

This demonstrates:

-   natural-language intent;
-   AI recommendation;
-   catalog validation;
-   product information;
-   budget validation;
-   human approval;
-   Razorpay Test Mode;
-   backend payment verification;
-   order creation;
-   audit trail.

------------------------------------------------------------------------

# 5. Step 1 --- Introduce AgentCart

Start at the login screen.

Say:

> AgentCart is an AI-powered commerce agent. Instead of manually
> searching through an e-commerce site, the customer can describe what
> they want. The agent understands the request and prepares a purchase,
> but payment remains behind a human approval gate.

Continue with the demo account.

------------------------------------------------------------------------

# 6. Step 2 --- Submit the Request

Enter:

``` text
Buy wireless ANC headphones under ₹5000
```

Explain:

> The customer is expressing a goal rather than selecting a specific
> SKU. AgentCart uses AI to interpret that intent against a controlled
> catalog.

------------------------------------------------------------------------

# 7. Step 3 --- Show the Recommendation

A representative catalog recommendation is:

``` text
SoundMax Pro ANC
₹4,499
In stock
```

Point out:

-   product image;
-   product details;
-   price;
-   availability;
-   requested characteristics;
-   purchase plan.

------------------------------------------------------------------------

# 8. Step 4 --- Show "Why This Product?"

Open the explanation.

Say:

> The recommendation is visible to the customer instead of being hidden
> inside the agent. This makes the AI decision understandable before
> authorization.

Connect the explanation to:

``` text
Customer request
      ↓
Product match
      ↓
Budget
```

------------------------------------------------------------------------

# 9. Step 5 --- Show the Policy Boundary

Highlight:

``` text
AI decision
     ↓
Policy check
     ↓
Your approval
     ↓
Payment
```

Say:

> This is the critical control boundary. The AI can recommend and
> prepare the purchase, but it cannot authorize the customer's payment.

------------------------------------------------------------------------

# 10. Step 6 --- Review the Purchase Plan

Point out:

-   product;
-   quantity;
-   unit price;
-   total;
-   maximum budget;
-   explanation;
-   policy result.

Representative values:

``` text
Product: SoundMax Pro ANC
Price:   ₹4,499
Budget:  ₹5,000
Result:  Within budget
```

------------------------------------------------------------------------

# 11. Step 7 --- Human Approval

Click the explicit approval action.

Say:

> This action is performed by the customer, not by the AI.

The backend changes the plan into an approved state.

Payment can now proceed.

------------------------------------------------------------------------

# 12. Step 8 --- Razorpay Test Payment

Open the Razorpay Test Mode checkout.

Complete the test payment.

Important:

-   use Test Mode;
-   do not use real payment credentials;
-   do not claim that real money was transferred.

Explain:

> The checkout response is not the final source of truth. AgentCart
> verifies the payment on the backend before completing the purchase.

------------------------------------------------------------------------

# 13. Step 9 --- Show the Completed Order

Show the resulting order.

Representative:

``` text
Amount:  ₹4,499
Status:  Completed
```

Then open order details.

Point out:

-   Order ID;
-   Plan ID;
-   amount;
-   payment status;
-   Razorpay order reference;
-   Razorpay payment reference.

------------------------------------------------------------------------

# 14. Step 10 --- Show the Audit Trail

Open the audit timeline.

Expected lifecycle:

``` text
PLAN_CREATED
POLICY_VALIDATED
PLAN_APPROVED
PAYMENT_ORDER_CREATED
PAYMENT_VERIFIED
PURCHASE_COMPLETED
```

Say:

> The system does not only remember the final result. It records the
> important state transitions that led to it.

------------------------------------------------------------------------

# 15. Step 11 --- Demonstrate Tracking

Open the tracking section.

The controlled demo lifecycle is:

``` text
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

-   current state;
-   completed states;
-   audit update;
-   notification.

Clarify:

> This is a controlled hackathon fulfillment flow, not a live logistics
> integration.

------------------------------------------------------------------------

# 16. Step 12 --- Demonstrate Notifications

Open the notification center.

Show notifications such as:

``` text
Order is being prepared
Shipped
Out for delivery
Delivered
```

Explain:

> Notifications are generated when the backend changes the fulfillment
> state.

------------------------------------------------------------------------

# 17. Step 13 --- Demonstrate an Unavailable Catalog Request

Use:

``` text
Is there any TV?
```

Because the current demo catalog does not represent TV as an available
catalog category, AgentCart should return:

``` text
CATALOG_INQUIRY
```

Expected UX:

``` text
Requested category
       ↓
Not represented in catalog
       ↓
Explain unavailability
       ↓
Show available catalog
       ↓
Customer chooses if desired
```

Important:

-   no purchase plan should be created;
-   no approval gate should appear;
-   no payment should start;
-   no unrelated product should be silently selected.

Say:

> The agent does not invent a product just to complete the workflow. It
> tells the customer that the requested category is unavailable and lets
> the customer choose something that actually exists.

------------------------------------------------------------------------

# 18. Step 14 --- Demonstrate Out-of-Stock Recovery

Use the intentionally unavailable catalog product.

Expected:

``` text
Requested Product
       ↓
Stock = 0
       ↓
Alternatives
       ↓
Customer Chooses
       ↓
Backend Revalidation
       ↓
Purchase Plan
```

Say:

> An agent should not silently substitute something the customer never
> selected.

------------------------------------------------------------------------

# 19. Step 15 --- Demonstrate Alternative Selection

Show the available alternatives.

The customer explicitly chooses one.

The backend revalidates:

``` text
Product
Stock
Quantity
Budget
```

Only a valid selection can continue.

------------------------------------------------------------------------

# 20. Step 16 --- Demonstrate Budget Preservation

Use the scenario where an alternative is above the original budget.

Example:

``` text
Original budget: ₹5000
Alternative:     ₹5799
```

Say:

> AgentCart does not silently raise the customer's budget because the
> original product became unavailable.

The original constraint remains authoritative.

------------------------------------------------------------------------

# 21. Step 17 --- Demonstrate Rejection

Create another purchase plan.

Instead of approving it, reject it.

Show:

``` text
Purchase Plan
      ↓
Customer Rejects
      ↓
Purchase Stops
```

Say:

> The customer's rejection is authoritative. The AI recommendation
> cannot override it.

------------------------------------------------------------------------

# 22. Suggested 5-Minute Presentation

## 0:00--0:30 --- Problem + Concept

> Shopping intent is increasingly conversational, but financial actions
> still need strong controls.

## 0:30--1:15 --- Natural-Language Request

Enter:

``` text
Buy wireless ANC headphones under ₹5000
```

Show the recommendation.

## 1:15--1:45 --- Explainability + Safety

Show:

``` text
Why this product?
```

and:

``` text
AI → Policy → Human Approval → Payment
```

## 1:45--2:30 --- Approval + Payment

Approve and complete the Razorpay Test Mode payment.

## 2:30--3:00 --- Order + Audit

Show order details and the audit timeline.

## 3:00--3:45 --- Tracking + Notifications

Advance tracking and show backend-driven notifications.

## 3:45--4:30 --- Failure Recovery

Demonstrate unavailable/out-of-stock handling and explicit alternative
selection.

## 4:30--5:00 --- Rejection + Close

Reject another plan and deliver the closing statement.

------------------------------------------------------------------------

# 23. Recommended Closing Statement

> AgentCart makes AI commerce actionable without making it uncontrolled.
> The agent understands the customer's intent, recommends and prepares
> the purchase, the backend enforces the policies, the customer approves
> the financial action, payment is verified, and the lifecycle remains
> auditable.

------------------------------------------------------------------------

# 24. Demo Checklist

## Application

-   [ ] Frontend loads
-   [ ] Backend is healthy
-   [ ] Login works
-   [ ] Catalog loads

## AI

-   [ ] Natural-language request works
-   [ ] Recommendation appears
-   [ ] Explanation appears
-   [ ] Missing catalog category returns `CATALOG_INQUIRY`

## Policy

-   [ ] Budget validation works
-   [ ] Stock validation works
-   [ ] Quantity validation works
-   [ ] Approval gate works
-   [ ] Rejection stops progression

## Payment

-   [ ] Razorpay Test Mode works
-   [ ] Payment verification works
-   [ ] Purchase completion works

## Post-Purchase

-   [ ] Order history works
-   [ ] Order details work
-   [ ] Audit timeline works
-   [ ] Tracking works
-   [ ] Notifications work

## Failure Handling

-   [ ] Missing catalog request works
-   [ ] Out-of-stock recovery works
-   [ ] Alternative selection works
-   [ ] Original budget remains enforced
-   [ ] Rejection works

## Docker

-   [ ] `docker compose up --build` works
-   [ ] Frontend available at `http://localhost`
-   [ ] Backend available at `http://localhost:8000`
-   [ ] Swagger available at `http://localhost:8000/docs`

## Demo Hygiene

-   [ ] No API secrets visible
-   [ ] No `.env` displayed
-   [ ] Test Mode clearly identified
-   [ ] Tracking described as controlled/simulated
