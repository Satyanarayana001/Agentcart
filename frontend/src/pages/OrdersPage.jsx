import { useEffect, useState } from "react";
import { ordersApi } from "../api/client";

function OrdersPage({ onBack, onOpenOrder }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  // =========================================================
  // LOAD ORDERS
  // =========================================================

  useEffect(() => {
    async function loadOrders() {
      setLoading(true);
      setError("");

      try {
        const data = await ordersApi.getOrders();

        setOrders(data || []);

      } catch (err) {
        setError(
          err.message ||
            "Unable to load your orders."
        );
      } finally {
        setLoading(false);
      }
    }

    loadOrders();
  }, []);


  // =========================================================
  // FORMAT DATE
  // =========================================================

  function formatDate(dateString) {
    if (!dateString) {
      return "Unknown date";
    }

    const date = new Date(dateString);

    return date.toLocaleString(
      "en-IN",
      {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }
    );
  }


  // =========================================================
  // STATUS LABEL
  // =========================================================

  function getStatusLabel(status) {
    switch (status) {
      case "PAYMENT_VERIFIED":
        return "Payment verified";

      case "ORDER_CREATED":
        return "Payment pending";

      case "PAYMENT_FAILED":
        return "Payment failed";

      default:
        return status
          ?.replaceAll("_", " ")
          ?.toLowerCase()
          ?.replace(
            /\b\w/g,
            (char) => char.toUpperCase()
          ) || "Unknown";
    }
  }


  // =========================================================
  // STATUS CLASS
  // =========================================================

  function getStatusClass(status) {
    switch (status) {
      case "PAYMENT_VERIFIED":
        return "order-status-success";

      case "PAYMENT_FAILED":
        return "order-status-failed";

      case "ORDER_CREATED":
        return "order-status-pending";

      default:
        return "order-status-default";
    }
  }


  // =========================================================
  // RENDER
  // =========================================================

  return (
    <main className="orders-page">

      {/* =====================================================
          NAVIGATION
      ===================================================== */}

      <nav className="navbar">

        <div className="brand">
          <span className="brand-mark">
            A
          </span>

          <span>
            AgentCart
          </span>
        </div>


        <button
          type="button"
          className="orders-back-button"
          onClick={onBack}
        >
          ← Back to shopping
        </button>

      </nav>


      {/* =====================================================
          HEADER
      ===================================================== */}

      <section className="orders-header">

        <div className="section-label">
          ORDER HISTORY
        </div>

        <h1>
          Your orders
        </h1>

        <p>
          Review purchases created through
          AgentCart and track their payment status.
        </p>

      </section>


      {/* =====================================================
          LOADING
      ===================================================== */}

      {loading && (
        <section className="orders-state">

          <div className="orders-loading-indicator">
            Loading orders...
          </div>

        </section>
      )}


      {/* =====================================================
          ERROR
      ===================================================== */}

      {!loading && error && (
        <section className="orders-state">

          <div className="orders-error">

            <strong>
              Unable to load orders
            </strong>

            <span>
              {error}
            </span>

          </div>

        </section>
      )}


      {/* =====================================================
          EMPTY
      ===================================================== */}

      {!loading &&
        !error &&
        orders.length === 0 && (
          <section className="orders-state">

            <div className="orders-empty">

              <div className="orders-empty-icon">
                🛍
              </div>

              <h2>
                No orders yet
              </h2>

              <p>
                Your completed AgentCart purchases
                will appear here.
              </p>

              <button
                type="button"
                className="approve-button"
                onClick={onBack}
              >
                Start shopping →
              </button>

            </div>

          </section>
        )}


      {/* =====================================================
          ORDER LIST
      ===================================================== */}

      {!loading &&
        !error &&
        orders.length > 0 && (

          <section className="orders-content">

            <div className="orders-summary">

              <span>
                {orders.length}{" "}
                {orders.length === 1
                  ? "order"
                  : "orders"}
              </span>

              <span>
                Latest first
              </span>

            </div>


            <div className="orders-list">

              {orders.map((order) => (

                <article
                  className="order-card"
                  key={order.order_id}
                >

                  {/* -----------------------------------------
                      PRODUCT
                  ----------------------------------------- */}

                  <div className="order-product">

                    <div className="order-product-icon">
                      🎧
                    </div>

                    <div>

                      <div className="order-label">
                        ORDER
                      </div>

                      <h2>
                        {order.primary_product}
                      </h2>

                      <p>
                        {order.item_count}{" "}
                        {order.item_count === 1
                          ? "item"
                          : "items"}
                      </p>

                    </div>

                  </div>


                  {/* -----------------------------------------
                      AMOUNT
                  ----------------------------------------- */}

                  <div className="order-amount">

                    <span>
                      Amount
                    </span>

                    <strong>
                      ₹
                      {Number(
                        order.amount
                      ).toLocaleString(
                        "en-IN"
                      )}
                    </strong>

                  </div>


                  {/* -----------------------------------------
                      STATUS
                  ----------------------------------------- */}

                  <div className="order-status">

                    <span>
                      Status
                    </span>

                    <strong
                      className={
                        getStatusClass(
                          order.status
                        )
                      }
                    >
                      <span className="order-status-dot" />

                      {getStatusLabel(
                        order.status
                      )}
                    </strong>

                  </div>


                  {/* -----------------------------------------
                      DATE
                  ----------------------------------------- */}

                  <div className="order-date">

                    <span>
                      Created
                    </span>

                    <strong>
                      {formatDate(
                        order.created_at
                      )}
                    </strong>

                  </div>


                  {/* -----------------------------------------
                      VIEW
                  ----------------------------------------- */}

                  <button
                    type="button"
                    className="order-view-button"
                      onClick={() =>onOpenOrder(order.order_id)}
                  >
                    View details →
                  </button>

                </article>

              ))}

            </div>

          </section>

        )}

    </main>
  );
}


export default OrdersPage;