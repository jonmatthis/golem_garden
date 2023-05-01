import logging
from pathlib import Path
from typing import Union

import toml
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

logger = logging.getLogger(__name__)



class AgentBuilder:
    def __init__(self,
                 config_file: Union[str, Path]):
        self._config = toml.load(config_file)
        self._name = self._config["name"]
        self._llm = self._configure_llm()
        self._prompt = self._create_prompt()

    def _configure_llm(self):
        llm_config = self._config["llm"]
        if llm_config["type"] == "ChatOpenAI":
            return ChatOpenAI(temperature=llm_config["temperature"],
                              model_name=llm_config["model_name"])

    def _create_prompt(self):
        prompt_config = self._config["prompt"]
        return PromptTemplate(
            template=prompt_config["template"],
            input_variables=["input_language", "output_language"],
        )

    # def configure_memory(self):
    #     memory_config = self._config["memory"]
    #     self._golem._memory = ConversationBufferMemory(memory_key=memory_config["memory_key"],
    #                                                    return_messages=memory_config["return_messages"])
    #     return self
    #
    #
    # def build(self):
    #     self._golem._chain = initialize_agent(self._golem._tools,
    #                                           self._golem._llm,
    #                                           agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    #                                           verbose=True,
    #                                           memory=self._golem._memory)
    #     return self._golem


if __name__ == "__main__":
    builder = AgentBuilder(config_file="./configuration_tomls/dunkthulu.toml")
