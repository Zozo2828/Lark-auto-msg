from flask import Flask, request
import requests
import json

app = Flask(__name__)

ANYCROSS_URL = "https://open-sg.larksuite.com/anycross/trigger/callback/MDVhOTM4YWZlNmNkYTYxMDcxNDVmNWRjMTNiY2Q4N2U0"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    event = data.get("event", {})
    message = event.get("message", {})
    msg_type = message.get("message_type", "")
    content_str = message.get("content", "{}")

    if msg_type == "interactive":
        try:
            content = json.loads(content_str)
            title = content.get("title", "無標題卡片")
            message_id = message.get("message_id")
            ts = message.get("create_time")

            requests.post(ANYCROSS_URL, json={
                "title": title,
                "message_id": message_id,
                "timestamp": ts
            })

            print(f"✅ 轉送卡片到 Anycross：{title}")

        except Exception as e:
            print(f"❌ 卡片處理失敗：{e}")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
