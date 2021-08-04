from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from callback_data import state_callback, done_callback, scanning_callback

button_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Добавить мем', callback_data=state_callback.new(key_name='Добавить_мем')),
            InlineKeyboardButton('Найти мем', callback_data=state_callback.new(key_name='Найти_мем'))
        ]
    ]
)

choosing_analysis = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Написать', callback_data=state_callback.new(key_name='Написать')),
            InlineKeyboardButton('Сканировать', callback_data=scanning_callback.new(key_name='Сканировать'))
        ],
        [
            InlineKeyboardButton('Назад', callback_data=state_callback.new(key_name='Добавить_мем'))
        ]
    ]
)

confirm_input = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Подтверждаю', callback_data=done_callback.new(readily='ok')),
            InlineKeyboardButton('Исправить', callback_data=state_callback.new(key_name='Написать'))
        ]
    ]
)

start = KeyboardButton('/start')
help = KeyboardButton('/help')

button_commands = ReplyKeyboardMarkup(resize_keyboard=True).add(start).add(help)
