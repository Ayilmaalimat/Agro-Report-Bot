from app.bot_service import send_help, get_today_statistic, get_yesterday_statistic, checked_text
from app.config import USER_LIST_ID, types, bot, dp
from app.callback import keyboard
from app import db_service

auth_bool = False


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = keyboard.gen_markup_help()
    is_checked = db_service.checked_user_in_list(USER_LIST_ID, message)
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


@dp.message_handler(content_types=['text'])
async def all_commands(message: types.Message):
    text_bool = await checked_text(message)
    if text_bool:
        global auth_bool
        auth_bool = True
        markup = keyboard.gen_markup_help()
        stick = open('./stickers/index3.webp', 'rb')
        await bot.send_sticker(message.chat.id, stick)
        return await message.reply(
            'Хорошая работа, {} {}! ✊\n'
            'Мы вас запомнили, теперь можете посмотреть в чем я силен'.format(message.from_user.first_name,
                                                                              message.from_user.last_name),
            reply_markup=markup,
            reply=False)
    if auth_bool:
        if message.text == 'Команды':
            await send_help(message)
        elif message.text == '1. Отчет за сегодняшний день':
            await get_today_statistic(message)
        elif message.text == '2. Отчет за вчерашний день':
            await get_yesterday_statistic(message)
    else:
        stick = open('./stickers/index.webp', 'rb')
        await bot.send_sticker(message.chat.id, stick)
        return await message.reply('Ого-го-го! 😱 У вас нет доступа!', reply=False)
