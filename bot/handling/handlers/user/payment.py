import logging
from typing import TYPE_CHECKING

from aiogram import Bot, Router, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.enums import ContentType
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


payment_router = Router()


@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_succesful_payment(
    mesage: Message, bot: Bot, i18n: TranslatorRunner, club_chat_id: int
):
    if mesage.successful_payment.invoice_payload == "club":
        club_access_link = await bot.create_chat_invite_link(
            chat_id=club_chat_id, member_limit=1, name="club_link"
        )
        await mesage.answer(
            text=i18n.successful.payment.club(link=club_access_link.invite_link)
        )
