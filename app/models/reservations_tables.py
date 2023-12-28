from sqlalchemy import ForeignKey, Table, Column

from app.core.db import Base


association_table = Table(
    "association_reservation_tables",
    Base.metadata,
    Column("reservation_id", ForeignKey("reservation.id"), primary_key=True),
    Column("table_id", ForeignKey("table.id"), primary_key=True),
)
