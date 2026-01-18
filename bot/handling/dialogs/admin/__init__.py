from aiogram import Router

from .menu import menu_dialog

dialog_admin_router = Router()
dialog_admin_router.include_routers(menu_dialog)

__all__ = ["dialog_admin_router"]
