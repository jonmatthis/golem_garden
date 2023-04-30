# TODO: Need to get this into an Agent form
# TODO: IO tools, blobs for people, then index and embeddings

import os
from pathlib import Path

from dotenv import load_dotenv

from golem_garden.experimental.jkl.NPCBuilder import NPCBuilderGPT

load_dotenv()

import toml

from typing import Dict, List, Any, Callable

from langchain.chat_models import ChatOpenAI

agent_enpisi_config_path = str(Path(__file__).parent.parent.parent / "jkl" / "agent_definition" / "enpisi.config")

class ConversationEngine:
    def __init__(self,
                 poll_func: Callable[[], int],
                 publish_func: Callable[[int], None],
                 agents: list,
                 model_name  = 'gpt-3.5-turbo'):

        self.agents = agents
        llm = ChatOpenAI(model=model_name, temperature=0.9)

        self.agent_1, self.agent_2 = [agent_from_config_path(path, llm = llm)  for path in agents]

        self.publish = publish_func

        self.poll = poll_func

    def begin(self):

        while True:
            
            message_1 = self.agent_1.step()
            self.publish(message_1)
            self.agent_2.input_step(message_1)

            message_2 = self.agent_2.step()
            self.publish(message_2)
            self.agent_1.input_step(message_2)
               
            human_response = self.poll()
            if (human_response == 'QUIT') or (human_response == 'quit') or (human_response == 'q') or (human_response == 'Q'):
                break
            elif human_response=='':
                pass
            else:
                self.agent_1.input_step(human_response)
                self.agent_2.input_step(human_response)


def agent_from_config_path(config_path, llm):
    path = os.path.dirname(os.path.realpath(__file__)) + config_path
    agent_definition=toml.load(path)

    agent = NPCBuilderGPT.from_llm(llm, verbose=False, agent_config=agent_definition)
    agent.seed_agent()

    return agent

def poll_func():

    user_input = input("Enter your response, or 'QUIT' to cancel:")

    return user_input

def publish_func(msg):
    print(msg)


if __name__ == '__main__':
    conversation_engine = ConversationEngine(poll_func,
                                             publish_func,
                                             agents=[ agent_enpisi_config_path, agent_enpisi_config_path],
                                             model_name='gpt-3.5-turbo')
    conversation_engine.begin()
