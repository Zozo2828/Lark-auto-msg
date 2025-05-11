import requests
import json

# 🔐 應用憑證
APP_ID = "cli_a897c38c52b8d029"
APP_SECRET = "nDlF541TrIb2S7Fq1wMcsdCQ1mSmEkG8"

# 💬 群組 ID（chat_id）
CHAT_ID = "oc_26ce9e9628f0f869d598dae7dcdd6fca"

def get_app_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    res = requests.post(url, json=payload)
    data = res.json()
    if data.get("code") == 0:
        return data["app_access_token"]
    else:
        print("❌ token 失敗:", data)
        return None

def get_group_messages(chat_id, token, limit=20):
    url = f"https://open.feishu.cn/open-apis/im/v1/messages"
    params = {
        "container_id_type": "chat",
        "container_id": chat_id,
        "page_size": limit
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers, params=params)
    return res.json()

def is_lark_base_msg(item):
    sender_type = item.get("sender", {}).get("sender_type")
    msg_type = item.get("message_type")
    return sender_type == "app" and msg_type == "post"

def parse_post_content(content_str):
    try:
        parsed = json.loads(content_str)
        if "post" in parsed:
            lang = "zh_cn" if "zh_cn" in parsed["post"] else "en_us"
            post = parsed["post"][lang]
            title = post.get("title", "")
            body = " ".join([
                i["text"] for line in post["content"]
                for i in line if i.get("tag") == "text"
            ])
            return title, body
    except Exception as e:
        return "[解析失敗]", str(e)

if __name__ == "__main__":
    token = get_app_access_token(APP_ID, APP_SECRET)
    if token:
        print("🚀 Token OK，開始拉訊息")
        result = get_group_messages(CHAT_ID, token)
        items = result.get("items", [])
        for msg in items:
            if is_lark_base_msg(msg):
                print("📦 [來自 Lark Base 的卡片]")
                ts = msg.get("create_time")
                content_raw = msg.get("body", {}).get("content", "{}")
                title, body = parse_post_content(content_raw)
                print(f"🕒 時間: {ts}")
                print(f"📝 標題: {title}")
                print(f"📋 內容: {body}")
                print("-" * 40)
