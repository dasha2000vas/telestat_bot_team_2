from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
)
from settings import (
    Configs, configure_logging
)
logger = configure_logging()


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

engine = create_async_engine(Configs.DB_URL)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
