import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.handling.handlers.start_command import start_router
from bot.handling.handlers.user import user_router
from bot.handling.dialogs import dialog_user_router
from bot.handling.middlewares import (
    DbSessionMiddleware,
    ShadowBanMiddleware,
    TranslatorRunnerMiddleware,
    RoleMiddleware,
)
from config.config import Config
from I18N import i18n_factory
from utils.bootstrap import upload_assets

# Module logger init
logger = logging.getLogger(__name__)


# Function for config and launch bot
async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Init redis storage
    logger.info("Init redis storage...")
    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        username=config.redis.username,
        password=config.redis.password.get_secret_value(),
    )
    storage = RedisStorage(
        redis=redis,
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    # Create sqlalchemy engine to connect db
    logger.info("Creation sqlalchemy engine...")
    engine = create_async_engine(url=str(config.db.dsn))
    # Create sqlalchemy Sessionmaker
    logger.info("Creation sqlalchemy Sessionmaker...")
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Create object type TranslatorHub
    logger.info("Creation translator_hub...")
    translator_hub = i18n_factory()

    # Init Bot and Dispatcher
    logger.info("Init bot and dispatcher...")
    tg_bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Setup dialogs
    logger.info("Setting up dialogs...")
    setup_dialogs(dp)

    # Include routers
    logger.info("Including routers into dispatcher...")
    dp.include_routers(start_router, user_router, dialog_user_router)

    # Register middlewares
    logger.info("Registration middlewares...")
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=Sessionmaker))
    dp.update.outer_middleware(ShadowBanMiddleware())
    dp.update.outer_middleware(
        TranslatorRunnerMiddleware(translator_hub=translator_hub)
    )
    dp.update.outer_middleware(RoleMiddleware())

    # Start polling
    await dp.start_polling(
        tg_bot,
        admin_id=config.bot.admin_id,
        admin_username=config.bot.admin_username,
        club_chat_id=config.bot.club_chat_id,
        yoo_token=config.yoo.token,
        file_ids=await upload_assets(
            redis=redis, bot=tg_bot, chat_id=config.bot.assets_chat_id
        ),
    )
