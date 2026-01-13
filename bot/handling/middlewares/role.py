import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update, User

from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests, User as DBUser
from bot.enums.roles import Role

logger = logging.getLogger(__name__)
requests = Requests()


class RoleMiddleware(BaseMiddleware):
    """Middleware which drops user's role into the context."""

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        admin_id: int = data.get("admin_id")
        session: AsyncSession = data.get("session")

        db_user: DBUser = data.get("db_user")

        if db_user is None:

            if user.id != admin_id:
                data["role"] = Role.USER
                return await handler(event, data)
            else:
                data["role"] = Role.ADMIN
        else:

            if db_user.role == Role.ADMIN and user.id != admin_id:
                await requests.users.set_role(
                    session=session, tg_id=user.id, role=Role.USER
                )
                data["role"] = Role.USER
            elif db_user.role == Role.USER and user.id == admin_id:
                await requests.users.set_role(
                    session=session, telegram_id=user.id, role=Role.ADMIN
                )
                data["role"] = Role.ADMIN
            else:
                data["role"] = db_user.role

        return await handler(event, data)
