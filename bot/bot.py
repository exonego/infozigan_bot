import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import Config
from I18N import i18n_factory


# Module logger init
logger = logging.getLogger(__name__)


# Function for config and launch bot
async def main(config: Config) -> None:
    logger.info("Starting bot...")

    # Init redis storage
    logger.info("Init redis storage...")
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            username=config.redis.username,
            password=config.redis.password.get_secret_value(),
        ),
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
    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Setup dialogs
    logger.info("Setting up dialogs...")
    setup_dialogs(dp)

    # Include routers into dispatcher

    # Register middlewares

    # Start polling
    await dp.start_polling(bot, admin_id=config.bot.admin_id)
