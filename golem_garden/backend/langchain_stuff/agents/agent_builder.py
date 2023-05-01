import logging
from pathlib import Path
from typing import Union, List

import toml


import abc

from langchain.agents import Tool
from langchain.llms.base import LLM
from langchain.schema import Memory
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# class AbstractAgent(abc.ABC, BaseModel):
#     name: str = None
#     prompt: str = None
#     llm: LLM = None
#     memory: Memory = None
#     tools: List[Tool] = []
#
#     @abc.abstractmethod
#     def make_prompt(self):
#         pass
#     @abc.abstractmethod
#     def make_llm(self):
#         pass
#
#     @abc.abstractmethod
#     def make_memory(self):
#         pass
#
#     @abc.abstractmethod
#     def add_tool(self, func, name, description=None):
#         pass
#
#     @abc.abstractmethod
#     def intake_message(self, message: str):
#         pass
#



class AgentBuilder:
    def __init__(self,
                 config_file: Union[str, Path] = "./configuration_tomls/dunkthulu.toml"):
        self._config = toml.load(config_file)
        self._name = self._config["name"]
        self._llm = self._configure
        self._prompt = self._create_prompt()

    def configure_llm(self):
        llm_config = self._config["llm"]
        self._golem._llm = ChatOpenAI(temperature=llm_config["temperature"],
                                      model_name=llm_config["model_name"])
        return self

    def configure_memory(self):
        memory_config = self._config["memory"]
        self._golem._memory = ConversationBufferMemory(memory_key=memory_config["memory_key"],
                                                       return_messages=memory_config["return_messages"])
        return self


    def build(self):
        self._golem._chain = initialize_agent(self._golem._tools,
                                              self._golem._llm,
                                              agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                              verbose=True,
                                              memory=self._golem._memory)
        return self._golem
