from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

creation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_user_menu', text="Пользователи"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_restaurant_menu', text="Рестораны"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_table_menu', text="Столы"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_set_menu', text="Блюда"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_google_sync', text="Синхронизация данных в гугл-таблицей")
    ]

])

creation_user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_user_new', text="Создание нового пользователя"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_user_redact', text="Редактирование существующего пользователя"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_user_look_by_email',
                             text="Просмотр существующих пользователей по email")
    ],
    [
        InlineKeyboardButton(callback_data='creation_user_look_by_phone',
                             text="Просмотр существующих пользователей по телефону")
    ]
])

creation_restaurant_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_restaurant_new', text="Создание нового филиала кафе"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_restaurant_redaction',
                             text="Редактирование существующего филиала кафе"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_restaurant_look', text="Просмотр существующих филиалов кафе")

    ]
])

creation_table_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_table_new', text="Создание нового стола"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_table_redaction', text="Редактирование существующего стола"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_table_look', text="Просмотр существующих столов")

    ]
])

creation_set_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_set_new', text="Создание нового блюда"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_dinnerset_redaction', text="Редактирование существующего блюда"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_set_look', text="Просмотр существующих блюд")

    ]
])

creation_user_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_creation_admin', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_creation_admin', text="Подтверждаю")

    ]
])

redaction_user_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_redaction_admin', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_redaction_admin', text="Подтверждаю")

    ]
])

creation_restaurant_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_creation_restaurant', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_creation_restaurant', text="Подтверждаю")

    ]
])

redaction_restaurant_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_redaction_restaurant', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_redaction_restaurant', text="Подтверждаю")

    ]
])

creation_table_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_creation_table', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_creation_table', text="Подтверждаю")

    ]
])

redaction_table_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_redaction_table', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_redaction_table', text="Подтверждаю")

    ]
])

creation_set_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_creation_set', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_creation_set', text="Подтверждаю")

    ]
])

redaction_set_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_redaction_set', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_redaction_set', text="Подтверждаю")

    ]
])

creation_return_keyboard_users = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_user_menu', text="Вернуться в меню пользователей"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_main_menu', text="Вернуться в меню настроек")

    ]
])

creation_return_keyboard_restaurant = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_restaurant_menu', text="Вернуться в меню кафе"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_main_menu', text="Вернуться в меню настроек")

    ]
])

creation_return_keyboard_tables = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_table_menu', text="Вернуться в меню столов"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_main_menu', text="Вернуться в меню настроек")

    ]
])

creation_return_keyboard_sets = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='creation_set_menu', text="Вернуться в меню блюд"),
    ],
    [
        InlineKeyboardButton(callback_data='creation_main_menu', text="Вернуться в меню настроек")

    ]
])
