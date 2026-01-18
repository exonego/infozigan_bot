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

from bot.enums.levels import Level
from database import User, Requests

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def send_invoice_club_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    db_user: User = dialog_manager.middleware_data.get("db_user")
    club_chat_id: int = dialog_manager.middleware_data.get("club_chat_id")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    user_status = (
        await bot.get_chat_member(chat_id=club_chat_id, user_id=callback.from_user.id)
    ).status

    if user_status == ChatMemberStatus.LEFT and db_user.level == Level.FREE:
        session: AsyncSession = dialog_manager.middleware_data.get("session")

        await dialog_manager.done()

        yoo_token: SecretStr = dialog_manager.middleware_data.get("yoo_token")
        cur_price_club: Decimal = await requests.prices.get_cur_price(
            session=session, title="club"
        )

        await callback.message.answer_invoice(
            title=i18n.menu.invoice.club.title(),
            description=i18n.menu.invoice.club.description(),
            payload="club",
            provider_token=yoo_token.get_secret_value(),
            currency="RUB",
            prices=[{"label": "RUB", "amount": int(cur_price_club * 100)}],
        )
    elif user_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED):
        await callback.message.answer(text=i18n.menu.invoice.club.member())
    elif user_status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        await callback.message.answer(text=i18n.menu.invoice.club.admin())
    elif user_status == ChatMemberStatus.KICKED:
        await callback.message.answer(text=i18n.menu.invoice.club.kicked())
    else:
        admin_username: str = dialog_manager.middleware_data.get("admin_username")
        await callback.message.answer(
            text=i18n.menu.invoice.club.leave(username=admin_username)
        )


async def send_invoice_mentor_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    bot: Bot = dialog_manager.middleware_data.get("bot")
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    db_user: User = dialog_manager.middleware_data.get("db_user")
    club_chat_id: int = dialog_manager.middleware_data.get("club_chat_id")
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    admin_username: str = dialog_manager.middleware_data.get("admin_username")

    user_status = (
        await bot.get_chat_member(chat_id=club_chat_id, user_id=callback.from_user.id)
    ).status

    yoo_token: SecretStr = dialog_manager.middleware_data.get("yoo_token")

    if user_status == ChatMemberStatus.LEFT and db_user.level == Level.FREE:
        cur_price_mentor: Decimal = await requests.prices.get_cur_price(
            session=session, title="mentor"
        )

        await dialog_manager.done()

        await callback.message.answer_invoice(
            title=i18n.menu.invoice.mentor.title(),
            description=i18n.menu.invoice.mentor.description(),
            payload="mentor",
            provider_token=yoo_token.get_secret_value(),
            currency="RUB",
            prices=[{"label": "RUB", "amount": int(cur_price_mentor * 100)}],
        )
    elif (
        user_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED)
        and db_user.level == Level.CLUB
    ):
        cur_price_mentor_upgrade: Decimal = await requests.prices.get_cur_price(
            session=session, title="mentor_upgrade"
        )

        await dialog_manager.done()

        await callback.message.answer(
            text=i18n.menu.invoice.mentor.member(price=cur_price_mentor_upgrade)
        )
        await callback.message.answer_invoice(
            title=i18n.menu.invoice.mentor.title(),
            description=i18n.menu.invoice.mentor.description(),
            payload="mentor_upgrade",
            provider_token=yoo_token.get_secret_value(),
            currency="RUB",
            prices=[{"label": "RUB", "amount": int(cur_price_mentor_upgrade * 100)}],
        )
    elif (
        user_status in (ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED)
        and db_user.level == Level.MENTOR
    ):
        await callback.message.answer(
            text=i18n.menu.invoice.mentor.mentor(username=admin_username)
        )
    elif user_status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR):
        await callback.message.answer(text=i18n.menu.invoice.club.admin())
    elif user_status == ChatMemberStatus.KICKED:
        await callback.message.answer(text=i18n.menu.invoice.club.kicked())
    else:
        await callback.message.answer(
            text=i18n.menu.invoice.club.leave(username=admin_username)
        )
