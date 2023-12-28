from datetime import date, datetime

from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload, selectinload
from typing_extensions import List

from app.models.dinner_sets import DinnerSet
from app.models.reservation import Reservation
from app.models.table import Table
from app.core.db import AsyncSessionLocal
from app.crud.validators import validate_reservation_data
from app.crud.base import BaseCRUD


class ReservationCRUD(BaseCRUD):
    model = Reservation

    async def create_reservation(self, reservation_data):
        validate = validate_reservation_data(reservation_data)
        if validate:
            return validate
        query = insert(self.model).values(**reservation_data).returning(self.model.id)
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    async def get(self, reservation_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    self.model
                ).options(
                    selectinload(Reservation.user),
                    selectinload(Reservation.tables).selectinload(Table.restaurant),
                    selectinload(Reservation.dinner_sets).selectinload(DinnerSet.reservations),
                ).where(
                    self.model.id == reservation_id
                )
            )
            reservation = result.scalars().first()
            if reservation:
                return reservation
            else:
                return "Данные о переданном ID бронирования отсутствуют в базе"

    async def read_reservation_by_date(self, reservation_date_str):
        reservation_date = datetime.strptime(reservation_date_str, "%d%m%Y").date()
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).options(
                selectinload(Reservation.user)).where(Reservation.reservation_date == reservation_date))
            reservation = result.scalars().all()
            if reservation:
                return reservation
            else:
                return "Данные о бронированиях за указанную дату отсутствуют в базе"

    async def get_multi(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).options(selectinload(Reservation.user)))
            reservations = result.scalars().all()
            if reservations:
                return reservations
            else:
                return "В базе нет информации о бронированиях"

    async def read_actual_reservations(self):
        async with AsyncSessionLocal() as session:
            current_date = date.today()
            actual = select(
                Reservation
            ).options(
                selectinload(Reservation.user),
                selectinload(Reservation.tables).selectinload(Table.restaurant),
                selectinload(Reservation.dinner_sets).selectinload(DinnerSet.reservations),
            ).where(
                current_date <= Reservation.reservation_date
            )
            result = await session.execute(actual)
            reservations = result.scalars().all()
            if reservations:
                return reservations
            else:
                return "В базе нет информации о бронированиях на актуальные даты"

    async def read_actual_reservations_by_client(self, user_id):
        async with AsyncSessionLocal() as session:
            current_date = date.today()
            actual = select(Reservation).options(
                selectinload(Reservation.user),
            ).where(
                (current_date <= Reservation.reservation_date) &
                (Reservation.user_id == user_id)
            )
            result = await session.execute(actual)
            reservations = result.scalars().all()
            if reservations:
                return reservations
            else:
                return "В базе нет информации о бронированиях на актуальные даты"

    async def update_reservation(self, reservation_id: int, new_data: dict):
        new_data['updated'] = datetime.now()
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == reservation_id))
            reservation = result.scalar()
            if reservation:
                for attr, value in new_data.items():
                    setattr(reservation, attr, value)
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID бронирования отсутствуют в базе"

    async def delete_reservation(self, reservation_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == reservation_id))
            reservation = result.scalars().first()
            if reservation:
                await session.delete(reservation)
                await session.commit()
            else:
                return "Удаление невозможно - данные о переданном ID бронирования отсутствуют в базе"

    async def cancel_reservation(self, reservation_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == reservation_id))
            reservation = result.scalar()
            if reservation:
                setattr(reservation, 'canceled', 1)
                setattr(reservation, 'updated', datetime.now())
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID бронирования отсутствуют в базе"

    async def get_reservations_by_date_for_notification(
            self, reservation_date
    ):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(self.model).options(
                    joinedload(Reservation.user),
                    selectinload(
                        Reservation.tables
                    ).selectinload(Table.restaurant),
                    selectinload(Reservation.dinner_sets)
                ).where(Reservation.reservation_date == reservation_date))
            reservations = result.scalars().all()
            return reservations

    async def add_tables_dinner_sets_to_reservation(
            self,
            reservation: Reservation,
            tables: List[Table],
            dinner_sets: List[DinnerSet]

    ) -> None:
        """
        Добавляет объекты столов и сетов к объекту бронирования. Используется
        методы ORM для добавления связей m2m к объекту бронирования.
        По факту в БД добавляются данные в соответствующие таблицы ассоциаций.
        :param reservation: Объект бронирования
        :param tables: Список объектов столов
        :param dinner_sets: Список объектов сетов
        :return: Возвращает None
        """
        async with AsyncSessionLocal() as session:
            reservation.tables.extend(tables)
            reservation.dinner_sets.extend(dinner_sets)
            session.add(reservation)
            await session.commit()


reservation_crud = ReservationCRUD()
