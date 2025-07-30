class Author:
    def __init__(self, name, age):
        self.name = name  # Убираем запятую
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age}"


class Book:
    def __init__(self, title, author, year):
        self.title = title  # Убираем запятую
        self.author = author
        self.year = year

    def __str__(self):
        return f"{self.title}, {self.author.name}, {self.year}"


author1 = Author('Вотан', '∞')
author2 = Author('Андрей', '2003')
author3 = Author('Теодор Драйзер', '2003')
book1 = Book('Старшая эдда', author1, '1270')
book2 = Book('Зов волка', author2, '1334')
book3 = Book('Неудачная книга', author3, '1488')

print(book3.author)  # Теперь вывод будет более читаемым