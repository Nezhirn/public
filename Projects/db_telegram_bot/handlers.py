from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telebot.asyncio_handler_backends import State, StatesGroup
from utils import datetime
import logging

from bot import bot
from utils import request_db, load_users_db, get_user_info

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
SMS_PHONE = ''

markup = ReplyKeyboardMarkup(resize_keyboard=True).add('/key', '/how_long')
markup_c = ReplyKeyboardMarkup(resize_keyboard=True).add('/cancel')

class LinkStates(StatesGroup):
    waiting_for_link = State()
    choosing_user = State()
    base = State()


async def log_current_state(message):
    current_state = await bot.get_state(message.chat.id, message.from_user.id)
    logging.info(f"[{message.from_user.id}] Message: '{message.text}' | Current FSM State: {current_state}")
    # НЕ ДЕЛАЙ return здесь, чтобы сообщение прошло дальше по цепочке хендлеров.


@bot.message_handler(state='*', commands=['cancel'])
async def any_state(message):
    await bot.set_state(message.from_user.id, state=None)
    await log_current_state(message)
    await bot.send_message(message.chat.id, "Отмена", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, 'Выбери команду:', reply_markup=markup)
    await log_current_state(message)

@bot.message_handler(state=None, commands=['start'])
async def send_welcome(message):
    await bot.set_state(message.from_user.id, state=LinkStates.base)
    await log_current_state(message)
    user = await get_user_info(message)
    user_id = user.get('user_id')
    user_nickname = user.get('user_nickname')
    request = f"select user_id from users where user_id = '{user_id}'"
    result = await request_db(request)
    msg = f"""
    Привет, {user_nickname}! Ты запустил бот-помощник по подключению к VPN.
Тут ты можешь получить ссылку на подключение с помощью команды /key .
Также можешь узнать, когда нужно продлевать аренду сервера, чтобы продлить доступ к VPN. Команда: /how_long .

Бот за 2 суток до дня продления аренды автоматически отсылает уведомление о том, что срок аренды нужно продлевать.

По всем интересуюим вопросам ходи к @wolf_of_wotan
"""
    if not result:
       await load_users_db(user_id, user_nickname, 1)
    await bot.send_message(message.chat.id, msg, reply_markup=markup) 
    
@bot.message_handler(state=LinkStates.base, commands=['key'])
async def check_key(message):
    user = await get_user_info(message)
    user_id = user.get('user_id')
    request = f"select local_user_id, is_active, nickname, link from vpn_links where local_user_id = '{user_id}'"
    result = await request_db(request)
    if not result:
        await bot.send_message(message.chat.id, f"Хуй тебе")
        return
    result = result[0]
    is_active = result['is_active']
    link = result['link']
    nickname = result['nickname']
    if not is_active:
        await bot.send_message(message.chat.id, 'Пошёл на хуй')
    else:
        await bot.send_message(message.chat.id, f"{nickname}, ты солнышко! Спасибо тебе за помощь в аренде. Вот твоя ссылка: {link}")

@bot.message_handler(state=LinkStates.base, commands=['how_long'])
async def how_long(message):
    user = await get_user_info(message)
    user_id = user.get('user_id')
    user_nickname = user.get('user_nickname')
    request = f"select * from vpn_links where local_user_id = '{user_id}'"
    result = await request_db(request)
    result = result[0]
    due_date = result['expire_on'].date()
    today = datetime.now().date()
    delta = (due_date - today).days
    if delta < 0:
        await bot.send_message(message.chat.id,
                         f"Срок аренды истёк {abs(delta)} дней назад ({due_date}).")
    elif delta == 0:
        await bot.send_message(message.chat.id,
                         f"Сегодня последний день аренды: {due_date}!")
    else:
        await bot.send_message(message.chat.id,
                         f"До продления аренды осталось {delta} дн. (до {due_date}).")
    await log_current_state(message)
                                          




@bot.message_handler(state=LinkStates.base, commands=['upload_key'])
async def upload_key(message):
    user = await get_user_info(message)
    user_id = user.get('user_id')
    user_nickname = user.get('user_nickname')
    request = f"select user_id, is_admin from users where user_id = '{user_id}'"
    result = await request_db(request)
    if not result or not result[0].get('is_admin'):
        return
    users = await request_db("SELECT user_id, nickname FROM users")
    if not users:
        await bot.send_message(message.chat.id, "Нет пользователей.")
        return
    markup_users = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for u in users:
        markup_users.add(f"{u['nickname']} ({u['user_id']})")
    markup_users.add('/cancel')
    await bot.set_state(message.from_user.id, LinkStates.choosing_user, message.chat.id)
    await bot.send_message(message.chat.id, "Выберите пользователя для загрузки ключа:", reply_markup=markup_users)
    await log_current_state(message)



###################################STATES#####################################

@bot.message_handler(
    state=LinkStates.waiting_for_link,
    content_types=['text']
)
async def process_link_step(message, state):
    link = message.text
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_user_id = data.get('target_user_id')
        target_user_nickname = data.get('target_user_nickname')
    
    if not target_user_id:
        await bot.send_message(message.chat.id, "Ошибка состояния. Попробуйте снова.")
        await bot.delete_state(message.chat.id, message.from_user.id)
        return
    request = f"select local_user_id from vpn_links where local_user_id = '{target_user_id}' "
    result = await request_db(request)
    if not result:

        await load_users_db(
            user_id=target_user_id,
            user_nickname=target_user_nickname,
            db=2,
            link=link,
            is_active=True
        )
        await bot.delete_state(
            message.chat.id,            # chat_id
            message.from_user.id        # user_id
        )
        await bot.send_message(message.chat.id, 'Ссылка сохранена!', reply_markup=markup)
    else:
        await bot.delete_state(
            message.chat.id,            # chat_id
            message.from_user.id        # user_id
        )
        await bot.send_message(message.chat.id, 'Для тебя уже добавлена ссылка иди на хуй', reply_markup=markup)

@bot.message_handler(
    state=LinkStates.choosing_user,
    content_types=['text']
)
async def admin_choose_user(message, state):
    text = message.text.strip()
    if "(" not in text or ")" not in text:
        await bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")
        return

    try:
        nickname_part, user_id_part = text.rsplit("(", 1) 
        selected_user_id = user_id_part.replace(")", "").strip()
  
    except Exception:
        await bot.send_message(message.chat.id, "Не удалось распознать пользователя.")
        return

    # ✅ Сохраняем данные в FSM
    await bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        target_user_id=selected_user_id,
        target_user_nickname=nickname_part
    )

    await bot.set_state(message.from_user.id, LinkStates.waiting_for_link, message.chat.id)

    message_bot_id = await bot.send_message(message.chat.id, 'Загрузка', reply_markup=ReplyKeyboardRemove())
    
    message_bot_id = message_bot_id.message_id
    await bot.delete_message(
    chat_id=message.chat.id,
    message_id=message_bot_id)   
    await bot.send_message(message.chat.id, f"Введите ссылку для пользователя {text}:", reply_markup=markup_c)

    

