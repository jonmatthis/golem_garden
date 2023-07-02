import asyncio
import logging as logging
import os

import discord

from chatbot.discord_bot.cogs.summary_sender_cog import SummarySenderCog
from chatbot.discord_bot.cogs.thread_scraper_cog.thread_scraper_cog import ThreadScraperCog
from chatbot.discord_bot.cogs.video_chatter_cog import VideoChatterCog
from chatbot.mongo_database.mongo_database_manager import MongoDatabaseManager
from chatbot.system.logging.configure_logging import configure_logging

configure_logging(entry_point="discord")



from dotenv import load_dotenv

from chatbot.discord_bot.cogs.chat_cog.chat_cog import ChatCog

load_dotenv()



logger = logging.getLogger(__name__)


class DiscordBot(discord.Bot):
    def __init__(self,
                 mongo_database: MongoDatabaseManager):
        super().__init__(intents=discord.Intents.all())
        self.mongo_database = mongo_database

    @discord.Cog.listener()
    async def on_ready(self):
        logger.info("Bot is ready!")
        print(f"{self.user} is ready and online!")

    @discord.Cog.listener()
    async def on_message(self, message):
        logger.info(f"Received message: {message.content}")
        print(f"Received message: {message.content}")
        if message.guild is None:
            server_name = 'DM-with-' + str(message.author)
            channel_name = 'DM-with-' + str(message.author)
            collection_name  = "dm_messages"
        else:
            server_name = message.guild.name
            channel_name = message.channel.name
            collection_name = f"server_{message.guild.name}_messages"

        await self.mongo_database.upsert(
            collection=collection_name,
            query={"server_name": server_name},
            data={"$push": {"messages": {
                'author': str(message.author),
                'author_id': message.author.id,
                'user_id': message.author.id,
                'content': message.content,
                'timestamp': message.created_at.isoformat(),
                'guild': server_name,
                'channel': channel_name,
                'jump_url': message.jump_url,
                'thread': message.thread if message.thread else 'None',
                'dump': str(message)
            }}}
        )

    @discord.slash_command(name="hello", description="Say hello to the bot")
    async def hello(self, ctx):
        logger.info(f"Received hello command: {ctx}")
        await ctx.respond("Hey!")

    def run(self, token: str):
        self.run(token)

async def main():
    mongo_database_manager = MongoDatabaseManager()
    discord_bot = DiscordBot(mongo_database=mongo_database_manager)

    discord_bot.add_cog(ChatCog(bot=discord_bot,
                                mongo_database_manager=mongo_database_manager))

    discord_bot.add_cog(ThreadScraperCog(bot=discord_bot,
                                         mongo_database_manager=mongo_database_manager))

    discord_bot.add_cog(SummarySenderCog(bot=discord_bot,
                                         mongo_database_manager=mongo_database_manager))

    discord_bot.add_cog(VideoChatterCog(bot=discord_bot,
                                        mongo_database_manager=mongo_database_manager))

    await discord_bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(main())
