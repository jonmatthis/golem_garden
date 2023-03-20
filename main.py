import asyncio

from golem_garden.golem_garden import GolemGarden
from golem_garden.user_interface import UserInterface

golem_garden = GolemGarden()
user_interface = UserInterface(golem_garden)
asyncio.run(user_interface.run())
