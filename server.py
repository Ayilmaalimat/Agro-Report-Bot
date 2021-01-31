from aiogram import Bot, Dispatcher, executor, types
import datetime
from decouple import config
import logging
import writeXlsx
import service

API_TOKEN = config('API_TOKEN')
USER_PASSWORD = config('USER_PASSWORD')
USER_LIST_ID = []

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def auth(func):
    async def wrapper(message):
        is_present = False
        for user in USER_LIST_ID:
            if message['from']['id'] == user:
                is_present = True
        if not is_present:
            stick = open('./stickers/index.webp', 'rb')
            await bot.send_sticker(message.chat.id, stick)
            return await message.reply('Ого-го-го! 😱 У вас нету доступа!', reply=False)
        return await func(message)

    return wrapper


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    is_checked = service.checked_user_in_list(USER_LIST_ID, message)
    if is_checked:
        mess = 'Снова здравствуйте!\n' \
               'Мы вас не забыли, мистер <b>{} {}</b> 😉\n' \
               'Какой отчет хотели посмотреть?\n' \
               'Если что команды здесь -> /help'.format(message.from_user.first_name, message.from_user.last_name)
    else:
        mess = 'Добро пожаловать, мистер <b>{} {}!</b>\n' \
               'Я - <b>SF</b> бот, созданный для формирования отчета\n' \
               'Стойте! Чтобы получить доступ ко всем функциям, сначала введите пароль, а то не пущу 😠'.format(
            message.from_user.first_name, message.from_user.last_name)
    await bot.send_message(message.chat.id, mess, parse_mode='HTML')


@dp.message_handler(lambda message: message.text == USER_PASSWORD)
async def send_password_text(message: types.Message):
    """ Проверка пароля пользователя """
    USER_LIST_ID.append(message.chat.id)
    stick = open('./stickers/index3.webp', 'rb')
    await bot.send_sticker(message.chat.id, stick)
    return await message.reply(
        'Хорошая работа Сэр! ✊\n'
        'Мы вас запомняли, теперь можете посмотреть в чем я силен -> /help', reply=False)


@dp.message_handler(commands=['help'])
@auth
async def send_help(message: types.Message):
    """ Справочник для пользователя """
    await message.answer(
        'Какие команды есть?\n'
        '1. Отчет за сегодняшний день - /today_report\n'
        '2. Отчет за вчерашний день   - /yesterday_report\n'
        '3. Отчет за весь период      - /all_report'
    )


@dp.message_handler(commands=['all_report'])
@auth
async def get_all_statistic(message: types.Message):
    """ Отправка отчета за весь период времени"""
    stat = service.get_all_statistic()
    writeXlsx.write_in_xlsx('_all', stat)
    doc = open('./xlsx-files/statistics_all.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)


@dp.message_handler(commands=['yesterday_report'])
@auth
async def get_yesterday_statistic(message: types.Message):
    """ Отправка отчета за вчеращний день"""
    stat = service.get_yesterday_statistic()
    date = datetime.date.today() - datetime.timedelta(days=1)
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)


@dp.message_handler(commands=['today_report'])
@auth
async def get_today_statistic(message: types.Message):
    """ Отправка отчета за сегоднящний день"""
    stat = service.get_today_statistic()
    date = datetime.datetime.now().date()
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
