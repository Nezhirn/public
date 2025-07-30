import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils import notify_upcoming
from bot import bot
import handlers  # Убедитесь, что хендлеры регистрируются при импорте


async def main():
    
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(notify_upcoming, CronTrigger(hour=9, minute=0))
    scheduler.start()
    print("Бот запущен")
    await bot.infinity_polling(restart_on_change=True)
    #restart_on_change=True
    

if __name__ == '__main__':
    asyncio.run(main())
