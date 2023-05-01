import logging
import os
from pathlib import Path
from typing import Union

import toml
from langchain import PromptTemplate, LLMChain, SerpAPIWrapper
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()


class AgentBuilder:
    def __init__(self,
                 config_file: Union[str, Path]):
        self._config = toml.load(config_file)
        self._name = self._config["prompt"]["input_variables"]["name"]
        self._llm = self._configure_llm()
        self._prompt = self._create_prompt()
        # self._llm_chain = self._make_llm_chain()
        self._memory = self._configure_memory()
        self._llm_chain = LLMChain(llm=self._llm,
                                   prompt=self._prompt,
                                   memory=self._memory,
                                   verbose=True)


    def intake_message(self, message: str):
        logger.info(f"Received message: {message}")
        return self._llm_chain.predict(human_input=message)
    def _configure_llm(self):
        llm_config = self._config["llm"]
        if llm_config["type"] == "ChatOpenAI":
            return ChatOpenAI(temperature=llm_config["temperature"],
                              model_name=llm_config["model_name"])

    def _create_prompt(self):
        prompt_config = self._config["prompt"]
        input_variables = list(prompt_config["input_variables"].keys())
        input_variables.append("chat_history")
        input_variables.append("human_input")
        # input_variables.append("agent_scratchpad")

        prompt_template = PromptTemplate(
            template=prompt_config["template"],
            input_variables=input_variables,
        )
        prompt_formatted = prompt_template.partial(**prompt_config["input_variables"])

        return prompt_formatted

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


if __name__ == "__main__":
    agent = AgentBuilder(config_file="./configuration_tomls/dunkthulu.toml")
    print(agent.intake_message("Hello, tell me about yourself!"))
    print(agent.intake_message("Thats wild, tell me more!"))
    print("Done!")


