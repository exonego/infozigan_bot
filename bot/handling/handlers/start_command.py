import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums.roles import Role
from bot.handling.states import MenuSG
from database import Requests, User

logger = logging.getLogger(__name__)

requests = Requests()
start_router = Router()


@start_router.message(CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager,
    session: AsyncSession,
    db_user: User | None,
    role: Role,
) -> None:
    """Handles /start command"""

    if db_user is None:
        await requests.users.add_user(
            session=session,
            tg_id=message.from_user.id,
            language=message.from_user.language_code,
            role=role,
        )

    if role == Role.USER:
        await dialog_manager.start(
            state=MenuSG.start,
            mode=StartMode.RESET_STACK,
        )
    else:
        pass
