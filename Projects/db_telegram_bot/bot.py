from telebot.async_telebot import AsyncTeleBot

from telebot.states.asyncio.middleware import StateMiddleware
from telebot.asyncio_storage import StateMemoryStorage
from telebot import asyncio_filters

from config import API_TOKEN

bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())

bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(asyncio_filters.StateFilter(bot))
