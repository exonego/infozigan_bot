import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests
from bot.handling.states import MenuSG

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def switch_to_user_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=MenuSG.start)
