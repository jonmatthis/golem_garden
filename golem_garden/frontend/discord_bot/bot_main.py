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
        self._conversation_engine = ConversationEngine(publish_func=self._publish_message)
        self._active_chat = {}
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

        self._active_chat["thread"] = await message_thread.create_thread(
            name=ctx.user.name + "'s conversation with GPT"
        )

        self._active_chat["owner"] = ctx.user.id


        await ctx.respond("Conversation started.")
        await self._active_chat["thread"].send(f"<@{str(ctx.user.id)}> is the thread owner.")
        await self._active_chat["thread"].send(self._golem.intake_message("Say hello to yr friend"))

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Make sure we won't be replying to ourselves.
        if message.author.id == self._bot.user.id:
            return


        if not message.channel.id == self._active_chat["thread"].id:
            return

        if not message.author.id == self._active_chat["owner"]:
            return

        logger.info(f"Sending message to the agent: {message.content}")
        await self._conversation_engine.step(message.content)
        # await self._active_chat["thread"].send(self._golem.intake_message(message.content))


    async def _publish_message(self, message):
        try:
            await self._active_chat["thread"].send(message)
        except Exception as e:
            logger.error(f"Error posting message: {e}")




async def main():

    bot = make_bot()
    bot.add_cog(AgentCog(bot))
    await bot.start(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    logger.info("Starting bot...")
    asyncio.run(main())
