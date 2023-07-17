# TODO: Need to get this into an Agent form
# TODO: IO tools, blobs for people, then index and embeddings

from pathlib import Path

from dotenv import load_dotenv

from experimental.Builder.npc_builder_chain import NPCBuilderChain

load_dotenv()

import toml

from typing import Callable

from langchain.chat_models import ChatOpenAI

agent_enpisi_config_path = str(Path(__file__).parent.parent.parent / "Builder" / "agent_definitions" / "enpisi.config")
agent_list = [agent_enpisi_config_path, agent_enpisi_config_path]


def npc_builder_chain_from_config_path(config_path, conversation_llm=None, analysis_llm=None) -> NPCBuilderChain:
    if conversation_llm is None:
        conversation_llm = ChatOpenAI(model='gpt-4', temperature=0.9)

    if analysis_llm is None:
        analysis_llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)

    agent_definition = toml.load(config_path)

    npc_builder_chain = NPCBuilderChain.from_llm(conversation_llm, analysis_llm, verbose=False,
                                                 agent_config=agent_definition)
    npc_builder_chain.seed_agent()

    return npc_builder_chain


def poll_func():
    user_input = input("Enter your response, or 'QUIT' to cancel:")

    return user_input


def publish_func(msg):
    print(msg)


class ConversationEngine:
    def __init__(self,
                 poll_func: Callable[[], int] = None,
                 publish_func: Callable[[str], None] = None,
                 agents: list = agent_list,
                 model_name='gpt-3.5-turbo'):

        self.agents = agents

        self.agent_1, self.agent_2 = [npc_builder_chain_from_config_path(path) for path in self.agents]

        self._tell_agents_to_collaborate()

        self.publish = publish_func

        self.poll = poll_func

    def _tell_agents_to_collaborate(self):
        collaboration_message = "You are going to be working with another agent to work with the human to complete the task."
        self.agent_1.input_step(collaboration_message)
        self.agent_2.input_step(collaboration_message)
        self._previous_message_1 = ''
        self._previous_message_2 = ''

    async def step(self, human_message=''):

        if human_message != 'pass':
            if self._previous_message_1 == '':
                self.agent_1.input_step(f"You're going first! The human said{human_message}")
            else:
                self.agent_1.input_step(
                    f"The other agent said: {self._previous_message_2}, the human said{human_message} - collaborate!")
        else:
            self.agent_1.input_step(
                f"The other agent said: {self._previous_message_2} - the human doesn't have input this step- collaborate!")

        await self.publish(f"Agent 1 says:")
        self._previous_message_1 = self.agent_1.step()
        await self.publish(self._previous_message_1)
        self.agent_2.input_step(self._previous_message_1)

        if human_message != 'pass':
            self.agent_2.input_step(
                f"The other agent said: {self._previous_message_1}, the human said{human_message} - collaborate!")
        else:
            self.agent_2.input_step(
                f"The other agent said: {self._previous_message_1} - the human doesn't have input this step - collaborate!")

        await self.publish(f"Agent 2 says:")
        self._previous_message_2 = self.agent_2.step()
        await self.publish(self._previous_message_2)
        self.agent_1.input_step(self._previous_message_2)

    def begin(self):

        while True:

            message_1 = self.agent_1.step()
            self.publish(message_1)
            self.agent_2.input_step(message_1)

            message_2 = self.agent_2.step()
            self.publish(message_2)
            self.agent_1.input_step(message_2)

            human_response = self.poll()

            if (human_response == 'QUIT') or (human_response == 'quit') or (human_response == 'q') or (
                    human_response == 'Q'):
                break
            elif human_response == '':
                pass
            else:
                self.agent_1.input_step(human_response)
                self.agent_2.input_step(human_response)


if __name__ == '__main__':
    conversation_engine = ConversationEngine(poll_func,
                                             publish_func,
                                             agents=agent_list,
                                             model_name='gpt-3.5-turbo')

    conversation_engine.step()

    while True:
        human_response = input("Enter your response, or 'QUIT' to cancel:")
        if (human_response == 'QUIT') or (human_response == 'quit') or (human_response == 'q') or (
                human_response == 'Q'):
            break
        conversation_engine.step(human_response)
