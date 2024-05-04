from crud.admins import admins_crud
from core.db import async_session


async def check_authorization(user_id=None):
    """Проверка пользователя бота в базе админов."""

    if user_id is None:
        return False
    async with async_session() as session:
        db_obj = await admins_crud.get(
            user_id,
            session
            )

    if db_obj is None:
        return False

    if (user_id == db_obj.user_id
            and (db_obj.is_admin or db_obj.is_superuser) and db_obj.is_active):
        return True
    return False


async def create_admin(obj):
    """Создание нового админа"""
    if obj is None:
        return False
    async with async_session() as session:
        db_obj = await admins_crud.create(obj, session)
        return db_obj
