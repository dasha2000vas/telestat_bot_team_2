from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс CRUD"""

    def __init__(
            self,
            model):
        self.model = model

    async def get(
            self,
            value: int,
            session: AsyncSession,
    ):
        """Получение значения из БД"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.user_id == value))
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj: dict,
            session: AsyncSession,
    ):
        """Создание объекта в таблице БД"""

        db_obj = self.model(**obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update_data(
            self,
            db_obj: object,
            obj_in: dict,
            session: AsyncSession,
    ):
        """Обновление значений объекта админа в БД"""

        for field in db_obj:
            if field in obj_in:
                setattr(
                    db_obj,
                    field,
                    obj_in[field],
                )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: object,
            session: AsyncSession,
    ):
        """Удаление объекта из БД"""

        await session.delete(db_obj)
        await session.commit()
        return f'Запись админа {db_obj.username} была удалена'
