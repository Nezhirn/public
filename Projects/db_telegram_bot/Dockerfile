FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean
RUN apt-get install nano

# Создание рабочей директории
WORKDIR /app

# Копируем зависимости и исходники
COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Команда запуска
CMD ["python", "main.py"]
