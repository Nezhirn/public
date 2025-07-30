import requests
import json
import time
from datetime import datetime
from statuses import claim_ids_to_process   # ← ваш список словарей
from config import proxies

ERRORS_FILE = 'errors.log'  # имя журнала


def log_error(message: str) -> None:
    """Дописать одну строку в журнал ошибок."""
    with open(ERRORS_FILE, 'a', encoding='utf-8') as f:   # режим append!
        f.write(message + '\n')

def send_post_request(item: dict) -> None:
    url = "https://gu.cnp.mosreg.ru/api/services/status"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/problem+json"
    }
    payload = {
        "claim_id":  item["claim_id"],
        "status_id": item["status_id"]
    }

    try:
        response = requests.post(url, headers=headers,
                                 json=payload, proxies=proxies)
    except requests.RequestException as exc:
        err_msg = (f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
                   f"Сетевая ошибка для claim_id {item['claim_id']}: {exc}")
        print(err_msg)
        log_error(err_msg)
        return

    try:
        data = response.json()
    except ValueError:
        data = response.text        # ответ не JSON

    if response.status_code in (200, 204):
        print(f"✅ OK claim_id {item['claim_id']}\n"
              f"{json.dumps(data, ensure_ascii=False)}\n")
    else:
        err_msg = (f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
                   f"Ошибка {response.status_code} для claim_id {item['claim_id']}:\n"
                   f"{json.dumps(data, ensure_ascii=False)}")
        print(err_msg + '\n')
        log_error(err_msg)

# ── точка входа ──────────────────────────────────────────────────────────
# отделяем запуск в логе визуальным разделителем
log_error(f"\n===== Запуск {datetime.now():%Y-%m-%d %H:%M:%S} =====")

for item in claim_ids_to_process:
    send_post_request(item)
    # time.sleep(0.2)  # при необходимости пауза между запросами

print(f"\nГотово! Все ошибки (если были) дописаны в «{ERRORS_FILE}».")
