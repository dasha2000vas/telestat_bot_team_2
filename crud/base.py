from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс операций CRUD."""

    def __init__(
            self,
            model):
        self.model = model

    async def get(
            self,
            value,
            session: AsyncSession,
    ):
        """Получение значения из ДБ"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.user_id == value))
        return db_obj.scalars().first()

    async def create(
            self,
            obj,
            session: AsyncSession,
    ):
        """Обновление значений в таблице ДБ."""

        db_obj = self.model(**obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
