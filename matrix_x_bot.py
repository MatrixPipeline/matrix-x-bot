from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
DEFAULT_CHAT_ID = os.environ.get("CHAT_ID")  # Optional fallback for outbound messages

@app.route('/', methods=['GET'])
def home():
    return "Matrix XP Bot is Online. 🧠🕶️"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/start"):
            send_message(chat_id, "🧠 Welcome, Morpheus. The Matrix XP Bot is now active.")
        elif text.startswith("/status"):
            send_message(chat_id, "🧬 Portal Status: Awaiting DNS propagation. System: STABLE.")
        elif text.startswith("/oracle"):
            send_message(chat_id, "🔮 The Oracle is silent... for now.")
        else:
            send_message(chat_id, "Neo:/ I'm listening...")

    return "OK"

@app.route('/send', methods=['POST'])
def external_send():
    data = request.get_json()
    message = data.get("text", "")
    chat_id = data.get("chat_id", DEFAULT_CHAT_ID)

    if not chat_id or not message:
        return jsonify({"status": "error", "message": "Missing 'chat_id' or 'text'"}), 400

    response = send_message(chat_id, message)
    return jsonify({"status": "success", "message": "Message sent", "telegram_response": response})

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Telegram API response:", response.json())  # Debug output
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
