from aiogram import Bot
from aiogram.fsm.context import FSMContext

from datetime import date

from app.crud.reservation import reservation_crud


async def send_notification_cron(bot: Bot, date: date):
    reservations = (
        await reservation_crud.get_reservations_by_date_for_notification(date)
    )
    for reservation in reservations:
        dinnersets = []
        for dinnerset in reservation.dinner_sets:
            dinnersets.append(dinnerset.name)
        msg = (f'Сегодня мы вас ждет в '
               f'{reservation.tables[0].restaurant.name}. '
               f'Номер вашей брони {reservation.id}. '
               f'Вы заказали {dinnersets} на '
               f'{reservation.guest_count} гостей.')
        await bot.send_message(
            reservation.user.chat_id,
            msg,
        )


async def delete_reservation_by_time_limit(
    reservation_id: int,
    state: FSMContext,
    bot: Bot,
    chat_id: int,
):
    await bot.send_message(
        chat_id,
        'Вы не успели забронировать и оплатить. '
        'Процесс бронирования был сброшен.'
    )
    await reservation_crud.delete_reservation(reservation_id)
    await state.clear()
