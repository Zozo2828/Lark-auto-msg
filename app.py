from flask import Flask, request, jsonify
import json
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info("📩 收到訊息: %s", json.dumps(data, ensure_ascii=False, indent=2))

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    message = event.get("message", {})
    content = json.loads(message.get("content", "{}")).get("text", "")
    logging.info("🧾 解析後文字內容: %s", content)

    if "新增" in content:
        logging.info("📢 偵測到『新增』，你可以在這裡加入通知邏輯")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
