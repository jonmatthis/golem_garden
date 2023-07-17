import asyncio
import logging

from golem_garden.frontends.discord_bot.bot_main import bot_main

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(bot_main())
