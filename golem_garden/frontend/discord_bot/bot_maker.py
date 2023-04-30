import logging

import discord


logger = logging.getLogger(__name__)
def make_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = discord.Bot(intents=intents)

    @bot.event
    async def on_ready():
        logger.info("Bot is ready!")
        print(f"{bot.user} is ready and online!")


    @bot.slash_command(name = "hello", description = "Say hello to the bot")
    async def hello(ctx):
        logger.info(f"Received hello command: {ctx}")
        await ctx.respond("Hey!")

    return bot

