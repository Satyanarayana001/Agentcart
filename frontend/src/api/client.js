const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";


async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      data.detail ||
        data.message ||
        `Request failed (${response.status})`
    );
  }

  return data;
}


/* =========================================================
   AGENT API
   ========================================================= */

export const agentApi = {
  createPurchaseRequest(userRequest) {
    return apiRequest("/api/agent/purchase", {
      method: "POST",
      body: JSON.stringify({
        request: userRequest,
      }),
    });
  },

  selectProduct(productId, quantity = 1, maxBudget) {
    return apiRequest("/api/agent/select-product", {
      method: "POST",
      body: JSON.stringify({
        product_id: productId,
        quantity,
        max_budget: maxBudget,
      }),
    });
  },
};


/* =========================================================
   PURCHASE API
   ========================================================= */

export const purchaseApi = {
  getPlan(planId) {
    return apiRequest(`/api/purchase/plans/${planId}`);
  },

  approvePlan(planId) {
    return apiRequest(
      `/api/purchase/plans/${planId}/approve`,
      {
        method: "POST",
      }
    );
  },

  rejectPlan(planId) {
    return apiRequest(
      `/api/purchase/plans/${planId}/reject`,
      {
        method: "POST",
      }
    );
  },
};


/* =========================================================
   PAYMENT API
   ========================================================= */

export const paymentApi = {
  createOrder(planId) {
    return apiRequest(
      `/api/payment/plans/${planId}/orders`,
      {
        method: "POST",
      }
    );
  },

  getOrder(paymentOrderId) {
    return apiRequest(
      `/api/payment/orders/${paymentOrderId}`
    );
  },

  verifyPayment(paymentOrderId, paymentData) {
    return apiRequest(
      `/api/payment/orders/${paymentOrderId}/verify`,
      {
        method: "POST",
        body: JSON.stringify(paymentData),
      }
    );
  },
};


/* =========================================================
   AUDIT API
   ========================================================= */

export const auditApi = {
  getPlanHistory(planId) {
    return apiRequest(
      `/api/audit/plans/${planId}`
    );
  },

  getAllEvents() {
    return apiRequest("/api/audit/");
  },
};


/* =========================================================
   ORDERS API
   ========================================================= */

export const ordersApi = {
  getOrders() {
    return apiRequest("/api/orders/");
  },

  getOrder(orderId) {
    return apiRequest(
      `/api/orders/${orderId}`
    );
  },

  getTracking(orderId) {
    return apiRequest(
      `/api/orders/${orderId}/tracking`
    );
  },

  advanceTracking(orderId) {
    return apiRequest(
      `/api/orders/${orderId}/tracking/advance`,
      {
        method: "POST",
      }
    );
  },
};


/* =========================================================
   CATALOG API
   ========================================================= */

export const catalogApi = {
  getProducts() {
    return apiRequest(
      "/api/catalog/products"
    );
  },

  getProduct(productId) {
    return apiRequest(
      `/api/catalog/products/${productId}`
    );
  },

  searchProducts(params = {}) {
    const searchParams = new URLSearchParams();

    Object.entries(params).forEach(
      ([key, value]) => {
        if (
          value !== undefined &&
          value !== null &&
          value !== ""
        ) {
          searchParams.append(key, value);
        }
      }
    );

    const query = searchParams.toString();

    return apiRequest(
      `/api/catalog/search${
        query ? `?${query}` : ""
      }`
    );
  },
};

/* =========================================================
   NOTIFICATIONS API
   ========================================================= */

export const notificationsApi = {
  getNotifications(unreadOnly = false) {
    return apiRequest(
      `/api/notifications/?unread_only=${unreadOnly}`
    );
  },

  getUnreadCount() {
    return apiRequest(
      "/api/notifications/unread-count"
    );
  },

  markAsRead(notificationId) {
    return apiRequest(
      `/api/notifications/${notificationId}/read`,
      {
        method: "POST",
      }
    );
  },

  markAllAsRead() {
    return apiRequest(
      "/api/notifications/read-all",
      {
        method: "POST",
      }
    );
  },
};