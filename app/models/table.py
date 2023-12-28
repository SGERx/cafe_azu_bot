from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.reservations_tables import (
    association_table as reservations_tables
)


class Table(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    table_number: Mapped[int]
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id"))
    capacity: Mapped[int]
    group: Mapped[int] = mapped_column(nullable=True)

    restaurant: Mapped["Restaurant"] = relationship(back_populates="tables")
    reservations: Mapped[List["Reservation"]] = relationship(
        secondary=reservations_tables, back_populates="tables"
    )

    def __repr__(self):
        try:
            return f"Стол - id {self.id}, " \
                   f"номер {self.table_number}, " \
                   f"группа {self.group} " \
                   f"{self.restaurant.name} на " \
                   f"{self.capacity} человек"
        except AttributeError:
            return f"Стол - id {self.id}, " \
                   f"номер {self.table_number}, " \
                   f"группа {self.group} " \
                   f"{self.capacity} человек"
