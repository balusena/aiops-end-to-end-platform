from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json, time, random, signal, sys

# =========================
# CONNECT TO KAFKA
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
# STATEFUL SYSTEM MODEL
# =========================

services = ["catalogue", "user", "cart", "shipping", "payment"]

service_state = {
    svc: {
        "cpu": random.randint(10, 40),
        "memory": random.randint(10, 40),
        "incident": False,
        "incident_timer": 0
    }
    for svc in services
}

# randomly trigger incidents
def maybe_trigger_incident():
    if random.random() < 0.05:  # 5% chance
        svc = random.choice(services)
        service_state[svc]["incident"] = True
        service_state[svc]["incident_timer"] = random.randint(10, 30)
        print(f"🔥 INCIDENT STARTED in {svc}")

def update_state(svc):
    state = service_state[svc]

    # incident behavior
    if state["incident"]:
        state["cpu"] += random.randint(5, 15)
        state["memory"] += random.randint(3, 10)
        state["incident_timer"] -= 1

        if state["incident_timer"] <= 0:
            state["incident"] = False
            print(f"✅ INCIDENT RECOVERED in {svc}")

    # normal drift
    else:
        state["cpu"] += random.randint(-2, 3)
        state["memory"] += random.randint(-2, 2)

    # clamp values
    state["cpu"] = max(5, min(100, state["cpu"]))
    state["memory"] = max(5, min(100, state["memory"]))

    return state

# =========================
# SHUTDOWN HANDLER
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
while True:

    maybe_trigger_incident()

    for svc in services:
        state = update_state(svc)

        # inject failure probability during incidents
        if state["incident"]:
            status = random.choices([200, 500], weights=[50, 50])[0]
            latency = random.randint(300, 1200)
        else:
            status = random.choices([200, 500], weights=[95, 5])[0]
            latency = random.randint(50, 300)

        event = {
            "service": svc,
            "status": status,
            "request_time": latency,
            "cpu": state["cpu"],
            "memory": state["memory"]
        }

        producer.send(
            "aiops-stream",
            key=svc.encode(),
            value=event
        )

        print("sent:", event)

    producer.flush()
    time.sleep(1)