from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json, time, random, signal, sys

# =========================
# WAIT FOR KAFKA (WITH BACKOFF)
# =========================
attempt = 0

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=5,
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

# =========================
# GRACEFUL SHUTDOWN
# =========================
def shutdown(sig, frame):
    print("Shutting down producer...")
    producer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# =========================
# EVENT LOOP
# =========================
services = ["catalogue", "user", "cart", "shipping", "payment"]

while True:
    event = {
        "service": random.choice(services),
        "status": random.choice([200, 200, 200, 500]),
        "request_time": random.randint(50, 500),
        "cpu": random.randint(10, 95),
        "memory": random.randint(10, 90)
    }

    producer.send(
        "aiops-stream",
        key=event["service"].encode(),
        value=event
    )

    producer.flush()

    print("sent:", event)
    time.sleep(1)