from aiogram import Router

from .menu_command import menu_router
from .payment import payment_router

user_router = Router()
user_router.include_routers(menu_router, payment_router)

__all__ = ["user_router"]
