from typing import TYPE_CHECKING

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from I18N.locales.stub import TranslatorRunner  # type: ignore


async def start_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "text": i18n.menu.text(),
        "button_description": i18n.menu.button.description(),
        "button_guides": i18n.menu.button.guides(),
    }


async def description_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    return {
        "description": i18n.menu.description(),
        "button_pay": i18n.menu.button.pay(),
    }
