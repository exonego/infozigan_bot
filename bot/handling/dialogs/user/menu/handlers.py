import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import SecretStr
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.enums import ChatMemberStatus
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from utils.business_logic import get_cur_price

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def send_invoice_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    club_chat_id: int = dialog_manager.middleware_data.get("club_chat_id")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    user_status = (
        await bot.get_chat_member(chat_id=club_chat_id, user_id=callback.from_user.id)
    ).status

    if user_status == ChatMemberStatus.LEFT:
        session: AsyncSession = dialog_manager.middleware_data.get("session")

        await dialog_manager.done()

        yoo_token: SecretStr = dialog_manager.middleware_data.get("yoo_token")
        cur_price_club: Decimal = await get_cur_price(session=session, title="club")

        await callback.message.answer_invoice(
            title=i18n.menu.invoice.club.title(),
            description=i18n.menu.invoice.club.description(),
            payload="club",
            provider_token=yoo_token.get_secret_value(),
            currency="RUB",
            prices=[{"label": "RUB", "amount": int(cur_price_club * 100)}],
        )
    elif (
        user_status == ChatMemberStatus.MEMBER
        or user_status == ChatMemberStatus.RESTRICTED
    ):
        await bot.send_message(
            chat_id=callback.from_user.id, text=i18n.menu.invoice.club.member()
        )
    elif (
        user_status == ChatMemberStatus.ADMINISTRATOR
        or user_status == ChatMemberStatus.CREATOR
    ):
        await bot.send_message(
            chat_id=callback.from_user.id, text=i18n.menu.invoice.club.admin()
        )
    elif user_status == ChatMemberStatus.KICKED:
        await bot.send_message(
            chat_id=callback.from_user.id, text=i18n.menu.invoice.club.kicked()
        )
