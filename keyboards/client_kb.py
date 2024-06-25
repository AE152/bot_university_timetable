from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kb = [
    [
        KeyboardButton(text = 'Сегодня')
    ],
    [
        KeyboardButton(text = 'Завтра'),
        KeyboardButton(text = 'Неделя'),
        KeyboardButton(text = 'Погода')
    ]
]

kb_client = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
