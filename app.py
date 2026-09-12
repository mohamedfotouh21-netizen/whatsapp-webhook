from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "koshri_webhook_2026"


@app.route("/app.py", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403


@app.route("/app.py", methods=["POST"])
def webhook():
    data = request.get_json()
    print(data)
    return "OK", 200
