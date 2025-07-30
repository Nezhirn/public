import requests
import json

from config import proxies, base_url, nums_mku



headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }


for mku in nums_mku:
        full_url = f"{base_url}{mku}"


        try:
            response = requests.get(full_url, headers=headers, proxies=proxies)

            if response.status_code == 200:
                data = response.json()
                claims = data.get('_embedded', {}).get('claims', [])

                claim = claims[0]
                fields = claim.get('fields')
                srgu_name = claim.get('service', {}).get('name')
                status_code = claim.get('currStatus', {}).get('statusCode')
                sequenceValue = fields.get('sequenceValue')
                customClaimNumber = claim.get('customClaimNumber')
                personsInfo = claim.get('personsInfo')
                claim_id = claim.get('id')
                print(f'{mku}: {status_code} \n\n')
            else:
                print(f"HTTP ошибка: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке запроса {mku}: {e}")






