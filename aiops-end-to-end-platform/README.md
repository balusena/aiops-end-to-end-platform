# 🚀 Real-Time AIOps Monitoring & Anomaly Detection System using Kafka, ML, and Observability Stack

## Overview
End-to-end AIOps pipeline using Kafka, ML, and Elasticsearch for real-time anomaly detection.

---

## Architecture
Kafka → Stream Processor → Feature Engine → ML Model → Elasticsearch → Alerts

## Project Tree Structure
'''

aiops-streaming-ml-project/
│
├── services/
│   │
│   ├── producer/                     # Simulates real-world service telemetry
│   │   ├── producer.py               # Generates fake service metrics and sends to Kafka
│   │   ├── Dockerfile                # Container setup for producer service
│   │   └── requirements.txt          # Python dependencies for producer
│   │
│   ├── consumer/                     # Core AIOps streaming + ML system
│   │   ├── app.py                    # Main pipeline: Kafka → ML → alerts
│   │   ├── state.py                  # Sliding window for feature engineering
│   │   ├── ml.py                     # Isolation Forest anomaly detection
│   │   ├── alerts.py                 # Slack + PagerDuty alerts
│   │   ├── otel.py                   # OpenTelemetry tracing
│   │   ├── metrics.py                # Prometheus metrics
│   │   ├── __init__.py               # ✅ IMPORTANT (empty file)
│   │   ├── Dockerfile                # Container setup
│   │   └── requirements.txt          # Dependencies
│
├── infra/                            # Infrastructure config (Docker + OTel)
│   ├── docker-compose.yml            # Main orchestration file
│   └── otel-collector.yaml           # OTel → Jaeger config
│
├── monitoring/                       # Observability
│   ├── prometheus.yml                # Metrics scraping config
│   └── grafana_dashboard.json        # Dashboard definition
│
├── tracing/                          # Optional standalone configs
│   └── jaeger-config.yaml
│
├── models/                           # (future use) ML model storage
│
├── docs/
│   └── architecture.png              # System diagram (very useful for portfolio)
│
└── README.md                         # Project explanation


'''

---

## Tech Stack
- Kafka
- Python
- Scikit-learn (Isolation Forest)
- Elasticsearch
- OpenTelemetry

---

## Features
- Real-time streaming
- Sliding window feature engineering
- ML anomaly detection
- Observability-ready design

---

## How to Run

```bash
docker-compose up -d
python producer.py
python aiops_stream_processor.py

- This system simulates a real-time AIOps pipeline by generating application metrics and sending them through a streaming platform. A producer continuously publishes synthetic service data (like latency, CPU, and error rates) into a Kafka topic. A consumer ingests this stream, aggregates recent data into a sliding window, and extracts features for analysis. It uses a machine learning model (Isolation Forest) to detect anomalies in real time and identifies unusual system behavior. When anomalies are detected, it triggers alerts and exposes metrics for monitoring via Prometheus.

docker --version
docker-compose --version
python --version

Note: If Kafka images fail, Docker must have at least 6–8 GB RAM allocated.

# =========================
# 1. GO TO PROJECT
# =========================
cd aiops-streaming-ml-project/infra


# =========================
# 2. BUILD EVERYTHING
# =========================
docker-compose build


# =========================
# 3. START SYSTEM (DETACHED MODE)
# =========================
docker-compose up -d


# =========================
# 4. CHECK RUNNING SERVICES
# =========================
docker ps


# =========================
# 5. FOLLOW LOGS (OPTIONAL DEBUG)
# =========================

# Kafka logs
docker logs -f kafka

# Producer logs
docker logs -f producer

# Consumer logs (AIOps ML engine)
docker logs -f consumer


# =========================
# 6. PROMETHEUS UI
# =========================
# Open in browser:
Prometheus - http://localhost:9090
Metrics endpoint - http://localhost:8000/metrics
Jaeger - http://localhost:16686

# =========================
# 7. PROMETHEUS QUERIES
# =========================

aiops_events_total
aiops_anomalies_total
aiops_error_rate


# =========================
# 8. RESTART SERVICE (IF NEEDED)
# =========================
docker restart consumer


# =========================
# 9. STOP SYSTEM
# =========================
docker-compose down


# =========================
# 10. FULL CLEAN RESET
# =========================
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

1. docker-compose build
2. docker-compose up
3. producer sends events
4. Kafka streams data
5. consumer processes ML
6. Prometheus scrapes metrics
7. alerts trigger if anomaly

#Final Flow
Kafka Event
   ↓
Sliding Window (state)
   ↓
Feature Engineering
   ↓
ML Inference (Isolation Forest)
   ↓
Alerting (Slack + PagerDuty)
   ↓
Observability (OTEL spans + Prometheus metrics)

🔥 WHAT YOU ACHIEVED
You now have:
✔ Real-time streaming pipeline
✔ ML anomaly detection system
✔ Observability with Prometheus
✔ Event-driven architecture
✔ Production-style DevOps setup

============

🧠 If you implement this project properly, what outputs you will see:

Your system will produce 4 main visible outputs 👇

1️⃣ 📊 Kafka Event Flow (data moving)
Apache Kafka

👉 You will see:
- producer sending events
- consumer receiving events

✔ Logs like:
- "event sent"
- "event consumed"


2️⃣ 🤖 ML anomaly detection output

👉 Your ML (Isolation Forest) will output:
- NORMAL event ✅
- ANOMALY event ❌

✔ Example:
- "request latency abnormal"
- "traffic spike detected"


3️⃣ 🚨 Alerts (real output)

Your alerts service will send:
- Slack message
- PagerDuty alert

✔ Example:
- "⚠️ Anomaly detected in consumer latency"


4️⃣ 📊 Monitoring dashboards

Using:
Prometheus + Grafana

👉 You will see:
- CPU usage graphs
- request rate
- latency spikes
- error rate


🔥 Final simple answer:

👉 Your project output =
✔ Kafka event flow logs
✔ ML anomaly predictions
✔ Alert notifications
✔ Grafana dashboards (live system health)


🧠 Now portfolio lo ela petali?

📄 README lo show cheyyali:
- architecture diagram
- "Kafka → ML → Alerts" flow
- screenshots of:
  - Grafana dashboard
  - alert messages
  - logs


💡 One line summary:

👉 “This project shows real-time streaming data processing, ML-based anomaly detection, and automated alerting with full observability dashboards.”

===============

⚠️ What you MAY be missing (important for “top-tier” level)

1️⃣ Data persistence (optional but strong)
Right now unclear:
👉 Where raw events stored long-term?

You can add:
- time-series DB or storage layer
- logs storage
- feature store


2️⃣ Failure handling (very important in real systems)

You should ideally have:
- retry logic
- dead-letter queue (DLQ)
- Kafka consumer error handling

👉 This makes it production-grade


3️⃣ Model lifecycle (MLOps missing piece)

You have ML, but maybe missing:
- model saving/loading strategy
- retraining pipeline
- versioning

👉 This is what makes it “real ML system”


4️⃣ Load / stress testing (nice-to-have)

- simulate high traffic
- see system behavior under load


5️⃣ Clear architecture explanation (VERY important for interviews)

Make sure README clearly shows:

👉 Producer → Kafka → Consumer → ML → Alerts  
👉 plus Observability side layer


🧠 Final honest verdict

👉 You did 90% of a strong AIOps system

You already have:
✔ streaming system  
✔ ML pipeline  
✔ monitoring  
✔ alerting  

Missing only:
- production hardening (retry/DLQ)
- ML lifecycle (retraining/versioning)
- storage layer (optional)