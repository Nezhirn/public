# Пример данных
list1 = [
('1INN', '1FIO'),
('2INN', '2FIO')
]
list2 = [
'1INN',
'2INN'
]

# Инициализация пустых списков
inn1 = []
name = []
result = []
seen_inn = set() 

# Сопоставляем ИНН из list1 с list2
for inn, full_name in list1:
    if inn in list2:
        if inn not in seen_inn:  # Проверяем, был ли этот ИНН уже добавлен
            inn1.append(inn)
            name.append(full_name)
            result.append(f"{inn} {full_name}")
            seen_inn.add(inn)  # Добавляем ИНН в множество, чтобы избежать дублирования

# Вывод результатов
print("Сопоставленные ИНН и ФИО:")
for item in result:
    print(item)