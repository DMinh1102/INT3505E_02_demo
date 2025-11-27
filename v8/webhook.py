# webhook.py
from flask import Blueprint, request, jsonify
import hmac, hashlib, json

webhook_bp = Blueprint("webhook", __name__)

WEBHOOK_SECRET = "MY_WEBHOOK_SECRET"   # change to your own secret


def verify_signature(raw_body, signature):
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@webhook_bp.route("/webhook/notification", methods=["POST"])
def receive_webhook():
    raw_body = request.get_data()
    signature = request.headers.get("X-Signature", "")

    # Optional security: verify signature
    if not verify_signature(raw_body, signature):
        return jsonify({"message": "Invalid signature"}), 401

    payload = request.json
    event = payload.get("event")
    data = payload.get("data")

    print("Webhook received:", event, data)

    # Example handling
    if event == "USER_REGISTERED":
        print("New user registered:", data["username"])

    return jsonify({"status": "ok"})
