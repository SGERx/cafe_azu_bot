from collections import defaultdict
from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.crud.reservation import reservation_crud

DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'
DATE_FORMAT = '%d.%m.%Y'
ROW_COUNT = 100
COLUMN_COUNT = 11

DRIVE_API_NAME = 'drive'
DRIVE_API_VERSION = 'v3'
SHEETS_API_NAME = 'sheets'
SHEETS_API_VERSION = 'v4'

VALUE_INPUT_OPTION = 'USER_ENTERED'
MAJOR_DIMENSION = 'ROWS'
RANGE = 'R2C1:R{}C{}'

SHEET_ERROR_MESSAGE = (f'Передана некорректная информация. Ожидалось '
                       f'{ROW_COUNT} строк и {COLUMN_COUNT} колонок. '
                       'Передано {} строк и {} колонок.')


async def set_user_permissions(
        spreadsheet_id: str,
        user_email: str,
        wrapper_services: Aiogoogle,
) -> None:
    """
    Устанавливает разрешение на редактирование таблицы
    пользователю с указанным email.
    """
    permission_user_data = dict(
        type='user',
        role='reader',
        emailAddress=user_email
    )
    service = await wrapper_services.discover(
        DRIVE_API_NAME,
        DRIVE_API_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permission_user_data,
            fields='id'
        )
    )


async def spreadsheet_read_value(
        spreadsheet_id: str,
        restaurant: str,
        wrapper_services: Aiogoogle,
) -> list:
    """
    Получает данные из указанной таблицы для указанного ресторана.
    """
    service = await wrapper_services.discover(
        SHEETS_API_NAME,
        SHEETS_API_VERSION
    )
    results = await wrapper_services.as_service_account(
        service.spreadsheets.values.get(
            spreadsheetId=spreadsheet_id,
            range=f'{restaurant}!{RANGE.format(ROW_COUNT, COLUMN_COUNT)}'
        )
    )
    return results['values']


async def spreadsheet_update_values(
        spreadsheet_id: str,
        restaurant: str,
        rows_values: list,
        wrapper_services: Aiogoogle,
        append: bool = False
) -> None:
    """
    Обновляет или добавляет данные в указанной таблице для нужного ресторана.
    Если append == True, то используется дополнение данных
    """
    service = await wrapper_services.discover(
        SHEETS_API_NAME,
        SHEETS_API_VERSION
    )
    table_values = deepcopy(rows_values)
    row_amount = len(table_values) + 1
    column_amount = max(len(row) for row in table_values)
    if row_amount > ROW_COUNT or column_amount > COLUMN_COUNT:
        raise ValueError(SHEET_ERROR_MESSAGE.format(row_amount, column_amount))
    range_value = f'{restaurant}!{RANGE.format(row_amount, column_amount)}'
    update_method = (
        service.spreadsheets.values.append
        if append
        else service.spreadsheets.values.update
    )
    await wrapper_services.as_service_account(
        update_method(
            spreadsheetId=spreadsheet_id,
            range=range_value,
            valueInputOption=VALUE_INPUT_OPTION,
            json={
                'values': table_values
            }
        )
    )


async def spreadsheet_delete_data(
        spreadsheet_id: str,
        restaurant: str,
        range_to_delete: str,
        wrapper_services: Aiogoogle,
):
    """
    Удаляет данные с листа ресторана о бронированиях из указанного диапазона.
    """
    service = await wrapper_services.discover(
        SHEETS_API_NAME,
        SHEETS_API_VERSION
    )

    await wrapper_services.as_service_account(
        service.spreadsheets.values.clear(
            spreadsheetId=spreadsheet_id,
            range=f'{restaurant}!{range_to_delete}'
        )
    )


async def archive_data(
        spreadsheet_id: str,
        restaurants: list,
        wrapper_services: Aiogoogle,
):
    """
    Помещает инфо по бронированию прошлых дат в таблицу с архивом.
    Нужно запускать в начале суток
    """

    def need_archive(reservation_date: str) -> bool:
        return (
            datetime.now() > datetime.strptime(reservation_date, DATE_FORMAT)
        )

    all_spreadsheet_reservations = []
    for restaurant in restaurants:
        data = await spreadsheet_read_value(
            spreadsheet_id=spreadsheet_id,
            restaurant=restaurant,
            wrapper_services=wrapper_services
        )
        all_spreadsheet_reservations.extend(data)
        to_archive = []
        to_spreadsheet = []
        for reservation in all_spreadsheet_reservations:
            if need_archive(reservation[0]):
                to_archive.append([restaurant] + reservation)
            else:
                to_spreadsheet.append(reservation)
        if not to_archive:
            continue
        await spreadsheet_update_values(
            spreadsheet_id=spreadsheet_id,
            restaurant='Архив',
            rows_values=to_archive,
            wrapper_services=wrapper_services,
            append=True
        )
        await spreadsheet_delete_data(
            spreadsheet_id=spreadsheet_id,
            restaurant=restaurant,
            range_to_delete=f'{RANGE.format(ROW_COUNT, COLUMN_COUNT)}',
            wrapper_services=wrapper_services
        )
        await spreadsheet_update_values(
            spreadsheet_id=spreadsheet_id,
            restaurant=restaurant,
            rows_values=to_spreadsheet,
            wrapper_services=wrapper_services,
            append=True
        )
    return all_spreadsheet_reservations


async def synchronize_data(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle,
) -> None:
    """
    Синхронизирует данные между БД и таблицей.
    Синхронизируем только актуальные бронирования.
    Нужно запускать каждый час
    """
    actual_reservations = await reservation_crud.read_actual_reservations()
    data_to_update = defaultdict(list)
    for reservation in actual_reservations:
        print(await reservation.dinnerset_quantity)
        restaurant_name = reservation.tables[0].restaurant.name
        try:
            data = [
                reservation.reservation_date.strftime(DATE_FORMAT),
                reservation.id,
                f'{reservation.user.name}, {reservation.user.phone_number}',
                reservation.guest_count,
                ', '.join([str(table.table_number) for table in reservation.tables]),
                ', '.join(await reservation.dinnerset_quantity),
                await reservation.total_cost,
                'Да' if reservation.paid else 'Нет',
                'Да' if reservation.confirmed else 'Нет',
                'Да' if reservation.canceled else 'Нет',
                reservation.special
            ]
        except AttributeError:
            data = [
                reservation.reservation_date.strftime(DATE_FORMAT),
                reservation.id,
                reservation.guest_count,
                ', '.join([str(table.table_number) for table in reservation.tables]),
                ', '.join(await reservation.dinnerset_quantity),
                await reservation.total_cost,
                'Да' if reservation.paid else 'Нет',
                'Да' if reservation.confirmed else 'Нет',
                'Да' if reservation.canceled else 'Нет',
                reservation.special
            ]
        data_to_update[restaurant_name].append(data)
    if not data_to_update:
        return
    data_to_update = dict(data_to_update)
    for restaurant, data_to_row in data_to_update.items():
        await spreadsheet_delete_data(
            spreadsheet_id=spreadsheet_id,
            restaurant=restaurant,
            range_to_delete='R2C1:R100C11',
            wrapper_services=wrapper_services
        )
        await spreadsheet_update_values(
            spreadsheet_id=spreadsheet_id,
            restaurant=restaurant,
            rows_values=data_to_row,
            wrapper_services=wrapper_services,
        )
