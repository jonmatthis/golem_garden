import logging

import discord

from golem_garden.backend.golem import Golem
from golem_garden.backend.langchain_stuff.agents.agent_builder import AgentBuilder
from golem_garden.backend.langchain_stuff.agents.get_available_agents import get_available_agents
from golem_garden.experimental.karl.steerable_conversation.conversation_engine import \
    npc_builder_chain_from_config_path, agent_enpisi_config_path, ConversationEngine

logger = logging.getLogger(__name__)

class AgentCog(discord.Cog):
    def __init__(self, discord_bot: discord.Bot):
        self._discord_bot = discord_bot
        self._active_chat = {}

    @discord.slash_command(name="chat", description="Chat with the bot")
    @discord.option(name="agent",
                    description="The agent to chat with",
                    required=False,
                    choices=list(get_available_agents().keys())
                    )
    @discord.option(name="model",
                    description="gpt-4`: slow, expensive, smart; `gpt-3.5-turbo`: fast, cheap, tries its best",
                    required=False,
                    choices=['gpt-4', 'gpt-3.5-turbo']
                    )
    async def chat(self,
                   ctx: discord.ApplicationContext,
                   agent: str = "dunkthulu",
                   model: str = "gpt-4",):


        chat_title = f"{ctx.user.name} & {agent}"
        logger.info(f"Starting chat: {chat_title}")

        self._agent = self._get_agent(agent_name=agent,
                                      model=model,)
        assert self._agent is not None, f"Agent {agent} not found!"

        message_embed = discord.Embed(
            title=chat_title,
            description=f"a conversation between {ctx.user.name} and {agent}\n"
                        f"Model: {model}"
                        f"User: {ctx.user.name}\n"
                        f"Agent: {agent}\n"
                        f"Config: {self._agent._configuration}",
            color=0x25d790,
        )

        message_thread = await ctx.send(embed=message_embed)

        self._active_chat["thread"] = await message_thread.create_thread(
            name=chat_title,
        )

        self._active_chat["owner"] = ctx.user.id
        self._active_chat["agent"] = agent
        self._active_chat["title"] = chat_title

        await ctx.respond("Conversation started.")
        await self._active_chat["thread"].send(f"<@{str(ctx.user.id)}> is the thread owner.")
        await self._active_chat["thread"].send(f"`{agent} is ready to chat!`")

    @discord.Cog.listener()
    async def on_message(self, message: discord.Message):
        logger.info(f"Received message: {message.content}")

        # Make sure we won't be replying to ourselves.
        if message.author.id == self._discord_bot.user.id:
            return

        if not message.channel.id == self._active_chat["thread"].id:
            return

        if not message.author.id == self._active_chat["owner"]:
            return

        logger.info(f"Sending message to the agent: {message.content}")

        await self._active_chat["thread"].send("`Awaiting agent response...`")

        agent_response = self._intake_message(message.content)

        await self._active_chat["thread"].send(agent_response)

    def _get_agent(self, agent_name: str, model: str):
        if agent_name == "golem":
            agent = Golem()
            self._intake_message = agent.intake_message


        if agent_name == "enpisi":
            agent = npc_builder_chain_from_config_path(config_path=agent_enpisi_config_path)
            self._intake_message = agent.intake_message

        if agent_name == "enpisi+enpisi":
            agent = ConversationEngine(publish_func=self._publish_message)
            self._intake_message = agent.step


        try:
            agent = AgentBuilder(configuration=get_available_agents()[agent_name], model=model)
            self._intake_message = agent.intake_message
        except Exception as e:
            agent = None
            raise Exception(f"Erorr getting agent: {e}")

        return agent
    async def _publish_message(self, message):
        try:
            await self._active_chat["thread"].send(message)
        except Exception as e:
            logger.error(f"Error posting message: {e}")
