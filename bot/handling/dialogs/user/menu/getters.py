import logging

from decimal import Decimal
from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def start_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str | MediaAttachment]:
    file_ids: dict[str, int] = dialog_manager.middleware_data.get("photo_ids")
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
    cur_price: Decimal = dialog_manager.middleware_data.get("cur_price")
    file_ids: dict[str, int] = dialog_manager.middleware_data.get("photo_ids")
    photo = MediaAttachment(
        type=ContentType.PHOTO, file_id=MediaId(file_ids.get("course"))
    )

    return {
        "description": i18n.menu.description(price=cur_price),
        "button_pay": i18n.menu.button.pay(price=cur_price),
        "course_photo": photo,
    }
