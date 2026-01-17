import logging

from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode, ShowMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.enums.roles import Role
from bot.enums.levels import Level
from bot.handling.states import MenuSG
from database import Requests, User

logger = logging.getLogger(__name__)

requests = Requests()
start_router = Router()


@start_router.message(CommandStart())
async def command_start(
    message: Message,
    dialog_manager: DialogManager,
    bot: Bot,
    session: AsyncSession,
    db_user: User | None,
    role: Role,
    club_chat_id: int,
) -> None:
    """Handles /start command"""

    if db_user is None:
        user_status = (
            await bot.get_chat_member(
                chat_id=club_chat_id, user_id=message.from_user.id
            )
        ).status
        await requests.users.add_user(
            session=session,
            tg_id=message.from_user.id,
            language=message.from_user.language_code,
            role=role,
            level=(
                Level.FREE
                if user_status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED)
                else Level.CLUB
            ),
        )

    if role == Role.USER:
        await dialog_manager.start(
            state=MenuSG.start,
            mode=StartMode.RESET_STACK,
        )
    else:
        pass
