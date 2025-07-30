from telebot.types import Message, ReplyKeyboardRemove
from markups import markup
from states import LinkStates
from bot import bot


@bot.message_handler(state='*', commands=['cancel'])
async def any_state(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await bot.reset_data(user_id, chat_id)
    await bot.set_state(user_id, state=LinkStates.base)
    await bot.send_message(chat_id, "Отмена", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id, 'Выбери команду:', reply_markup=markup)
    

@bot.message_handler(state=None, commands=['start', 'help'])
async def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    nickname = message.from_user.username or 'Гость'
    await bot.set_state(user_id, state=LinkStates.base)
    msg = f"""
Привет! Ты запустил бота для скачивания видосиков с ютуба. 
Для скачивания видео нажми на кнопку download_video. Для отмены действия нажми на кнопку cancel.

После нажатия на кнопку введи ссылку с ютуба, отправь боту, после этого дождись, пока видос найдётся.
Затем выбери желаемое разрешение видео. После этого жди, пока бот отправит тебе ссылку для скачивания, ничего боту не отправляй до получения ссылки. 
ССЫЛКА ОДНОРАЗОВАЯ. Срок годности ссылки: 15 минут.

Для бесплатного скачивания доступны видосы в качестве до 480p. Если хочешь скачивать видео из бота в максимальном качестве, то сходи в личные сообщения к @wolf_of_wotan, также по всем интересующим вопросам ходи к нему.
    """
    await bot.send_message(chat_id, msg, reply_markup=markup)