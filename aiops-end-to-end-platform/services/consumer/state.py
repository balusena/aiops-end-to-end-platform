from collections import defaultdict, deque
from datetime import datetime, timedelta

windows = defaultdict(lambda: deque(maxlen=200))


def update_window(service, event):
    windows[service].append((datetime.utcnow(), event))


def build_features(service):
    now = datetime.utcnow()
    window = windows[service]

    data = [e for t, e in window if now - t < timedelta(seconds=60)]

    if len(data) < 10:
        return None

    return {
        "service": service,
        "timestamp": now.isoformat(),
        "req_count": len(data),

        "error_rate": sum(1 for d in data if d["status"] >= 500) / len(data),

        "cpu": sum(d["cpu"] for d in data) / len(data),

        "memory": sum(d["memory"] for d in data) / len(data),

        "latency": sum(d["request_time"] for d in data) / len(data),
    }