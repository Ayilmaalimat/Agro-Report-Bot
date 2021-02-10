from app.config import types, bot, USER_LIST_ID
from app.callback import keyboard
from app import writeXlsx, db_service
import datetime


async def checked_text(message: types.Message):
    dec = db_service.decode_password()
    for d in dec:
        if message.text == d[1]:
            USER_LIST_ID.append([message.chat.id, d[1]])
            return True
    return False


async def send_help(message: types.Message):
    """ Справочник для пользователя """
    markup = keyboard.gen_markup_commands()
    await bot.send_message(
        message.chat.id,
        'Какие команды есть?\n',
        reply_markup=markup
    )


async def get_yesterday_statistic(message: types.Message):
    """ Отправка отчета за вчеращний день"""
    psw = db_service.ckecked_id(USER_LIST_ID, message)
    encode = db_service.encode_password(psw)
    dep = db_service.get_department(encode)
    stat = db_service.get_yesterday_statistic(dep)
    date = datetime.date.today() - datetime.timedelta(days=1)
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)


async def get_today_statistic(message: types.Message):
    """ Отправка отчета за сегоднящний день"""
    psw = db_service.ckecked_id(USER_LIST_ID, message)
    encode = db_service.encode_password(psw)
    dep = db_service.get_department(encode)
    stat = db_service.get_today_statistic(dep)
    date = datetime.datetime.now().date()
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)
