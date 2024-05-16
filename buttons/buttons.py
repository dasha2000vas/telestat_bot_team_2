from pyrogram.types import (
    KeyboardButton, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton
)

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сбор данных'),
     KeyboardButton(text='Управление админами')]
], resize_keyboard=True)

data_collection_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Настройка интервала и сбор данных')],
    # [KeyboardButton(text='Отменить сбор данных')]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад')],
    [KeyboardButton(text='Добавить админа')],
    [KeyboardButton(text='Удалить админа')],
    [KeyboardButton(text='Все админы')]
], resize_keyboard=True)

report_menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сформировать отчет')]
], resize_keyboard=True)


time_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                '1 час',
                callback_data='1'
            ),
            InlineKeyboardButton(
                '5 часов',
                callback_data='300'
            )
        ],
        [
            InlineKeyboardButton(
                '10 часов',
                callback_data='600'
            ),
            InlineKeyboardButton(
                '15 часов',
                callback_data='900'
            )
        ],
        [
            InlineKeyboardButton(
                '24 часа',
                callback_data='1440'
            ),
            InlineKeyboardButton(
                'Задать интервал',
                callback_data='custom'
            )
        ],
        [
            InlineKeyboardButton(
                'Без интервала',
                callback_data='no_interval'
            )
        ]
    ]
)


async def make_inline_keyboard(value):
    lst = []
    for i, v in value.items():
        button = [InlineKeyboardButton(text=i, callback_data=v)]
        lst.append(button)
    keyboard = InlineKeyboardMarkup(lst)
    return keyboard
