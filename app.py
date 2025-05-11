from flask import Flask, request, jsonify
import json
import sys
import logging
import requests

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
    msg_raw = json.loads(message.get("content", "{}"))
    text = msg_raw.get("text", "")

    # 🧠 處理卡片訊息（post 類型）
    if "post" in msg_raw:
        try:
            post = msg_raw["post"]["zh_cn"]
            title = post.get("title", "")
            body_text = " ".join([
                item["text"]
                for line in post["content"]
                for item in line if item.get("tag") == "text"
            ])
            content = f"{title} {body_text}"
        except Exception as e:
            content = "[無法解析卡片]"
    else:
        content = text

    logging.info("🧾 解析後文字內容: %s", content)

    if "新增" in content:
        logging.info("📢 偵測到『新增』，你可以在這裡加入通知邏輯")

        # 範例：轉發給 AnyCross（請換上你自己的 URL）
        anycross_url = "https://open-sg.larksuite.com/anycross/trigger/your_webhook"
        try:
            res = requests.post(anycross_url, json=data)
            logging.info("✅ 已轉發到 AnyCross，狀態碼: %s", res.status_code)
        except Exception as e:
            logging.error("❌ 轉發 AnyCross 失敗: %s", str(e))

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

