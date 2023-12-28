from app.crud.dinnerset import dinnerset_crud
from app.crud.reservation import reservation_crud
from app.crud.table import table_crud


async def add_reservation(
        reservation_data=None,
        table_ids=None,
        dinner_set_ids_quantity=None):
    """ формат передачи данных:
        reservation_data = dict(
            user_id=3,
            reservation_date=date(year=2023, month=12, day=12),
            guest_count=4,
            special='Четыре джигита хотят красиво отдохнуть'
        )
        table_ids = [2, 3]
        dinner_set_ids_quantity = {
            1: 1,
            2: 1,
            3: 2
        }"""
    if not any([reservation_data, table_ids, dinner_set_ids_quantity]):
        raise ValueError(
            'Переданы не все необходимые данные для создания брони'
        )
    reservation_id = await reservation_crud.create_reservation(
        reservation_data
    )
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
