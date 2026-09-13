import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "koshri_webhook_2026"
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")


@app.route("/api/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403


@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    print("\n================ WEBHOOK EVENT ================")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("================================================\n")

    try:
        entry = data.get("entry", [])

        for entry_item in entry:
            changes = entry_item.get("changes", [])

            for change in changes:
                value = change.get("value", {})

                # =========================
                # Incoming messages
                # =========================
                messages = value.get("messages", [])

                if messages:
                    print(">>> INCOMING MESSAGE")

                    for message in messages:
                        print("Message ID:", message.get("id"))
                        print("From:", message.get("from"))
                        print("Type:", message.get("type"))

                # =========================
                # Outgoing message statuses
                # =========================
                statuses = value.get("statuses", [])

                if statuses:
                    print(">>> WHATSAPP MESSAGE STATUS")

                    for status in statuses:
                        print("Message ID:", status.get("id"))
                        print("Status:", status.get("status"))
                        print("Recipient:", status.get("recipient_id"))
                        print("Timestamp:", status.get("timestamp"))

                        if status.get("errors"):
                            print("ERRORS:")
                            print(
                                json.dumps(
                                    status.get("errors"),
                                    indent=4,
                                    ensure_ascii=False
                                )
                            )

    except Exception as e:
        print("Webhook processing error:", str(e))

    return "OK", 200
