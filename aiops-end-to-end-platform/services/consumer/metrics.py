from prometheus_client import Counter, Gauge, start_http_server
import os

PORT = int(os.getenv("METRICS_PORT", "8000"))

EVENT_COUNT = Counter("aiops_events_total", "Total events", ["service"])
ANOMALY_COUNT = Counter("aiops_anomalies_total", "Total anomalies", ["service"])
ERROR_RATE = Gauge("aiops_error_rate", "Error rate", ["service"])

try:
    start_http_server(PORT)
except Exception as e:
    print("Metrics server already running:", e)