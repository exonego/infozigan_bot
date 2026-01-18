import logging
from typing import TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.enums import ContentType
from sqlalchemy.ext.asyncio import AsyncSession
from fluentogram import TranslatorRunner

from database import Requests
from bot.enums.levels import Level

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()
payment_router = Router()


@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_succesful_payment(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    i18n: TranslatorRunner,
    club_chat_id: int,
    admin_id: int,
    admin_username: int,
):
    if message.successful_payment.invoice_payload == "club":
        await requests.users.set_level(
            session=session, tg_id=message.from_user.id, level=Level.CLUB
        )

        club_link = await bot.create_chat_invite_link(
            chat_id=club_chat_id, member_limit=1, name="club_link"
        )
        await message.answer(
            text=i18n.successful.payment.club(link=club_link.invite_link)
        )

        await bot.send_message(
            chat_id=admin_id,
            text=i18n.successful.payment.admin.club(
                first_name=message.from_user.first_name,
                username=(
                    message.from_user.username
                    if message.from_user.username is not None
                    else "no"
                ),
            ),
        )

    elif message.successful_payment.invoice_payload == "mentor":
        await requests.users.set_level(
            session=session, tg_id=message.from_user.id, level=Level.MENTOR
        )

        club_link = await bot.create_chat_invite_link(
            chat_id=club_chat_id, member_limit=1, name="club_link"
        )
        await message.answer(
            text=i18n.successful.payment.mentor.left(
                link=club_link.invite_link, username=admin_username
            )
        )

        await bot.send_message(
            chat_id=admin_id,
            text=i18n.successful.payment.admin.mentor.left(
                first_name=message.from_user.first_name,
                username=(
                    message.from_user.username
                    if message.from_user.username is not None
                    else "no"
                ),
            ),
        )

    elif message.successful_payment.invoice_payload == "mentor_upgrade":
        await requests.users.set_level(
            session=session, tg_id=message.from_user.id, level=Level.MENTOR
        )
        await message.answer(
            text=i18n.successful.payment.mentor.member(username=admin_username)
        )

        await bot.send_message(
            chat_id=admin_id,
            text=i18n.successful.payment.admin.mentor.member(
                first_name=message.from_user.first_name,
                username=(
                    message.from_user.username
                    if message.from_user.username is not None
                    else "no"
                ),
            ),
        )
