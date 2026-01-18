from aiogram import Router

from .menu import menu_dialog

dialog_user_router = Router()
dialog_user_router.include_routers(menu_dialog)

__all__ = ["dialog_user_router"]
