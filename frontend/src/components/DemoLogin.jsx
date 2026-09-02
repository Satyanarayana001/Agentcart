import { useState } from "react";


const DEFAULT_DEMO_USER = {
  name: "Arjun Mehta",
  phone: "+91 9876543210",
  email: "arjun.mehta@demo.agentcart.ai",
  customerId: "AC-DEMO-001",
  accountType: "Demo Customer",
  currency: "INR",
  location: "Bengaluru, India",
  memberSince: "2026",
};


function DemoLogin({ onLogin }) {
  const [phone, setPhone] =
    useState("9876543210");

  const [error, setError] =
    useState("");


  function handleSubmit(event) {
    event.preventDefault();

    const cleanedPhone =
      phone.replace(/\D/g, "");

    if (cleanedPhone.length !== 10) {
      setError(
        "Enter a valid 10-digit mobile number."
      );
      return;
    }

    setError("");

    const session = {
      ...DEFAULT_DEMO_USER,
      phone: `+91 ${cleanedPhone}`,
      demo: true,
      loggedInAt: new Date().toISOString(),
    };

    localStorage.setItem(
      "agentcart_demo_session",
      JSON.stringify(session)
    );

    onLogin(session);
  }


  return (
    <main className="demo-login-page">

      <section className="demo-login-card">

        <div className="demo-login-brand">

          <span className="brand-mark">
            A
          </span>

          <span>
            AgentCart
          </span>

        </div>


        <div className="demo-login-badge">
          Hackathon Demo
        </div>


        <h1>
          Welcome,
          <br />
          <span>Arjun.</span>
        </h1>


        <p className="demo-login-description">
          Your AI commerce agent finds products,
          checks policies, and prepares purchases
          for your approval.
        </p>


        <form
          className="demo-login-form"
          onSubmit={handleSubmit}
        >

          <label htmlFor="demo-phone">
            Mobile number
          </label>


          <div className="demo-phone-input">

            <span>
              +91
            </span>

            <input
              id="demo-phone"
              type="tel"
              inputMode="numeric"
              value={phone}
              onChange={(event) => {
                setPhone(
                  event.target.value
                );
                setError("");
              }}
              placeholder="9876543210"
              maxLength={10}
              autoComplete="tel"
            />

          </div>


          {error && (
            <p className="demo-login-error">
              {error}
            </p>
          )}


          <button
            type="submit"
            className="demo-login-button"
          >
            Continue to AgentCart

            <span>
              →
            </span>
          </button>

        </form>


        <div className="demo-login-note">

          <span className="demo-login-note-icon">
            ✓
          </span>

          <div>

            <strong>
              Demo account
            </strong>

            <p>
              Arjun Mehta · AC-DEMO-001
            </p>

          </div>

        </div>


        <div className="demo-login-trust">

          <span>
            AI decision
          </span>

          <span>
            →
          </span>

          <span>
            Policy check
          </span>

          <span>
            →
          </span>

          <span>
            Your approval
          </span>

          <span>
            →
          </span>

          <span>
            Payment
          </span>

        </div>

      </section>

    </main>
  );
}


export default DemoLogin;