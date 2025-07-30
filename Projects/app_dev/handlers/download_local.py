import asyncio
from telebot.types import Message
from states import LinkStates
from bot import bot
from markups import markup
from utils.download_video import download_video
from utils.generate_token import generate_token
from utils.schedule_cleanup import schedule_cleanup
from utils.has_premium import has_premium


@bot.message_handler(state=LinkStates.wait_video, content_types=['text'])
async def downloading_video(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        height = int(''.join(filter(str.isdigit, message.text)))
        if await has_premium(user_id) == False:
            if height >= 720:
                await bot.send_message(chat_id, 'Видео с высоким резрешением доступны только для PREMIUM пользователей. Для получения PREMIUM свяжитесь с @wolf_of_wotan', reply_markup=markup)
                await bot.set_state(user_id, state=LinkStates.base)
                return
        
        async with bot.retrieve_data(user_id, chat_id) as data:
            url = data['url']
            del data['url']
        await bot.send_message(chat_id, f'{height}, {url}', disable_web_page_preview=True)
        await bot.send_message(chat_id, 'Начало загрузки....')
        final_file = await download_video(url, height)
        share_link = await generate_token(final_file)
        await bot.send_message(chat_id, f'Загрузка завершена: вот ссылка на скачивание видоса: {share_link}', reply_markup=markup, disable_web_page_preview=True)
        await bot.set_state(user_id, state=LinkStates.base)
        await asyncio.create_task(schedule_cleanup(final_file))
    except Exception as e:
        await bot.send_message(chat_id, f'Ошибка: \n{e}')
        await bot.set_state(user_id, state=LinkStates.base)