from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .keyboards.keyboards_main import to_start_keyboard, work_keyboard
from .states import StateAdmin

command_router = Router()


@command_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=f"Добрый день, {message.from_user.full_name}!\n"
             "Для перезапуска нажмите             /start \n"
             "Для работы с ботом нажмите      /work \n"
             "Для описания опций нажмите    /help \n"
             "Кнопка 'К главному меню' (внизу) возвращает на главный экран. \n"
             "Кнопка 'Назад' (внизу) возвращает на предыдущее действие. \n"
             "Скрыть кнопки можно опцией справа.",
        reply_markup=to_start_keyboard
    )
    await state.set_state(StateAdmin.start_menu)


@command_router.message(Command("work"))
async def command_work(message: Message, state: FSMContext):
    await message.answer("Переходим в рабочие функции бота", reply_markup=work_keyboard)
    await state.set_state(StateAdmin.work_menu)


@command_router.message(Command("help"))
async def handle_help(message: Message, state: FSMContext):
    await message.answer(text="Это телеграм-бот для администраторов кафе azu!\n"
                              "Для перезапуска нажмите   /start. \n"
                              "С помощью этого бота можно: \n"
                              "- управлять бронированиями (создавать и редактировать)\n"
                              "- создавать, редактировать, смотреть блюда в кафе azu\n"
                              "- создавать, редактировать, смотреть филиалы кафе azu\n"
                              "- создавать, редактировать, смотреть столы в филиалах кафе azu\n"
                              "- создавать, редактировать, смотреть администраторов кафе azu\n"
                              "все эти действия доступны через меню  /work"
                         )
    await state.set_state(StateAdmin.help_menu)
