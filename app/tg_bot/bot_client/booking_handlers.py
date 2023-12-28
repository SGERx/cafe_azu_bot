from pathlib import Path
from datetime import datetime, timedelta

from aiogram import Bot, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery, Message, FSInputFile,
    InputMediaPhoto, LabeledPrice, PreCheckoutQuery, ContentType
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from app.crud.dinnerset import dinnerset_crud
from app.services.services_cli_bot import (
    search_places_in_restaurants,
)
from app.tg_bot.bot_client.apscheduler_hendler import (
    delete_reservation_by_time_limit
)
from app.tg_bot.bot_client.callback_factories import (
    CalendarCallbackFactory,
    DishCallbackFactory,
)
from app.tg_bot.bot_client.filters import (
    IsValidFillFhone,
    IsValidFillName,
    IsValidFillNumPeople,
    is_valid_date,
)
from app.tg_bot.bot_client.keyboards import (
    ChoiceDinnerSets,
    SimpleCalendar,
    create_choice_dish_keyboard,
    create_positive_negative_keyboard,
    create_restaurant_keyboard,
    keyboard_generator,
)
from app.tg_bot.bot_client.lexicon_cli import (
    FORMAT_DATE,
    LEXICON_TEXT,
    BUTTON_TEXT,
    LEXICON_WARNINGS,
    RESTAURANTS,
    get_prev_text,
)
from app.tg_bot.bot_client.states import (
    FSMReservation,
    add_curr_state,
    get_prev_state,
)
from app.tg_bot.bot_client.utils import map_orm_to_pydantic, map_pydantic_to_json

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

booking_router = Router()


@booking_router.callback_query(~StateFilter(default_state), F.data == "cancel")
async def process_cancel_command_state(callback: CallbackQuery, state: FSMContext):
    #! новая правка
    inp_ph = FSInputFile(path=BASE_DIR / "media/choice_dish.jpg")
    photo = InputMediaPhoto(
        media=inp_ph,
        caption=LEXICON_TEXT["cancel"],
    )
    try:
        await callback.message.edit_media(media=photo)
    except TelegramBadRequest:
        await callback.message.edit_text(text=LEXICON_TEXT["cancel"])

    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@booking_router.message(StateFilter(FSMReservation.fill_name), IsValidFillName())
async def process_name_for_reserv(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    markup = create_positive_negative_keyboard(
        positive=BUTTON_TEXT["back"],
        negative=BUTTON_TEXT["cancel"],
        calback_n="cancel",
        callback_p="back",
    )
    await message.answer(
        text=LEXICON_TEXT["fill_phone"],
        reply_markup=markup,
    )
    await state.set_state(FSMReservation.fill_phone)
    await add_curr_state(state, lexicon_key="fill_phone", markup="yes_no")


# * Этот хэндлер будет срабатывать, если во время ввода имени
# * будет введено что-то некорректное
@booking_router.message(StateFilter(FSMReservation.fill_name))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_WARNINGS["fill_name"])


# * обработка телефона, смена состояния на получение даты для бронирования
@booking_router.message(StateFilter(FSMReservation.fill_phone), IsValidFillFhone())
async def process_phone_for_reserv(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(
        LEXICON_TEXT["choice_date"],
        reply_markup=await SimpleCalendar().start_calendar(),
    )

    await state.set_state(FSMReservation.fill_date)
    await add_curr_state(state, lexicon_key="choice_date", markup="calendar")


# * Хендлер для возврата на шаг с выбором даты в случае отсутствия мест при прошлом выборе.
@booking_router.callback_query(
    StateFilter(FSMReservation.fill_phone), F.data == "another_date"
)
async def process_choice_another_date_for_reserv(
    callback: CallbackQuery, state: FSMContext
):
    await callback.message.answer(
        text=LEXICON_TEXT["choice_date"],
        reply_markup=await SimpleCalendar().start_calendar(),
    )

    await state.set_state(FSMReservation.fill_date)


# * Этот хэндлер будет срабатывать, если во время ввода номера телефона
# * будет введено что-то некорректное
@booking_router.message(StateFilter(FSMReservation.fill_phone))
async def warning_not_phone(message: Message):
    await message.answer(text=LEXICON_WARNINGS["fill_phone"])


# * обработка даты, смена состояния на получение количества гостей
# todo сделать календарь ограниченным в соответствии с константами продолжительности поста
@booking_router.callback_query(
    StateFilter(FSMReservation.fill_date),
    CalendarCallbackFactory.filter(),
)
async def process_date_for_reserv(
    callback: CallbackQuery, callback_data: dict, state: FSMContext
):
    selected, date = await SimpleCalendar().process_selection(callback, callback_data)
    if selected:
        if is_valid_date(date):
            # todo настроить формат даты под модель reservation
            await state.update_data(date=date.strftime(FORMAT_DATE))
            await callback.message.edit_text(f"Ваш выбор: {date.strftime(FORMAT_DATE)}")
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT["back"],
                negative=BUTTON_TEXT["cancel"],
                calback_n="cancel",
                callback_p="back",
            )
            storage_data = await state.get_data()
            num_people = storage_data.get("num_people", None)
            # * если в хранилище есть данные о количестве человек, значит это повторный выбор даты
            # * добавлено для отправки немного другого сообщения
            if num_people:
                await callback.message.answer(
                    text=LEXICON_TEXT["number_of_seats_correct"],
                    reply_markup=markup,
                )
            else:
                await callback.message.answer(
                    text=LEXICON_TEXT["number_of_seats"],
                    reply_markup=markup,
                )
            await state.set_state(FSMReservation.fill_num_people)
            await add_curr_state(
                state,
                lexicon_key="number_of_seats_correct",
                markup=None,
            )
        else:
            await callback.message.edit_text(
                text=LEXICON_WARNINGS["choice_date"],
                reply_markup=await SimpleCalendar().start_calendar(),
            )


@booking_router.message(StateFilter(FSMReservation.fill_date))
async def warning_not_correct_date(message: Message):
    await message.answer(text=LEXICON_WARNINGS["choice_date"])


# * обработка данных по людям, проверка наличия мест, если нет предлагается выбрать другую дату или закончить
# * если да переход на выбор ресторанов, смена состояния на выбор ресторанов;
# todo если процес подбора будет продолжительным, добавить состояние печати бота
@booking_router.message(
    StateFilter(FSMReservation.fill_num_people), IsValidFillNumPeople()
)
async def process_num_people_for_reserv(message: Message, state: FSMContext):
    num_people = message.text
    # * Сохраняем колочество гостей
    await state.update_data(num_people=num_people)

    # * Запускается поиск мест в ресторанах и возвращается список ресторанов,
    # * подходящих для бронирования. Создаем клавиматуру со списком
    # * для выбора варианта либо отказаться
    # data_storage = await state.get_data()
    # possible_booking_options = await table_crud.get_restaurants_and_tables(
    #     guest_count=int(num_people), date=data_storage["date"]
    # )
    result = search_places_in_restaurants(
        num_people, date="01-01-99"
    )  # ? search_places_in_restaurants - фиктивная функция
    # if possible_booking_options:
    if result:  # ! новые правки
        await message.answer_photo(
            photo=FSInputFile(BASE_DIR / "media/choice_rest.jpg"),
            caption=LEXICON_TEXT["fill_restaurant"],
            reply_markup=create_restaurant_keyboard(
                RESTAURANTS
            ),  # todo убрать dict из аргументов и исправить цикл
        )
        await state.set_state(FSMReservation.fill_restaurant)
        await add_curr_state(
            state, lexicon_key="fill_restaurant", markup="create_rest_kb"
        )
        # todo сохранить полученные рестораны или нет
    else:
        markup = create_positive_negative_keyboard(
            positive=BUTTON_TEXT["another_date"],
            negative=BUTTON_TEXT["cancel"],
            calback_n="cancel",
            callback_p="another_date",
        )
        await message.answer(
            text=LEXICON_TEXT["choice_another_date"], reply_markup=markup
        )
        await state.set_state(FSMReservation.fill_phone)
        await add_curr_state(
            state,
            lexicon_key="choice_another_date",
            markup="yes_no",
            param_kb={"positive": "another_date", "negative": "cancel"},
        )


@booking_router.message(StateFilter(FSMReservation.fill_num_people))
async def warning_not_correct_num_people(message: Message):
    await message.answer(text=LEXICON_WARNINGS["number_of_seats"])


# * обработка выбора ресторана, смена состояния на
# * отправка сообщения с клавиатурой выбор сетов
@booking_router.callback_query(
    StateFilter(FSMReservation.fill_restaurant),
    F.data.in_(
        [
            "kazanmall",
            "it_park",
            "republic",
            "decembrites",
        ]
    ),
)
async def process_restaurant_for_reserv(
        callback: CallbackQuery,
        state: FSMContext,
        apscheduler: AsyncIOScheduler,
        bot: Bot
):
    await state.update_data(restaurant=RESTAURANTS[callback.data])
    data_storage = await state.get_data()
    # * Здесь пока приблизительно, настрою по факту получения данных на предыдущем шаге
    # reserv_params = {
    #     "user_id": callback.message.from_user.id,
    #     "reservation_date": data_storage["date"],
    #     "guest_count": data_storage["num_people"],
    #     "special": False,
    #     "restaurant_id": data_storage["restaurant"],
    #     "tables": data_storage["tables"],
    # }
    # reserv_obj = await reservation_crud.create_reservation(reserv_params)
    # await state.update_data(reserv_obj=reserv_obj)

    # * получаем сеты и преобразуем их в pydantic-схемы для дальнейшей работы
    # * и сохраняем их в формате json в хранилище
    sets = map_orm_to_pydantic(await dinnerset_crud.get_multi())
    await state.update_data(sets_list=map_pydantic_to_json(sets))
    #! новые правки
    inp_ph = FSInputFile(path=BASE_DIR / "media/choice_dish.jpg")
    photo = InputMediaPhoto(
        media=inp_ph,
        caption=LEXICON_TEXT["choose_dish"],

    )
    await callback.message.edit_media(
        media=photo, reply_markup=create_choice_dish_keyboard(sets_menue=sets)
    )
    job = apscheduler.add_job(
        delete_reservation_by_time_limit,
        trigger='date',
        run_date=datetime.now() + timedelta(minutes=20),
        kwargs={
            'reservation_id': data_storage["restaurant"],
            'state': state,
            'chat_id': callback.message.from_user.id,
            'bot': bot
        })
    await state.update_data(job_id=job.id)
    await state.set_state(FSMReservation.fill_dinner_sets)
    await add_curr_state(state, lexicon_key="choose_dish", markup="choose_dish")


# * Этот хэндлер будет срабатывать, если во время выбора ресторана
# * будет введено/отправлено что-то некорректное
@booking_router.message(StateFilter(FSMReservation.fill_restaurant))
async def warning_not_restaurant(message: Message):
    await message.answer(text=LEXICON_WARNINGS["fill_restaurant"])


@booking_router.callback_query(
    StateFilter(FSMReservation.fill_dinner_sets),
    DishCallbackFactory.filter(),
)
async def process_continue_choice_sets(
    callback: CallbackQuery,
    callback_data: dict,
    state: FSMContext,
):
    data_storage = await state.get_data()
    await ChoiceDinnerSets(data_storage["sets_list"]).process_selection(
        callback, callback_data, state
    )


# * Этот хэндлер будет срабатывать, если во время выбора из списка сетов
# * будет нажата кнопка названия блюда, появится флеш-сообщение.
@booking_router.callback_query(
    StateFilter(FSMReservation.fill_dinner_sets), F.data == "tap_name_set"
)
async def warning_not_set(callback: CallbackQuery):
    await callback.answer(
        text=LEXICON_WARNINGS["tap_name_set"],
    )


# * Этот хэндлер будет срабатывать, если во время выбора из списка сетов
# * будет введено/отправлено что-то некорректное
@booking_router.message(StateFilter(FSMReservation.fill_dinner_sets))
async def warning_not_set(message: Message):
    await message.answer(
        text=LEXICON_WARNINGS["choose_dish"],
    )


@booking_router.callback_query(
    StateFilter(FSMReservation.payment), F.data == "yes"
)
async def process_pay_for_reserv(callback: CallbackQuery, state: FSMContext):
    data_storage = await state.get_data()
    prices = []
    for dish, count in data_storage['sets']:
        prices.append(
            LabeledPrice(
                label=f'{dish.name} * {count} шт.',
                amount=dish.price * count * 100)
        )
    await callback.message.answer_invoice(
        title=LEXICON_TEXT["title_invoice"],
        description=LEXICON_TEXT["description_invoice"],
        provider_token='401643678:TEST:17af4eaa-fe98-4c8d-b4eb-e64015d6eba3',  # os.getenv['PAYMENTS_PROVIDER_TOKEN'],
        currency='rub',
        prices=prices,
        payload='Payment through a bot',
        start_parameter='cafe_azu_bot',
    )


@booking_router.pre_checkout_query()
async def pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@booking_router.message(
    F.content_type == ContentType.SUCCESSFUL_PAYMENT,
)
async def successful_payment(
    message: Message,
    state: FSMContext,
    apscheduler: AsyncIOScheduler
):
    data_storage = await state.get_data()
    apscheduler.remove_job(data_storage['job_id'])
    # await reservation_crud.update_reservation(reservation_id=data_storage["reserv_obj"].id, new_data=data_storage["sets"])
    await message.answer(
        text=LEXICON_TEXT["payment"]
    )
    await state.clear()


@booking_router.callback_query(F.data == "back")
async def process_back_button(callback: CallbackQuery, state: FSMContext):
    prev_step = await get_prev_state(state)
    text = get_prev_text(LEXICON_TEXT[prev_step["lexicon_key"]])
    await callback.message.edit_text(
        text=text,
        reply_markup=await keyboard_generator(
            prev_step["markup"], prev_step["param_kb"]
        ),
    )
    await state.set_state(prev_step["prev_state"])

    # * добавляем в стек то состояние к которому вернулись
    await add_curr_state(
        state,
        lexicon_key=prev_step["lexicon_key"],
        markup=prev_step["markup"],
        param_kb=prev_step["param_kb"],
    )


# * Этот хэндлер будет реагировать на любые сообщения пользователя,
# * не предусмотренные логикой работы бота
@booking_router.message()
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_TEXT["no_answer"])
