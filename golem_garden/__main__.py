import asyncio
import sys
from pathlib import Path

try:
    from golem_garden.golems.golem_garden import GolemGarden
except ModuleNotFoundError:
    base_package_path = Path(__file__).parent.parent
    print(f"adding base_package_path: {base_package_path} : to sys.path")
    sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path
    from golem_garden.golems.golem_garden import GolemGarden




from golem_garden.golems.golem_garden import GolemGarden
from golem_garden.user_interface import UserInterface

def main():
    golem_garden = GolemGarden()
    user_interface = UserInterface(golem_garden)
    asyncio.run(user_interface.run())

if __name__ == '__main__':
    print("Starting Golem Garden...")
    main()
    print("Thanks for visiting the Golem Garden \U0001F331 \U00002728")
