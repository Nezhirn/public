import requests
from config import token as bearer_token
from config import p_url

def modify_process_instance(objects_process, bearer_token, activity_id):
    for index, it in enumerate(objects_process):
        try:
            response = requests.post(
                url=f"{p_url}{it}/modification",
                json={
                    "instructions": [
                        {
                            "type": "startBeforeActivity",
                            "activityId": activity_id,
                        }
                    ]
                },
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': bearer_token
                }
            )
            
            # Обработка ответа
            if response.status_code == 200:
                print(f"Processed index: {index}, Success: {response.json()}")               
            elif response.status_code == 204:
                print(f"Processed index: {index}, Success: {response.status_code},{response.json()}") 
            else:
                print(f"Processed index: {index}, Error: {response.status_code}, Message: {response.text}")
        
        except requests.exceptions.RequestException as e:
            print(f"Processed index: {index}, Exception occurred: {e}")

# Параметры для вызова функции
objects_process = [

]  # Список объектов для обработки
activity_id = "Activity_0hxv61d"  # ID задания

modify_process_instance(objects_process, bearer_token, activity_id)