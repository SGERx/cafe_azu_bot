import asyncio
from datetime import datetime
from pprint import pprint

from app.crud.dinnerset import dinnerset_crud
from app.crud.reservation import reservation_crud
from app.crud.table import table_crud
from app.crud.user import user_crud


async def add_reservation(
        reservation_data=None,
        table_ids=None,
        dinner_set_ids_quantity=None):
    if reservation_data is None:
        reservation_data = dict(
            user_id=3,
            reservation_date=datetime(year=2023, month=12, day=12),
            guest_count=4,
            special='Четыре джигита хотят красиво отдохнуть'
        )
    if table_ids is None:
        table_ids = [2, 3]
    if dinner_set_ids_quantity is None:
        dinner_set_ids_quantity = {
            1: 1,
            2: 1,
            3: 2
        }
    reservation_id = await reservation_crud.create_reservation(
        **reservation_data
    )
    print(reservation_id)
    reservation = await reservation_crud.get(reservation_id['id'])

    tables = [await table_crud.get(table_id) for table_id in table_ids]
    dinner_sets = [
        await dinnerset_crud.get(dinner_set_id)
        for dinner_set_id in dinner_set_ids_quantity.keys()
    ]

    await reservation_crud.add_tables_dinner_sets_to_reservation(
        reservation=reservation,
        tables=tables,
        dinner_sets=dinner_sets
    )
    await dinnerset_crud.update_dinner_sets_quantity(
        reservation_id=reservation_id['id'],
        dinner_set_ids_quantity=dinner_set_ids_quantity
    )


async def test_reservation_total_cost(reservation_id=None):
    if reservation_id is None:
        reservation_id = 2
    reservation = await reservation_crud.get(reservation_id=reservation_id)
    print(await reservation.total_cost)


async def test_get_reservatons_by_email():
    email = 'test2@test.ru'
    user = await user_crud.get_by_email(email=email)
    reservations = await reservation_crud.read_actual_reservations_by_client(
        user.id
    )
    print(reservations)


async def test_get_restaurants_and_tables():
    guest_count = 8
    date = datetime(year=2023, month=12, day=1)
    restaurants_and_tables = await table_crud.get_restaurants_and_tables(
        guest_count=guest_count,
        date=date
    )
    pprint(restaurants_and_tables)


async def async_main():
    # await add_reservation()
    # await test_reservation_total_cost()
    # await test_get_reservatons_by_email()
    await test_get_restaurants_and_tables()


if __name__ == '__main__':
    asyncio.run(async_main())
