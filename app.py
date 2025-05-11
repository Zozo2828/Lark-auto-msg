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
    content = ""

    # 嘗試抓 text（純文字訊息）
    if "text" in msg_raw:
        content = msg_raw["text"]

    # 如果是 post 類型（卡片訊息）
    elif "post" in msg_raw:
        post_obj = msg_raw["post"]
        lang = "zh_cn" if "zh_cn" in post_obj else "en_us" if "en_us" in post_obj else None
        if lang:
            try:
                post = post_obj[lang]
                title = post.get("title", "")
                body_text = " ".join([
                    item["text"]
                    for line in post["content"]
                    for item in line if item.get("tag") == "text"
                ])
                content = f"{title} {body_text}"
            except Exception as e:
                content = "[解析 post 卡片失敗]"
        else:
            content = "[無法讀取語系]"

    else:
        content = "[無法擷取文字]"

    logging.info("🧾 解析後文字內容: %s", content)

    if "新增" in content:
        logging.info("📢 偵測到『新增』，你可以在這裡加入通知邏輯")

        anycross_url = "https://open-sg.larksuite.com/anycross/trigger/your_webhook"
        try:
            res = requests.post(anycross_url, json=data)
            logging.info("✅ 已轉發到 AnyCross，狀態碼: %s", res.status_code)
        except Exception as e:
            logging.error("❌ 轉發 AnyCross 失敗: %s", str(e))

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
