import os
import time
import json
import requests
from flask import Flask, jsonify

app = Flask(__name__)

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
CHAT_ID = os.getenv("CHAT_ID")

# 快取 token 和過期時間
TOKEN_CACHE = {
    "token": None,
    "expire_at": 0
}

def get_tenant_access_token():
    now = int(time.time())
    if TOKEN_CACHE["token"] and now < TOKEN_CACHE["expire_at"]:
        return TOKEN_CACHE["token"]

    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    resp = requests.post(url, json=payload)
    data = resp.json()

    if data.get("code") != 0:
        raise Exception(f"Failed to get token: {data}")

    token = data["tenant_access_token"]
    expire = data["expire"]  # 有效秒數
    TOKEN_CACHE["token"] = token
    TOKEN_CACHE["expire_at"] = now + expire - 60  # 提前一分鐘過期

    return token

@app.route("/fetch-messages", methods=["GET"])
def fetch_messages():
    token = get_tenant_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://open.larksuite.com/open-apis/im/v1/messages"

    params = {
        "container_id_type": "chat",
        "container_id": CHAT_ID,
        "page_size": 10  # 調整你要拿幾筆
    }

    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
