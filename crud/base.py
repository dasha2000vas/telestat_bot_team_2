from typing import TypeVar, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase:
    """Базовый класс CRUD"""

    def __init__(self, model: ModelType):
        self.model = model

    async def get(
            self,
            value: int,
            session: AsyncSession,
    ) -> Union[None, ModelType]:
        """Получение значения из БД"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.user_id == value))

        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:
        """Получение списка данных всех объектов."""
        db_objs = await session.execute(select(self.model))

        return db_objs.scalars().all()

    async def create(
            self,
            obj: dict,
            session: AsyncSession,
    ) -> ModelType:
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
    ) -> ModelType:
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
    ) -> ModelType:
        """Удаление объекта из БД"""
        await session.delete(db_obj)
        await session.commit()

        return f'Запись админа {db_obj.username} была удалена'
