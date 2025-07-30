
import requests
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
import calendar
import telebot
from collections import defaultdict
import time
from config import username, password, r_url, base_url, API_TOKEN, CHAT_ID

bot = telebot.TeleBot(API_TOKEN)

def send_api(message):
    chat_ids = [CHAT_ID]
    
    for chat_id in chat_ids:
        try:
            sent_message = bot.send_message(chat_id, message)
        except Exception as e:
            print(f"Ошибка отправки в чат {chat_id}: {e}")

def get_mku_list(username, password):
    now = datetime.now()
    year = now.year
    month = now.month - 1
    day = now.day

    formatted_date = datetime(year, month, day).strftime("%Y-%m-%d")

    url = f'{r_url}unreceived_report_{formatted_date}.xls'

    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        with open("unreceived_report.xls", "wb") as f:
            f.write(response.content)

        df = pd.read_excel("unreceived_report.xls", engine="openpyxl")

        mku_list = df["Номер МКУ"].dropna().unique().tolist()

        formatted_mku_list = [f"'{mku}'" for mku in mku_list]
        nums_mku = [mku for mku in mku_list]

        return nums_mku
    else:
        print("Ошибка при скачивании файла:", response.status_code)
        return None


def check_claims_status(username, password):
    nums_mku = get_mku_list(username, password)

    if not nums_mku:
        print("Не удалось получить список МКУ.")
        return

    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }

    services_by_name = defaultdict(list)

    for mku in nums_mku:
        full_url = f"{base_url}{mku}"

        try:
            response = requests.get(full_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                claims = data.get('_embedded', {}).get('claims', [])
                claim = claims[0]
                srgu_name = claim.get('service', {}).get('name')
                status_code = claim.get('currStatus', {}).get('statusCode')

                if status_code == '2':  # Непринятая заявка
                        services_by_name[srgu_name].append(mku)

            else:
                print(f"HTTP ошибка: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке запроса {mku}: {e}")

    date = datetime.now()
    forsend_date = date.strftime("%d-%m-%Y %H:%M:%S") + '\n\n'

    message_short = [forsend_date, 'Непринятые заявки на данный момент:\n\n']
    for service_name, mku_list in services_by_name.items():
        message_short.append(f"{service_name}: {len(mku_list)}\n\n")

    message_detailed = [forsend_date, 'Отчёт с перечнем МКУ:\n\n']
    for service_name, mku_list in services_by_name.items():
        mku_str = '\n'.join(mku_list)
        message_detailed.append(f"{service_name} ({len(mku_list)}):\n\n{mku_str}\n\n")

    # Отправка двух сообщений
    send_api(''.join(message_detailed))
    time.sleep(3)
    send_api(''.join(message_short))
    

check_claims_status(username, password)