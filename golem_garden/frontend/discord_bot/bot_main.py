import asyncio
import logging
import os

from dotenv import load_dotenv

from golem_garden.frontend.discord_bot.bot_maker import make_discord_bot
from golem_garden.frontend.discord_bot.cogs.agent_cog.agent_cog import AgentCog

load_dotenv()

logger = logging.getLogger(__name__)


async def main():
    discord_bot = make_discord_bot()
    discord_bot.add_cog(AgentCog(discord_bot=discord_bot))
    await discord_bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(main())
