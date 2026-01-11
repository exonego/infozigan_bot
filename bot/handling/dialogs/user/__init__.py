from aiogram import Router

from .menu import menu_dialog

user_router = Router()
user_router.include_routers(menu_dialog)

__all__ = ["user_router"]
