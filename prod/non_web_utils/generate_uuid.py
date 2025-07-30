import uuid

counts = int(71)

def generate_uuids(counts):
    uuids = ''
    for _ in range(counts):
        oneuid = str(uuid.uuid4())
        fuid = str(oneuid + '\n')
        uuids += fuid
    return uuids

uuids = generate_uuids(counts)

print(uuids)
    







