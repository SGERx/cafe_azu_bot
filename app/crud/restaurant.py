from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.core.db import AsyncSessionLocal
from app.models.restaurant import Restaurant
from app.models.table import Table
from app.crud.base import BaseCRUD
from app.crud.validators import validate_restaurant_data


class RestaurantCRUD(BaseCRUD):
    model = Restaurant

    async def create(self, restaurant_data):
        validate = validate_restaurant_data(restaurant_data)
        if validate:
            return validate
        query = insert(self.model).values(**restaurant_data).returning(self.model.id)
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    async def get_multi(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Restaurant)
            )
            return result.scalars().all()

    async def get_by_id(self, id_data):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Restaurant).where(Restaurant.id == id_data)
            )
            return result.scalars().first()

    async def get_restaurant_tables(self, restaurant_id):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Table).options(
                    selectinload(Table.restaurant)
                ).filter(Table.restaurant_id == restaurant_id)
            )
            return result.scalars().all()

    async def update_restaurant(self, restaurant_id: int, new_data: dict):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == restaurant_id))
            reservation = result.scalar()
            if reservation:
                for attr, value in new_data.items():
                    setattr(reservation, attr, value)
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID филиала кафе отсутствуют в базе"


restaurant_crud = RestaurantCRUD()
