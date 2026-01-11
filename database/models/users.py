from datetime import datetime

from sqlalchemy import BigInteger, Text, Boolean, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    language: Mapped[str] = mapped_column(Text, nullable=False)
    banned: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    is_alive: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
