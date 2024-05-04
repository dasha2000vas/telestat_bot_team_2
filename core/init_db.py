"""Создание суперюзера при инициализации БД"""

from sqlalchemy import inspect
from core import Admins
from core.db import async_session, engine
from settings import Config


def use_inspector(conn):
    inspector = inspect(conn)
    return inspector.get_table_names()


async def create_user(
    user_id,
    username,
    is_superuser,
    is_admin,
):
    data = {'user_id': user_id,
            'username': username,
            'is_superuser': is_superuser,
            'is_admin': is_admin
            }
    db_obj = Admins(**data)
    try:
        async with async_session() as session:
            session.add(
                db_obj
                )
            await session.commit()
    except Exception:
        pass


async def create_super_user():
    async with engine.connect() as conn:
        tables = await conn.run_sync(use_inspector)
        if 'admins' in tables:
            await create_user(Config.MY_ID, Config.MY_USERNAME, True, True)
