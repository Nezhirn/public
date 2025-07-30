# main.py
import asyncio
from bot import bot
from handlers import common, download_local, link # Убедитесь, что все ваши хендлеры импортируются, чтобы они зарегистрировались

async def main():
    print("Бот запущен")
    await bot.infinity_polling(restart_on_change=False)

if __name__ == '__main__':
    asyncio.run(main())