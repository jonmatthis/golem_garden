import asyncio
import uuid

from golem_garden.golems.golem import Golem


def chat_with_golem(session_id: str = str(uuid.uuid4())):
    """A simple CLI chat interface for interacting with the Golem object."""

    golem = Golem(user_id="UnknownUser", session_id=session_id)

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Exiting chat...")
                break

            response = asyncio.run(golem.chat(user_input))

            print(f"{golem.name}: {response}")

        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

if __name__ == "__main__":
    chat_with_golem()
