from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # ✅ Log 整包收到的 JSON 資料
    print("\n📩 收到訊息 (原始資料):")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})

    # ✅ 拆解文字內容
    event = data.get("event", {})
    message = event.get("message", {})
    content = json.loads(message.get("content", "{}")).get("text", "")

    print(f"🧾 解析後文字內容: {content}")

    if "新增" in content:
        print("📢 偵測到『新增』，你可以在這裡加入通知邏輯！")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
