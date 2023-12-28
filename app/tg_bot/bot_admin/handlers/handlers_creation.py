from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from app.crud.dinnerset import dinnerset_crud
from app.crud.restaurant import restaurant_crud
from app.crud.table import table_crud
from app.crud.user import user_crud
from app.test_google_sheets import test_synchronize_data
from ..states import StateAdmin
from ..keyboards.keyboards_creation import creation_keyboard, creation_user_keyboard, creation_restaurant_keyboard, \
    creation_table_keyboard, creation_set_keyboard, creation_user_confirmation_keyboard, \
    creation_table_confirmation_keyboard, creation_set_confirmation_keyboard, creation_restaurant_confirmation_keyboard, \
    creation_return_keyboard_users, creation_return_keyboard_restaurant, creation_return_keyboard_tables, \
    creation_return_keyboard_sets


creation_router = Router()


# Меню настроек и редактирования объектов

@creation_router.callback_query(F.data == "creation_main_menu")
async def creation_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Меню настроек и редактирования данных, выберите объект",
                                  reply_markup=creation_keyboard)
    await state.set_state(StateAdmin.creation_main_menu)


# Выбор создания или просмотра пользователей

@creation_router.callback_query(F.data == "creation_user_menu")
async def creation_user_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание или просмотр пользователей?",
                                  reply_markup=creation_user_keyboard)
    await state.set_state(StateAdmin.creation_user_menu)


# Создание нового администратора - шаг 1

@creation_router.callback_query(F.data == "creation_user_new")
async def creation_user_new_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Cоздание нового администратора - введите имя нового администратора")
    await state.set_state(StateAdmin.creation_user_new_step_one)


# Создание нового администратора - шаг 2

@creation_router.message(StateFilter(StateAdmin.creation_user_new_step_one))
async def creation_user_new_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Введенное имя нового администратора - {message.text}, введите chat_id администратора")
    await state.set_state(StateAdmin.creation_user_new_step_two)


# Создание нового администратора - шаг 3

@creation_router.message(StateFilter(StateAdmin.creation_user_new_step_two))
async def creation_user_new_step_three(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    print(message.text)
    await message.reply(
        f"Введенный chat_id нового администратора - {message.text}, введите номер телефона администратора в формате +7XXXxxxxxxx")
    await state.set_state(StateAdmin.creation_user_new_step_three)


# Создание нового администратора - шаг 4

@creation_router.message(StateFilter(StateAdmin.creation_user_new_step_three))
async def creation_user_new_step_four(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    print(message.text)
    await message.reply(
        f"Введенный номер телефона нового администратора - {message.text}, введите email администратора")
    await state.set_state(StateAdmin.creation_user_new_step_four)


# Создание нового администратора - шаг 5

@creation_router.message(StateFilter(StateAdmin.creation_user_new_step_four))
async def creation_user_new_step_five(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    print(message.text)
    await state.set_state(StateAdmin.creation_user_new_step_five)
    await message.reply(f"Введенный email нового администратора - {message.text}, подтвердите корректность данных",
                        reply_markup=creation_user_confirmation_keyboard)


# Создание нового администратора - отмена

@creation_router.callback_query(StateFilter(StateAdmin.creation_user_new_step_five),
                                F.data == "cancel_creation_admin")
async def cancel_creation_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание администратора отменено")
    await state.clear()
    await callback.message.answer("вернуться в меню", reply_markup=creation_return_keyboard_users)


# Создание нового администратора - подтверждение

@creation_router.callback_query(StateFilter(StateAdmin.creation_user_new_step_five),
                                F.data == "confirm_creation_admin")
async def confirm_creation_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание администратора подтверждено")
    await state.set_state(StateAdmin.creation_user_new_step_six)
    user_data = await state.get_data()

    user_data_dict = dict(
        name=user_data['name'],
        chat_id=user_data['chat_id'],
        phone_number=user_data['phone_number'],
        email=user_data['email'],
        is_active=True,
        is_admin=True,
        is_staff=True,
        created=datetime.now(),
    )
    await user_crud.create(user_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_users)
    await state.clear()


# Просмотр пользователя по email

@creation_router.callback_query(F.data == "creation_user_look_by_email")
async def creation_user_look_by_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Просмотр пользователя по email, введите email для просмотра")
    await state.set_state(StateAdmin.creation_user_look_by_email)


# Просмотр пользователя по email - продолжение

@creation_router.message(StateFilter(StateAdmin.creation_user_look_by_email))
async def creation_user_look_by_email_continue(message: Message, state: FSMContext):
    await state.update_data(look_admin_email=message.text)
    print(message.text)
    await state.set_state(StateAdmin.creation_user_look_by_email_continue)
    user_email = str(message.text)

    try:
        user_info = await user_crud.get_by_email(user_email)
        await message.answer(
            f"Данные о пользователе с email {message.text}:\n    "
            f"имя - {user_info.name},\n    "
            f"телефон - {user_info.phone_number},\n    "
            f"email - {user_info.email},\n    "
            f"chat_id - {user_info.chat_id}\n    "
            f"id - {user_info.id}", reply_markup=creation_return_keyboard_users)
    except AttributeError:
        await message.answer("Пользователь с указанным email в базе отсутствует",
                             reply_markup=creation_return_keyboard_users)
    await state.clear()


# Просмотр пользователя по телефону

@creation_router.callback_query(F.data == "creation_user_look_by_phone")
async def creation_user_look_by_email(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Просмотр пользователя по телефону, введите номер для просмотра в формате +7XXXxxxxxxx")
    await state.set_state(StateAdmin.creation_user_look_by_phone)


# Просмотр пользователя по телефону - продолжение

@creation_router.message(StateFilter(StateAdmin.creation_user_look_by_phone))
async def creation_user_look_by_phone_continue(message: Message, state: FSMContext):
    await state.update_data(look_admin_phone=message.text)
    print(message.text)
    await state.set_state(StateAdmin.creation_user_look_by_phone_continue)
    user_phone = str(message.text)
    user_info = await user_crud.get_by_phone_number(user_phone)

    try:
        user_info = await user_crud.get_by_phone_number(user_phone)
        await message.answer(
            f"Данные о пользователе с email {message.text}:\n    "
            f"имя - {user_info.name},\n    "
            f"телефон - {user_info.phone_number},\n    "
            f"email - {user_info.email},\n    "
            f"chat_id - {user_info.chat_id},\n    "
            f"id - {user_info.id}", reply_markup=creation_return_keyboard_users)
    except AttributeError:
        await message.answer("Пользователь с указанным номером телефоне в базе отсутствует",
                             reply_markup=creation_return_keyboard_users)
    await state.clear()


# Меню выбора создания или просмотра филиалов кафе

@creation_router.callback_query(F.data == "creation_restaurant_menu")
async def creation_restaurant_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание или просмотр филиалов кафе?",
                                  reply_markup=creation_restaurant_keyboard)
    await state.set_state(StateAdmin.creation_restaurant_menu)


# Создание нового кафе - шаг 1

@creation_router.callback_query(F.data == "creation_restaurant_new")
async def creation_restaurant_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание нового кафе, введите название нового филиала")
    await state.set_state(StateAdmin.creation_restaurant_step_one)


# Создание нового кафе - шаг 2

@creation_router.message(StateFilter(StateAdmin.creation_restaurant_step_one))
async def creation_restaurant_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Выбрано имя филиала - {message.text}, введите адрес филиала")
    await state.set_state(StateAdmin.creation_restaurant_step_two)


# Создание нового кафе - шаг 3

@creation_router.message(StateFilter(StateAdmin.creation_restaurant_step_two))
async def creation_restaurant_step_three(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    print(message.text)
    await message.reply(f"Выбран адрес филиала - {message.text}, введите контакты менеджера филиала")
    await state.set_state(StateAdmin.creation_restaurant_step_three)


# Создание нового кафе - шаг 4

@creation_router.message(StateFilter(StateAdmin.creation_restaurant_step_three))
async def creation_restaurant_step_four(message: Message, state: FSMContext):
    await state.update_data(contact_info=message.text)
    print(message.text)
    await message.reply(f"Контакты менеджера филиала - {message.text}, введите id изображения кафе")
    await state.set_state(StateAdmin.creation_restaurant_step_four)


# Создание нового кафе - шаг 6 (да, шестой шаг после четвертого)

@creation_router.message(StateFilter(StateAdmin.creation_restaurant_step_four))
async def creation_restaurant_step_six(message: Message, state: FSMContext):
    await state.update_data(image_id=message.text)
    print(message.text)
    await message.reply("Подтвердите корректность данных",
                        reply_markup=creation_restaurant_confirmation_keyboard)
    await state.set_state(StateAdmin.creation_restaurant_step_six)


# Создание нового филиала кафе - отмена

@creation_router.callback_query(StateFilter(StateAdmin.creation_restaurant_step_six),
                                F.data == "cancel_creation_restaurant")
async def cancel_creation_restaurant(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание филиала кафе отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_restaurant)
    await state.clear()


# Создание нового филиала кафе - подтверждение

@creation_router.callback_query(StateFilter(StateAdmin.creation_restaurant_step_six),
                                F.data == "confirm_creation_restaurant")
async def confirm_creation_restaurant(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание филиала кафе подтверждено")
    await state.set_state(StateAdmin.creation_restaurant_step_seven)
    restaurant_data = await state.get_data()

    restaurant_data_dict = dict(
        name=restaurant_data['name'],
        location=restaurant_data['location'],
        contact_info=restaurant_data['contact_info'],
        image_id=restaurant_data['image_id'],
    )
    print(restaurant_data_dict)
    await state.clear()
    await restaurant_crud.create(restaurant_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_restaurant)


# Просмотр существующих кафе

@creation_router.callback_query(F.data == "creation_restaurant_look")
async def creation_restaurant_look(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.creation_restaurant_look)
    restaurants_info = await restaurant_crud.get_multi()
    if restaurants_info:
        print(restaurants_info)
        await callback.message.answer(text="Просмотр существующих кафе:")
        for i in range(0, len(restaurants_info)):
            await callback.message.answer(text=f"{restaurants_info[i]}")
    else:
        await callback.message.answer(text="В базе нет ни одного филиала кафе")
    await state.clear()
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_restaurant)


# Меню создания или редактирования столов

@creation_router.callback_query(F.data == "creation_table_menu")
async def creation_table_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание или редактирование столов",
                                  reply_markup=creation_table_keyboard)
    await state.set_state(StateAdmin.creation_table_menu)


# Создание нового стола - шаг 1

@creation_router.callback_query(F.data == "creation_table_new")
async def creation_table_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Cоздание стола, введите id кафе для которого создается стол")
    await state.set_state(StateAdmin.creation_table_step_one)


# Создание нового стола - шаг 2

@creation_router.message(StateFilter(StateAdmin.creation_table_step_one))
async def creation_table_step_two(message: Message, state: FSMContext):
    await state.update_data(restaurant_id=message.text)
    print(message.text)
    await message.reply(
        f"Выбран id кафе для которого создается стол - {message.text}, введите номер создаваемого стола")
    await state.set_state(StateAdmin.creation_table_step_two)


# Создание нового стола - шаг 3

@creation_router.message(StateFilter(StateAdmin.creation_table_step_two))
async def creation_table_step_three(message: Message, state: FSMContext):
    await state.update_data(table_number=message.text)
    print(message.text)
    await message.reply(f"Номер создаваемого стола - {message.text}, укажите вместимость создаваемого стола от 1 до 6")
    await state.set_state(StateAdmin.creation_table_step_three)


@creation_router.message(StateFilter(StateAdmin.creation_table_step_three))
async def creation_table_step_four(message: Message, state: FSMContext):
    await state.update_data(capacity=message.text)
    print(message.text)
    await message.reply(f"Номер создаваемого стола - {message.text}, укажите группу создаваемого стола")
    await state.set_state(StateAdmin.creation_table_step_four)


# Создание нового стола - шаг 5

@creation_router.message(StateFilter(StateAdmin.creation_table_step_four))
async def creation_table_step_five(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    print(message.text)
    await message.reply("подтвердите создание стола", reply_markup=creation_table_confirmation_keyboard)
    await state.set_state(StateAdmin.creation_table_step_five)


# Создание нового стола - отмена

@creation_router.callback_query(StateFilter(StateAdmin.creation_table_step_five),
                                F.data == "cancel_creation_table")
async def cancel_creation_table(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание стола отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_tables)
    await state.clear()


# Создание нового стола - подтверждение

@creation_router.callback_query(StateFilter(StateAdmin.creation_table_step_five),
                                F.data == "confirm_creation_table")
async def creation_table_step_five(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.creation_restaurant_step_six)

    table_data = await state.get_data()

    table_data_dict = dict(
        restaurant_id=table_data['restaurant_id'],
        table_number=table_data['table_number'],
        capacity=table_data['capacity'],
        group=table_data['group'],
    )
    print(table_data_dict)
    await table_crud.create(table_data=table_data_dict)
    await callback.message.answer(text="Создание стола подтверждено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_tables)
    await state.clear()


# Просмотр столов

@creation_router.callback_query(F.data == "creation_table_look")
async def creation_table_look(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.creation_table_look)
    tables_info = await table_crud.get_multi()
    if tables_info and tables_info != "В базе нет информации о столах":
        print(tables_info)
        await callback.message.answer(text="Просмотр существующих столов:")
        for i in range(0, len(tables_info)):
            await callback.message.answer(text=f"{tables_info[i]}")

    else:
        await callback.message.answer(text="В базе нет ни одного стола")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_tables)
    await state.clear()


# Меню выбора создания или редактирования блюд

@creation_router.callback_query(F.data == "creation_set_menu")
async def creation_set_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание или редактирование блюд",
                                  reply_markup=creation_set_keyboard)
    await state.set_state(StateAdmin.creation_set_menu)


# Создание блюда - шаг 1

@creation_router.callback_query(F.data == "creation_set_new")
async def creation_set_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание блюда, введите название блюда")
    await state.set_state(StateAdmin.creation_set_step_one)


# Создание блюда - шаг 2

@creation_router.message(StateFilter(StateAdmin.creation_set_step_one))
async def creation_set_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Введено название блюда - {message.text}, введите описание блюда")
    await state.set_state(StateAdmin.creation_set_step_two)


# Создание блюда - шаг 3

@creation_router.message(StateFilter(StateAdmin.creation_set_step_two))
async def creation_set_step_three(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    print(message.text)
    await message.reply(f"Введено описание блюда - {message.text}, введите стоимость блюда")
    await state.set_state(StateAdmin.creation_set_step_three)


# Создание блюда - шаг 4

@creation_router.message(StateFilter(StateAdmin.creation_set_step_three))
async def creation_set_step_four(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    print(message.text)
    await message.reply(f"Введена стоимость блюда - {message.text}, введите id изображения")
    await state.set_state(StateAdmin.creation_set_step_four)


# Создание блюда - шаг 5

@creation_router.message(StateFilter(StateAdmin.creation_set_step_four))
async def creation_set_step_five(message: Message, state: FSMContext):
    await state.update_data(image_id=message.text)
    print(message.text)
    await message.reply("подтвердите создание блюда", reply_markup=creation_set_confirmation_keyboard)
    await state.set_state(StateAdmin.creation_set_step_five)


# Создание нового блюда - отмена

@creation_router.callback_query(StateFilter(StateAdmin.creation_set_step_five),
                                F.data == "cancel_creation_set")
async def cancel_creation_set(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание блюда отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_sets)
    await state.clear()


# Создание нового блюда - подтверждение

@creation_router.callback_query(StateFilter(StateAdmin.creation_set_step_five),
                                F.data == "confirm_creation_set")
async def creation_set_step_seven(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание блюда подтверждено")
    await state.set_state(StateAdmin.creation_set_step_seven)

    # TODO: добавить передачу данных в CRUD создания блюда
    set_data = await state.get_data()

    set_data_dict = dict(
        name=set_data['name'],
        description=set_data['description'],
        price=set_data['price'],
        image_id=set_data['image_id'],
    )
    await dinnerset_crud.create(obj_in_data=set_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_sets)
    await state.clear()


# Просмотр блюд

@creation_router.callback_query(F.data == "creation_set_look")
async def creation_set_look(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.creation_set_look)
    sets_info = await dinnerset_crud.get_multi()
    if sets_info:
        print(sets_info)
        await callback.message.answer(text="Просмотр существующих блюд:")
        for i in range(0, len(sets_info)):
            await callback.message.answer(text=f"{sets_info[i]}")
    else:
        await callback.message.answer(text="В базе нет ни одного блюда")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_sets)
    await state.clear()


# Регулирование количества гостей


@creation_router.callback_query(F.data == "creation_guests_number")
async def creation_guests_number(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Регулирование количества гостей")
    await state.set_state(StateAdmin.creation_guests_number)


# Синхронизация данных с Google-таблицей


@creation_router.callback_query(F.data == "creation_google_sync")
async def creation_google_sync(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Синхронизация данных с Google-таблицей")
    await state.set_state(StateAdmin.creation_google_sync)
    await test_synchronize_data()
