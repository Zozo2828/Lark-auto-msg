from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 收到訊息:", data)

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    message = event.get("message", {})
    content = json.loads(message.get("content", "{}")).get("text", "")

    if "新增" in content:
        print("🚨 有人說了『新增』，你可以在這裡加上通知邏輯")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
