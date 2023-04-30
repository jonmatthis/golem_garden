import logging
import os

import discord
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

bot = discord.Bot()

@bot.event
async def on_ready():
    logger.info("Bot is ready!")
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    logger.info(f"Received hello command: {ctx}")
    await ctx.respond("Hey!")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
