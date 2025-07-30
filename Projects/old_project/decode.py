

def decode_unicode_escape(unicode_str):
    return unicode_str.encode('latin1').decode('unicode_escape')

# Пример использования
encoded_string = r'\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u043e\u0442\u0434\u0430\u0447\u0438'
decoded_string = decode_unicode_escape(encoded_string)

print(decoded_string)  # Вывод: Начать тест