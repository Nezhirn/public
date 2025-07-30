import requests

from config import rldd_uuids, proxies, token
from config import s_url as url
    
def send_status_updates(rldd_uuids):
    # URL и заголовки
    headers = {
        'accept': '*/*',
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    # Отправка запросов
    for rldd_uuid in rldd_uuids:
        payload = {
            "rldd_uuid": rldd_uuid,
            "status_code": '4',
            "comment": ''
        }
        
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        
        # Обработка ответа
        if response.status_code == 200:
            print(f"Успешно отправлено для {rldd_uuid}: {response.json()}")
        else:
            print(f"Ошибка для {rldd_uuid}: {response.status_code}, {response.text}")

send_status_updates(rldd_uuids)
