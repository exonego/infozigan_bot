import logging
from decimal import Decimal

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database import Price

logger = logging.getLogger(__name__)


class PriceNotFoundError(Exception):
    "Calling when there is no one price record in database"

    def __init__(self, message: str = "Current price not found in database"):
        self.message = message
        super().__init__(self.message)


async def get_cur_price(session: AsyncSession, title: str) -> Decimal:
    stmt = (
        select(Price)
        .where(Price.title == title)
        .order_by(desc(Price.created_at))
        .limit(1)
    )
    result = await session.execute(stmt)
    last_price = result.scalar()
    if last_price is None:
        raise PriceNotFoundError()
    return last_price.price
