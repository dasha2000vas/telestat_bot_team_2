from pyrogram.types import (
    KeyboardButton, ReplyKeyboardMarkup
)

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сбор данных'),
     KeyboardButton(text='Управление админами')]
], resize_keyboard=True)

data_collection_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Начать сбор данных')],
    [KeyboardButton(text='Задать интервал сбора данных')]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Добавить админа')],
    [KeyboardButton(text='Удалить админа')],
    [KeyboardButton(text='Все админы')]
], resize_keyboard=True)
