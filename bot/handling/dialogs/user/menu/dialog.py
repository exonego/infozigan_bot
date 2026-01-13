import logging

from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Url, Next
from aiogram_dialog.widgets.media import StaticMedia

from bot.handling.states import MenuSG
from bot.handling.dialogs.user.menu.getters import start_getter, description_getter
from bot.handling.dialogs.user.menu.handlers import send_invoice_handler

logger = logging.getLogger(__name__)


menu_dialog = Dialog(
    Window(
        StaticMedia(
            path="/infozigan_bot/assets/greeting_photo.jpg", type=ContentType.PHOTO
        ),
        Format("{text}"),
        Url(text=Format("{button_guides}"), url=Const("https://t.me/neirostart23")),
        Next(text=Format("{button_description}")),
        getter=start_getter,
        state=MenuSG.start,
    ),
    Window(
        StaticMedia(
            path="/infozigan_bot/assets/course_photo.jpg", type=ContentType.PHOTO
        ),
        Format("{description}"),
        Button(
            text=Format("{button_pay}"), id="pay_access", on_click=send_invoice_handler
        ),
        getter=description_getter,
        state=MenuSG.description,
    ),
)
