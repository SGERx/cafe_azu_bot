import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .admin_env import ADMIN_TOKEN
from .commands import command_router

from app.tg_bot.bot_admin.handlers.handlers_main import admin_router
from app.tg_bot.bot_admin.handlers.handlers_creation import creation_router
from app.tg_bot.bot_admin.handlers.handlers_reservation import reservation_router
from app.tg_bot.bot_admin.keyboards.return_button import back_router
from app.tg_bot.bot_admin.states import state_router
from .handlers.handlers_creation_redaction import creation_redaction_router

logger_admin = logging.getLogger(__name__)


async def main_bot_admin():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger_admin.info("Starting bot_admin")
    admin_bot = Bot(token=ADMIN_TOKEN)
    admin_storage = MemoryStorage()
    admin_dp = Dispatcher(storage=admin_storage)
    admin_dp.include_router(state_router)
    admin_dp.include_router(back_router)
    admin_dp.include_router(creation_router)
    admin_dp.include_router(creation_redaction_router)
    admin_dp.include_router(reservation_router)
    admin_dp.include_router(command_router)
    admin_dp.include_router(admin_router)

    await admin_bot.delete_webhook(drop_pending_updates=True)
    await admin_dp.start_polling(admin_bot)
