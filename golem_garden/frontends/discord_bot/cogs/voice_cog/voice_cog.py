from discord.ext import commands
import discord
import logging
from typing import Optional

from golem_garden.frontends.discord_bot.bot import DiscordBot

logger = logging.getLogger(__name__)

class VoiceCog(commands.Cog):
    def __init__(self, bot: DiscordBot):
        self.audio_source = None
        self.bot = bot
        self.voice_channel = None
        self.voice_client = None

    @commands.slash_command(name="voice", description="Enter a voice channel and start recording")
    async def voice(self, ctx: commands.Context):
        """
        Start recording the voice channel the invoker is currently in.
        If invoked outside a thread, opens a new thread.
        If invoked within a thread, the bot will post in the current thread.

        Args:
            ctx (commands.Context): The context in which a command is called.
        """
        # Get user's voice channel
        author_vc = ctx.author.voice
        if not author_vc:
            # If the user isn't in a voice channel, get the first voice channel in the guild
            voice_channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.VoiceChannel)]
            if not voice_channels:
                await ctx.respond("No voice channels found in this server.")
                return
            self.voice_channel = voice_channels[0]
            await ctx.respond(
                f"You weren't in a voice channel, so I'm joining the first available one: {self.voice_channel.name}")
        else:
            self.voice_channel = author_vc.channel

        # If the bot is already in a voice channel, leave it
        if self.voice_client:
            await self.voice_client.disconnect()

        # Join the user's voice channel
        self.voice_client = await self.voice_channel.connect()


        await ctx.respond(f"Joined voice channel: {self.voice_channel.name}", ephemeral=True)
        logger.info(f"Joined voice channel: {self.voice_channel.name}")


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        Handle the event when a member's voice state changes.

        Args:
            member (discord.Member): The member whose voice states changed.
            before (discord.VoiceState): The voice state prior to the changes.
            after (discord.VoiceState): The current voice state.
        """
        logger.info(f"Voice state updated for member: {member.name}")


