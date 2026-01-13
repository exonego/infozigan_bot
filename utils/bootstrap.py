from decimal import Decimal

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from database import Price


class PriceNotFoundError(Exception):
    "Calling when there is no one price record in database"

    def __init__(self, message: str = "Current price not found in database"):
        self.message = message
        super().__init__(self.message)


async def get_cur_price(engine: AsyncEngine) -> Decimal:
    async with AsyncSession(engine) as session:
        stmt = select(Price).order_by(desc(Price.created_at)).limit(1)
        result = await session.execute(stmt)
        last_price = result.scalar()
        if last_price is None:
            raise PriceNotFoundError()
        return last_price.price
