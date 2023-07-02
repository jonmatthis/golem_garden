import asyncio
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.base import LLM
from langchain.schema import Document
from langchain.vectorstores import Chroma
from pydantic import BaseModel, root_validator

from golem_garden.backend.ai.chatbot.chatbot_prompts import CHATBOT_SYSTEM_PROMPT_TEMPLATE
from golem_garden.backend.mongo_database.mongo_database_manager import MongoDatabaseManager

load_dotenv()
from langchain import LLMChain, OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory, VectorStoreRetrieverMemory, CombinedMemory
from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate, SystemMessagePromptTemplate,
)


class Chatbot(BaseModel):
    llm: ChatOpenAI = ChatOpenAI(
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
            temperature=0.8,
            model_name="gpt-4")
    prompt: Any = None
    memory: Any = None
    chain: Any = None

    async def create_chatbot(self):
        if self.prompt is None:
            self.prompt = self._create_prompt(prompt_template=CHATBOT_SYSTEM_PROMPT_TEMPLATE)
        if self.memory is None:
            self.memory = await self._configure_memory()
        if self.chain is None:
            self.chain = self._create_llm_chain()
        return self

    async def _configure_memory(self):
        conversation_memory = self._configure_conversation_memory()
        vectorstore_memory = await self._configure_vectorstore_memory()
        combined_memory = CombinedMemory(memories=[conversation_memory,
                                                   vectorstore_memory])
        return combined_memory

    async def _configure_vectorstore_memory(self, ):
        chroma_vector_store = await self._create_vector_store()

        retriever = chroma_vector_store.as_retriever(search_kwargs=dict(k=3))

        return VectorStoreRetrieverMemory(retriever=retriever,
                                          memory_key="vectorstore_memory",
                                          input_key="human_input",)


    @staticmethod
    def _configure_conversation_memory():
        return ConversationSummaryBufferMemory(memory_key="chat_memory",
                                               input_key="human_input",
                                               llm=OpenAI(temperature=0),
                                               max_token_limit=1000)

    def _create_llm_chain(self):
        return LLMChain(llm=self.llm,
                        prompt=self.prompt,
                        memory=self.memory,
                        verbose=True,
                        )

    def _create_prompt(self, prompt_template: str):
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            prompt_template
        )

        human_template = "{human_input}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template
        )

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        return chat_prompt

    async def async_process_input(self, input_text):
        print(f"Input: {input_text}")
        print("Streaming response...\n")
        ai_response = await self.chain.arun(human_input=input_text)
        return ai_response


    async def load_memory_from_thread(self, thread, bot_name: str):
        async for message in thread.history(limit=None, oldest_first=True):
            if message.content == "":
                continue
            if str(message.author) == bot_name:
                self._memory.chat_memory.add_ai_message(message.content)
            else:
                self._memory.chat_memory.add_user_message(message.content)

    async def _create_vector_store(self, collection_name:str="test_collection"):
        chroma_vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(),
            collection_name=collection_name,
            persist_directory=str(Path(os.getenv("PATH_TO_CHROMA_PERSISTENCE_FOLDER")) / collection_name),
        )
        return chroma_vector_store


    async def demo(self):
        print("Welcome to the Neural Control Assistant demo!")
        print("Type 'exit' to end the demo.\n")

        while True:
            input_text = input("Enter your input: ")

            if input_text.strip().lower() == "exit":
                print("Ending the demo. Goodbye!")
                break

            response = await self.async_process_input(input_text)

            print("\n")

if __name__ == "__main__":
    async def main():
        chatbot = await Chatbot().create_chatbot()
        await chatbot.demo()


    asyncio.run(main())
