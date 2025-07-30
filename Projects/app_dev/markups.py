from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

markup = ReplyKeyboardMarkup(resize_keyboard=True).add('/help', '/download_video')
markup_c = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add('/cancel')