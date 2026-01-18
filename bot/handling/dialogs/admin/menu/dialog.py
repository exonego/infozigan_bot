import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row

from bot.handling.states import AdminMenuSG, MenuSG
from bot.handling.dialogs.admin.menu.getters import start_getter
from bot.handling.dialogs.admin.menu.handlers import switch_to_user_handler

logger = logging.getLogger(__name__)


menu_dialog = Dialog(
    Window(
        Format("{admin_menu_text}"),
        Button(text=Format("{admin_menu_button_analytics}"), id="switch_to_analytics"),
        Row(
            SwitchTo(
                text=Format("{admin_menu_button_price}"),
                id="switch_to_price",
                state=AdminMenuSG.price,
            ),
            Button(
                text=Format("{admin_menu_button_mailing}"),
                id="switch_to_mailing",
            ),
        ),
        Button(
            text=Format("{admin_menu_button_user}"),
            id="switch_to_user",
            on_click=switch_to_user_handler,
        ),
        getter=start_getter,
        state=AdminMenuSG.start,
    )
)
