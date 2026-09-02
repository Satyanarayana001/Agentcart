import { useEffect, useState } from "react";
import { auditApi } from "../api/client";

function formatEventType(eventType) {
  return eventType
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatTime(timestamp) {
  if (!timestamp) {
    return "";
  }

  return new Date(timestamp).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function AuditTimeline({ plan }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!plan?.plan_id) {
      setEvents([]);
      return;
    }

    let cancelled = false;

    async function loadAuditHistory() {
      setLoading(true);
      setError("");

      try {
        const result = await auditApi.getPlanHistory(
          plan.plan_id
        );

        if (!cancelled) {
          setEvents(result.events || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err.message || "Unable to load audit history."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadAuditHistory();

    return () => {
      cancelled = true;
    };
  }, [plan?.plan_id, plan?.status]);

  if (!plan) {
    return null;
  }

  return (
    <section className="audit-timeline">
      <div className="section-label">
        AUDIT TRAIL
      </div>

      <div className="audit-header">
        <div>
          <h2>Purchase audit trail</h2>

          <p>
            Every important action is recorded from agent
            decision through payment.
          </p>
        </div>

        {events.length > 0 && (
          <span className="audit-count">
            {events.length}{" "}
            {events.length === 1 ? "event" : "events"}
          </span>
        )}
      </div>

      {loading && (
        <div className="audit-state">
          Loading audit history...
        </div>
      )}

      {error && (
        <div className="audit-error">
          <strong>Audit history unavailable</strong>
          <span>{error}</span>
        </div>
      )}

      {!loading && !error && events.length === 0 && (
        <div className="audit-state">
          No audit events recorded yet.
        </div>
      )}

      {!loading && !error && events.length > 0 && (
        <div className="audit-events">
          {events.map((event, index) => {
            const isFailure =
              event.event_type.includes("FAILED") ||
              event.event_type.includes("BLOCKED") ||
              event.event_type.includes("ERROR");

            return (
              <div
                className={`audit-event ${
                  isFailure ? "audit-event-failure" : ""
                }`}
                key={
                  event.event_id ||
                  `${event.event_type}-${index}`
                }
              >
                <div className="audit-marker">
                  {isFailure ? "!" : "✓"}
                </div>

                <div className="audit-event-content">
                  <div className="audit-event-top">
                    <strong>
                      {formatEventType(
                        event.event_type
                      )}
                    </strong>

                    <span>
                      {formatTime(event.timestamp)}
                    </span>
                  </div>

                  <p>{event.message}</p>

                  {event.metadata &&
                    Object.keys(event.metadata).length > 0 && (
                      <details className="audit-metadata">
                        <summary>
                          View event details
                        </summary>

                        <pre>
                          {JSON.stringify(
                            event.metadata,
                            null,
                            2
                          )}
                        </pre>
                      </details>
                    )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

export default AuditTimeline;

