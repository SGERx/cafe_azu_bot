import asyncio
from pprint import pprint

from app.core.config import settings
from app.core.google_client import service
from app.services.google_api import (
    set_user_permissions, spreadsheet_read_value, spreadsheet_update_values,
    spreadsheet_delete_data, archive_data, synchronize_data
)

DATA_TO_UPDATE = [
    [
        '12.12.2023',
        '',
        'Тулай Торун, +90 555 123 4567',
        '4',
        '4',
        'Анталийская Роскошь Кебаба 1 шт, Адана Арома 3 шт',
        '5000',
        'да',
        'да',
        'Самый красивый столик!',
    ]
]
USERS_EMAILS = (
    'Samsooon5@gmail.com',
    'plastilinman@gmail.com',
    'pankirbor@gmail.com'
)


async def test_set_permissions(
        emails: tuple = USERS_EMAILS,
        sheet_id: str = settings.SHEET_ID,
) -> None:
    async with service as wrapper_services:
        for email in emails:
            await set_user_permissions(sheet_id, email, wrapper_services)
            print(f'Добавлен доступ для пользователя с email: {email}')


async def test_get_sheet_data(
        sheet_id: str = settings.SHEET_ID,
        restaurant: str = 'Ресторан 1'):
    async with service as wrapper_services:
        results = await spreadsheet_read_value(
            spreadsheet_id=sheet_id,
            restaurant=restaurant,
            wrapper_services=wrapper_services
        )
    pprint(results)


async def test_update_sheet_data(
        sheet_id: str = settings.SHEET_ID,
        restaurant: str = 'Ресторан 1',
        update_data: list = DATA_TO_UPDATE,

) -> None:
    async with service as wrapper_services:
        await spreadsheet_update_values(
            spreadsheet_id=sheet_id,
            restaurant=restaurant,
            rows_values=update_data,
            wrapper_services=wrapper_services,
            append=True
        )


async def test_delete_data_from_sheet(
        sheet_id: str = settings.SHEET_ID,
        restaurant: str = 'Ресторан 1',
        range_to_delete: str = 'R2C1:R4C10'
) -> None:
    async with service as wrapper_services:
        await spreadsheet_delete_data(
            spreadsheet_id=sheet_id,
            restaurant=restaurant,
            range_to_delete=range_to_delete,
            wrapper_services=wrapper_services
        )


async def test_archive_data(
        sheet_id: str = settings.SHEET_ID,
        restaurants: list = None,
) -> None:
    if restaurants is None:
        restaurants = settings.RESTAURANT_NAMES
    async with service as wrapper_services:
        await archive_data(
            spreadsheet_id=sheet_id,
            restaurants=restaurants,
            wrapper_services=wrapper_services
        )


async def test_synchronize_data(
        sheet_id: str = settings.SHEET_ID,
):
    async with service as wrapper_services:
        await synchronize_data(
            spreadsheet_id=sheet_id,
            wrapper_services=wrapper_services
        )


async def async_main():
    # await test_get_sheet_data()
    # await test_set_permissions()
    # await test_update_sheet_data()
    # await test_delete_data_from_sheet()
    # await test_archive_data()
    await test_synchronize_data()


if __name__ == '__main__':
    asyncio.run(async_main())
