import logging
import json
from datetime import datetime

from aiogram import Bot
from aiogram.types import FSInputFile
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


async def upload_assets(redis: Redis, bot: Bot, chat_id: int) -> dict[str, int]:
    """
    Try to get asset file_id's from redis and return they in dict
    If can't, upload assets in chat and save them file_id's
    """
    # Try to take file_id's from Redis
    result_raw = await redis.get("asset_file_ids")
    if result_raw:
        logger.info("File_id's loaded from Redis")
        return json.loads(result_raw)

    # If can't - upload assets in chat and save them file_ids
    assets = {
        "greeting": "/infozigan_bot/assets/greeting_photo.jpg",
        "course": "/infozigan_bot/assets/course_video.mp4",
    }
    result = dict()
    for key, path in assets.items():
        logger.info(f"Uploading the {key} asset...")
        file_extension = path.split(".")[-1].lower()

        if file_extension in ("jpg", "jpeg", "png"):
            photo = FSInputFile(path)
            message = await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=f"{key}: {datetime.now()}",
                request_timeout=60,
            )
            result[key] = message.photo[-1].file_id
        elif file_extension in ["mov", "mp4"]:
            video = FSInputFile(path)
            message = await bot.send_video(
                chat_id=chat_id,
                video=video,
                caption=f"{key}: {datetime.now()}",
                request_timeout=600,
            )
            result[key] = message.video.file_id

        logger.info(f"The {key} asset loaded")

    # Load file_id's in Redis
    await redis.set("asset_file_ids", json.dumps(result))

    return result
