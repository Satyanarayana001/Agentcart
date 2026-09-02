import { useState } from "react";
import { purchaseApi } from "../api/client";

function ApprovalGate({ plan, onPlanUpdated }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!plan || plan.status !== "AWAITING_APPROVAL") {
    return null;
  }

  async function handleAction(action) {
    setLoading(true);
    setError("");

    try {
      const updatedPlan =
        action === "approve"
          ? await purchaseApi.approvePlan(plan.plan_id)
          : await purchaseApi.rejectPlan(plan.plan_id);

      onPlanUpdated(updatedPlan);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="approval-gate">
      <div>
        <div className="section-label">
          HUMAN APPROVAL GATE
        </div>

        <h2>Your approval is required</h2>

        <p>
          The AI can recommend and prepare the purchase,
          but it cannot authorize the transaction.
        </p>
      </div>

      <div className="approval-actions">
        <button
          className="reject-button"
          onClick={() => handleAction("reject")}
          disabled={loading}
        >
          {loading ? "Processing..." : "Reject"}
        </button>

        <button
          className="approve-button"
          onClick={() => handleAction("approve")}
          disabled={loading}
        >
          {loading ? "Processing..." : "Approve purchase →"}
        </button>
      </div>

      {error && (
        <div className="approval-error">
          {error}
        </div>
      )}
    </section>
  );
}

export default ApprovalGate;
