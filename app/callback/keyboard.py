from app.config import types, bot, dp


def gen_markup_help():
    btn = types.KeyboardButton('Команды')
    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(btn)
    return kb


def gen_markup_commands():
    btn1 = types.KeyboardButton('1. Отчет за сегодняшний день')
    btn2 = types.KeyboardButton('2. Отчет за вчерашний день')
    kb = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    ).add(btn1, btn2)
    return kb


