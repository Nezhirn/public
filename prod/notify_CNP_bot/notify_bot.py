import telebot
import time
from config import chat_ids, API_BOT

#API бота.
bot = telebot.TeleBot(API_BOT, parse_mode='HTML')

def send_api(message):
    
    print('Ты уверен в своём решении? (y/n)')
    resolution = input(str())
    if resolution == 'y':
        for chat_id in chat_ids:
            try:
                sent_message = bot.send_message(chat_id, message)
                print(f"Сообщение в чат {chat_id} отправлено.")
                time.sleep(4)
                #bot.delete_message(chat_id, sent_message.message_id)
                #print(f"Сообщение в чате {chat_id} удалено.")
            except Exception as e:
                print(f"Ошибка отправки в чат {chat_id}: {e}")
    else:
        print('Правильно, ещё раз подумай.')
        return

message = f"""

"""

send_api(message)