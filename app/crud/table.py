from collections import defaultdict
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.core.db import AsyncSessionLocal
from app.crud.base import BaseCRUD
from app.models import Table, Reservation
from app.crud.restaurant import restaurant_crud


class CRUDTable(BaseCRUD):
    model = Table

    async def create(self, table_data: dict):
        db_obj = self.model(**table_data)
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return [db_obj.id, db_obj.table_number, db_obj.restaurant_id, db_obj.capacity, db_obj.group]

    async def update_table(self, table_id: int, new_data: dict):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == table_id))
            reservation = result.scalar()
            if reservation:
                for attr, value in new_data.items():
                    setattr(reservation, attr, value)
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID стола отсутствуют в базе"

    async def get_available_tables_in_restaurant_by_capacity_and_date(
            self,
            capacity_value: int,
            restaurant_id: int,
            date: datetime
    ) -> list[Table]:
        async with AsyncSessionLocal() as session:
            tables = await session.execute(
                select(self.model).options(
                    joinedload(self.model.restaurant)
                ).where(

                    self.model.capacity >= capacity_value,
                    self.model.restaurant_id == restaurant_id,
                    ~self.model.reservations.any(
                        Reservation.reservation_date == date
                    ),
                )
            )
            return tables.scalars().all()

    async def get_restaurants_and_tables(self, guest_count, date):
        restaurants = await restaurant_crud.get_multi()
        results_tables: list = []
        for restaurant in restaurants:
            available_tables = await self.get_available_tables_in_restaurant_by_capacity_and_date(
                guest_count, restaurant.id, date
            )
            if not available_tables:
                available_tables = await self.get_neighbour_tables_by_restaurant(
                    restaurant=restaurant,
                    guest_count=guest_count,
                    date=date
                )
                if not available_tables:
                    continue
            available_tables = await self.choose_optimal_tables(
                available_tables,
                guest_count
            )
            results_tables.append([available_tables[0].restaurant, available_tables])
        return results_tables

    async def get_neighbour_tables_by_restaurant(
            self,
            restaurant,
            guest_count,
            date
    ):
        available_tables = await self.get_available_tables_in_restaurant_by_capacity_and_date(
            2, restaurant.id, date
        )
        if sum([table.capacity for table in available_tables]) < guest_count:
            return None
        tables = await self.choose_optimal_tables(
            available_tables,
            guest_count
        )
        return tables

    async def choose_optimal_tables(self, available_tables, guest_count):
        grouped_tables = defaultdict(list)
        for table in available_tables:
            group = table.group
            grouped_tables[group].append(table)
        grouped_tables = dict(grouped_tables)

        group_to_delete = []
        for group, tables in grouped_tables.items():
            if sum([table.capacity for table in tables]) < guest_count:
                group_to_delete.append(group)
            grouped_tables[group] = sorted(
                tables, key=lambda table: table.capacity, reverse=True
            )
        if group_to_delete:
            for group in group_to_delete:
                del grouped_tables[group]

        if not grouped_tables:
            return None

        min_group = min(
            grouped_tables,
            key=lambda group: sum(
                table.capacity for table in grouped_tables[group]
            )
        )
        optimal_group_tables = grouped_tables[min_group]

        matching_tables = []
        total_capacity = 0
        for table in optimal_group_tables:
            if total_capacity >= guest_count:
                break
            total_capacity += table.capacity
            matching_tables.append(table)

        return matching_tables

    async def get_multi(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).options(selectinload(Table.restaurant)))
            reservations = result.scalars().all()
            if reservations:
                return reservations
            else:
                return "В базе нет информации о столах"


table_crud = CRUDTable()
