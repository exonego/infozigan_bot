import logging
from datetime import datetime
from decimal import Decimal

from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from database import Price

logger = logging.getLogger(__name__)


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


async def upload_assets(bot: Bot, chat_id: int) -> dict[str, int]:
    """Upload assets in chat and return them file_id's in dict"""
    assets = {
        "greeting": "/infozigan_bot/assets/greeting_photo.jpg",
        "course": "/infozigan_bot/assets/course_photo.jpg",
    }
    result = dict()
    for key, path in assets.items():
        logger.info(f"Loading the {key} asset...")
        photo = FSInputFile(path)
        msg = await bot.send_photo(
            chat_id=chat_id, photo=photo, caption=f"{key}: {datetime.now()}"
        )
        result[key] = msg.photo[-1].file_id
        logger.info(f"The {key} asset loaded")

    return result
