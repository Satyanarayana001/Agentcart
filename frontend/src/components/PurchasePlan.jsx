function PurchasePlan({ plan }) {
  if (!plan) {
    return null;
  }

  const isBlocked = plan.status === "BLOCKED";
  const isAwaitingApproval =
    plan.status === "AWAITING_APPROVAL";
  const isCompleted = plan.status === "COMPLETED";

  const description = isCompleted
    ? "Payment was verified and the purchase was completed."
    : isBlocked
      ? "The agent prepared this plan, but the purchase was blocked by policy."
      : "The agent prepared this plan. No payment has been made.";

  return (
    <section className="purchase-plan">
      <div className="section-label">
        PURCHASE PLAN
      </div>

      <div className="plan-header">
        <div>
          <h2>Purchase details</h2>
          <p>{description}</p>
        </div>

        <span
          className={`status-badge status-${plan.status.toLowerCase()}`}
        >
          {plan.status.replaceAll("_", " ")}
        </span>
      </div>

      <div className="product-list">
        {plan.items.map((item) => (
          <div
            className="product-line"
            key={item.product_id}
          >
            <div>
              <strong>{item.name}</strong>

              <span>
                {item.quantity} {"\u00D7"} {"\u20B9"}
                {item.unit_price.toLocaleString("en-IN")}
              </span>
            </div>

            <strong>
              {"\u20B9"}
              {item.total_price.toLocaleString("en-IN")}
            </strong>
          </div>
        ))}
      </div>

      <div className="plan-summary">
        <div>
          <span>Subtotal</span>
          <strong>
            {"\u20B9"}
            {plan.subtotal.toLocaleString("en-IN")}
          </strong>
        </div>

        <div>
          <span>Maximum budget</span>
          <strong>
            {"\u20B9"}
            {plan.max_budget.toLocaleString("en-IN")}
          </strong>
        </div>

        <div>
          <span>Currency</span>
          <strong>{plan.currency}</strong>
        </div>
      </div>

      <div
        className={`policy-result ${
          isBlocked
            ? "policy-blocked"
            : "policy-passed"
        }`}
      >
        <span className="policy-icon">
          {isBlocked ? "!" : "\u2713"}
        </span>

        <div>
          <strong>
            {isBlocked
              ? "Purchase blocked"
              : "Policy checks passed"}
          </strong>

          <p>{plan.explanation}</p>
        </div>
      </div>

      {isAwaitingApproval && (
        <div className="plan-next-step">
          <span>Human approval required</span>

          <p>
            AgentCart will not create a payment order until
            you explicitly approve this purchase.
          </p>
        </div>
      )}

      {isCompleted && (
        <div className="plan-next-step">
          <span>Purchase completed</span>

          <p>
            Payment was successfully verified through
            Razorpay test mode.
          </p>
        </div>
      )}
    </section>
  );
}

export default PurchasePlan;
