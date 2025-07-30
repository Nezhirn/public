from telebot.asyncio_handler_backends import State, StatesGroup

class LinkStates(StatesGroup):
    waiting_for_link = State()
    wait_video = State()
    base = State()