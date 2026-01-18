import logging

from decimal import Decimal
from typing import TYPE_CHECKING

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from database import Requests

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)

requests = Requests()


async def start_getter(
    dialog_manager: DialogManager,
    i18n: TranslatorRunner,
    session: AsyncSession,
    **kwargs
) -> dict[str, str]:
    club_price = await requests.prices.get_cur_price(session=session, title="club")
    mentor_price = await requests.prices.get_cur_price(session=session, title="mentor")
    mentor_upgrade_price = await requests.prices.get_cur_price(
        session=session, title="mentor_upgrade"
    )
    return {
        "admin_menu_text": i18n.admin.menu.text(
            club_price=club_price if club_price else "no",
            mentor_price=mentor_price if mentor_price else "no",
            mentor_upgrade_price=mentor_upgrade_price if mentor_upgrade_price else "no",
        ),
        "admin_menu_button_analytics": i18n.admin.menu.button.analytics(),
        "admin_menu_button_price": i18n.admin.menu.button.price(),
        "admin_menu_button_mailing": i18n.admin.menu.button.mailing(),
        "admin_menu_button_user": i18n.admin.menu.button.user(),
    }
