from aiogram import Bot, Dispatcher, executor, types
from decouple import config
import logging

USER_PASSWORD = config('USER_PASSWORD')
API_TOKEN = config('API_TOKEN')

USER_LIST_ID = []

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
