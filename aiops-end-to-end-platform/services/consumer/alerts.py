import requests
import time
import os

last_alert = {}

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
PAGERDUTY_ROUTING_KEY = os.getenv("PAGERDUTY_ROUTING_KEY")


def can_alert(service):
    now = time.time()
    if service not in last_alert or now - last_alert[service] > 60:
        last_alert[service] = now
        return True
    return False


def send_slack(features):
    if not SLACK_WEBHOOK_URL:
        return
    try:
        requests.post(
            SLACK_WEBHOOK_URL,
            json={
                "text": f"🚨 ALERT: {features['service']} | error={features['error_rate']:.2f}"
            },
            timeout=3
        )
    except Exception as e:
        print("Slack failed:", e)


def send_pagerduty(features):
    if not PAGERDUTY_ROUTING_KEY:
        return
    try:
        payload = {
            "routing_key": PAGERDUTY_ROUTING_KEY,
            "event_action": "trigger",
            "payload": {
                "summary": f"AIOps anomaly in {features['service']}",
                "severity": "critical",
                "source": "aiops"
            }
        }

        requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            json=payload,
            timeout=3
        )
    except Exception as e:
        print("PagerDuty failed:", e)


def trigger_alerts(features, score):
    if score == -1 and features["error_rate"] > 0.2:
        if can_alert(features["service"]):
            send_slack(features)
            send_pagerduty(features)