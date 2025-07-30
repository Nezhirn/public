from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import ReplyKeyboardMarkup
import pyotp

from config import API_TOKEN, CHAT_ID, SECRET

markup = ReplyKeyboardMarkup(resize_keyboard=True).add('/get_token')

bot = AsyncTeleBot(API_TOKEN)

async def send_api(message):
    try:
        await bot.send_message(CHAT_ID, message)
    except Exception as e:
        await bot.send_message(CHAT_ID, e)
        print(f"Ошибка отправки в чат {CHAT_ID}: {e}")

@bot.message_handler(commands=['get_token'])
async def generate_token(message):
        totp_row = pyotp.TOTP(SECRET)
        totp = totp_row.now()
        await send_api(totp)



if __name__ == '__main__':
     asyncio.run(bot.polling(restart_on_change=True))
        

