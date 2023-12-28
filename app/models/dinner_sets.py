from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.reservations_dinnersets import (
    association_table as reservations_dinnersets,
)


class DinnerSet(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    image_id: Mapped[int]
    reservations: Mapped[List['Reservation']] = relationship(
        secondary=reservations_dinnersets,
        back_populates='dinner_sets',
    )

    def __repr__(self):
        return f"Сет: {self.name} стоимость: {self.price}"
