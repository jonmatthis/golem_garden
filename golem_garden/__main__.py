
import os

from dotenv import load_dotenv

load_dotenv()
# os.environ["LANGCHAIN_HANDLER"] = "langchain"

from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType



from rich.console import Console
console = Console()

class Golem:
    def __init__(self):

        console.print("Initializing Golem...")
        self._serper_search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPER_API_KEY"])
        self._tools = [
            Tool(
                name="Current Search",
                func=self._serper_search.run,
                description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
            ),
        ]
        self._memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self._llm = ChatOpenAI(temperature=0)
        self._chain = initialize_agent(self._tools,
                                       self._llm,
                                       agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True,
                                       memory=self._memory)

    def intake_message(self, message:str):
        console.print(f"Received message: {message}")
        response =  self._chain.run(message)
        return response


class GolemGarden:
    def __init__(self):

        self._golem = Golem()

    def run(self):
        console.print(f"[bold cyan] {self._golem.intake_message('A human is here and said Hello')}")

        while True:
            message = input("Enter message (or `quit`): ")
            if message == "quit":
                break
            console.print(self._golem.intake_message(message))

def main():
    console.rule("Welcome to Golem Garden 🌱", style="bold green")
    golem_garden = GolemGarden()
    golem_garden.run()


if __name__ == "__main__":
    main()
