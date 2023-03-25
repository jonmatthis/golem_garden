import asyncio

import click

from golem_garden.golems.golem import Golem


@click.command()
@click.option('--user_id', default='UnknownUser', help='The user ID for this session.')
def chat_with_golem(user_id):
    """A simple CLI chat interface for interacting with the Golem object."""

    print("Creating Golem...")
    golem = Golem(user_id=user_id)

    asyncio.run(golem.poke())

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["quit", "exit"]:
                print("Exiting chat...")
                break
            elif user_input.lower() in ["poke"]:
                print("Poking Golem...")
                asyncio.run(golem.poke())
                print("Golem poked successfully")
                continue
            elif user_input.lower() in ["golem"]:
                print(golem)
                continue

            response = asyncio.run(golem.chat(user_input))
            print(f"{golem.name}: {response}")

        except KeyboardInterrupt:
            print("\nExiting chat...")
            break

if __name__ == "__main__":
    chat_with_golem()