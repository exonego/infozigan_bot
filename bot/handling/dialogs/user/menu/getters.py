import logging

from decimal import Decimal
from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from utils.business_logic import get_cur_price

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def start_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str | MediaAttachment]:
    file_ids: dict[str, int] = dialog_manager.middleware_data.get("file_ids")
    photo = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("greeting"))
    )

    return {
        "text": i18n.menu.text(),
        "button_description": i18n.menu.button.description(),
        "button_guides": i18n.menu.button.guides(),
        "greeting_photo": photo,
    }


async def description_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    file_ids: dict[str, int] = dialog_manager.middleware_data.get("file_ids")

    cur_price_club: Decimal = await get_cur_price(session=session, title="club")
    cur_price_mentor: Decimal = await get_cur_price(session=session, title="mentor")

    video = MediaAttachment(
        type=ContentType.VIDEO, file_id=MediaId(file_ids.get("course"))
    )

    return {
        "description": i18n.menu.description(
            club_price=cur_price_club,
            mentor_price=(cur_price_mentor),
        ),
        "button_pay_club": i18n.menu.button.pay.club(price=cur_price_club),
        "button_pay_mentor": i18n.menu.button.pay.mentor(price=cur_price_mentor),
        "course_video": video,
    }
