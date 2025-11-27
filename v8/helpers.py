import requests
import hmac, hashlib, json

WEBHOOK_URL = "http://127.0.0.1:5000/webhook/notification"  # change to your URL
WEBHOOK_SECRET = "MY_WEBHOOK_SECRET"


def send_webhook(event, data):
    body = json.dumps({
        "event": event,
        "data": data
    })

    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature": signature
    }

    try:
        requests.post(WEBHOOK_URL, data=body, headers=headers, timeout=3)
    except Exception as e:
        print("Webhook failed:", e)
