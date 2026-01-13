import logging

from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import SecretStr
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore

logger = logging.getLogger(__name__)


async def send_invoice_handler(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    await dialog_manager.done()

    yoo_token: SecretStr = dialog_manager.middleware_data.get("yoo_token")
    cur_price: Decimal = dialog_manager.middleware_data.get("cur_price")

    await callback.message.answer_invoice(
        title="Title",
        description="Description",
        payload="club_access",
        provider_token=yoo_token.get_secret_value(),
        currency="RUB",
        prices=[{"label": "RUB", "amount": int(cur_price * 100)}],
    )
