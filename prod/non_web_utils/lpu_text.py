import re

# Исходный текст
text = '''

'''

# Поиск всех значений, начинающихся с minzdrav_ и за которыми следуют цифры
pattern = r'minzdrav_\d+'

# Находим все совпадения
matches = re.findall(pattern, text)

# Выводим результаты
for match in matches:
    print(match)
