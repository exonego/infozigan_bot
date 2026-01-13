import asyncio
import logging
import os
import sys

from config.config import load_config
from bot.bot import main

config = load_config()

logging.basicConfig(
    level=config.log.level,
    format=config.log.format,
    style=config.log.style,
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main(config))
