import { useEffect, useState } from "react";

import { notificationsApi } from "../api/client";


function formatNotificationTime(timestamp) {
  if (!timestamp) {
    return "";
  }

  const date = new Date(timestamp);
  const now = new Date();

  const diffMs = now - date;
  const diffMinutes = Math.floor(
    diffMs / (1000 * 60)
  );

  if (diffMinutes < 1) {
    return "Just now";
  }

  if (diffMinutes < 60) {
    return `${diffMinutes} min ago`;
  }

  const diffHours = Math.floor(
    diffMinutes / 60
  );

  if (diffHours < 24) {
    return `${diffHours} hr ago`;
  }

  const diffDays = Math.floor(
    diffHours / 24
  );

  if (diffDays === 1) {
    return "Yesterday";
  }

  return date.toLocaleDateString();
}


function getNotificationIcon(type) {
  if (type === "ORDER_PROCESSING") {
    return "📦";
  }

  if (type === "ORDER_SHIPPED") {
    return "🚚";
  }

  if (type === "ORDER_OUT_FOR_DELIVERY") {
    return "🛵";
  }

  if (type === "ORDER_DELIVERED") {
    return "✓";
  }

  if (type === "PAYMENT_SUCCESS") {
    return "₹";
  }

  return "•";
}


function NotificationCenter({
  isOpen,
  onClose,
}) {
  const [notifications, setNotifications] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  async function loadNotifications() {
    try {
      setLoading(true);
      setError("");

      const data =
        await notificationsApi.getNotifications();

      setNotifications(
        Array.isArray(data)
          ? data
          : data?.value || []
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to load notifications."
      );
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    if (!isOpen) {
      return;
    }

    loadNotifications();
  }, [isOpen]);


  async function handleMarkAsRead(
    notificationId
  ) {
    try {
      await notificationsApi.markAsRead(
        notificationId
      );

      setNotifications((current) =>
        current.map((notification) =>
          notification.notification_id ===
          notificationId
            ? {
                ...notification,
                is_read: true,
              }
            : notification
        )
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to update notification."
      );
    }
  }


  async function handleMarkAllAsRead() {
    try {
      await notificationsApi.markAllAsRead();

      setNotifications((current) =>
        current.map((notification) => ({
          ...notification,
          is_read: true,
        }))
      );
    } catch (err) {
      setError(
        err.message ||
          "Unable to update notifications."
      );
    }
  }


  if (!isOpen) {
    return null;
  }


  const unreadCount =
    notifications.filter(
      (notification) =>
        !notification.is_read
    ).length;


  return (
    <>
      <div
        className="notification-overlay"
        onClick={onClose}
      />

      <aside className="notification-panel">
        <div className="notification-panel-header">
          <div>
            <p className="notification-eyebrow">
              AgentCart
            </p>

            <h2>
              Notifications
            </h2>
          </div>

          <button
            type="button"
            className="notification-close"
            onClick={onClose}
            aria-label="Close notifications"
          >
            ×
          </button>
        </div>


        <div className="notification-toolbar">
          <span>
            {unreadCount} unread
          </span>

          {unreadCount > 0 && (
            <button
              type="button"
              onClick={handleMarkAllAsRead}
            >
              Mark all as read
            </button>
          )}
        </div>


        <div className="notification-list">
          {loading && (
            <div className="notification-state">
              Loading notifications...
            </div>
          )}


          {!loading && error && (
            <div className="notification-error">
              {error}
            </div>
          )}


          {!loading &&
            !error &&
            notifications.length === 0 && (
              <div className="notification-empty">
                <div className="notification-empty-icon">
                  ✓
                </div>

                <strong>
                  You're all caught up
                </strong>

                <p>
                  New order and payment
                  updates will appear here.
                </p>
              </div>
            )}


          {!loading &&
            !error &&
            notifications.map(
              (notification) => (
                <article
                  key={
                    notification.notification_id
                  }
                  className={`notification-item ${
                    notification.is_read
                      ? "notification-read"
                      : "notification-unread"
                  }`}
                >
                  <div className="notification-icon">
                    {getNotificationIcon(
                      notification.notification_type
                    )}
                  </div>

                  <div className="notification-content">
                    <div className="notification-title-row">
                      <strong>
                        {notification.title}
                      </strong>

                      {!notification.is_read && (
                        <span className="notification-unread-dot" />
                      )}
                    </div>

                    <p>
                      {notification.message}
                    </p>

                    <div className="notification-meta">
                      <time>
                        {formatNotificationTime(
                          notification.created_at
                        )}
                      </time>

                      {!notification.is_read && (
                        <button
                          type="button"
                          onClick={() =>
                            handleMarkAsRead(
                              notification.notification_id
                            )
                          }
                        >
                          Mark read
                        </button>
                      )}
                    </div>
                  </div>
                </article>
              )
            )}
        </div>
      </aside>
    </>
  );
}


export default NotificationCenter;