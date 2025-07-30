start_id = 433
counts = 14

result = ''

for count in range(counts):
    start_id = start_id + 1
    result = result + str(start_id) + '.' + '\n'
        
print(result)