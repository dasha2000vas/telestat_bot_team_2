from crud.admins import admins_crud
from core.db import async_session


async def check_authorization(user_id=None):
    """Базовая проверка наличия пользователя в БД"""

    if user_id is None:
        return False
    async with async_session() as session:
        db_obj = await admins_crud.get(
            user_id,
            session
            )
    return db_obj

    # if (user_id == db_obj.user_id
    #         and (db_obj.is_admin or db_obj.is_superuser)):
    #     return True
    # return False


async def check_admin(user_id=None):
    db_obj = await check_authorization(user_id)
    if db_obj is None:
        return False
    if (user_id == db_obj.user_id
            and (db_obj.is_admin or db_obj.is_superuser)):
        return True
    return False


async def check_superuser(user_id=None):
    db_obj = await check_authorization(user_id)
    if db_obj is None:
        return False
    if (user_id == db_obj.user_id
            and db_obj.is_superuser):
        return True
    return False
