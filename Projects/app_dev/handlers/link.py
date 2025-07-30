from telebot.types import Message, ReplyKeyboardMarkup
from states import LinkStates
from bot import bot
from markups import markup_c
from utils import list_unique_resolutions

@bot.message_handler(state=LinkStates.base, commands=['download_video'])
async def start_download_process(message: Message):
    await bot.set_state(message.from_user.id, state=LinkStates.waiting_for_link)
    await bot.send_message(message.chat.id, 'Отправь ссылку на видео с ютуба.', reply_markup=markup_c)

@bot.message_handler(state=LinkStates.waiting_for_link, content_types=['text'])
async def get_link(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    url = message.text
    await bot.add_data(user_id=user_id, chat_id=chat_id, url=url)
    await bot.send_message(chat_id, 'Ищу видос...')
    try:
        res_list = await list_unique_resolutions(url)
        markup_res = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for r in res_list:
            if r >= 720:
                markup_res.add(f"Разрешение: {r}p (Только для PREMIUM)")
            else:
                markup_res.add(f"Разрешение: {r}p")
        markup_res.add('/cancel')
        await bot.send_message(chat_id, 'Выбери разрешение:', reply_markup=markup_res)
        await bot.set_state(user_id, state=LinkStates.wait_video)
    except Exception as e:
        await bot.send_message(chat_id, f'Ошибка: \n{e}')