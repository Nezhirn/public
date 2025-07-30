import requests
import json
from minzdrav_post import posts
from config import base_url, proxies, nums_mku

from datetime import datetime


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

                snils = personsInfo[0].get('snils')

                target_title = next((item for item in sequenceValue if item.get('stringId') == "dateOfBirthApplicant"), None)
                sec_target_title = next((item for item in sequenceValue if item.get('stringId') == "genderApplicant"), None)
                third_title = next((item for item in sequenceValue if item.get('title') == "Наименование медицинской организации, в которой вы работаете"), None)
                four_title = next((item for item in sequenceValue if item.get('title') == "Должность"), None)
                post = int(four_title.get('value'))
                post = posts[post]
                place_work = third_title.get('sequenceValue')[0].get('value')
                genderApplicant = sec_target_title.get('value')

                if genderApplicant == 'female' or 'FEMALE':
                     genderApplicant = 'Женский'
                elif genderApplicant == 'male' or 'MALE':
                     genderApplicant = 'Мужской'
                     

                dateOfBirth = target_title.get('value')
                fdatebirth = datetime.strptime(dateOfBirth, "%Y-%m-%d")
                fdatebirth = fdatebirth.strftime("%d-%m-%Y")
                claim_id = claim.get('id')
                surname = claim['person'].get('surname')
                firstName = claim['person'].get('firstName')
                middleName = claim['person'].get('middleName')
                currIdentityDoc	= personsInfo[0].get('currIdentityDoc')
                typeCode = currIdentityDoc.get('title')
                serial = currIdentityDoc.get('serial')
                number = currIdentityDoc.get('number')
                fromDate = currIdentityDoc.get('fromDate')
                fromDate = datetime.strptime(fromDate, "%Y-%m-%d")
                fromDate = fromDate.strftime("%d-%m-%Y")
                org	= currIdentityDoc.get('org')
                orgCode	= currIdentityDoc.get('currIdentityDoc')
                email = personsInfo[0].get('contacts')[0].get('value')
                phone = personsInfo[0].get('contacts')[1].get('value')

        



                result = f"""
{mku}
                
Сведения о заявителе

Фамилия : {surname}
Имя : {firstName}
Отчество : {middleName}

Дата рождения : {fdatebirth}
СНИЛС : {snils}
ПОЛ : {genderApplicant}


Документ удостоверяющий личность

Документ : {typeCode}
Серия : {serial}
Номер : {number}
Кем выдан : {org}
Код подразделения : {number}
Дата выдачи : {fromDate}


Сведения о месте работы

Наименование медицинской организации : {place_work}
Должность : {post}
Ставка : 1


Контакты

Телефон для связи : {phone}
Адрес электронной почты : {email}
                """
                print(result)
            else:
                print(f"HTTP ошибка: {response.status_code}")

        except Exception as e:
            print(f"Произошла ошибка при обработке запроса {mku}: {e}")