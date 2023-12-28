from typing import List

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Restaurant(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    contact_info: Mapped[str] = mapped_column(nullable=True)
    image_id: Mapped[int]
    tables: Mapped[List["Table"]] = relationship(back_populates="restaurant")

    @hybrid_property
    def tables_quantity(self):
        return len(self.tables)

    def __repr__(self):
        return f"Ресторан: {self.name} Адрес: {self.location}, id {self.id}"
