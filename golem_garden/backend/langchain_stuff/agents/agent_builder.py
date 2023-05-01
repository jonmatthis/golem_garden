import logging
import os
from pathlib import Path
from typing import Union

import toml
from langchain import PromptTemplate, LLMChain, SerpAPIWrapper
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()


class AgentBuilder:
    def __init__(self,
                 config_file: Union[str, Path]):
        self._config = toml.load(config_file)
        self._name = self._config["name"]
        self._llm = self._configure_llm()
        self._prompt = self._create_prompt()
        self._llm_chain = self._make_llm_chain()
        self._memory = self._configure_memory()
        self._tools = self._configure_tools()
        self._agent_chain = self._make_agent_chain()


    def run(self, message: str):
        logger.info(f"Received message: {message}")
        return self._agent_chain.run(message)

    def _configure_llm(self):
        llm_config = self._config["llm"]
        if llm_config["type"] == "ChatOpenAI":
            return ChatOpenAI(temperature=llm_config["temperature"],
                              model_name=llm_config["model_name"])

    def _create_prompt(self):
        prompt_config = self._config["prompt"]


        # human_message_prompt = HumanMessagePromptTemplate(prompt=prompt)
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompt_config["template"],
                input_variables=list(prompt_config["input_vars"].keys()),
            )
        )
        human_message_prompt_formatted = human_message_prompt.format(**prompt_config["input_vars"])
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt_formatted])


        return chat_prompt_template

    def _configure_memory(self):

        memory_config = self._config["memory"]
        logger.info(f"Configuring memory of type {memory_config}")

        if memory_config["type"] == "ConversationBufferMemory":
            memory = ConversationBufferMemory(memory_key=memory_config["memory_key"],
                                              return_messages=memory_config["return_messages"])
        elif memory_config["type"] == "ConversationBufferWindowMemory":
            memory = ConversationBufferWindowMemory(memory_key=memory_config["memory_key"],
                                                    return_messages=memory_config["return_messages"])
        elif memory_config["type"] == "ConversationSummaryMemory":
            memory = ConversationSummaryMemory(memory_key=memory_config["memory_key"],
                                               return_messages=memory_config["return_messages"])
        else:
            raise NotImplementedError(f"Memory type {memory_config['type']} not implemented... YET!")

        return memory

    def _make_llm_chain(self):
        llm_chain = LLMChain(llm=self._llm, prompt=self._prompt, verbose=True)

        return llm_chain

    def _configure_tools(self):
        self._serper_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPER_API_KEY"])
        tools_config = self._config["tools"]
        tools = [
            Tool(
                name="Current Search",
                func=self._serper_search.run,
                description="useful for when you need to answer questions about current events or the current state of the world"
            ),
        ]
        return tools

    # def _make_agent(self):
    #     agent_chain = initialize_agent(tools=self._tools,
    #                                    llm= self.llm,
    #                                    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    #                                    verbose=True,
    #                                    memory= self._memory)
    def _make_agent_chain(self):

        agent_chain = initialize_agent(tools=self._tools,
                                       llm=self._llm,
                                       agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                       memory=self._memory,
                                       verbose=True, )
        return agent_chain




if __name__ == "__main__":
    agent = AgentBuilder(config_file="./configuration_tomls/dunkthulu.toml")
    print(agent.run("Hello, Tell me about youreself!"))
    f = 9
