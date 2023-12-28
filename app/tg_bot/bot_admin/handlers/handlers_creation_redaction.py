from datetime import datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from app.crud.dinnerset import dinnerset_crud
from app.crud.restaurant import restaurant_crud
from app.crud.table import table_crud
from app.crud.user import user_crud
from ..states import StateAdmin
from ..keyboards.keyboards_creation import creation_return_keyboard_users, creation_return_keyboard_restaurant, creation_return_keyboard_tables, \
    creation_return_keyboard_sets, redaction_user_confirmation_keyboard, redaction_restaurant_confirmation_keyboard, \
    redaction_table_confirmation_keyboard, redaction_set_confirmation_keyboard

creation_redaction_router = Router()


# Редактирование администратора - вводим id

@creation_redaction_router.callback_query(F.data == "creation_user_redact")
async def creation_user_new_step_one(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование администратора - введите id изменяемого администратора")
    await state.set_state(StateAdmin.creation_user_redact)


# Редактирование администратора - шаг 1

@creation_redaction_router.message(StateFilter(StateAdmin.creation_user_redact))
async def redaction_user_step_one(message: Message, state: FSMContext):
    await state.update_data(id_data=message.text)
    user_redaction_data_id = await state.get_data()
    user_id = user_redaction_data_id['id_data']
    our_user = await user_crud.get_by_id(user_id)
    await message.answer(text=f"{our_user}")
    await message.answer(text="Редактирование администратора - введите новое имя администратора")
    await state.set_state(StateAdmin.redaction_user_step_one)


# Редактирование администратора - шаг 2

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_user_step_one))
async def redaction_user_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Введенное имя администратора - {message.text}, введите новый chat_id администратора")
    await state.set_state(StateAdmin.redaction_user_step_two)


# Редактирование администратора - шаг 3

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_user_step_two))
async def redaction_user_step_three(message: Message, state: FSMContext):
    await state.update_data(chat_id=message.text)
    print(message.text)
    await message.reply(
        f"Введенный chat_id администратора - {message.text}, введите новый номер телефона администратора в формате +7XXXxxxxxxx")
    await state.set_state(StateAdmin.redaction_user_step_three)


# Редактирование администратора - шаг 4

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_user_step_three))
async def redaction_user_step_four(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    print(message.text)
    await message.reply(
        f"Введенный номер телефона администратора - {message.text}, введите новый email администратора")
    await state.set_state(StateAdmin.redaction_user_step_four)


# Редактирование администратора - шаг 5

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_user_step_four))
async def redaction_user_step_five(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    print(message.text)
    await state.set_state(StateAdmin.redaction_user_step_five)
    await message.reply(f"Введенный email администратора - {message.text}, подтвердите корректность данных",
                        reply_markup=redaction_user_confirmation_keyboard)


# Редактирование администратора - отмена

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_user_step_five),
                                          F.data == "cancel_redaction_admin")
async def cancel_redaction_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование администратора отменено")
    await state.clear()
    await callback.message.answer("вернуться в меню", reply_markup=creation_return_keyboard_users)


# Редактирование администратора - подтверждение

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_user_step_five),
                                          F.data == "confirm_redaction_admin")
async def confirm_creation_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование администратора подтверждено")
    await state.set_state(StateAdmin.redaction_user_step_six)
    user_data = await state.get_data()
    redacted_user_id = user_data['id_data']
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
    await user_crud.update_user(redacted_user_id, user_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_users)
    await state.clear()


# Редактирование кафе - вводим id

@creation_redaction_router.callback_query(F.data == "creation_restaurant_redaction")
async def creation_restaurant_redaction(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Создание нового кафе, введите id изменяемого филиала кафе")
    await state.set_state(StateAdmin.creation_restaurant_redaction)


# Редактирование кафе - шаг 1

@creation_redaction_router.message(StateFilter(StateAdmin.creation_restaurant_redaction))
async def creation_restaurant_step_two(message: Message, state: FSMContext):
    await state.update_data(id_data=message.text)
    restaurant_redaction_data_id = await state.get_data()
    restaurant_id = restaurant_redaction_data_id['id_data']
    our_restaurant = await restaurant_crud.get_by_id(restaurant_id)
    await message.answer(text=f"{our_restaurant}")
    await message.answer(text="Редактирование филиала кафе - введите новое имя филиала")
    await state.set_state(StateAdmin.redaction_restaurant_step_one)


# Редактирование кафе - шаг 2

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_restaurant_step_one))
async def redaction_restaurant_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Новое имя филиала - {message.text}, введите новый адрес филиала")
    await state.set_state(StateAdmin.redaction_restaurant_step_two)


# Редактирование кафе - шаг 3

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_restaurant_step_two))
async def redaction_restaurant_step_three(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    print(message.text)
    await message.reply(f"Новый адрес филиала - {message.text}, введите новые контакты менеджера филиала")
    await state.set_state(StateAdmin.redaction_restaurant_step_three)


# Редактирование кафе - шаг 4

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_restaurant_step_three))
async def redaction_restaurant_step_four(message: Message, state: FSMContext):
    await state.update_data(contact_info=message.text)
    print(message.text)
    await message.reply(f"Новые контакты менеджера филиала - {message.text}, введите новый id изображения кафе")
    await state.set_state(StateAdmin.redaction_restaurant_step_four)


# Редактирование кафе - шаг 6

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_restaurant_step_four))
async def redaction_restaurant_step_six(message: Message, state: FSMContext):
    # await state.update_data(tables=message.text)
    await state.update_data(image_id=message.text)
    print(message.text)
    await message.reply("Подтвердите корректность данных",
                        reply_markup=redaction_restaurant_confirmation_keyboard)
    await state.set_state(StateAdmin.redaction_restaurant_step_six)


# Редактирование филиала кафе - отмена

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_restaurant_step_six),
                                          F.data == "cancel_redaction_restaurant")
async def cancel_redaction_restaurant(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование филиала кафе отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_restaurant)
    await state.clear()


# Редактирование филиала кафе - подтверждение

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_restaurant_step_six),
                                          F.data == "confirm_redaction_restaurant")
async def confirm_creation_restaurant(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование филиала кафе подтверждено")
    await state.set_state(StateAdmin.redaction_restaurant_step_seven)
    restaurant_data = await state.get_data()
    restaurant_id_redaction = restaurant_data['id_data']
    restaurant_data_dict = dict(
        name=restaurant_data['name'],
        location=restaurant_data['location'],
        contact_info=restaurant_data['contact_info'],
        image_id=restaurant_data['image_id'],
    )
    print(restaurant_data_dict)
    await restaurant_crud.update_restaurant(restaurant_id_redaction, restaurant_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_restaurant)
    await state.clear()


# Редактирование стола - вводим id

@creation_redaction_router.callback_query(F.data == "creation_table_redaction")
async def creation_restaurant_redaction(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование стола, введите id изменяемого стола")
    await state.set_state(StateAdmin.creation_table_redaction)


# Редактирование стола - шаг 1

@creation_redaction_router.message(StateFilter(StateAdmin.creation_table_redaction))
async def redaction_table_step_one(message: Message, state: FSMContext):
    await state.update_data(table_id=message.text)
    await message.answer(text="Редактирование стола, введите id кафе для которого редактируется стол")
    await state.set_state(StateAdmin.redaction_table_step_one)


# Редактирование стола - шаг 2

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_table_step_one))
async def redaction_table_step_two(message: Message, state: FSMContext):
    await state.update_data(restaurant_id=message.text)
    print(message.text)
    await message.reply(
        f"Выбран id кафе для которого редактируется стол - {message.text}, введите новый номер редактируемого стола")
    await state.set_state(StateAdmin.redaction_table_step_two)


# Редактирование стола - шаг 3

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_table_step_two))
async def redaction_table_step_three(message: Message, state: FSMContext):
    await state.update_data(table_number=message.text)
    print(message.text)
    await message.reply(f"Номер редактируемого стола - {message.text}, укажите вместимость редактируемого стола - от "
                        f"1 до 6 человек")
    await state.set_state(StateAdmin.redaction_table_step_three)


# Редактирование стола - шаг 4

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_table_step_three))
async def redaction_table_step_four(message: Message, state: FSMContext):
    await state.update_data(capacity=message.text)
    print(message.text)
    await message.reply(f"Номер создаваемого стола - {message.text}, укажите группу создаваемого стола")
    await state.set_state(StateAdmin.redaction_table_step_four)


# Редактирование стола - шаг 5

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_table_step_four))
async def redaction_table_step_five(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    print(message.text)
    await message.reply("подтвердите редактирование стола", reply_markup=redaction_table_confirmation_keyboard)
    await state.set_state(StateAdmin.redaction_table_step_five)


# Редактирование стола - отмена

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_table_step_five),
                                          F.data == "cancel_redaction_table")
async def cancel_redaction_table(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование стола отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_tables)
    await state.clear()


# Редактирование стола - подтверждение

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_table_step_five),
                                          F.data == "confirm_redaction_table")
async def redaction_table_step_six(callback: CallbackQuery, state: FSMContext):
    await state.set_state(StateAdmin.redaction_table_step_six)

    table_data = await state.get_data()
    table_id = table_data['table_id']
    table_data_dict = dict(
        restaurant_id=table_data['restaurant_id'],
        table_number=table_data['table_number'],
        capacity=table_data['capacity'],
        group=table_data['group'],
    )
    print(table_data_dict)
    await table_crud.update_table(table_id, table_data_dict)
    await callback.message.answer(text="Редактирование стола подтверждено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_tables)
    await state.clear()


# Редактирование блюда - вводим id

@creation_redaction_router.callback_query(F.data == "creation_dinnerset_redaction")
async def creation_set_redaction(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование блюда, введите id изменяемого блюда")
    await state.set_state(StateAdmin.creation_set_redaction)


# Редактирование блюда - шаг 1

@creation_redaction_router.message(StateFilter(StateAdmin.creation_set_redaction))
async def redaction_set_step_one(message: Message, state: FSMContext):
    await state.update_data(set_id=message.text)
    await message.answer(text="Редактирование блюда, введите новое название блюда")
    await state.set_state(StateAdmin.redaction_set_step_one)


# Редактирование блюда - шаг 2

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_set_step_one))
async def redaction_set_step_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    print(message.text)
    await message.reply(f"Новое название блюда - {message.text}, введите новое описание блюда")
    await state.set_state(StateAdmin.redaction_set_step_two)


# Редактирование блюда - шаг 3

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_set_step_two))
async def redaction_set_step_three(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    print(message.text)
    await message.reply(f"Введено новое описание блюда - {message.text}, введите новую стоимость блюда")
    await state.set_state(StateAdmin.redaction_set_step_three)


# Редактирование блюда - шаг 4

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_set_step_three))
async def redaction_set_step_four(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    print(message.text)
    await message.reply(f"Введена новая стоимость блюда - {message.text}, введите новый id изображения")
    await state.set_state(StateAdmin.redaction_set_step_four)


# Редактирование блюда - шаг 5

@creation_redaction_router.message(StateFilter(StateAdmin.redaction_set_step_four))
async def redaction_set_step_five(message: Message, state: FSMContext):
    await state.update_data(image_id=message.text)
    print(message.text)
    await message.reply("подтвердите редактирование блюда", reply_markup=redaction_set_confirmation_keyboard)
    await state.set_state(StateAdmin.redaction_set_step_five)


# Редактирование блюда - отмена

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_set_step_five),
                                          F.data == "cancel_redaction_set")
async def cancel_creation_set(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование блюда отменено")
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_sets)
    await state.clear()


# Редактирование блюда - подтверждение

@creation_redaction_router.callback_query(StateFilter(StateAdmin.redaction_set_step_five),
                                          F.data == "confirm_redaction_set")
async def redaction_set_step_seven(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Редактирование блюда подтверждено")
    await state.set_state(StateAdmin.redaction_set_step_seven)

    set_data = await state.get_data()
    set_id = set_data['set_id']
    set_data_dict = dict(
        name=set_data['name'],
        description=set_data['description'],
        price=set_data['price'],
        image_id=set_data['image_id'],
    )
    await dinnerset_crud.update_dinnerset(set_id, set_data_dict)
    await callback.message.answer(" вернуться в меню", reply_markup=creation_return_keyboard_sets)
    await state.clear()
