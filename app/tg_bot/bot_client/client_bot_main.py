from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from datetime import datetime
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.tg_bot.bot_client import apscheduler_hendler
from app.tg_bot.bot_client.command_handlers import commands_router
from app.tg_bot.bot_client.booking_handlers import booking_router
from app.tg_bot.bot_client.keyboards import set_main_menu
from app.tg_bot.bot_client.constans import DATETIME_HOUR, DATETIME_MINUTE
from app.tg_bot.bot_client.apscheduler_middleware import SchedulerMiddleware


load_dotenv(".env")

client_logger = logging.getLogger(__name__)


async def main_bot_client():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    client_logger.info("Starting bot_client")
    client_bot = Bot(token=os.getenv("CLIENT_BOT_TOKEN"), parse_mode="HTML")
    storage = RedisStorage.from_url("redis://localhost:6379/0")
    client_dp: Dispatcher = Dispatcher(storage=storage)

    # Запуск уведомлений по расписанию
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        apscheduler_hendler.send_notification_cron,
        trigger='cron',
        hour=DATETIME_HOUR,
        minute=DATETIME_MINUTE,
        start_date=datetime.now(),
        kwargs={'bot': client_bot, 'date': datetime.now().date()}
    )
    scheduler.start()

    # Добавление обновления планировщика
    client_dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # запуск функциии для установки меню команд
    await set_main_menu(client_bot)

    client_dp.include_router(commands_router)
    client_dp.include_router(booking_router)

    await client_bot.delete_webhook(drop_pending_updates=True)
    await client_dp.start_polling(client_bot)
