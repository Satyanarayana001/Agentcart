import { useEffect, useState } from "react";

import {
  agentApi,
  purchaseApi,
  notificationsApi,
} from "../api/client";

import PurchasePlan from "../components/PurchasePlan";
import ApprovalGate from "../components/ApprovalGate";
import PaymentGate from "../components/PaymentGate";
import AuditTimeline from "../components/AuditTimeline";
import ProductDiscovery from "../components/ProductDiscovery";
import AlternativeProducts from "../components/AlternativeProducts";
import NotificationCenter from "../components/NotificationCenter";


function CommercePage({
  onOpenOrders,
  onLogout,
  session,
}) {
  const [request, setRequest] = useState("");
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [agentMessage, setAgentMessage] =
    useState("");

  const [notificationsOpen, setNotificationsOpen] =
    useState(false);

  const [unreadCount, setUnreadCount] =
    useState(0);

  const [accountOpen, setAccountOpen] =
    useState(false);

  const [alternatives, setAlternatives] =
    useState([]);

  const [
    selectedUnavailableProduct,
    setSelectedUnavailableProduct,
  ] = useState(null);


  // =========================================================
  // LOAD UNREAD NOTIFICATION COUNT
  // =========================================================

  async function loadUnreadCount() {
    try {
      const data =
        await notificationsApi.getUnreadCount();

      setUnreadCount(
        data?.unread_count || 0
      );
    } catch (err) {
      console.error(
        "Unable to load notification count:",
        err
      );
    }
  }


  useEffect(() => {
    loadUnreadCount();

    const interval = setInterval(
      loadUnreadCount,
      10000
    );

    return () => {
      clearInterval(interval);
    };
  }, []);


  // =========================================================
  // SUBMIT NATURAL-LANGUAGE PURCHASE REQUEST
  // =========================================================

  async function handleSubmit(event) {
    event.preventDefault();

    if (!request.trim()) {
      setError(
        "Tell AgentCart what you want to buy."
      );
      return;
    }

    setLoading(true);

    // Always clear the previous transaction workspace
    // before processing a new request.
    setError("");
    setAgentMessage("");
    setPlan(null);
    setAlternatives([]);
    setSelectedUnavailableProduct(null);

    try {
      const agentResult =
        await agentApi.createPurchaseRequest(
          request.trim()
        );


      // -------------------------------------------------------
      // CATALOG INQUIRY
      // -------------------------------------------------------
      //
      // IMPORTANT:
      // This is NOT a purchase request.
      //
      // Therefore:
      // - no plan
      // - no approval
      // - no payment
      // - no audit transaction workspace
      //
      // The user is simply informed and can choose
      // something from the catalog.
      // -------------------------------------------------------

      if (
        agentResult?.status ===
        "CATALOG_INQUIRY"
      ) {
        setPlan(null);
        setAlternatives([]);
        setSelectedUnavailableProduct(null);

        setAgentMessage(
          agentResult.explanation ||
            "That product is not currently available "
            + "in the AgentCart catalog. "
            + "If you'd like anything else, you can choose "
            + "from the products available below."
        );

        return;
      }


      // -------------------------------------------------------
      // PRODUCT UNAVAILABLE
      // -------------------------------------------------------

      if (
        agentResult?.status ===
        "ALTERNATIVES_REQUIRED"
      ) {
        // There must never be a purchase plan displayed
        // while the user is choosing an alternative.
        setPlan(null);
        setAgentMessage("");

        setAlternatives(
          agentResult.alternatives || []
        );

        setSelectedUnavailableProduct(
          agentResult.selected_product || null
        );

        return;
      }


      // -------------------------------------------------------
      // NORMAL PURCHASE PLAN
      // -------------------------------------------------------

      if (!agentResult?.plan_id) {
        throw new Error(
          "Agent did not return a purchase plan."
        );
      }

      const fullPlan =
        await purchaseApi.getPlan(
          agentResult.plan_id
        );

      setAgentMessage("");
      setAlternatives([]);
      setSelectedUnavailableProduct(null);

      setPlan(fullPlan);

    } catch (err) {
      // A failed request must never leave an old
      // purchase plan visible.
      setPlan(null);
      setAlternatives([]);
      setSelectedUnavailableProduct(null);

      setError(
        err.message ||
          "Unable to process your request."
      );
    } finally {
      setLoading(false);
    }
  }


  // =========================================================
  // PLAN UPDATED
  // =========================================================

  function handlePlanUpdated(updatedPlan) {
    setPlan(updatedPlan);

    loadUnreadCount();
  }


  // =========================================================
  // USER SELECTS AN AVAILABLE ALTERNATIVE
  // =========================================================

  async function handleAlternativeSelected(
    product
  ) {
    if (!selectedUnavailableProduct) {
      return;
    }

    setLoading(true);
    setError("");
    setAgentMessage("");

    try {
      const quantity =
        selectedUnavailableProduct.quantity || 1;

      // Preserve the original purchase budget.
      const maxBudget =
        selectedUnavailableProduct.max_budget;

      if (!maxBudget) {
        throw new Error(
          "Original purchase budget is unavailable."
        );
      }

      const result =
        await agentApi.selectProduct(
          product.product_id,
          quantity,
          maxBudget
        );

      if (!result?.plan_id) {
        throw new Error(
          "Unable to create a purchase plan."
        );
      }

      const fullPlan =
        await purchaseApi.getPlan(
          result.plan_id
        );

      setPlan(fullPlan);

      setAlternatives([]);

      setSelectedUnavailableProduct(null);

    } catch (err) {
      setPlan(null);

      setError(
        err.message ||
          "Unable to select this product."
      );
    } finally {
      setLoading(false);
    }
  }


  // =========================================================
  // PRODUCT SELECTED FROM CATALOG
  // =========================================================

  function handleCatalogProductSelected(
    product
  ) {
    setAgentMessage("");
    setError("");

    setPlan(null);
    setAlternatives([]);
    setSelectedUnavailableProduct(null);

    setRequest(
      `Buy ${product.name}`
    );

    document
      .getElementById("purchase-request")
      ?.scrollIntoView({
        behavior: "smooth",
        block: "center",
      });
  }


  // =========================================================
  // NOTIFICATION CENTER
  // =========================================================

  function handleNotificationToggle() {
    setNotificationsOpen(
      (current) => !current
    );

    setAccountOpen(false);
  }


  function handleNotificationClose() {
    setNotificationsOpen(false);

    loadUnreadCount();
  }


  // =========================================================
  // CUSTOMER ACCOUNT
  // =========================================================

  function handleAccountToggle() {
    setAccountOpen(
      (current) => !current
    );

    setNotificationsOpen(false);
  }


  function handleLogoutClick() {
    setAccountOpen(false);

    if (onLogout) {
      onLogout();
    }
  }


  const customerInitial =
    session?.name
      ?.charAt(0)
      .toUpperCase() || "A";


  return (
    <main className="commerce-page">

      {/* =====================================================
          NAVIGATION
      ===================================================== */}

      <nav className="navbar">

        <div className="navbar-inner">

          {/* =================================================
              BRAND
          ================================================= */}

          <div className="brand">

            <img
              src="/agentcart-logo.svg"
              alt="AgentCart"
              className="brand-logo"
            />

            <div className="brand-copy">

              <span className="brand-name">
                AgentCart
              </span>

              <span className="brand-subtitle">
                AI commerce
              </span>

            </div>

          </div>


          {/* =================================================
              NAV ACTIONS
          ================================================= */}

          <div className="nav-actions">

            {/* ===============================================
                NOTIFICATIONS
            =============================================== */}

            <button
              type="button"
              className="nav-icon-button"
              onClick={
                handleNotificationToggle
              }
              aria-label="Open notifications"
              aria-expanded={
                notificationsOpen
              }
            >

              <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
              >

                <path
                  d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"
                />

                <path
                  d="M10 21h4"
                />

              </svg>


              {unreadCount > 0 && (
                <span className="notification-badge">
                  {unreadCount > 99
                    ? "99+"
                    : unreadCount}
                </span>
              )}

            </button>


            {/* ===============================================
                ORDERS
            =============================================== */}

            <button
              type="button"
              className="nav-orders-button"
              onClick={onOpenOrders}
            >

              <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
              >

                <path
                  d="M6 2h12l2 4v15H4V6l2-4Z"
                />

                <path
                  d="M4 6h16"
                />

                <path
                  d="M9 10h6"
                />

                <path
                  d="M9 14h6"
                />

              </svg>

              <span>
                Orders
              </span>

            </button>


            {/* ===============================================
                SHOP
            =============================================== */}

            <button
              type="button"
              className="nav-shop-button"
              onClick={() => {
                document
                  .querySelector(".hero")
                  ?.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                  });
              }}
            >
              Shop
            </button>


            {/* ===============================================
                CUSTOMER ACCOUNT
            =============================================== */}

            <div className="nav-account">

              <button
                type="button"
                className="nav-account-button"
                onClick={
                  handleAccountToggle
                }
                aria-label="Open customer account"
                aria-expanded={
                  accountOpen
                }
              >

                <span className="nav-avatar">
                  {customerInitial}
                </span>


                <span className="nav-account-copy">

                  <strong>
                    {session?.name ||
                      "Demo User"}
                  </strong>

                  <span>
                    Demo account
                  </span>

                </span>


                <span
                  className={`nav-account-chevron ${
                    accountOpen
                      ? "nav-account-chevron-open"
                      : ""
                  }`}
                >
                  ▾
                </span>

              </button>


              {/* =============================================
                  ACCOUNT MENU
              ============================================= */}

              {accountOpen && (
                <div className="account-menu">

                  <div className="account-menu-profile">

                    <div className="account-menu-avatar">
                      {customerInitial}
                    </div>

                    <div>

                      <strong>
                        {session?.name ||
                          "Demo User"}
                      </strong>

                      <span>
                        {session?.email ||
                          "Demo account"}
                      </span>

                    </div>

                  </div>


                  <div className="account-menu-details">

                    <div>

                      <span>
                        Customer ID
                      </span>

                      <strong>
                        {session?.customerId ||
                          "AC-DEMO-001"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Phone
                      </span>

                      <strong>
                        {session?.phone ||
                          "+91 9876543210"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Location
                      </span>

                      <strong>
                        {session?.location ||
                          "Bengaluru, India"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Account
                      </span>

                      <strong>
                        {session?.accountType ||
                          "Demo Customer"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Currency
                      </span>

                      <strong>
                        {session?.currency ||
                          "INR"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Payment
                      </span>

                      <strong>
                        Razorpay Test Mode
                      </strong>

                    </div>

                  </div>


                  <div className="account-demo-label">
                    Hackathon Demo Account
                  </div>


                  <button
                    type="button"
                    className="account-logout-button"
                    onClick={
                      handleLogoutClick
                    }
                  >
                    Sign out
                  </button>

                </div>
              )}

            </div>

          </div>

        </div>

      </nav>


      {/* =====================================================
          NOTIFICATION CENTER
      ===================================================== */}

      <NotificationCenter
        isOpen={notificationsOpen}
        onClose={
          handleNotificationClose
        }
      />


      {/* =====================================================
          HERO
      ===================================================== */}

      <section className="hero">

        <div className="hero-badge">
          AI-powered agentic commerce
        </div>


        <h1>
          Tell AgentCart
          <br />

          <span>
            what you want to buy.
          </span>
        </h1>


        <p className="hero-description">
          AgentCart finds the right product, checks your
          budget and purchase policies, then asks for your
          approval before any money moves.
        </p>


        {/* =================================================
            PURCHASE REQUEST
        ================================================= */}

        <form
          className="request-card"
          onSubmit={handleSubmit}
        >

          <label htmlFor="purchase-request">
            What would you like to buy?
          </label>


          <textarea
            id="purchase-request"
            value={request}
            onChange={(event) =>
              setRequest(event.target.value)
            }
            placeholder="Buy ANC headphones under ₹5000"
            rows={3}
            disabled={loading}
          />


          <div className="request-footer">

            <span className="hint">
              Try: "Buy wireless headphones under ₹5000"
            </span>


            <button
              type="submit"
              disabled={loading}
            >
              {loading
                ? "Agent is thinking..."
                : "Ask Agent →"}
            </button>

          </div>

        </form>


        {/* =================================================
            AGENT CATALOG MESSAGE
        ================================================= */}

        {agentMessage && (
          <div className="agent-message">

            <strong>
              AgentCart
            </strong>

            <span>
              {agentMessage}
            </span>

          </div>
        )}


        {/* =================================================
            ERROR
        ================================================= */}

        {error && (
          <div className="error-message">

            <strong>
              Something went wrong
            </strong>

            <span>
              {error}
            </span>

          </div>
        )}

      </section>


      {/* =====================================================
          PRODUCT DISCOVERY
      ===================================================== */}

      <ProductDiscovery
        onProductSelected={
          handleCatalogProductSelected
        }
      />


      {/* =====================================================
          ALTERNATIVES
      ===================================================== */}

      {alternatives.length > 0 && (
        <AlternativeProducts
          unavailableProduct={
            selectedUnavailableProduct
          }
          alternatives={alternatives}
          onSelect={
            handleAlternativeSelected
          }
        />
      )}


      {/* =====================================================
          TRANSACTION WORKSPACE
      ===================================================== */}

      {plan && (
        <section className="commerce-content">

          <div className="purchase-layout">

            <div className="purchase-primary">

              <PurchasePlan
                plan={plan}
              />


              <ApprovalGate
                plan={plan}
                onPlanUpdated={
                  handlePlanUpdated
                }
              />


              <PaymentGate
                plan={plan}
                onPlanUpdated={
                  handlePlanUpdated
                }
              />

            </div>


            <aside className="purchase-audit">

              <AuditTimeline
                plan={plan}
              />

            </aside>

          </div>

        </section>
      )}


      {/* =====================================================
          TRUST FEATURES
      ===================================================== */}

      <section className="trust-section">

        <div className="trust-grid">

          <div className="trust-item">

            <span>
              01
            </span>

            <div>

              <strong>
                Explainable
              </strong>

              <p>
                Every decision has a reason.
              </p>

            </div>

          </div>


          <div className="trust-item">

            <span>
              02
            </span>

            <div>

              <strong>
                Budget bounded
              </strong>

              <p>
                Policies limit every purchase.
              </p>

            </div>

          </div>


          <div className="trust-item">

            <span>
              03
            </span>

            <div>

              <strong>
                Human gated
              </strong>

              <p>
                You approve before payment.
              </p>

            </div>

          </div>


          <div className="trust-item">

            <span>
              04
            </span>

            <div>

              <strong>
                Auditable
              </strong>

              <p>
                Actions are recorded end to end.
              </p>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}


export default CommercePage;