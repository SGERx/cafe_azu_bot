from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


to_start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        # KeyboardButton(
        #     text='DEBUG:print state'),
        # KeyboardButton(
        #     text='Назад'
        # ),
        KeyboardButton(
            text='К главному меню')
    ]
], resize_keyboard=True, selective=True)


work_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_main_menu', text="Просмотр и создание бронирований")
    ],
    [
        InlineKeyboardButton(callback_data='creation_main_menu', text="Настройки объектов и просмотр данных"),
    ]

])
