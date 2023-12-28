import calendar
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    InputMediaPhoto,
)


from app.models import DinnerSet
from app.models.restaurant import Restaurant
from app.schemas.dinnerset_schema import DinnerSetDB
from app.tg_bot.bot_client.lexicon_cli import (
    LEXICON_COMMANDS,
    BUTTON_TEXT,
    LEXICON_TEXT,
    format_order,
)
from app.tg_bot.bot_client.callback_factories import (
    CalendarCallbackFactory,
    DishCallbackFactory,
)
from app.tg_bot.bot_client.states import FSMReservation, add_curr_state
from app.tg_bot.bot_client.utils import map_json_to_pydantic


BASE_DIR = Path(__file__).resolve().parent.parent


# * Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in LEXICON_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)


# * Функция генерации клавиатуры для выбора да или нет
def create_positive_negative_keyboard(
    positive: str,
    negative: str,
    callback_p: str,
    calback_n: str,
    back_b: Optional[tuple[str, str]] = None,
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    positive_button = InlineKeyboardButton(text=positive, callback_data=callback_p)
    negative_button = InlineKeyboardButton(text=negative, callback_data=calback_n)
    if back_b:
        back_button = InlineKeyboardButton(text=back_b[0], callback_data=back_b[1])
        kb_builder.row(positive_button, negative_button, back_button, width=3)
    else:
        kb_builder.row(positive_button, negative_button, width=2)

    return kb_builder.as_markup()


# todo убрать dict из аргументов и исправить цикл
def create_restaurant_keyboard(restaurants: Union[list[Restaurant], dict]):
    kb_builder = InlineKeyboardBuilder()
    for key, value in restaurants.items():
        kb_builder.row(InlineKeyboardButton(text=value, callback_data=key))
    kb_builder.row(
        # InlineKeyboardButton(text=BUTTON_TEXT["back"], callback_data="back"),
        InlineKeyboardButton(text=BUTTON_TEXT["cancel"], callback_data="cancel"),
    )
    return kb_builder.as_markup()


def create_choice_dish_keyboard(sets_menue: list[DinnerSetDB]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    for button in sets_menue:
        callback_data = DishCallbackFactory(
            price=button.price,
            id=button.id,
        )
        buttons.append(
            InlineKeyboardButton(
                text=BUTTON_TEXT["name_set"].format(
                    name=button.name[:6],
                    price=button.price,  # ! сопоставить срез имени с текущей базой
                ),
                callback_data="tap_name_set",
            )
        )
        buttons.append(
            InlineKeyboardButton(
                text=BUTTON_TEXT["description"],
                callback_data=callback_data.set_attr(
                    name="act", value="description"
                ).pack(),
            )
        )
        buttons.append(
            InlineKeyboardButton(
                text=BUTTON_TEXT["add"],
                callback_data=callback_data.set_attr(name="act", value="add").pack(),
            )
        )
    buttons.append(InlineKeyboardButton(text=BUTTON_TEXT["back"], callback_data="back"))
    buttons.append(
        InlineKeyboardButton(text=BUTTON_TEXT["cancel"], callback_data="cancel")
    )
    kb_builder.row(*buttons)
    kb_builder.adjust(3)
    return kb_builder.as_markup()


class SimpleCalendar:
    """Класс для формирования клавиатуры календаря и обработки значений возвращемых клавиатурой"""

    async def start_calendar(
        self, year: int = datetime.now().year, month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        """
        Создает встроенную клавиатуру с указанными годом и месяцем
        :param int year: год для использования в календаре, если его нет, используется текущий год.
        :param int month: месяц для использования в календаре, если его нет, используется текущий месяц.
        ::return: Возвращает объект клавиатуры в виде календаря.
        """
        inline_kb = InlineKeyboardBuilder()
        ignore_callback = CalendarCallbackFactory(
            act="IGNORE", year=year, month=month, day=0
        ).pack()
        inline_kb.row(width=7)
        inline_kb.add(
            InlineKeyboardButton(
                text="<<",
                callback_data=CalendarCallbackFactory(
                    act="PREV-YEAR", year=year, month=month, day=1
                ).pack(),
            )
        )
        inline_kb.add(
            InlineKeyboardButton(
                text=f"{calendar.month_name[month]} {str(year)}",
                callback_data=ignore_callback,
            )
        )
        inline_kb.add(
            InlineKeyboardButton(
                text=">>",
                callback_data=CalendarCallbackFactory(
                    act="NEXT-YEAR", year=year, month=month, day=1
                ).pack(),
            )
        )
        # Second row - Week Days
        inline_kb.row(width=7)
        for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
            inline_kb.add(InlineKeyboardButton(text=day, callback_data=ignore_callback))

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row(width=7)
            for day in week:
                if day == 0:
                    inline_kb.add(
                        InlineKeyboardButton(text=" ", callback_data=ignore_callback)
                    )
                    continue
                inline_kb.add(
                    InlineKeyboardButton(
                        text=str(day),
                        callback_data=CalendarCallbackFactory(
                            act="DAY", year=year, month=month, day=day
                        ).pack(),
                    )
                )

        # Last row - Buttons
        inline_kb.row(width=7)
        inline_kb.add(
            InlineKeyboardButton(
                text="<",
                callback_data=CalendarCallbackFactory(
                    act="PREV-MONTH", year=year, month=month, day=day
                ).pack(),
            )
        )
        inline_kb.add(InlineKeyboardButton(text=" ", callback_data=ignore_callback))
        inline_kb.add(
            InlineKeyboardButton(
                text=">",
                callback_data=CalendarCallbackFactory(
                    act="NEXT-MONTH", year=year, month=month, day=day
                ).pack(),
            )
        )
        inline_kb.add(
            InlineKeyboardButton(text=BUTTON_TEXT["back"], callback_data="back")
        )
        inline_kb.adjust(3, 7)
        return inline_kb.as_markup()

    async def process_selection(
        self, query: CallbackQuery, data: CalendarCallbackFactory
    ) -> tuple:
        """
        Обработчик callback_query. Этот метод генерирует новый календарь, если нажата кнопка "Вперед" или
        "Назад". Этот метод должен вызываться внутри обработчика запроса обратного вызова.
        :param query: callback_query, как предусмотрено обработчиком запроса обратного вызова
        :param data: callback_data, словарь, заданный calendar_callback
        :return: Возвращает кортеж (логическое значение,datetime), указывающий, выбрана ли дата
                    и возвращает дату, если это так.
        """
        return_data = (False, None)
        temp_date = datetime(int(data.year), int(data.month), 1)
        # * обработка пустых кнопок, ответ без каких-либо действий
        if data.act == "IGNORE":
            await query.answer(cache_time=60)

        # * пользователь выбрал кнопку "День", формируется возвращаемый кортеж
        if data.act == "DAY":
            await query.message.delete_reply_markup()  # removing inline keyboard
            return_data = True, datetime(int(data.year), int(data.month), int(data.day))

        # * пользователь переходит к предыдущему году, редактируется сообщение с новым календарем
        if data.act == "PREV-YEAR":
            prev_date = datetime(int(data.year) - 1, int(data.month), 1)
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(
                    int(prev_date.year), int(prev_date.month)
                )
            )
        # * пользователь переходит к следующему году
        if data.act == "NEXT-YEAR":
            next_date = datetime(int(data.year) + 1, int(data.month), 1)
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(
                    int(next_date.year), int(next_date.month)
                )
            )
        # * пользователь переходит к предыдущему месяцу, редактируется сообщение с новым календарем
        if data.act == "PREV-MONTH":
            prev_date = temp_date - timedelta(days=1)
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(
                    int(prev_date.year), int(prev_date.month)
                )
            )
        # * пользователь переходит к следующему месяцу
        if data.act == "NEXT-MONTH":
            next_date = temp_date + timedelta(days=31)
            await query.message.edit_reply_markup(
                reply_markup=await self.start_calendar(
                    int(next_date.year), int(next_date.month)
                )
            )

        return return_data


class ChoiceDinnerSets:
    """Класс осуществляющий обработку выбора блюд в ресторане."""

    def __init__(self, sets_menu: list[DinnerSet]):
        self.sets_menu = map_json_to_pydantic(sets_menu)

    async def create_num_menu(
        self, count: int, data: DishCallbackFactory, back_b: Optional[bool] = None
    ) -> InlineKeyboardMarkup:
        """
        Метод ля формирования числовой клавиатуры для выбора количества порций блюд.
        :param count: int, количество необходимых кнопок в клавиатуре
        :param data: callback_data, словарь данных заданый в DishCallbackFactory
        :param back_b: bool, для формирования callback для кнопки назад.
        """

        kb_builder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = []
        for button in range(1, count):
            buttons.append(
                InlineKeyboardButton(
                    text=f"{button}",
                    callback_data=data.set_attr(name="count", value=button).pack(),
                ),
            )
        kb_builder.row(*buttons, width=8)
        back_button = DishCallbackFactory(act="back").pack() if back_b else "back"
        kb_builder.row(
            InlineKeyboardButton(text=BUTTON_TEXT["back"], callback_data=back_button),
            InlineKeyboardButton(text=BUTTON_TEXT["cancel"], callback_data="cancel"),
            width=2,
        )

        return kb_builder.as_markup()

    async def process_selection(
            self,
            callback: CallbackQuery,
            data: CalendarCallbackFactory,
            state: FSMContext
    ):
        if data.payment and data.act == "payment":
            storage_data = await state.get_data()
            order_list = format_order(storage_data)
            # todo возможно стоит представить сеты в виде клавиатуры и кнопка удалить
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT["confirm"],
                negative=BUTTON_TEXT["del"],
                calback_n="cancel",
                callback_p="yes",
            )
            #! новые правки
            inp_ph = FSInputFile(path=BASE_DIR / "media/choice_dish.jpg")
            photo = InputMediaPhoto(
                media=inp_ph,
                caption=LEXICON_TEXT["confirm"].format(order_list=order_list),
            )
            await callback.message.edit_media(media=photo, reply_markup=markup)

            await state.set_state(FSMReservation.payment)
            # todo добавить сохранение состояния, возможна проблема сохранением текста из за формата
            # await add_curr_state(
            #     state,
            #     lexicon_key=LEXICON_TEXT["confirm"].format(order_list=order_list),
            #     markup="yes_no",
            #     param_kb={
            #         "positive": "confirm",
            #         "negative": "del",
            #         "callback_p": "yes",
            #         "calback_n": "cancel",
            #     },
            # )

        if data.resume or data.act == "back":
            if data.act == "back":
                data_storage = await state.get_data()
                # * Отменяем выбор последнего блюда
                if data_storage.get("sets", None):
                    data_storage["sets"].pop()
                    await state.update_data(sets=data_storage["sets"])
            markup = create_choice_dish_keyboard(sets_menue=self.sets_menu)
            #! новые правки
            inp_ph = FSInputFile(path=BASE_DIR / "media/choice_dish.jpg")
            photo = InputMediaPhoto(
                media=inp_ph,
                caption=LEXICON_TEXT["add_new_dish"],
            )
            await callback.message.edit_media(media=photo, reply_markup=markup)

        if data.count:
            data.set_attr(name="act", value="None")
            data_storage = await state.get_data()
            callback_pay = DishCallbackFactory(
                act="payment",
                payment=True,
            )
            callback_resume = DishCallbackFactory(
                act="resume",
                resume=True,
            )
            callback_back = DishCallbackFactory(
                act="add_b",
            )
            data_storage["sets"][-1][1] = data.count
            await state.update_data(sets=data_storage["sets"])
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT["continue_selection"],
                negative=BUTTON_TEXT["payment"],
                calback_n=callback_pay.pack(),
                callback_p=callback_resume.pack(),
                back_b=("Назад", callback_back.pack()),
            )
            #! новые правки
            url = BASE_DIR / "media/start_2.jpg"

            caption = LEXICON_TEXT["continue_selection"]
            inp_ph = FSInputFile(path=url)
            photo = InputMediaPhoto(media=inp_ph, caption=caption)
            await callback.message.edit_media(media=photo, reply_markup=markup)

            await state.set_state(FSMReservation.fill_dinner_sets)

        if data.act in ("add", "add_b"):
            if data.act == "add":
                data_storage = await state.get_data()
                dish = None
                for obj in map_json_to_pydantic(data_storage["sets_list"]):
                    if obj.id == data.id:
                        dish = obj
                if data_storage.get("sets", None):
                    data_storage["sets"].append([dish.model_dump_json(), 1])
                    sets = data_storage["sets"]
                else:
                    sets = [
                        [dish.model_dump_json(), 1],
                    ]
                await state.update_data(sets=sets)

            markup = await self.create_num_menu(16, data, back_b=True)
            #! новые правки
            url = BASE_DIR / "media/start_2.jpg"

            caption = LEXICON_TEXT["num_servings"]
            inp_ph = FSInputFile(path=url)
            photo = InputMediaPhoto(media=inp_ph, caption=caption)
            await callback.message.edit_media(media=photo, reply_markup=markup)

            # todo проверить необходимость
            await add_curr_state(
                state,
                lexicon_key="num_servings",
                markup="num_servings",
                param_kb={"count": 16, "data": data.pack(), "back_b": True},
            )

            await state.set_state(FSMReservation.fill_dinner_sets)

        if data.act == "description":
            data_storage = await state.get_data()
            dish: DinnerSetDB or None = None
            for obj in map_json_to_pydantic(data_storage["sets_list"]):
                if obj.id == data.id:
                    dish = obj

            callback_back = DishCallbackFactory(
                act="back",
            )
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT["add"],
                negative=BUTTON_TEXT["back"],
                calback_n=callback_back.pack(),
                callback_p=data.set_attr(name="act", value="add").pack(),
            )
            #! новые правки
            url = BASE_DIR / "media/{0}.jpg".format(dish.id)

            caption = f"{dish.name}:\n {dish.description}\n Цена: {dish.price}"
            inp_ph = FSInputFile(path=url)
            photo = InputMediaPhoto(media=inp_ph, caption=caption)
            await callback.message.edit_media(media=photo, reply_markup=markup)


async def keyboard_generator(
    type_kb: str, params: dict = None
) -> InlineKeyboardMarkup or None:
    markup = None
    if type_kb == "yes_no":
        if params:
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT[params["positive"]],
                negative=BUTTON_TEXT[params["negative"]],
                calback_n=params["negative"],
                callback_p=params["positive"],
            )
        else:
            markup = create_positive_negative_keyboard(
                positive=BUTTON_TEXT["back"],
                negative=BUTTON_TEXT["cancel"],
                calback_n="cancel",
                callback_p="back",
            )
    if type_kb == "num_servings":
        markup = ChoiceDinnerSets().create_num_menu(**params)

    if type_kb == "choose_dish":
        markup = create_choice_dish_keyboard(sets_menue=params["sets"])

    if type_kb == "calendar":
        markup = await SimpleCalendar().start_calendar()

    return markup
