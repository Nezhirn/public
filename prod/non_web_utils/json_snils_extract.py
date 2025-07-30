import re

def extract_snils(text):
    # Регулярное выражение для поиска значений после "snils":
    snils_pattern = r'"snils":\s*"(\d{11})"'
    # Найти все совпадения в тексте
    snils_numbers = re.findall(snils_pattern, text)
    return snils_numbers


text = """

"""
snils_numbers = extract_snils(text)

# Вывод списка с переходом на новую строку
file_path = 'C:/Users/Andrew/Documents/cleaned_data.txt'
with open('file_path', 'w', encoding='utf-8') as file:
    file.write(text)

print("Данные успешно записаны в файл 'cleaned_data.txt'.")
