from sqlalchemy import select, insert

from app.core.db import AsyncSessionLocal


class BaseCRUD:
    model = None

    @classmethod
    async def create(
            cls,
            **data
    ):
        query = insert(cls.model).values(**data).returning(cls.model.id)
        async with AsyncSessionLocal() as session:
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()

    @classmethod
    async def get(
            cls,
            object_id: int
    ):
        async with AsyncSessionLocal() as session:
            query = select(cls.model).where(cls.model.id == object_id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def get_multi(
            cls
    ):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(cls.model)
            )
            return result.scalars().all()

    @classmethod
    async def remove(
            cls,
            db_obj_id
    ):
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(cls.model).where(cls.model.id == db_obj_id))
            db_obj = result.scalars().first()
            if db_obj:
                await session.delete(db_obj)
                await session.commit()
            return db_obj
