from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_reservation_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_look_menu', text='Просмотр бронирований')
    ],
    [
        InlineKeyboardButton(callback_data='reservation_redaction_menu', text='Изменение бронирований')
    ],
    [
        InlineKeyboardButton(callback_data='reservation_creation', text="Создание нового бронирования"),
    ],
]
)

look_reservation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_all', text="Все бронирования"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_date', text="Бронирования по дате"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_actual',
                             text="Актуальные бронирования (сегодня и далее)"),
    ],

    [
        InlineKeyboardButton(callback_data='reservation_email', text="Бронирования по email пользователя")
    ],
    [
        InlineKeyboardButton(callback_data='reservation_phone', text="Бронирования по телефону пользователя")
    ],
])

redaction_reservation_keyboard = InlineKeyboardMarkup(inline_keyboard=[

    [
        InlineKeyboardButton(callback_data='reservation_update', text="Редактирование существующего бронирования"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_cancellation', text="Отмена существующего бронирования"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_deletion',
                             text="Удаление существующего бронирования (из базы!)"),
    ],
])

reservation_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='cancel_reservation_creation', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_reservation_creation', text="Подтверждаю")

    ]
])

reservation_deletion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='delete_reservation', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_reservation', text="Подтверждаю")

    ]
])

reservation_update_keyboard_step_two = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_two_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_two_yes', text="Да"),
    ],
])

reservation_update_keyboard_step_three = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_three_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_three_yes', text="Да"),
    ],
])

reservation_update_keyboard_step_four = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_four_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_four_yes', text="Да"),
    ],
])

reservation_update_keyboard_step_five = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_five_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_five_yes', text="Да"),
    ],
])

reservation_update_keyboard_step_six = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_six_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_six_yes', text="Да"),
    ],

])

reservation_update_keyboard_step_seven = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_seven_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_seven_yes', text="Да"),
    ],
])

reservation_update_keyboard_step_eight = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_update_step_eight_no', text="Нет")

    ],
    [
        InlineKeyboardButton(callback_data='reservation_update_step_eight_yes', text="Да"),
    ],
])


reservation_update_confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='confirm_cancel_update', text="Отмена"),
    ],
    [
        InlineKeyboardButton(callback_data='confirm_submit_update', text="Подтверждаю")

    ]
])


reservation_creation_return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_creation', text="Создать еще одно бронирование"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_main_menu', text="Вернуться в меню работы с бронированиями")

    ]
])


reservation_look_all_return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_look_menu', text="Вернуться в просмотр бронирований"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_main_menu', text="Вернуться в меню работы с бронированиями")

    ]
])


reservation_redact_all_return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(callback_data='reservation_redaction_menu', text="Вернуться в изменение бронирований"),
    ],
    [
        InlineKeyboardButton(callback_data='reservation_main_menu', text="Вернуться в меню работы с бронированиями")

    ]
])