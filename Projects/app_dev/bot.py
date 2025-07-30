from telebot.async_telebot import AsyncTeleBot

from telebot.asyncio_storage import StateRedisStorage
from telebot.states.asyncio.middleware import StateMiddleware
#from telebot.asyncio_storage import StateMemoryStorage
from telebot import asyncio_filters

from config import r_url, r_port, r_pass, API_TOKEN

state_storage = StateRedisStorage(host=r_url, port=r_port, db=1, password=r_pass, prefix='fsm')

bot = AsyncTeleBot(API_TOKEN, state_storage=state_storage)

bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(asyncio_filters.StateFilter(bot))