from flask import Flask, request, jsonify
import requests
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# TODO: 設定你的 Lark token & chat_id
TENANT_ACCESS_TOKEN = "<你的 tenant_access_token>"
CHAT_ID = "<你的群組 chat_id>"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info("✅ 收到訊息: %s", data)

    # 嘗試抓出文字訊息或卡片內容
    try:
        event = data.get("event", {})
        message = event.get("message", {})
        raw_content_str = message.get("content", "{}")
        msg_type = message.get("message_type", "")
        content_raw = json.loads(raw_content_str)

        if msg_type == "text":
            content = content_raw.get("text", "")
            logging.info("💬 純文字內容: %s", content)

        elif msg_type == "interactive":
            title = content_raw.get("title", "")
            logging.info("📌 卡片標題: %s", title)
            # 可以加上自動通知的動作，例如 call API

    except Exception as e:
        logging.error("❌ 錯誤: %s", e)

    return "ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
