from app.config import USER_PASSWORD, USER_LIST_ID, types, bot, dp
from app.callback import keyboard
from app import writeXlsx, service
import datetime


def auth(func):
    async def wrapper(message):
        is_present = False
        for user in USER_LIST_ID:
            if message['from']['id'] == user:
                is_present = True
        if not is_present:
            stick = open('./stickers/index.webp', 'rb')
            await bot.send_sticker(message.chat.id, stick)
            return await message.reply('Ого-го-го! 😱 У вас нет доступа!', reply=False)
        return await func(message)

    return wrapper


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = keyboard.gen_markup_help()
    is_checked = service.checked_user_in_list(USER_LIST_ID, message)
    if is_checked:
        mess = 'Снова здравствуйте!\n' \
               'Мы вас не забыли, <b>{} {}</b> 😉\n' \
               'Какой отчет хотели посмотреть?\n'.format(message.from_user.first_name, message.from_user.last_name)
        await bot.send_message(message.chat.id, mess, parse_mode='HTML', reply_markup=markup)
    else:
        mess = 'Добро пожаловать, <b>{} {}!</b>\n' \
               'Я - <b>SF</b> бот, созданный для формирования отчета\n' \
               'Стойте! Чтобы получить доступ ко всем функциям, сначала введите пароль, а то не пущу 😠'.format(
            message.from_user.first_name, message.from_user.last_name)
        await bot.send_message(message.chat.id, mess, parse_mode='HTML')


@dp.message_handler(lambda message: message.text == USER_PASSWORD)
async def send_password_text(message: types.Message):
    """ Проверка пароля пользователя """
    USER_LIST_ID.append(message.chat.id)
    markup = keyboard.gen_markup_help()
    stick = open('./stickers/index3.webp', 'rb')
    await bot.send_sticker(message.chat.id, stick)
    return await message.reply(
        'Хорошая работа, {} {}! ✊\n'
        'Мы вас запомнили, теперь можете посмотреть в чем я силен'.format(message.from_user.first_name,
                                                                                   message.from_user.last_name),
        reply_markup=markup,
        reply=False)


@dp.message_handler(lambda message: message.text == 'Команды')
@auth
async def send_help(message: types.Message):
    """ Справочник для пользователя """
    markup = keyboard.gen_markup_commands()
    await bot.send_message(
        message.chat.id,
        'Какие команды есть?\n',
        reply_markup=markup
    )


@dp.message_handler(lambda message: message.text == '2. Отчет за вчерашний день')
@auth
async def get_yesterday_statistic(message: types.Message):
    """ Отправка отчета за вчеращний день"""
    stat = service.get_yesterday_statistic()
    date = datetime.date.today() - datetime.timedelta(days=1)
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)


@dp.message_handler(lambda message: message.text == '1. Отчет за сегодняшний день')
@auth
async def get_today_statistic(message: types.Message):
    """ Отправка отчета за сегоднящний день"""
    stat = service.get_today_statistic()
    date = datetime.datetime.now().date()
    writeXlsx.write_in_xlsx(date, stat)
    doc = open('./xlsx-files/statistics' + str(date) + '.xlsx', 'rb')
    await bot.send_document(message.chat.id, doc)
