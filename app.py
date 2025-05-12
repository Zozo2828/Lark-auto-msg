from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    logging.info("\U0001f4e6 收到原始訊息：%s", json.dumps(data, indent=2, ensure_ascii=False))

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    event = data.get("event", {})
    message = event.get("message", {})
    raw_content_str = message.get("content", "{}")
    logging.info("\U0001f5dc 原始 content 欄位：%s", raw_content_str)

    try:
        msg_raw = json.loads(raw_content_str)
    except Exception as e:
        logging.warning("無法解析 JSON content：%s", e)
        return "ok"

    content = ""
    if "text" in msg_raw:
        content = msg_raw["text"]
    elif "post" in msg_raw:
        content = msg_raw["post"].get("zh_cn", {}).get("title", "[卡片無標題]")

    logging.info("\U0001f4dd 解析後文字內容：%s", content)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
