from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import string
import random
import uuid


app = FastAPI()

@app.get("/generate_password", summary="Функция генерации 1 пароля", tags=["Генерация паролей"])
def generate_password(length: int):
    punctuation_without_brackets = ''.join(ch for ch in string.punctuation if ch not in ",'<>`{}[]")
    characters = string.ascii_letters + string.digits + punctuation_without_brackets
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.get("/generate_passwords/{length}/{counts}", summary="Функция генерации множества паролей", tags=["Генерация паролей"])
def generate_passwords(length: int, counts: int):
    passwords = []
    for _ in range(counts):
        password = generate_password(length)
        passwords.append(password)
    return passwords

@app.get("/generate_uuid/{counts}", summary="Функция генерации UUID", tags=["Генерация паролей"])
def generate_uuids(counts: int):
    uuids = []
    for _ in range(counts):
        oneuid = str(uuid.uuid4())
        uuids.append(oneuid)
    return uuids

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="",
        port=443,
        reload=True,
        ssl_keyfile="",
        ssl_certfile=""
    )