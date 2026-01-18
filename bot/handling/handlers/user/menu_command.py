import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from bot.handling.filters.role import RoleFilter
from bot.enums.roles import Role
from bot.handling.states import MenuSG

logger = logging.getLogger(__name__)

menu_router = Router()
menu_router.message.filter(RoleFilter(Role.USER))
menu_router.callback_query.filter(RoleFilter(Role.USER))


@menu_router.message(Command("menu"))
async def command_menu(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        state=MenuSG.start,
        mode=StartMode.RESET_STACK,
    )
