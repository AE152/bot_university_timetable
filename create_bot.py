from aiogram import Bot
from aiogram import Dispatcher
import os
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)

load_dotenv(find_dotenv())

#хранение данных в оперативной памяти для машины состояний
storage = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(storage = storage)
scheduler = AsyncIOScheduler()