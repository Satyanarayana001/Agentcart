import { useEffect, useState } from "react";

import {
  auditApi,
  ordersApi,
} from "../api/client";


function OrderDetailsPage({
  orderId,
  onBack,
}) {
  const [order, setOrder] =
    useState(null);

  const [events, setEvents] =
    useState([]);

  const [tracking, setTracking] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [trackingLoading, setTrackingLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [trackingError, setTrackingError] =
    useState("");


  // =========================================================
  // LOAD ORDER
  // =========================================================

  useEffect(() => {
    async function loadOrder() {
      if (!orderId) {
        setError("Order ID is missing.");
        setLoading(false);
        return;
      }

      setLoading(true);
      setError("");
      setTrackingError("");

      try {
        // ---------------------------------------------------
        // ORDER
        // ---------------------------------------------------

        const orderData =
          await ordersApi.getOrder(
            orderId
          );

        setOrder(orderData);


        // ---------------------------------------------------
        // AUDIT HISTORY
        // ---------------------------------------------------

        try {
          const auditData =
            await auditApi.getPlanHistory(
              orderData.plan_id
            );

          setEvents(
            auditData?.events || []
          );

        } catch {
          setEvents([]);
        }


        // ---------------------------------------------------
        // FULFILLMENT TRACKING
        // ---------------------------------------------------

        try {
          const trackingData =
            await ordersApi.getTracking(
              orderId
            );

          setTracking(
            trackingData
          );

        } catch (err) {
          setTrackingError(
            err.message ||
              "Unable to load tracking."
          );
        }

      } catch (err) {
        setError(
          err.message ||
            "Unable to load order details."
        );

      } finally {
        setLoading(false);
      }
    }


    loadOrder();

  }, [orderId]);


  // =========================================================
  // DATE FORMATTER
  // =========================================================

  function formatDate(
    dateString
  ) {
    if (!dateString) {
      return "Unknown";
    }

    return new Date(
      dateString
    ).toLocaleString(
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
  // STATUS FORMATTER
  // =========================================================

  function formatStatus(
    status
  ) {
    if (!status) {
      return "Unknown";
    }

    return status
      .replaceAll(
        "_",
        " "
      )
      .toLowerCase()
      .replace(
        /\b\w/g,
        (char) =>
          char.toUpperCase()
      );
  }


  // =========================================================
  // STATUS CLASS
  // =========================================================

  function getStatusClass(
    status
  ) {
    switch (status) {

      case "PAYMENT_VERIFIED":
        return "details-status-success";

      case "PAYMENT_FAILED":
        return "details-status-failed";

      case "ORDER_CREATED":
        return "details-status-pending";

      default:
        return "details-status-default";
    }
  }


  // =========================================================
  // ADVANCE DEMO TRACKING
  // =========================================================

  async function handleAdvanceTracking() {
    if (
      !orderId ||
      trackingLoading
    ) {
      return;
    }

    setTrackingLoading(true);
    setTrackingError("");

    try {

      await ordersApi.advanceTracking(
        orderId
      );


      // ---------------------------------------------------
      // REFRESH TRACKING
      // ---------------------------------------------------

      const updatedTracking =
        await ordersApi.getTracking(
          orderId
        );

      setTracking(
        updatedTracking
      );


      // ---------------------------------------------------
      // REFRESH AUDIT TRAIL
      // ---------------------------------------------------

      if (order?.plan_id) {

        const updatedAudit =
          await auditApi.getPlanHistory(
            order.plan_id
          );

        setEvents(
          updatedAudit?.events || []
        );

      }

    } catch (err) {

      setTrackingError(
        err.message ||
          "Unable to update tracking."
      );

    } finally {

      setTrackingLoading(
        false
      );

    }
  }


  // =========================================================
  // LOADING STATE
  // =========================================================

  if (loading) {

    return (
      <main className="order-details-page">

        <nav className="navbar">

          <div className="navbar-inner">

            <div className="brand">

              <span className="brand-mark">
                A
              </span>

              <div className="brand-copy">

                <span className="brand-name">
                  AgentCart
                </span>

                <span className="brand-subtitle">
                  AI commerce
                </span>

              </div>

            </div>

          </div>

        </nav>


        <section className="order-details-state">

          <div className="order-details-loading">
            Loading order details...
          </div>

        </section>

      </main>
    );
  }


  // =========================================================
  // ERROR STATE
  // =========================================================

  if (
    error ||
    !order
  ) {

    return (
      <main className="order-details-page">

        <nav className="navbar">

          <div className="navbar-inner">

            <div className="brand">

              <span className="brand-mark">
                A
              </span>

              <div className="brand-copy">

                <span className="brand-name">
                  AgentCart
                </span>

                <span className="brand-subtitle">
                  AI commerce
                </span>

              </div>

            </div>


            <button
              type="button"
              className="orders-back-button"
              onClick={onBack}
            >
              ← Order history
            </button>

          </div>

        </nav>


        <section className="order-details-state">

          <div className="order-details-error">

            <strong>
              Unable to load order
            </strong>

            <span>
              {error ||
                "Order not found."}
            </span>

            <button
              type="button"
              className="details-back-button"
              onClick={onBack}
            >
              ← Back to orders
            </button>

          </div>

        </section>

      </main>
    );
  }


  // =========================================================
  // MAIN PAGE
  // =========================================================

  return (
    <main className="order-details-page">

      {/* =====================================================
          NAVIGATION
          ===================================================== */}

      <nav className="navbar">

        <div className="navbar-inner">

          <div className="brand">

            <span className="brand-mark">
              A
            </span>

            <div className="brand-copy">

              <span className="brand-name">
                AgentCart
              </span>

              <span className="brand-subtitle">
                AI commerce
              </span>

            </div>

          </div>


          <button
            type="button"
            className="orders-back-button"
            onClick={onBack}
          >
            ← Order history
          </button>

        </div>

      </nav>


      {/* =====================================================
          ORDER HEADER
          ===================================================== */}

      <section className="order-details-header">

        <button
          type="button"
          className="details-back-link"
          onClick={onBack}
        >
          ← Back to orders
        </button>


        <div className="section-label">
          ORDER DETAILS
        </div>


        <div className="details-title-row">

          <div>

            <h1>
              {order.items?.[0]?.name ||
                "Your order"}
            </h1>

            <p>
              Order {order.order_id}
            </p>

          </div>


          <div
            className={`details-status ${getStatusClass(
              order.status
            )}`}
          >

            <span className="details-status-dot" />

            {formatStatus(
              order.status
            )}

          </div>

        </div>

      </section>


      {/* =====================================================
          MAIN CONTENT
          ===================================================== */}

      <section className="order-details-content">

        <div className="details-main">

          {/* =================================================
              ORDER SUMMARY
          ================================================= */}

          <section className="details-card details-summary-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  PURCHASE
                </span>

                <h2>
                  Order summary
                </h2>

              </div>


              <div className="details-total">

                <span>
                  Total
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

            </div>


            <div className="details-items">

              {order.items?.map(
                (item) => (

                  <div
                    className="details-item"
                    key={
                      item.product_id
                    }
                  >

                    <div className="details-item-icon">
                      🛍
                    </div>


                    <div className="details-item-info">

                      <strong>
                        {item.name}
                      </strong>

                      <span>
                        Quantity:{" "}
                        {item.quantity}
                      </span>

                    </div>


                    <div className="details-item-price">

                      ₹
                      {Number(
                        item.total_price
                      ).toLocaleString(
                        "en-IN"
                      )}

                    </div>

                  </div>

                )
              )}

            </div>

          </section>


          {/* =================================================
              AI DECISION
          ================================================= */}

          <section className="details-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  AI DECISION
                </span>

                <h2>
                  Why this product?
                </h2>

              </div>

            </div>


            <div className="decision-box">

              <div className="decision-icon">
                ✦
              </div>


              <p>
                {order.plan_explanation ||
                  "AgentCart selected this product based on your purchase request."}
              </p>

            </div>


            <div className="decision-boundary">

              <div className="boundary-step">

                <span>
                  01
                </span>

                <strong>
                  AI decision
                </strong>

              </div>


              <div className="boundary-arrow">
                →
              </div>


              <div className="boundary-step">

                <span>
                  02
                </span>

                <strong>
                  Policy check
                </strong>

              </div>


              <div className="boundary-arrow">
                →
              </div>


              <div className="boundary-step">

                <span>
                  03
                </span>

                <strong>
                  Human approval
                </strong>

              </div>


              <div className="boundary-arrow">
                →
              </div>


              <div className="boundary-step">

                <span>
                  04
                </span>

                <strong>
                  Payment
                </strong>

              </div>

            </div>

          </section>


          {/* =================================================
              ORDER INFORMATION
          ================================================= */}

          <section className="details-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  ORDER INFORMATION
                </span>

                <h2>
                  Transaction details
                </h2>

              </div>

            </div>


            <div className="details-info-grid">

              <div className="details-info-item">

                <span>
                  Order ID
                </span>

                <strong>
                  {order.order_id}
                </strong>

              </div>


              <div className="details-info-item">

                <span>
                  Plan ID
                </span>

                <strong>
                  {order.plan_id}
                </strong>

              </div>


              <div className="details-info-item">

                <span>
                  Created
                </span>

                <strong>
                  {formatDate(
                    order.created_at
                  )}
                </strong>

              </div>


              <div className="details-info-item">

                <span>
                  Plan status
                </span>

                <strong>
                  {formatStatus(
                    order.plan_status
                  )}
                </strong>

              </div>

            </div>

          </section>


          {/* =================================================
              PAYMENT
          ================================================= */}

          <section className="details-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  PAYMENT
                </span>

                <h2>
                  Razorpay transaction
                </h2>

              </div>

            </div>


            <div className="details-info-grid">

              <div className="details-info-item">

                <span>
                  Payment status
                </span>

                <strong
                  className={getStatusClass(
                    order.status
                  )}
                >
                  {formatStatus(
                    order.status
                  )}
                </strong>

              </div>


              <div className="details-info-item">

                <span>
                  Razorpay order
                </span>

                <strong className="details-mono">
                  {order.razorpay_order_id}
                </strong>

              </div>


              <div className="details-info-item">

                <span>
                  Payment reference
                </span>

                <strong className="details-mono">
                  {order.razorpay_payment_id ||
                    "Not available"}
                </strong>

              </div>


              <div className="details-info-item">

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

            </div>

          </section>

        </div>


        {/* ===================================================
            SIDEBAR
        =================================================== */}

        <aside className="details-sidebar">

          {/* =================================================
              AUDIT TRAIL
          ================================================= */}

          <section className="details-card timeline-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  AUDIT TRAIL
                </span>

                <h2>
                  Order timeline
                </h2>

              </div>

            </div>


            {events.length > 0 ? (

              <div className="details-timeline">

                {events.map(
                  (
                    event,
                    index
                  ) => (

                    <div
                      className="timeline-event"
                      key={
                        event.event_id ||
                        `${event.event_type}-${index}`
                      }
                    >

                      <div className="timeline-marker">
                        <span />
                      </div>


                      <div className="timeline-content">

                        <strong>
                          {formatStatus(
                            event.event_type
                          )}
                        </strong>


                        <p>
                          {event.message}
                        </p>


                        <time>
                          {formatDate(
                            event.timestamp
                          )}
                        </time>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="timeline-empty">

                <span>
                  No audit events available.
                </span>

              </div>

            )}

          </section>


          {/* =================================================
              ORDER TRACKING
          ================================================= */}

          <section className="details-card tracking-card">

            <div className="details-card-header">

              <div>

                <span className="details-eyebrow">
                  ORDER TRACKING
                </span>

                <h2>
                  Delivery updates
                </h2>

              </div>


              {tracking && (
                <span className="tracking-status-label">
                  {tracking.fulfillment_label}
                </span>
              )}

            </div>


            {/* -----------------------------------------------
                TRACKING ERROR
            ----------------------------------------------- */}

            {trackingError && (

              <div className="tracking-error">

                {trackingError}

              </div>

            )}


            {/* -----------------------------------------------
                TRACKING TIMELINE
            ----------------------------------------------- */}

            {tracking?.events?.length > 0 ? (

              <div className="tracking-timeline">

                {tracking.events.map(
                  (event) => (

                    <div
                      className={`tracking-event ${
                        event.completed
                          ? "tracking-event-completed"
                          : ""
                      } ${
                        event.current
                          ? "tracking-event-current"
                          : ""
                      }`}
                      key={
                        event.status
                      }
                    >

                      <div className="tracking-marker">

                        <span />

                      </div>


                      <div className="tracking-event-content">

                        <strong>
                          {event.label}
                        </strong>


                        <p>
                          {event.description}
                        </p>


                        {event.current &&
                          event.timestamp && (

                            <time>
                              {formatDate(
                                event.timestamp
                              )}
                            </time>

                          )}

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="tracking-awaiting">

                Tracking will begin after
                payment confirmation.

              </div>

            )}


            {/* -----------------------------------------------
                ADVANCE DEMO TRACKING
            ----------------------------------------------- */}

            {tracking &&
              tracking.fulfillment_status !==
                "DELIVERED" &&
              tracking.payment_status ===
                "PAYMENT_VERIFIED" && (

                <button
                  type="button"
                  className="tracking-advance-button"
                  onClick={
                    handleAdvanceTracking
                  }
                  disabled={
                    trackingLoading
                  }
                >

                  {trackingLoading
                    ? "Updating..."
                    : "Advance demo status →"}

                </button>

              )}


            {/* -----------------------------------------------
                DELIVERED
            ----------------------------------------------- */}

            {tracking?.fulfillment_status ===
              "DELIVERED" && (

              <div className="tracking-delivered">

                ✓ Order delivered

              </div>

            )}

          </section>

        </aside>

      </section>

    </main>
  );
}


export default OrderDetailsPage;