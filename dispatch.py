from aiogram import Bot, Dispatcher

from configs.constants import TOKEN
from aiogram.contrib.fsm_storage.files import MemoryStorage


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
