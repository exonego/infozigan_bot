import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.enums.roles import Role

logger = logging.getLogger(__name__)


class RoleFilter(BaseFilter):
    """Checks the user_role"""

    def __init__(self, *roles: str | Role):
        if not roles:
            raise ValueError("At least one role must be passed to UserRoleFilter")

        self.roles = frozenset(
            Role(role) if isinstance(role, str) else role
            for role in roles
            if isinstance(role, (str, Role))
        )

        if not self.roles:
            raise ValueError("No valid roles passed to UserRoleFilter")

    async def __call__(self, event: Message | CallbackQuery, user_role: Role) -> bool:

        user = event.from_user
        if user is None:
            return False

        return user_role in self.roles
