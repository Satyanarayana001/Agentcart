import { useState } from "react";
import { paymentApi, purchaseApi } from "../api/client";

const RAZORPAY_SCRIPT =
  "https://checkout.razorpay.com/v1/checkout.js";

function loadRazorpayScript() {
  return new Promise((resolve) => {
    if (window.Razorpay) {
      resolve(true);
      return;
    }

    const existingScript = document.querySelector(
      `script[src="${RAZORPAY_SCRIPT}"]`
    );

    if (existingScript) {
      existingScript.addEventListener("load", () =>
        resolve(true)
      );
      existingScript.addEventListener("error", () =>
        resolve(false)
      );
      return;
    }

    const script = document.createElement("script");
    script.src = RAZORPAY_SCRIPT;
    script.async = true;

    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);

    document.body.appendChild(script);
  });
}

function PaymentGate({ plan, onPlanUpdated }) {
  const [loading, setLoading] = useState(false);
  const [paymentOrder, setPaymentOrder] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  if (!plan || plan.status !== "APPROVED") {
    return null;
  }

  async function handlePayment() {
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const scriptLoaded = await loadRazorpayScript();

      if (!scriptLoaded) {
        throw new Error(
          "Unable to load Razorpay Checkout."
        );
      }

      const order = await paymentApi.createOrder(
        plan.plan_id
      );

      setPaymentOrder(order);

      const razorpayKey =
        import.meta.env.VITE_RAZORPAY_KEY_ID;

      if (!razorpayKey) {
        throw new Error(
          "Razorpay Key ID is not configured in the frontend."
        );
      }

      const options = {
        key: razorpayKey,
        amount: Math.round(order.amount * 100),
        currency: order.currency,
        name: "AgentCart",
        description: "Agentic commerce purchase",
        order_id: order.razorpay_order_id,

        handler: async function (response) {
          try {
            setLoading(true);
            setError("");

            const verification =
              await paymentApi.verifyPayment(
                order.payment_order_id,
                {
                  razorpay_order_id:
                    response.razorpay_order_id,
                  razorpay_payment_id:
                    response.razorpay_payment_id,
                  razorpay_signature:
                    response.razorpay_signature,
                }
              );

            setSuccess(
              verification.message ||
                "Payment verified successfully."
            );

            const updatedPlan =
              await purchaseApi.getPlan(
                plan.plan_id
              );

            onPlanUpdated(updatedPlan);
          } catch (err) {
            setError(
              err.message ||
                "Payment verification failed."
            );
          } finally {
            setLoading(false);
          }
        },

        modal: {
          ondismiss: function () {
            setLoading(false);
          },
        },

        theme: {
          color: "#111111",
        },
      };

      const checkout = new window.Razorpay(options);

      checkout.on(
        "payment.failed",
        function (response) {
          setLoading(false);

          setError(
            response.error?.description ||
              "Payment failed. Please try again."
          );
        }
      );

      checkout.open();
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }

  return (
    <section className="payment-gate">
      <div>
        <div className="section-label">
          PAYMENT GATE
        </div>

        <h2>Purchase approved</h2>

        <p>
          Your purchase has been approved. Payment can now
          be completed securely through Razorpay test mode.
        </p>
      </div>

      <div className="payment-summary">
        <div>
          <span>Amount</span>
          <strong>
            ₹{Number(plan.subtotal).toLocaleString("en-IN")}
          </strong>
        </div>

        <div>
          <span>Currency</span>
          <strong>{plan.currency}</strong>
        </div>
      </div>

      {plan.status === "APPROVED" && (
        <button
          className="approve-button"
          onClick={handlePayment}
          disabled={loading}
        >
          {loading
            ? "Opening secure checkout..."
            : "Pay with Razorpay →"}
        </button>
      )}

      {paymentOrder && !success && (
        <div className="payment-created">
          <div className="payment-status">
            Payment order created
          </div>

          <p>
            Razorpay order:
            <strong>
              {paymentOrder.razorpay_order_id}
            </strong>
          </p>

          <p>
            Status:
            <strong>{paymentOrder.status}</strong>
          </p>
        </div>
      )}

      {success && (
        <div className="payment-success">
          <strong>Payment verified ✓</strong>
          <span>{success}</span>
        </div>
      )}

      {error && (
        <div className="approval-error">
          {error}
        </div>
      )}
    </section>
  );
}

export default PaymentGate;
