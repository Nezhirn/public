from initdb import *
import asyncio

try:
    asyncio.run(init_db())
except KeyboardInterrupt:
    print('Инициализация не выполнена')