"""Создание суперюзера при инициализации БД"""

from sqlalchemy import inspect
from core.db import async_session, engine
from settings import Config
from crud.admins import admins_crud

from constants import SUPERUSER


def use_inspector(conn):
    inspector = inspect(conn)
    return inspector.get_table_names()


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
