from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from .keyboards.keyboards_main import to_start_keyboard

state_router = Router()


class StateAdmin(StatesGroup):
    start_menu = State()
    work_menu = State()
    help_menu = State()
    creation_main_menu = State()
    creation_user_menu = State()
    creation_user_new = State()
    creation_user_new_step_one = State()
    creation_user_new_step_two = State()
    creation_user_new_step_three = State()
    creation_user_new_step_four = State()
    creation_user_new_step_five = State()
    creation_user_new_step_six = State()
    creation_user_look_by_email = State()
    creation_user_look_by_email_continue = State()
    creation_user_look_by_phone = State()
    creation_user_look_by_phone_continue = State()
    creation_user_redact = State()
    redaction_user_step_one = State()
    redaction_user_step_two = State()
    redaction_user_step_three = State()
    redaction_user_step_four = State()
    redaction_user_step_five = State()
    redaction_user_step_six = State()
    creation_restaurant_menu = State()
    creation_restaurant_step_one = State()
    creation_restaurant_step_two = State()
    creation_restaurant_step_three = State()
    creation_restaurant_step_four = State()
    creation_restaurant_step_five = State()
    creation_restaurant_step_six = State()
    creation_restaurant_step_seven = State()
    creation_restaurant_look = State()
    creation_restaurant_redaction = State()
    redaction_restaurant_step_one = State()
    redaction_restaurant_step_two = State()
    redaction_restaurant_step_three = State()
    redaction_restaurant_step_four = State()
    redaction_restaurant_step_six = State()
    redaction_restaurant_step_seven = State()
    creation_table_menu = State()
    creation_table_step_one = State()
    creation_table_step_two = State()
    creation_table_step_three = State()
    creation_table_step_four = State()
    creation_table_step_five = State()
    creation_table_look = State()
    creation_table_redaction = State()
    redaction_table_step_one = State()
    redaction_table_step_two = State()
    redaction_table_step_three = State()
    redaction_table_step_four = State()
    redaction_table_step_five = State()
    redaction_table_step_six = State()
    creation_set_menu = State()
    creation_set_step_one = State()
    creation_set_step_two = State()
    creation_set_step_three = State()
    creation_set_step_four = State()
    creation_set_step_five = State()
    creation_set_step_six = State()
    creation_set_step_seven = State()
    creation_set_look = State()
    creation_set_redaction = State()
    redaction_set_step_one = State()
    redaction_set_step_two = State()
    redaction_set_step_three = State()
    redaction_set_step_four = State()
    redaction_set_step_five = State()
    redaction_set_step_seven = State()
    creation_guests_number = State()
    creation_google_sync = State()
    reservation_main_menu = State()
    reservation_look_menu = State()
    reservation_all = State()
    reservation_date = State()
    reservation_date_continue = State()
    reservation_actual = State()
    reservation_email = State()
    reservation_email_continue = State()
    reservation_phone = State()
    reservation_phone_continue = State()
    reservation_by_tg_id = State()
    reservation_redaction_menu = State()
    reservation_creation_step_one = State()
    reservation_creation_step_two = State()
    reservation_creation_step_three = State()
    reservation_creation_step_four = State()
    reservation_creation_step_five = State()
    reservation_creation_step_six = State()
    reservation_creation_step_seven = State()
    reservation_creation_step_eight = State()
    reservation_creation_step_nine = State()
    reservation_update_step_one = State()
    reservation_update_step_two = State()
    reservation_update_step_two_yes = State()
    reservation_update_step_two_yes_continue = State()
    reservation_update_step_two_no = State()
    reservation_update_step_three_yes = State()
    reservation_update_step_three_yes_continue = State()
    reservation_update_step_three_no = State()
    reservation_update_step_four = State()
    reservation_update_step_four_yes = State()
    reservation_update_step_four_yes_continue = State()
    reservation_update_step_four_no = State()
    reservation_update_step_five_no = State()
    reservation_update_step_five_yes = State()
    reservation_update_step_five_yes_continue = State()
    reservation_update_step_six_yes = State()
    reservation_update_step_six_yes_continue = State()
    reservation_update_step_six_no = State()
    reservation_update_step_seven_yes = State()
    reservation_update_step_seven_yes_continue = State()
    reservation_update_step_seven_no = State()
    reservation_update_step_eight_no = State()
    reservation_update_continue = State()
    reservation_update_step_final = State()
    reservation_cancellation = State()
    reservation_cancellation_continue = State()
    reservation_deletion = State()
    reservation_deletion_continue = State()


@state_router.message(F.text.casefold() == "к главному меню")
async def process_(message: Message, state: FSMContext) -> None:
    await state.set_state(StateAdmin.start_menu)
    await message.reply(
        "Возвращение в главное меню! \n"
        "Для перезапуска нажмите /start. \n"
        "Для работы с ботом нажмите /work. \n"
        "Для описания опций нажмите /help. \n"
        "Кнопка 'К главному меню' возвращает на главный экран. \n"
        "Кнопка 'Назад' возвращает на предыдущее действие. \n"
        "Скрыть кнопки можно скрыть опцией справа.",
        reply_markup=to_start_keyboard,
    )


@state_router.message(F.text.casefold() == "debug:print state")
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

# @state_router.message(F.text.casefold() == "назад")
# async def process_like_write_bots(message: Message, state: FSMContext) -> None:
#     current_state = await state.get_state()
#     print(current_state)


# async def check_state(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()  # текущее машинное состояние пользователя
#     if current_state in registration: # registration - название класса состояний
#         print('Пользователь в одном из состояний регистрации')
#     if current_state == 'registration:waiting_for_name':
#         print('Пользователь находиться в конкретном состоянии - waiting_for_name из класса registration')


# @state_router.message(StateAdmin.name)
# async def process_name(message: Message, state: FSMContext) -> None:
#     await state.update_data(name=message.text)
#     await state.set_state(StateAdmin.like_bots)
#     await message.answer(
#         f"Nice to meet you! Did you like to write bots?",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[
#                 [
#                     KeyboardButton(text="Yes"),
#                     KeyboardButton(text="No"),
#                 ]
#             ],
#             resize_keyboard=True,
#         ),
#     )
#
#
# @state_router.message(StateAdmin.like_bots, F.text.casefold() == "yes")
# async def process_like_write_bots(message: Message, state: FSMContext) -> None:
#     await state.set_state(StateAdmin.language)
#
#     await message.reply(
#         "Cool! I'm too!\nWhat programming language did you use for it?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#
# @state_router.message(StateAdmin.like_bots, F.text.casefold() == "no")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     await state.clear()
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await show_summary(message=message, data=data, positive=False)
#
#
# @state_router.message(StateAdmin.like_bots)
# async def process_unknown_write_bots(message: Message) -> None:
#     await message.reply("I don't understand you :(")
#
#
# @state_router.message(StateAdmin.language)
# async def process_language(message: Message, state: FSMContext) -> None:
#     data = await state.update_data(language=message.text)
#     await state.clear()
#
#     if message.text.casefold() == "python":
#         await message.reply(
#             "Python, you say? That's the language that makes my circuits light up! 😉"
#         )
#
#     await show_summary(message=message, data=data)
#
#
# async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
#     name = data["name"]
#     language = data.get("language", "<something unexpected>")
#     text = f"I'll keep in mind that!"
#     text += (
#         f"you like to write bots with"
#         if positive
#         else "you don't like to write bots, so sad..."
#     )
#     await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
#
#
# @state_router.message(Command("cancel"))
# @state_router.message(F.text.casefold() == "cancel")
# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     logging.info("Cancelling state %r", current_state)
#     await state.clear()
#     await message.answer(
#         "Cancelled.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
