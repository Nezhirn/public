import string
import random

punctuation_without_brackets = ''.join(ch for ch in string.punctuation if ch not in ",'<>`{}[]")

def generate_password(length):
    characters = string.ascii_letters + string.digits + punctuation_without_brackets
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f'{password}')
    return password

count = 1

for _ in range(count):
    generate_password(24)
