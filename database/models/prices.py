from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, DECIMAL, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
