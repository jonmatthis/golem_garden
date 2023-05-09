import logging
import sys
from pathlib import Path
from typing import Union

import asyncio
import toml
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory

logger = logging.getLogger(__name__)

from dotenv import load_dotenv

load_dotenv()


class AgentBuilder:
    def __init__(self,
                 configuration: dict = None,
                 config_path: Union[str, Path] = None,
                 model: str = None):
        if configuration is None:
            try:
                self._configuration = toml.load(config_path)
            except Exception as e:
                logger.error(f"Could not load config TOML file at path: {config_path}")
                raise e
        else:
            self._configuration = configuration

        if model is not None:
            self._configuration["llm"]["model"] = model

        self._name = self._configuration["prompt"]["input_variables"]["name"]
        self._llm = self._configure_llm(**self._configuration["llm"])
        self._prompt = self._create_prompt()
        self._memory = self._configure_memory()

        self._llm_chain = LLMChain(llm=self._llm,
                                   prompt=self._prompt,
                                   memory=self._memory,
                                   verbose=True)

    def intake_message(self, message: str):
        logger.info(f"Received message: {message}")
        return self._llm_chain.predict(human_input=message)

    async def aintake_message(self, message: str):
        logger.info(f"Received message: {message}")
        return await self._llm_chain.apredict(human_input=message)

    def _configure_llm(self,
                       type: str = "ChatOpenAI",
                       **kwargs):
        if type == "ChatOpenAI":
            return ChatOpenAI(**kwargs)

    def _create_prompt(self):
        prompt_config = self._configuration["prompt"]
        input_variables = list(prompt_config["input_variables"].keys())

        # TODO - switch to `chat_model_template` or whatever so we don't need to do this
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

        memory_config = self._configuration["memory"]
        logger.info(f"Configuring memory of type {memory_config}")

        if memory_config["type"] == "ConversationBufferMemory":
            memory = ConversationBufferMemory(memory_key=memory_config["memory_key"],
                                              return_messages=memory_config["return_messages"])

        elif memory_config["type"] == "ConversationBufferWindowMemory":
            memory = ConversationBufferWindowMemory(memory_key=memory_config["memory_key"],
                                                    return_messages=memory_config["return_messages"])

        elif memory_config["type"] == "ConversationSummaryMemory":
            memory = ConversationSummaryMemory(llm=self._configure_llm(model="gpt-3.5-turbo", temperature=0),
                                               memory_key=memory_config["memory_key"],
                                               return_messages=memory_config["return_messages"])
        else:
            raise NotImplementedError(f"Memory type {memory_config['type']} not implemented... YET!")

        return memory


async def ademo_main():
    agent = AgentBuilder(config_path="./configuration_tomls/dunkthulu.toml")
    human_message_1 = "Hello, I am a human. I am here to talk to you about the weather."
    print(f"\n--Human says: {human_message_1}")
    print(await agent.aintake_message(human_message_1))
    human_message_2 = "Thats wild, tell me more!"
    print(f"\n--Human says: {human_message_2}")
    print(await agent.aintake_message(human_message_2))
    print("\n--Done!")


if __name__ == "__main__":
    # Set the event loop policy to WindowsSelectorEventLoopPolicy on Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(ademo_main())
