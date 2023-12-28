from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.reservation import Reservation
from app.crud.base import BaseCRUD
from app.crud.validators import validate_user_data


class UserCRUD(BaseCRUD):
    model = User

    async def create(self, user_data):
        validate = validate_user_data(user_data)
        if validate:
            return validate
        query = insert(self.model).values(**user_data).returning(self.model)
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            result = result.scalars().first()
            await session.commit()
            await session.refresh(result)
            return result

    async def update_user(self, user_id: int, new_data: dict):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == user_id))
            reservation = result.scalar()
            if reservation:
                for attr, value in new_data.items():
                    setattr(reservation, attr, value)
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID пользователя отсутствуют в базе"

    async def get_by_id(self, id_data):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.id == id_data)
            )
            return result.scalars().first()

    async def get_by_email(self, email):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalars().first()

    async def get_by_phone_number(self, phone_number):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.phone_number == phone_number)
            )
            return result.scalars().first()

    async def get_user_reservations(self, user_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    Reservation
                ).options(
                    selectinload(
                        Reservation.user)
                ).filter(
                    Reservation.user_id == user_id
                )
            )
            return result.scalars().all()


user_crud = UserCRUD()
