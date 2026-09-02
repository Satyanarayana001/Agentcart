import { useState } from "react";

import "./App.css";

import CommercePage from "./pages/CommercePage";
import OrdersPage from "./pages/OrdersPage";
import OrderDetailsPage from "./pages/OrderDetailsPage";
import DemoLogin from "./components/DemoLogin";


function App() {
  const [
    session,
    setSession,
  ] = useState(() => {
    try {
      const savedSession =
        localStorage.getItem(
          "agentcart_demo_session"
        );

      return savedSession
        ? JSON.parse(savedSession)
        : null;
    } catch {
      return null;
    }
  });


  const [page, setPage] =
    useState("shop");


  const [selectedOrderId, setSelectedOrderId] =
    useState(null);


  function handleLogin(newSession) {
    setSession(newSession);
    setPage("shop");
  }


  function handleLogout() {
    localStorage.removeItem(
      "agentcart_demo_session"
    );

    setSession(null);
    setSelectedOrderId(null);
    setPage("shop");
  }


  function openOrder(orderId) {
    setSelectedOrderId(orderId);
    setPage("order-details");
  }


  if (!session) {
    return (
      <DemoLogin
        onLogin={handleLogin}
      />
    );
  }


  if (page === "orders") {
    return (
      <OrdersPage
        onBack={() => setPage("shop")}
        onOpenOrder={openOrder}
      />
    );
  }


  if (page === "order-details") {
    return (
      <OrderDetailsPage
        orderId={selectedOrderId}
        onBack={() => setPage("orders")}
      />
    );
  }


  return (
    <CommercePage
      onOpenOrders={() =>
        setPage("orders")
      }
      onLogout={handleLogout}
      session={session}
    />
  );
}


export default App;