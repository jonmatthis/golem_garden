import asyncio

from golem_garden import Golem


async def main():
    print("Creating Golem...")
    golem = Golem()
    print(golem)
    print("\nPoking Golem...")
    await golem.poke()
    print("\n Golem poked successfully")


if __name__ == '__main__':
    asyncio.run(main())
