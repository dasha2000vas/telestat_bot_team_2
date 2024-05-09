"""Создание суперюзера при инициализации БД"""

from sqlalchemy import inspect
from core.db import async_session, engine
from settings import Config
from crud.admins import admins_crud

from constants import SUPERUSER


def use_inspector(conn):
    inspector = inspect(conn)
    return inspector.get_table_names()


# async def create_user(
#     user_id,
#     username,
#     is_superuser,
#     is_admin,
# ):
#     data = {'user_id': user_id,
#             'username': username,
#             'is_superuser': is_superuser,
#             'is_admin': is_admin
#             }
#     db_obj = Admins(**data)
#     try:
#         async with async_session() as session:
#             session.add(
#                 db_obj
#                 )
#             await session.commit()
#     except Exception:
#         pass


async def create_super_user():
    async with engine.connect() as conn:
        tables = await conn.run_sync(use_inspector)
        if 'admins' in tables:
            try:
                async with async_session() as session:
                    if not await admins_crud.get(Config.MY_ID, session):
                        await admins_crud.create(SUPERUSER, session)
            except Exception:
                pass
