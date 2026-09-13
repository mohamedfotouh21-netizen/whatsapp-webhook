import os
import requests
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
    data = request.get_json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        messages = value.get("messages", [])

        if not messages:
            return "OK", 200

        message = messages[0]

        # نتعامل حاليًا مع الرسائل النصية فقط
        if message.get("type") != "text":
            return "OK", 200

        customer_number = message["from"]
        message_text = message["text"]["body"]

        # رقم WhatsApp Business الذي استقبل الرسالة
        phone_number_id = value["metadata"]["phone_number_id"]

        reply_text = f"أهلاً بك 👋 وصلت رسالتك: {message_text}"

        url = f"https://graph.facebook.com/vXX.X/{phone_number_id}/messages"

        headers = {
            "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": customer_number,
            "type": "text",
            "text": {
                "body": reply_text
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        print("WhatsApp API status:", response.status_code)
        print("WhatsApp API response:", response.text)

    except Exception as e:
        print("Webhook error:", str(e))

    return "OK", 200
