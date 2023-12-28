from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from app.crud.dinnerset import CRUDDinnerSet
from app.crud.reservation import ReservationCRUD
from app.crud.table import table_crud
from app.crud.user import UserCRUD
from app.tg_bot.bot_admin.keyboards.keyboards_reservation import look_reservation_keyboard, main_reservation_kb, \
    redaction_reservation_keyboard, reservation_confirmation_keyboard, \
    reservation_update_keyboard_step_two, reservation_update_keyboard_step_three, \
    reservation_update_keyboard_step_four, \
    reservation_update_keyboard_step_five, reservation_update_confirmation_keyboard, \
    reservation_creation_return_keyboard, reservation_look_all_return_keyboard, reservation_redact_all_return_keyboard, \
    reservation_update_keyboard_step_six, reservation_update_keyboard_step_seven, reservation_update_keyboard_step_eight

from aiogram.fsm.context import FSMContext
from app.tg_bot.bot_admin.states import StateAdmin
from app.tg_bot.utils import add_reservation

reservation_router = Router()

admin_reservation_crud = ReservationCRUD()
user_crud = UserCRUD()
admin_dinnerset_crud = CRUDDinnerSet()


# Меню бронирований

@reservation_router.callback_query(F.data == "reservation_main_menu")
async def reservation_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_main_menu)
    await callback.message.answer(text="Меню бронирований, выберите опцию",
                                  reply_markup=main_reservation_kb)


# Меню просмотра бронирований

@reservation_router.callback_query(F.data == "reservation_look_menu")
async def reservation_look_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Меню просмотра бронирований",
                                  reply_markup=look_reservation_keyboard)
    await state.set_state(StateAdmin.reservation_look_menu)


# Просмотр всех бронирований

@reservation_router.callback_query(F.data == "reservation_all")
async def reservation_all(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_all)
    reservations_all = await admin_reservation_crud.get_multi()
    if reservations_all and reservations_all != "В базе нет информации о бронированиях":
        print(reservations_all)
        for i in range(0, len(reservations_all)):
            await callback.message.answer(f" Бронь №{i + 1}:\n{reservations_all[i]}")
        await callback.message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)
    else:
        print("В базе нет информации о бронированиях")
        await callback.message.answer("В базе нет информации о бронированиях")
        await callback.message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)


# Просмотр за определенную дату

@reservation_router.callback_query(F.data == "reservation_date")
async def reservation_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Смотрим все бронирования по дате, введите дату в формате ddmmyyyy")
    await state.set_state(StateAdmin.reservation_date)


# Просмотр за определенную дату - продолжение
@reservation_router.message(StateFilter(StateAdmin.reservation_date))
async def reservation_date_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_date_continue)
    await state.update_data(reservation_date=message.text)
    print(message.text)
    await message.reply(f"Введенная дата {message.text}, смотрим бронирования за эту дату")
    admin_data = await state.get_data()
    look_reservation_date = admin_data['reservation_date']
    look_reservation_date_str = str(look_reservation_date)
    reservations_by_date = await admin_reservation_crud.read_reservation_by_date(look_reservation_date_str)

    if reservations_by_date and reservations_by_date != "Данные о бронированиях за указанную дату отсутствуют в базе":
        await message.answer(f"Бронирования за дату {message.text}:")
        for i in range(0, len(reservations_by_date)):
            await message.answer(f"Бронь №{i + 1}- {reservations_by_date[i]}")
        await message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)
    else:
        print("Данные о бронированиях за указанную дату отсутствуют в базе")
        await message.answer("Данные о бронированиях за указанную дату отсутствуют в базе",
                             reply_markup=reservation_look_all_return_keyboard)
    await state.clear()


# Просмотр актуальных бронирований

@reservation_router.callback_query(F.data == "reservation_actual")
async def reservation_actual(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_actual)
    actual_reservations = await admin_reservation_crud.read_actual_reservations()
    if actual_reservations and actual_reservations != "В базе нет информации о бронированиях на актуальные даты":
        print(actual_reservations)
        await callback.message.answer("Данные об актуальных бронированиях:")
        for i in range(0, len(actual_reservations)):
            await callback.message.answer(f" Бронь №{i + 1}:\n{actual_reservations[i]}")
        await callback.message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)

    else:
        print("В базе нет информации о бронированиях на актуальные даты")
        await callback.message.answer("В базе нет информации о бронированиях на актуальные даты",
                                      reply_markup=reservation_look_all_return_keyboard)


# Просмотр бронирований по email клиента

@reservation_router.callback_query(F.data == "reservation_email")
async def reservation_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Просмотр бронирований по email клиента, введите email")
    await state.set_state(StateAdmin.reservation_email)


# Просмотр бронирований по email клиента - продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_email))
async def reservation_email_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_email_continue)
    await state.update_data(email=message.text)
    print(message.text)
    admin_data = await state.get_data()
    email = admin_data['email']
    user_by_email = await user_crud.get_by_email(email)
    print(email)
    print(user_by_email)
    if user_by_email:
        user_by_email_id = user_by_email.id
        print(user_by_email_id)
        reservations_by_email = await admin_reservation_crud.read_actual_reservations_by_client(user_by_email_id)
        print(reservations_by_email)
        if reservations_by_email and reservations_by_email != "В базе нет информации о бронированиях на актуальные даты":
            print(reservations_by_email)
            await message.answer(f"Данные об актуальных бронированиях пользователя с email {message.text}:")
            for i in range(0, len(reservations_by_email)):
                await message.answer(f" Бронь №{i + 1}:\n{reservations_by_email[i]}")
            await message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)
        else:
            print("Нет данных в базе")
            await message.answer("Бронирования по данному email в базе не найдены",
                                 reply_markup=reservation_look_all_return_keyboard)
    else:
        await message.answer("Пользователь по указанному email не найден")
    await state.clear()


# Просмотр бронирований по телефону клиента

@reservation_router.callback_query(F.data == "reservation_phone")
async def reservation_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Просмотр бронирований по телефону клиента, введите номер в формате +7XXXxxxxxxx")
    await state.set_state(StateAdmin.reservation_phone)


# Просмотр бронирований по телефону клиента - продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_phone))
async def reservation_email_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_phone_continue)
    await state.update_data(phone_number=message.text)
    print(message.text)
    admin_data = await state.get_data()
    phone_number_data = admin_data['phone_number']
    user_by_phone = await user_crud.get_by_phone_number(phone_number_data)
    print(phone_number_data)
    print(user_by_phone)
    if user_by_phone:
        user_by_phone_id = user_by_phone.id
        print(user_by_phone_id)
        reservations_by_phone = await admin_reservation_crud.read_actual_reservations_by_client(user_by_phone_id)
        print(reservations_by_phone)
        if reservations_by_phone and reservations_by_phone != "В базе нет информации о бронированиях на актуальные даты":
            print(reservations_by_phone)

            await message.answer(f"Данные об актуальных бронированиях пользователя с телефоном {message.text}:")
            for i in range(0, len(reservations_by_phone)):
                await message.answer(f" Бронь №{i + 1}:\n{reservations_by_phone[i]}")
            await message.answer(" вернуться в меню", reply_markup=reservation_look_all_return_keyboard)
        else:
            print("Нет данных в базе")
            await message.answer("Бронирования по данному номеру телефона в базе не найдены",
                                 reply_markup=reservation_look_all_return_keyboard)
    else:
        await message.answer("Пользователь по указанному телефону не найден",
                             reply_markup=reservation_look_all_return_keyboard)
    await state.clear()


# Меню редактирования бронирований

@reservation_router.callback_query(F.data == "reservation_redaction_menu")
async def reservation_redaction_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Меню редактирования бронирований",
                                  reply_markup=redaction_reservation_keyboard)
    await state.set_state(StateAdmin.reservation_redaction_menu)


# Создание нового бронирования - шаг 1

@reservation_router.callback_query(F.data == "reservation_creation")
async def reservation_creation_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Cоздание бронирования - укажите user_id клиента")
    await state.set_state(StateAdmin.reservation_creation_step_one)


# Создание нового бронирования - шаг 2

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_one))
async def reservation_creation_step_two(message: Message, state: FSMContext):
    user_id = message.text
    await state.update_data(user_id=user_id)
    print(message.text)
    await message.reply(f"Введен id пользователя - {message.text}, введите филиал бронирования")
    await state.set_state(StateAdmin.reservation_creation_step_two)


# Создание нового бронирования - шаг 3

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_two))
async def reservation_creation_step_three(message: Message, state: FSMContext):
    await state.update_data(reservation_restaurant_location=message.text)
    print(message.text)
    await message.reply(f"Выбран филиал - {message.text}, введите дату бронирования в формате ddmmYYYY")
    await state.set_state(StateAdmin.reservation_creation_step_three)


# Создание нового бронирования - шаг 4

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_three))
async def reservation_creation_step_four(message: Message, state: FSMContext):
    await state.update_data(reservation_date=message.text)
    print(message.text)
    await message.reply(f"Введена дата бронирования - {message.text}, введите количество гостей")
    await state.set_state(StateAdmin.reservation_creation_step_four)


# Создание нового бронирования - шаг 5

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_four))
async def reservation_creation_step_five(message: Message, state: FSMContext):
    await state.update_data(guest_count=message.text)
    print(message.text)
    await state.set_state(StateAdmin.reservation_creation_step_five)
    await message.reply(f"Количество гостей - {message.text}, введите дополнительную информацию о бронировании")


# Создание нового бронирования - шаг 6

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_five))
async def reservation_creation_step_six(message: Message, state: FSMContext):
    await state.update_data(special=message.text)
    print(message.text)
    await state.set_state(StateAdmin.reservation_creation_step_six)
    await message.reply(
        f"Дополнительная информация - {message.text}, выберите блюдо (введите номер блюда - или номера блюд через пробел)")


# Создание нового бронирования - шаг 7

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_six))
async def reservation_creation_step_seven(message: Message, state: FSMContext):
    await state.update_data(dinner_sets=message.text)
    print(message.text)
    await state.set_state(StateAdmin.reservation_creation_step_seven)
    await message.reply(
        f"Выбранное блюдо - {message.text}, укажите количество для блюд через пробел (по умолчанию будет выбрано 1)")


# Создание нового бронирования - шаг 8

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_seven))
async def reservation_creation_step_eight(message: Message, state: FSMContext):
    await state.update_data(dinner_sets_quantity=message.text)
    print(message.text)
    await state.set_state(StateAdmin.reservation_creation_step_eight)
    create_reservation_data = await state.get_data()
    await message.reply(
        f"Выбранное количество - {message.text}, укажите id столов (если столов несколько, то укажите id через пробел)")
    create_reservation_date = create_reservation_data['reservation_date']
    create_reservation_date_formatted = datetime.strptime(create_reservation_date, "%d%m%Y").date()
    tables_info = await table_crud.get_available_tables_in_restaurant_by_capacity_and_date(
        create_reservation_data['guest_count'],
        create_reservation_data['reservation_restaurant_location'],
        create_reservation_date_formatted
    )
    if tables_info:
        print(tables_info)
        await message.answer(text="Просмотр доступных столов:")
        for i in range(0, len(tables_info)):
            await message.answer(text=f"{tables_info[i]}")
    else:
        await message.answer(text="В базе нет ни одного доступного стола")


# Создание нового бронирования - шаг 9

@reservation_router.message(StateFilter(StateAdmin.reservation_creation_step_eight))
async def reservation_creation_step_nine(message: Message, state: FSMContext):
    await state.update_data(table_ids=message.text)
    print(message.text)
    await state.set_state(StateAdmin.reservation_creation_step_nine)
    create_reservation_data = await state.get_data()
    reserv_user = create_reservation_data['user_id']
    reserv_date = create_reservation_data.get('reservation_date')
    reserv_date_formatted = datetime.strptime(reserv_date, "%d%m%Y").date()
    reserv_guests = create_reservation_data.get('guest_count')
    reserv_special = create_reservation_data.get('special')

    await message.reply(f"Выбранные столы - {message.text}, подтвердите бронирование - "
                        f"пользователь с id {reserv_user}, дата {reserv_date_formatted}, гостей {reserv_guests}, "
                        f"комментарии к бронированию: {reserv_special}",
                        reply_markup=reservation_confirmation_keyboard)


# Создание нового бронирования - отмена

@reservation_router.callback_query(StateFilter(StateAdmin.reservation_creation_step_nine),
                                   F.data == "cancel_reservation_creation")
async def cancel_reservation_creation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание бронирования отменено",
                                  reply_markup=reservation_creation_return_keyboard)

    await state.clear()


# Создание нового бронирования - подтверждение

@reservation_router.callback_query(StateFilter(StateAdmin.reservation_creation_step_nine),
                                   F.data == "confirm_reservation_creation")
async def reservation_creation_step_nine(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание бронирования подтверждено",
                                  reply_markup=reservation_creation_return_keyboard)
    await state.set_state(StateAdmin.reservation_creation_step_nine)

    create_reservation_data = await state.get_data()

    create_reservation_date = create_reservation_data.get('reservation_date')
    create_reservation_date_formatted = datetime.strptime(create_reservation_date, "%d%m%Y").date()

    reservation_data_dict = dict(
        user_id=create_reservation_data['user_id'],
        reservation_date=create_reservation_date_formatted,
        guest_count=create_reservation_data['guest_count'],
        special=create_reservation_data['special'],
    )

    dinnersets_data_list = list(create_reservation_data.get('dinner_sets').split())
    dinnersets_quantity_data_list = list(create_reservation_data.get('dinner_sets_quantity').split())
    print(dinnersets_data_list)
    print(dinnersets_quantity_data_list)
    print(len(dinnersets_data_list))
    print(len(dinnersets_quantity_data_list))
    if len(dinnersets_data_list) > len(dinnersets_quantity_data_list):
        counter_quantity = len(dinnersets_data_list) - len(dinnersets_quantity_data_list)
        while counter_quantity != 0:
            counter_quantity = counter_quantity - 1
            dinnersets_quantity_data_list.append('1')

    dinnerset_data_dict = dict(zip(dinnersets_data_list, dinnersets_quantity_data_list))

    table_ids = list(create_reservation_data.get('table_ids').split())

    await add_reservation(reservation_data_dict, table_ids, dinnerset_data_dict)
    print(reservation_data_dict)
    print(table_ids)
    print(dinnerset_data_dict)
    await state.clear()


# Отмена существующего бронирования - шаг 1

@reservation_router.callback_query(F.data == "reservation_cancellation")
async def reservation_cancellation(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Отмена существующего бронирования, введите id бронирования")
    await state.set_state(StateAdmin.reservation_cancellation)


# Отмена существующего бронирования - шаг 2

@reservation_router.message(StateFilter(StateAdmin.reservation_cancellation))
async def reservation_cancellation_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_cancellation_continue)
    await state.update_data(reservation_cancellation_data=message.text)
    print(message.text)
    admin_data = await state.get_data()
    reservation_id = admin_data['reservation_cancellation_data']
    reservation_id_int = int(reservation_id)
    await admin_reservation_crud.cancel_reservation(reservation_id=reservation_id_int)
    await message.answer(" вернуться в меню", reply_markup=reservation_redact_all_return_keyboard)
    await state.clear()


# Удаление существующего бронирования - шаг 1

@reservation_router.callback_query(F.data == "reservation_deletion")
async def reservation_deletion(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Удаление существующего бронирования из базы, укажите ID бронирования")
    await state.set_state(StateAdmin.reservation_deletion)


# Удаление существующего бронирования - шаг 2

@reservation_router.message(StateFilter(StateAdmin.reservation_deletion))
async def reservation_deletion_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_deletion_continue)
    await state.update_data(reservation_deletion_id=message.text)
    print(message.text)
    admin_data = await state.get_data()
    reservation_id = admin_data['reservation_deletion_id']
    reservation_id_int = int(reservation_id)
    await admin_reservation_crud.delete_reservation(reservation_id=reservation_id_int)
    await message.answer(" вернуться в меню", reply_markup=reservation_redact_all_return_keyboard)


# Редактирование существующего бронирования - шаг 1

@reservation_router.callback_query(F.data == "reservation_update")
async def reservation_update_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование бронирования, введите reservation_id")
    await state.set_state(StateAdmin.reservation_update_step_one)


# Редактирование существующего бронирования - шаг 2
@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_one))
async def reservation_update_step_two(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_two)
    reservation_id = message.text
    await state.update_data(reservation_id=reservation_id)
    print(message.text)
    await message.reply(
        f"Введен id бронирования - {message.text}, требуется ли изменение user_id?",
        reply_markup=reservation_update_keyboard_step_two)


# Редактирование существующего бронирования - шаг 2-да
@reservation_router.callback_query(F.data == "reservation_update_step_two_yes")
async def reservation_update_step_two_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_two_yes)
    await callback.message.answer(
        "Введите новый user_id")


# Редактирование существующего бронирования - шаг 2-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_two_yes))
async def reservation_update_step_two_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_two_yes_continue)
    await state.update_data(user_id=message.text)
    print(message.text)
    await message.reply(
        f"Новый user_id - {message.text}, требуется ли изменение даты бронирования?",
        reply_markup=reservation_update_keyboard_step_three)


# Редактирование существующего бронирования - шаг 2-нет
@reservation_router.callback_query(F.data == "reservation_update_step_two_no")
async def reservation_update_step_two_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_two_no)
    await callback.message.answer(
        "user_id не меняем - требуется ли изменение даты бронирования?",
        reply_markup=reservation_update_keyboard_step_three)


# Редактирование существующего бронирования - шаг 3-да
@reservation_router.callback_query(F.data == "reservation_update_step_three_yes")
async def reservation_update_step_three_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_three_yes)
    await callback.message.answer(
        "Введите новую дату бронирования в формате ddmmyyyy, например, первое января двухтысячного года будет 01012000")


# Редактирование существующего бронирования - шаг 3-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_three_yes))
async def reservation_update_step_three_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_three_yes_continue)
    await state.update_data(reservation_date=message.text)
    print(message.text)
    await message.reply(
        f"Новая дата бронирования - {message.text}, требуется ли изменение количества гостей?",
        reply_markup=reservation_update_keyboard_step_four)


# Редактирование существующего бронирования - шаг 3-нет
@reservation_router.callback_query(F.data == "reservation_update_step_three_no")
async def reservation_update_step_three_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_three_no)
    await callback.message.answer(
        "Дату бронирования не меняем - требуется ли изменение количества гостей?",
        reply_markup=reservation_update_keyboard_step_four)


# Редактирование существующего бронирования - шаг 4-да
@reservation_router.callback_query(F.data == "reservation_update_step_four_yes")
async def reservation_update_step_four_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_four_yes)
    await callback.message.answer(
        "Введите новое количество гостей")


# Редактирование существующего бронирования - шаг 4-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_four_yes))
async def reservation_update_step_four_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_four_yes_continue)
    await state.update_data(guest_count=message.text)
    print(message.text)
    await message.reply(
        f"Новое количество гостей - {message.text}, требуется ли изменение комментариев к бронированию?",
        reply_markup=reservation_update_keyboard_step_five)


# Редактирование существующего бронирования - шаг 4-нет
@reservation_router.callback_query(F.data == "reservation_update_step_four_no")
async def reservation_update_step_four_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_four_no)
    await callback.message.answer(
        "Количество гостей не меняем - требуется ли изменение комментариев к бронированию?",
        reply_markup=reservation_update_keyboard_step_five)


# Редактирование существующего бронирования - шаг 5-да
@reservation_router.callback_query(F.data == "reservation_update_step_five_yes")
async def reservation_update_step_five_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_five_yes)
    await callback.message.answer("Введите новый комментарий")


# Редактирование существующего бронирования - шаг 5-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_five_yes))
async def reservation_update_step_five_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_five_yes_continue)
    await state.update_data(special=message.text)
    print(message.text)
    await message.reply(
        f"Новый комментарий - {message.text}, требуется ли изменение блюд?",
        reply_markup=reservation_update_keyboard_step_six)


# Редактирование существующего бронирования - шаг 5-нет
@reservation_router.callback_query(F.data == "reservation_update_step_five_no")
async def reservation_update_step_five_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_five_no)
    await callback.message.answer(
        "Комментарий не меняем - требуется ли изменение блюд?",
        reply_markup=reservation_update_keyboard_step_six)


# Редактирование существующего бронирования - шаг 6-да
@reservation_router.callback_query(F.data == "reservation_update_step_six_yes")
async def reservation_update_step_six_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_six_yes)
    await callback.message.answer("Введите новое блюдо (номер сета или номера сетов через пробел)")


# Редактирование существующего бронирования - шаг 6-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_six_yes))
async def reservation_update_step_six_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_six_yes_continue)
    await state.update_data(dinner_sets=message.text)
    print(message.text)
    await message.reply(
        f"Новые данные о блюдах - {message.text}, введите количество новых блюд (таким же образом. Если не выбрано "
        f"количество, будет выбрано 1)")


# Редактирование существующего бронирования - шаг 6-да-продолжение-количество

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_six_yes_continue))
async def reservation_update_step_six_yes_continue(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_six_yes_continue)
    await state.update_data(dinner_sets_quantity=message.text)
    print(message.text)
    await message.reply(
        f"Новые данные о количестве - {message.text}, требуется ли изменение столов?",
        reply_markup=reservation_update_keyboard_step_seven)


# Редактирование существующего бронирования - шаг 6-нет
@reservation_router.callback_query(F.data == "reservation_update_step_six_no")
async def reservation_update_step_six_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_six_no)
    await callback.message.answer(
        "Блюда не меняем - требуется ли изменение столов?",
        reply_markup=reservation_update_keyboard_step_seven)


# Редактирование существующего бронирования - шаг 7-да
@reservation_router.callback_query(F.data == "reservation_update_step_seven_yes")
async def reservation_update_step_seven_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_seven_yes)
    await callback.message.answer("Введите новый номер или новые номера столов")


# Редактирование существующего бронирования - шаг 7-да-продолжение

@reservation_router.message(StateFilter(StateAdmin.reservation_update_step_seven_yes))
async def reservation_update_step_seven_yes(message: Message, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_seven_yes_continue)
    await state.update_data(table_ids=message.text)
    print(message.text)
    await message.reply(
        f"Новые данные о столах - {message.text}, подтвердите корректность данных",
        reply_markup=reservation_update_confirmation_keyboard)


# Редактирование существующего бронирования - шаг 7-нет
@reservation_router.callback_query(F.data == "reservation_update_step_six_no")
async def reservation_update_step_seven_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_seven_no)
    await callback.message.answer(
        "Блюда не меняем - требуется ли изменение столов?",
        reply_markup=reservation_update_keyboard_step_eight)


# Редактирование существующего бронирования - шаг 8-нет
@reservation_router.callback_query(F.data == "reservation_update_step_seven_no")
async def reservation_update_step_eight_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.reservation_update_step_eight_no)
    await callback.message.answer(
        "Столы не меняем - подтвердите корректность данных",
        reply_markup=reservation_update_confirmation_keyboard)


# Редактирование существующего бронирования - отмена

@reservation_router.callback_query(F.data == "confirm_cancel_update")
async def cancel_reservation_update(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование бронирования отменено")
    await state.clear()
    await state.set_state(StateAdmin.reservation_main_menu)
    await state.clear()
    await callback.message.answer(" вернуться в меню", reply_markup=reservation_redact_all_return_keyboard)


# Редактирование существующего бронирования - подтверждение

@reservation_router.callback_query(F.data == "confirm_submit_update")
async def confirm_reservation_update(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование бронирования подтверждено")
    await state.set_state(StateAdmin.reservation_update_step_final)

    update_reservation_data = await state.get_data()

    update_reservation_date = update_reservation_data.get('reservation_date')
    if update_reservation_date:
        update_reservation_date_formatted = datetime.strptime(update_reservation_date, "%d%m%Y").date()
        update_reservation_date_time = datetime.combine(update_reservation_date_formatted, datetime.min.time())
    else:
        update_reservation_date_time = None
    update_data_dict = {k: v for k, v in {
        'user_id': update_reservation_data.get('user_id'),
        'reservation_date': update_reservation_date_time,
        'guest_count': update_reservation_data.get('guest_count'),
        'special': update_reservation_data.get('special'),
    }.items() if v is not None}
    reservation_id = update_reservation_data['reservation_id']
    print(reservation_id)
    print(update_data_dict)

    await admin_reservation_crud.update_reservation(reservation_id, update_data_dict)
    await state.clear()
    await callback.message.answer(" вернуться в меню", reply_markup=reservation_redact_all_return_keyboard)
