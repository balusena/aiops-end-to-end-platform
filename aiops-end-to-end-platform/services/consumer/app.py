from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import time

from ml import predict
from alerts import trigger_alerts
from otel import tracer
from metrics import EVENT_COUNT, ANOMALY_COUNT, ERROR_RATE
from state import update_window, build_features

# =========================
# WAIT FOR KAFKA (WITH BACKOFF)
# =========================
attempt = 0

while True:
    try:
        consumer = KafkaConsumer(
            "aiops-stream",
            bootstrap_servers="kafka:9092",
            group_id="aiops-group",
            auto_offset_reset="earliest",
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            reconnect_backoff_ms=500,
            reconnect_backoff_max_ms=5000,
        )
        print("Connected to Kafka")
        break

    except NoBrokersAvailable:
        wait = min(2 ** attempt, 30)
        print(f"Waiting for Kafka... retry in {wait}s")
        time.sleep(wait)
        attempt += 1

print("🚀 AIOps Engine Running...")

# =========================
# EVENT PROCESSING LOOP
# =========================
for msg in consumer:
    try:
        event = msg.value
        service = event["service"]

        EVENT_COUNT.labels(service=service).inc()

        update_window(service, event)

        if tracer:
            with tracer.start_as_current_span("aiops-pipeline"):

                with tracer.start_as_current_span("feature-engineering"):
                    features = build_features(service)

                if not features:
                    continue

                with tracer.start_as_current_span("ml-inference"):
                    score = predict(service, features)

                ERROR_RATE.labels(service=service).set(features["error_rate"])

                if score == -1:
                    ANOMALY_COUNT.labels(service=service).inc()

                with tracer.start_as_current_span("alerting"):
                    trigger_alerts(features, score)

                print(f"[{service}] anomaly={score} req={features['req_count']}")



    except Exception as e:
        print("Error processing event:", e)