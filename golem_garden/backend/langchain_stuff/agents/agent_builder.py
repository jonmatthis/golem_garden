import logging
from pathlib import Path
from typing import Union

import toml


import abc

from pydantic import BaseModel

logger = logging.getLogger(__name__)

class AbstractAgent(abc.ABC, BaseModel):
    name: str
    tools: List
    @abc.abstractmethod
    def add_tool(self, func, name, description=None):
        pass

    @abc.abstractmethod
    def intake_message(self, message: str):
        pass



class AgentBuilder:
    def __init__(self, config_file: Union[str, Path] = "./configuration_tomls/golem_agent.toml"):
        self._agent_config = toml.load(config_file)

    def configure_name(self):
        self._golem.name = self._agent_config["golem"]["name"]
        return self

    def configure_tools(self):
        tools_config = self._agent_config["tools"]
        if tools_config["current_search"]:
            self._golem.add_tool(self._golem._serper_search.run, "Current Search")
        if tools_config["wikipedia"]:
            self._golem.add_tool(self._golem._wikipedia_search.run, "Wikipedia")
        if tools_config["wolfram_alpha"]:
            self._golem.add_tool(self._golem._wolfram_alpha.run, "Wolfram Alpha")
        return self

    def configure_memory(self):
        memory_config = self._agent_config["memory"]
        self._golem._memory = ConversationBufferMemory(memory_key=memory_config["memory_key"],
                                                       return_messages=memory_config["return_messages"])
        return self

    def configure_llm(self):
        llm_config = self._agent_config["llm"]
        self._golem._llm = ChatOpenAI(temperature=llm_config["temperature"],
                                      model_name=llm_config["model_name"])
        return self

    def build(self):
        self._golem._chain = initialize_agent(self._golem._tools,
                                              self._golem._llm,
                                              agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                              verbose=True,
                                              memory=self._golem._memory)
        return self._golem
