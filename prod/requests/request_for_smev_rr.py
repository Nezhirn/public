import requests

from config import proxies, SMEV_API_KEY
from config import sm_url as base_url

requestsids = [
'b1f7203c-412a-11f0-bf90-005056b45494'
]


headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'X-API-KEY': SMEV_API_KEY
    }

resps = []

ERRORS_FILE = 'responses.log'

def log_responses(message: str) -> None:
    """Дописать одну строку в журнал ошибок."""
    with open(ERRORS_FILE, 'a', encoding='utf-8') as f:   # режим append!
        f.write(message + '\n')

for req in requestsids:
        full_url = f"{base_url}{req}"
        try:
            response = requests.get(full_url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                data = response.json()
                #print(data)
                print(f'response for {req}: {data.get('response')} \n\n')
                #resps.append(f'response for {req}: {data.get('response')} \n\n')
                #log_responses(f'response for {req}: {data.get('response')} \n\n')
                

            else:
                print(f"HTTP ошибка: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке запроса {req}: {e}")