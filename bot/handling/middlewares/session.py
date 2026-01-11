import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from sqlalchemy.ext.asyncio import async_sessionmaker

logger = logging.Logger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    """Middleware which drops session into the context."""

    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:

        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
