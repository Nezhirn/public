import re

def clean_text(text):
    # Регулярное выражение для удаления ключей и значений "sex" и "id"
    text = re.sub(r'"(sex|id)":\s*".*?",?\s*', '', text)
    # Регулярное выражение для удаления ключей "birthDate", "name", "patronymic" и "surname"
    text = re.sub(r'"(request_message_id)":\s*', '', text)
    
    # Регулярное выражение для удаления фигурных скобок и запятых
    text = re.sub(r'[{}"]', '', text)
    # Удаление лишних запятых и пробелов
    text = re.sub(r',\s*', '\n', text).strip()
    
    return text

# Пример использования
text = '''
[
  {
    "claim_custom_number": "",
    "fio": "",
    "object_id": "",
    "request_message_id": "",
    "type_request": ""
  }
]
'''

cleaned_text = clean_text(text)

# Запись в файл
file_path = ''
with open('file_path', 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

print("Данные успешно записаны в файл 'cleaned_data.txt'.")
