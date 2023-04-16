import os
from pathlib import Path

from dotenv import load_dotenv
from langchain import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from openai_pricing_logger import openai_api_listener

load_dotenv()

from rich.console import Console

console = Console()


from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator


class GolemDocumentEditor:
    def __init__(self):
        console.print("Initializing Golem...")

        self._index = self._load_index()
        self._serper_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPER_API_KEY"])
        self._tools = [
            Tool(
                name="Main Document",
                func=self._index.query,
                description="This is the document you are trying to make better. You will work the user to make better versions of this document"
            ),
            Tool(
                name="Current Search",
                func=self._serper_search.run,
                description="useful for when you need to answer questions about current events or the current state of the world."
                            " the input to this should be a single search term or phrase."
            ),
            # Tool(
            #     name="Wikipedia",
            #     func=self._wikipedia_search.run,
            #     description="useful when you what encyclopedic information about a topic."
            # ),
            # Tool(
            #     name="Wolfram Alpha",
            #     func=self._wolfram_alpha.run,
            #     description="useful when you need to answer questions about the world around you."
            # )
        ]
        self._memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self._llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")
        self._chain = initialize_agent(self._tools,
                                       self._llm,
                                       agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True,
                                       memory=self._memory)

    def _load_index(self):
        document_path = Path("../README.md")
        assert document_path.is_file(), "Document path is not a file"

        loader = TextLoader(str(document_path))
        creator = VectorstoreIndexCreator(embedding=HuggingFaceEmbeddings(),
                                          )

        index = creator.from_loaders([loader])
        return index

    def intake_message(self, message: str):
        console.print(f"Received message: {message}")
        with openai_api_listener():
            response = self._chain.run(message)
        return response
