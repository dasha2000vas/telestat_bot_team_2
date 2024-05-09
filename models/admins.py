from datetime import datetime as dt

from sqlalchemy import (
    Boolean, BigInteger, Column, DateTime, String
)

from core.db import Base


class Admins(Base):
    """Модель пользователя ТГ."""

    user_id = Column(BigInteger, unique=True)
    username = Column(String(50), unique=True)
    create_date = Column(DateTime, default=dt.now)
    is_superuser = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # def __repr__(self) -> str:
    #     return (f'{self.user_id},'
    #             f'{self.username},'
    #             f'{self.create_date},'
    #             f'{self.is_superuser},'
    #             f'{self.is_admin},')

    def as_dict(self):
        return {i.name: getattr(self, i.name) for i in self.__table__.columns}
