import telebot

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['check'])
def send_ip(message):
    raw_message = str(message)
    bot.send_message(message.chat.id, raw_message)

if __name__ == '__main__':
    bot.polling(restart_on_change=True)
