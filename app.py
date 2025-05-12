from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)

# === Lark 基本設定 ===
APP_ID = "cli_a897c38c52b8d029"
APP_SECRET = "nDlF541TrIb2S7Fq1wMcsdCQ1mSmEkG8"
CHAT_ID = "oc_26ce9e9628f0f869d598dae7dcdd6fca"

# === 取得 token ===
def get_access_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    res = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    data = res.json()
    return data.get("tenant_access_token") if data.get("code") == 0 else None

# === 取得群組訊息 ===
def get_group_messages(token, limit=10):
    url = "https://open.larksuite.com/open-apis/im/v1/messages"
    params = {
        "container_id_type": "chat",
        "container_id": CHAT_ID,
        "page_size": limit
    }
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers, params=params).json()

# === 傳訊息回群組 ===
def reply_to_group(text, token):
    url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    return requests.post(url, headers=headers, json=body).status_code == 200

# === 檢查是不是 Lark Base 的卡片訊息 ===
def is_base_card(msg):
    return msg.get("sender", {}).get("sender_type") == "app" and msg.get("message_type") == "post"

def extract_card_title(content_str):
    try:
        content = json.loads(content_str)
        return content.get("post", {}).get("zh_cn", {}).get("title", "")
    except:
        return "[解析失敗]"

# === Webhook 入口 ===
@app.route("/webhook", methods=["POST"])
def webhook():
    token = get_access_token()
    if not token:
        return jsonify({"error": "取得 token 失敗"}), 500

    result = get_group_messages(token)
    found = []
    for msg in result.get("items", []):
        if is_base_card(msg):
            ts = int(msg["create_time"]) // 1000
            tstr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
            content = msg.get("body", {}).get("content", "")
            title = extract_card_title(content)
            found.append(f"{tstr}｜{title}")

    if found:
        reply = "⚠️ 偵測到 Lark Base 卡片：\\n" + "\\n".join(found)
        reply_to_group(reply, token)
        return jsonify({"status": "sent", "cards": found})
    else:
        return jsonify({"status": "ok", "message": "沒有找到 Base 卡片"})

# === 啟動 Flask ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
