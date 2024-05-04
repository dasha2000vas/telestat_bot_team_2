from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
)
from settings import (
    Config,
)


class PreBase:
    """Базовый класс для таблиц. Названия в нижнем регистре."""

    id = Column(
        Integer,
        primary_key=True,
    )

    @declared_attr
    def __tablename__(
        cls,
    ):
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)

engine = create_async_engine(Config.DB_URL)

async_session = async_sessionmaker(engine)
