import requests
import time
import json

from statuses import claim_ids_to_process
from config import proxies, cl_url

def send_post_request(claim_id):
    # URL для отправки POST-запроса
    url = cl_url

    # Заголовки запроса
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/problem+json"
    }

    # Тело запроса (payload)
    payload = {
        "claim_id": claim_id  # Используем переданное значение claim_id
    }
    dir = '/home/andrew/sshfs/samba/files/Codes/Python/Запрос/'

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=payload, proxies=proxies)

    # Проверка статуса ответа
    try:
        data = response.json()
        
        if response.status_code == 200 or response.status_code == 204:
            print(f"Запрос для claim_id '{claim_id}' успешно выполнен!\n Ответ:\n{json.dumps(data, ensure_ascii=False)}\n")
        else:
            print(f"Ошибка при выполнении запроса для claim_id '{claim_id}': {response.status_code}\n Ответ от сервера:\n{json.dumps(data, ensure_ascii=False)}\n")
    
    except ValueError as e:
        print(f"Произошла ошибка при обработке ответа от сервера для claim_id '{claim_id}': {e}\n Текст ответа от сервера:\n{response.text}\n")
    

for claim_id in claim_ids_to_process:
    send_post_request(claim_id)
    time.sleep(1)
