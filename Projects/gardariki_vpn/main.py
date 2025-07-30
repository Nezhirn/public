import telebot
import json
import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


bot = telebot.TeleBot('')  # ← замени на свой токен
SMS_PHONE = ""
dir = os.getcwd() + '/Python/Projects/gardariki_vpn/'

def load_users():
    try:
        with open(os.path.join(dir, "ids.json"), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(os.path.join(dir, "ids.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def get_user_login(message):
    return message.from_user.username

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_login = get_user_login(message) or 'Гость'
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/key', '/how_long')
    msg = f"""
    Привет, {user_login}! Ты запустил бот-помощник по подключению к VPN.
Тут ты можешь получить ссылку на подключение с помощью команды /key .
Также можешь узнать, когда нужно продлевать аренду сервера, чтобы продлить доступ к VPN. Команда: /how_long .

Бот за 2 суток до дня продления аренды автоматически отсылает уведомление о том, что срок аренды нужно продлевать.

По всем интересуюим вопросам ходи к @wolf_of_wotan
    """

    bot.send_message(message.chat.id,
                     msg,
                     reply_markup=markup)

@bot.message_handler(commands=['key'])
def take_access(message):
    user_login = get_user_login(message)
    if not user_login:
        bot.send_message(message.chat.id,
                         "У тебя не установлен username в Telegram. Установи его, чтобы получить доступ.")
        return

    users = load_users()
    profile = users.get(user_login)
    if not profile:
        bot.send_message(message.chat.id, f"Тебя нет в перечне помощников в аренде сервера. Для получения доступа отправь 300 рублей по СБП (Т-Банк) на номер телефона {SMS_PHONE}.")
        return

    # Сохраняем chat_id, если его ещё нет
    if 'chat_id' not in profile:
        profile['chat_id'] = message.chat.id
        save_users(users)

    bot.send_message(message.chat.id, f"{user_login}, ты солнышко! Спасибо тебе за помощь в аренде. Вот твоя ссылка: {profile['link']}")

@bot.message_handler(commands=["me"])
def whoami(message):
    user_login = get_user_login(message)
    bot.reply_to(message,
                 f"Твой логин: {user_login}, ID: {message.from_user.id}")

@bot.message_handler(commands=['how_long'])
def how_long(message):
    user_login = get_user_login(message)
    users = load_users()
    profile = users.get(user_login)

    if not profile or 'date_required' not in profile:
        bot.send_message(message.chat.id,
                         "Информация о дате продления не найдена.")
        return

    due_date = datetime.datetime.strptime(profile['date_required'], "%Y-%m-%d").date()
    today = datetime.date.today()
    delta = (due_date - today).days

    if delta < 0:
        bot.send_message(message.chat.id,
                         f"Срок аренды истёк {abs(delta)} дней назад ({due_date}).")
    elif delta == 0:
        bot.send_message(message.chat.id,
                         f"Сегодня последний день аренды: {due_date}!")
    else:
        bot.send_message(message.chat.id,
                         f"До продления аренды осталось {delta} дн. (до {due_date}).")

def notify_upcoming():
    users = load_users()
    today = datetime.date.today()
    for login, profile in users.items():
        if 'date_required' not in profile or 'chat_id' not in profile:
            continue

        due_date = datetime.datetime.strptime(profile['date_required'], "%Y-%m-%d").date()
        if (due_date - today).days == 2:
            bot.send_message(profile['chat_id'],
                             f"{login}, до продления аренды сервера осталось 2 дня ({due_date}).")
        elif (due_date - today).days == 1:
            bot.send_message(profile['chat_id'],
                             f"{login}, до продления аренды сервера остались сутки ({due_date}).")


if __name__ == '__main__':
    # Настраиваем планировщик, чтобы уведомлять каждый день в 9:00 по часовому поясу Stockholm
    scheduler = BackgroundScheduler(timezone="Europe/Moscow")
    scheduler.add_job(notify_upcoming, 'cron', hour=9, minute=0)
    scheduler.start()

    print("Бот запущен")
    bot.polling(none_stop=True)