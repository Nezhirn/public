import requests
import time

TOKEN = ""
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

# ID последних обновлений, чтобы не получать старые сообщения
last_update_id = 0
known_chats = {}

while True:
    try:
        params = {
            "offset": last_update_id + 1,
            "timeout": 10  # Long polling
        }
        response = requests.get(URL, params=params)
        data = response.json()

        if data["ok"]:
            for result in data["result"]:
                last_update_id = result["update_id"]

                message = result.get("message") or result.get("channel_post")
                if not message:
                    continue

                chat = message["chat"]
                chat_id = chat["id"]
                chat_type = chat["type"]
                title = chat.get("title") or chat.get("username") or chat.get("first_name", "Unknown")

                if chat_id not in known_chats:
                    known_chats[chat_id] = title
                    print(f"Новое взаимодействие:\nID: {chat_id}\nТип: {chat_type}\nНазвание: {title}\n")

    except Exception as e:
        print(f"Ошибка: {e}")

    time.sleep(1)
