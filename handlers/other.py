from create_bot import dp, bot
from aiogram.types import Message
from aiogram import Router

router = Router()

@router.message()
async def echo_send(message : Message):
    await bot.send_message(message.from_user.id, "команда не распознана")
