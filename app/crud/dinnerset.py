from sqlalchemy import select, update, insert

from app.core.db import AsyncSessionLocal
from app.crud.validators import validate_dinnerset_name
from app.crud.base import BaseCRUD
from app.models.dinner_sets import DinnerSet
from app.models.reservations_dinnersets import association_table


class CRUDDinnerSet(BaseCRUD):
    model = DinnerSet

    async def create(
            self,
            obj_in_data: dict,
    ) -> DinnerSet:
        validate = validate_dinnerset_name(obj_in_data)
        if validate:
            return validate
        db_obj = self.model(**obj_in_data)
        async with AsyncSessionLocal() as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update_dinnerset(self, dinnerset_id: int, new_data: dict):
        # new_data['updated'] = datetime.now()
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(self.model).filter(self.model.id == dinnerset_id))
            reservation = result.scalar()
            if reservation:
                for attr, value in new_data.items():
                    setattr(reservation, attr, value)
                await session.commit()
            else:
                return "Изменение невозможно - данные о переданном ID блюда отсутствуют в базе"

    async def get_all_by_lower_price(
            self,
            price_value: float,
    ) -> list[DinnerSet]:
        async with AsyncSessionLocal() as session:
            dinnersets = await session.execute(
                select(self.model).where(
                    self.model.price <= price_value,
                )
            )
            return dinnersets.scalars().all()

    async def update_dinner_sets_quantity(
            self,
            reservation_id: int,
            dinner_set_ids_quantity: dict,

    ) -> None:
        """
        Обновляет количество сетов в заказе в соотвествии с переданными
        данными в таблице ассоциаций.
        :param reservation_id: id бронирования
        :param dinner_set_ids_quantity: словарь с id-шниками сетов и их
                                        количеством.
        :return: Возвращает None
        """
        async with AsyncSessionLocal() as session:
            for dinner_set_id, quantity in dinner_set_ids_quantity.items():
                update_stmt = update(
                    association_table
                ).where(
                    (association_table.c.reservation_id == reservation_id) &
                    (association_table.c.dinner_set_id == dinner_set_id)
                ).values(quantity=quantity)
                await session.execute(update_stmt)
            await session.commit()

    async def insert_dinner_sets_quantity(
            self,
            reservation_id: int,
            dinner_set_ids_quantity: dict,

    ) -> None:
        """
        Вставляет количество сетов в заказе в соотвествии с переданными
        данными в таблице ассоциаций.
        :param reservation_id: id бронирования
        :param dinner_set_ids_quantity: словарь с id-шниками сетов и их
                                        количеством.
        :return: Возвращает None
        """
        async with AsyncSessionLocal() as session:
            for dinner_set_id, quantity in dinner_set_ids_quantity.items():
                insert_stmt = insert(
                    association_table
                ).values(
                    reservation_id=reservation_id,
                    dinner_set_id=dinner_set_id,
                    quantity=quantity
                )
                await session.execute(insert_stmt)
            await session.commit()


dinnerset_crud = CRUDDinnerSet()
