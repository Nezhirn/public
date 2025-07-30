import re
import json

# Исходный текст
text = '''


'''

# Поиск всех JSON строк внутри основного текста
json_pattern = r'\{.*?\}'

# Найти все JSON строки
json_matches = re.findall(json_pattern, text)

values = []

for json_string in json_matches:
    # Заменяем двойные экранированные кавычки
    cleaned_json_string = json_string.replace('""', '"')
    
    # Преобразуем строку в словарь
    try:
        data = json.loads(cleaned_json_string)
        
        # Извлекаем значение "value"
        value = data.get("value", None)
        
        if value:
            # Декодируем Unicode-последовательности
            decoded_value = json.loads(f'"{value}"')
            values.append(decoded_value)
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")

# Вывод всех найденных значений
for val in values:
    print(val)

# Если значения не найдены
if not values:
    print("Значения 'value' не найдены.")
