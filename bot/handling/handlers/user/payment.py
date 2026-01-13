import logging

from aiogram import Router
from aiogram.types import PreCheckoutQuery

logger = logging.getLogger(__name__)


payment_router = Router()


@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)
