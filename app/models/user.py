from datetime import datetime
from typing import List

from sqlalchemy import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    chat_id: Mapped[int]
    phone_number: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column(DATETIME, default=datetime.now)
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"Пользователь:\n " \
               f"имя {self.name},\n " \
               f"телефон {self.phone_number},\n " \
               f"email {self.email},\n " \
               f"chat_id: {self.chat_id},\n " \
               f"id {self.id}"
