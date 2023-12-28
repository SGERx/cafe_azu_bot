from datetime import date, datetime
from typing import List

from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, AsyncSessionLocal
# from app.crud.dinnerset import dinnerset_crud
from app.models.reservations_dinnersets import (
    association_table as reservations_dinnersets,
)
from app.models.reservations_tables import association_table as reservations_tables


class Reservation(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    reservation_date: Mapped[date]
    guest_count: Mapped[int]
    special: Mapped[str] = mapped_column(default='нет')
    paid: Mapped[bool] = mapped_column(default=False, nullable=True)
    confirmed: Mapped[bool] = mapped_column(default=False)
    canceled: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    updated: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="reservations")
    tables: Mapped[List["Table"]] = relationship(
        secondary=reservations_tables, back_populates="reservations"
    )
    dinner_sets: Mapped[List['DinnerSet']] = relationship(
        secondary=reservations_dinnersets,
        back_populates='reservations',
    )

    @hybrid_property
    async def total_cost(self) -> float:
        """
        Получает общую стоимость текущего бронирования.
        Сначала получаем список количеств сетов из таблицы ассоциаций,
        отсортированный по id-шникам сетов.
        Далее получаем список объектов сетов, отсортированный по id-шникам
        сетов.
        Затем получаем ощую стоимость всех сетов в бронировании
        """
        association_query = (select(
            reservations_dinnersets.c.quantity
        ).where(
            reservations_dinnersets.c.reservation_id == self.id
        ).order_by(
            reservations_dinnersets.c.dinner_set_id
        ))
        async with AsyncSessionLocal() as session:
            results = await session.execute(association_query)
            quantities = [quantity for quantity, in results.fetchall()]
        dinner_sets = sorted(self.dinner_sets, key=lambda ds: ds.id)
        return sum(
            dinnerset.price * quantity
            for dinnerset, quantity in zip(dinner_sets, quantities)
        )

    @hybrid_property
    async def dinnerset_quantity(self) -> list:
        """
        Предназначен для получения форматированного списка из имен сетов и их
        количества для объекта бронирования.
        :return: Возвращает список
        """
        from app.crud.dinnerset import dinnerset_crud  # Локальный импорт

        association_query = (select(
            reservations_dinnersets.c.dinner_set_id,
            reservations_dinnersets.c.quantity
        ).where(
            reservations_dinnersets.c.reservation_id == self.id
        ).order_by(
            reservations_dinnersets.c.dinner_set_id
        ))
        async with AsyncSessionLocal() as session:
            results = await session.execute(association_query)
            dinnerset_id_quantities = [
                (await dinnerset_crud.get(ds_id), quantity)
                for ds_id, quantity, in results.fetchall()
            ]
            dinnerset_names_quantities = [
                f'{ds.name}: {quantity} шт'
                for ds, quantity in dinnerset_id_quantities
            ]
        return dinnerset_names_quantities

    # def __repr__(self):
    #     return f"Бронь пользователя: {self.user.name} " f"на {self.reservation_date}"

    def __repr__(self):
        try:
            return f"Бронирование пользователя: " \
                   f"{self.user.name}" \
                   f" на {self.reservation_date}, " \
                   f"user_id {self.user_id}, " \
                   f"гостей {self.guest_count}, " \
                   f"комментарий к заказу - {self.special}, " \
                   f"id бронирования {self.id}"
        except AttributeError:
            return f"Бронирование: " \
                   f"пользователя user_id {self.user_id}, " \
                   f" на {self.reservation_date}, " \
                   f"гостей {self.guest_count}, " \
                   f"комментарий к заказу - {self.special}, " \
                   f"id бронирования {self.id}"
