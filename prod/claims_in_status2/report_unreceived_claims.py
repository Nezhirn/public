import requests
import pandas as pd
from datetime import datetime
from requests.auth import HTTPBasicAuth
from collections import Counter
import calendar

from config import username, password, r_url, base_url



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

    names_count = Counter()

    for mku in nums_mku:
        full_url = f"{base_url}{mku}"

        try:
            response = requests.get(full_url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                claims = data.get('_embedded', {}).get('claims', [])
                if claims:
                    claim_number = claims[0].get('customClaimNumber')
                    srgu_name = claims[0].get('service', {}).get('name')

                    # Проверка статуса заявки
                    if claims[0].get('currStatus', {}).get('statusCode') == '2':  # статус 2
                        names_count[srgu_name] += 1

            else:
                print(f"HTTP ошибка: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке запроса {mku}: {e}")

    print('Непринятые заявки на данный момент:\n')
    for service_name, count in names_count.items():
        print(f"{service_name}: {count}\n")

check_claims_status(username, password)
