from create_bot import dp, scheduler, bot
from handlers import client, other
from data_base import sqlite_db
import asyncio

async def on_startup(dispatcher):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

async def main():
    #регистрация хэндлеров
    dp.include_router(client.router)
    dp.include_router(other.router)

    dp.startup.register(on_startup)
    #scheduler.start()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())



#
#Парсинг рассписания
#
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

s=Service('/home/aleksandr/tg_bot/geckodriver')

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

browser.get('https://sibsutis.ru/students/schedule/?type=student')

search_group = 'ип-012'

browser.find_element("xpath", '/html/body/div[3]/div[1]/div[2]/span/span[1]/span/span[1]/span').click()
browser.find_element("xpath", '/html/body/span/span/span[1]/input').send_keys(search_group)
#time.sleep(2)
browser.implicitly_wait(2)
check_res = browser.find_element(by=By.CLASS_NAME, value='select2-results__options')
if check_res.text == "": #проверяем что результаты поиска существуют
    print("сайт не выдал результаты поиска")
else:
    #print("not null")
    group = browser.find_element(by=By.CLASS_NAME, value='select2-results__option--highlighted')
    if group.text.lower() == search_group:
        print("группа " + group.text + " найдена")
        group.click()
        #time.sleep(2)
        browser.implicitly_wait(2)
        #тут нужен парсинг расписания
        #browser.find_element(by=By.XPATH, value='/html/body/div[3]/div[1]/div[2]/div[3]/a[20]').click()
        browser.implicitly_wait(2)
        time_class = browser.find_element(by=By.CLASS_NAME, value='schedule__item')
        str = time_class.text
        print(str)
        
        # //*[@id="layout"]/div[1]/div[1]/div[1]
        # //*[@id="layout"]/div[1]/div[1]/div[2]
    

        # /html/body/div[3]/div[1]/div[1]/div[1]
        # /html/body/div[3]/div[1]/div[1]/div[2]

    else:
        print("группа: "+ search_group + "  не найдена на сате sibsutis")
'''

#
#тг бот
#


'''
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6280439651:AAGDOlB1H6ueosT9rJ1mbrt1_tVs0p9aAUI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")



@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



'''


