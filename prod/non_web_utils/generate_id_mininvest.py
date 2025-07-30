start_id = 1425
counts = 112
service= 'franchises'

while True:
    for i in range(counts):
        id_value = f"{service}_{start_id + i}"
        print(id_value)
    break