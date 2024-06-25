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



