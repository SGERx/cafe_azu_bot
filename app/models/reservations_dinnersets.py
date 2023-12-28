from sqlalchemy import ForeignKey, Table, Column, Integer

from app.core.db import Base


association_table = Table(
    "association_reservation_dinner_set",
    Base.metadata,
    Column(
        'reservation_id',
        ForeignKey('reservation.id'),
        primary_key=True
    ),
    Column(
        'dinner_set_id',
        ForeignKey('dinnerset.id'),
        primary_key=True
    ),
    Column(
        'quantity',
        Integer,
        nullable=False,
        default=1
    )

)
