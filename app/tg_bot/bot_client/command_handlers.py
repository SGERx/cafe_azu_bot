from pathlib import Path

from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile

from app.tg_bot.bot_client.lexicon_cli import LEXICON_TEXT, format_as_text_list
from app.tg_bot.bot_client.states import FSMReservation, add_curr_state

commands_router = Router()

BASE_DIR = Path(__file__).resolve().parent.parent


@commands_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    """Хендлер для обработки команды /start. Приветствие клиента."""

    full_name = message.from_user.full_name
    url = BASE_DIR / "media/start.jpg"
    # "/home/llirik_05/Dev/cafe_azu_bot_3/app/tg_bot/media/start.jpg"

    caption = LEXICON_TEXT[message.text].format(full_name=full_name)

    # Создаем объект фотографии
    inp_ph = FSInputFile(path=url)
    await message.answer_photo(photo=inp_ph, caption=caption)


@commands_router.message(Command(commands=["help"]), StateFilter(default_state))
async def process_help_command(message: Message):
    """Хендлер для обработки команды /help. Выводит список доступных команд."""

    await message.answer(LEXICON_TEXT[message.text])


@commands_router.message(Command(commands=["cancel"]), ~StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    """
    Хендлер для обработки команды /cancel.
    Останавливает процесс бронирование на любом шаге,
    очищает данные во временном хранилище,
    работает во всех состояниях кроме дефолтного.
    """

    await message.answer(LEXICON_TEXT["cancel"])
    await state.clear()


@commands_router.message(
    Command(commands=["add_reservation"]), StateFilter(default_state)
)
async def process_add_restaurant(message: Message, state: FSMContext):
    """
    Хендлер для обработки команды /add_reservation.
    Запускает процесс бронирования,
    выводит сообщение в чат с просьбой ввести имя,
    устанавливает состояние ожидания данных о имени клиента."""

    await message.answer(text=LEXICON_TEXT["fill_name"])
    await state.set_state(FSMReservation.fill_name)
    await add_curr_state(state, lexicon_key="fill_name", markup=None)


@commands_router.message(Command(commands=["reservations"]), StateFilter(default_state))
async def process_my_reservations_command(message: Message):
    """
    Хендлер для обработки команды /reservations.
    Выводит список всех бронирований клиента.
    """
    # todo уточнить о необходимом user_id
    user_id = message.from_user.id
    # todo reservations = await reservation_crud.read_actual_reservations_by_client(user_id)
    reservations = ["Бронь на 30-11-2023", "Бронь на 03-12-2023", "Бронь на 05-12-2023"]
    if reservations:
        list_reserv = format_as_text_list(reservations, prefix="🌚 - ")
        await message.answer(LEXICON_TEXT[message.text].format(reserv=list_reserv))
    else:
        await message.answer(LEXICON_TEXT["no_reserv"])


if __name__ == "__main__":
    print(url=BASE_DIR / "media/start.jpg")
