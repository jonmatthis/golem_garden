import asyncio
import logging
import os

import discord

from dotenv import load_dotenv

from golem_garden.backend.golem import Golem
from golem_garden.experimental.karl.steerable_conversation.conversation_engine import ConversationEngine
from golem_garden.frontend.discord_bot.bot_maker import make_bot

load_dotenv()

logger = logging.getLogger(__name__)

class AgentCog(discord.Cog):
    def __init__(self, bot:discord.Bot):
        self._bot = bot
        # self._conversation_engine = ConversationEngine(poll_func=self.)
        self._active_chats = {}
        self._golem = Golem()


    @discord.slash_command(name = "chat", description = "Chat with the bot")
    async def chat(self, ctx):
        logger.info(f"Received chat command: {ctx}")
        embed_title = f"{ctx.user.name}'s conversation with GPT"
        message_embed = discord.Embed(
            title=embed_title,
            description=f"Conversation with a friendly golem agent",
            color=0x808080,
        )


        message_thread = await ctx.send(embed=message_embed)
        thread = await message_thread.create_thread(
            name=ctx.user.name + "'s conversation with GPT"
        )
        new_chat = {}
        new_chat["thread"] = thread
        new_chat["owner"] = ctx.user.id

        self._active_chats[ctx.user.id] = new_chat

        await ctx.respond("Conversation started.")
        await thread.send(f"<@{str(ctx.user.id)}> is the thread owner.")
        await thread.send(self._golem)

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Make sure we won't be replying to ourselves.
        if message.author.id == self._bot.user.id:
            return

        logger.info(f"Received message: {message}")



async def main():

    bot = make_bot()
    bot.add_cog(AgentCog(bot))
    await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(main())
