from core.db import async_session
from crud.admins import admins_crud
from permissions.permissions import check_authorization


async def create_admin(obj):
    """Создание нового админа"""
    db_obj = await check_authorization(obj['user_id'])
    if db_obj:
        return False
    else:
        async with async_session() as session:
            db_obj = await admins_crud.create(obj, session)
        return db_obj


async def delete_admin(user_id=None):
    """Удаление админа из БД"""
    db_obj = await check_authorization(user_id)
    if db_obj is None:
        return False
    else:
        async with async_session() as session:
            await admins_crud.remove(db_obj, session)
        return True


async def get_all_admins():
    async with async_session() as session:
        all_admins = await admins_crud.get_multi(session)
    return all_admins
