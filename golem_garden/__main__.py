# golem_garden/golem_garden/__main__.py
import asyncio
import sys
from pathlib import Path
from typing import Optional

from golem_garden.user_interface.command_line_interface import CommandLineInterface
from golem_garden.user_interface.web_app.app import get_web_app

try:
    from golem_garden.golem_garden import GolemGarden
except ModuleNotFoundError:
    base_package_path = Path(__file__).parent.parent
    print(f"adding base_package_path: {base_package_path} : to sys.path")
    sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path
    from golem_garden.golem_garden import GolemGarden



def main(interface: Optional[str] = None):
    if interface == "cli":
        golem_garden = GolemGarden()
        user_interface = CommandLineInterface(golem_garden)
        asyncio.run(user_interface.run())
    else:
        print("Starting Golem Garden Web App...")
        import uvicorn
        golem_garden = GolemGarden()
        app = get_web_app(golem_garden)
        uvicorn.run(app, host="localhost", port=8000)
        print("Thanks for visiting the Golem Garden Web App \U0001F331 \U00002728")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "cli":
            main(interface="cli")
    else:
        main()
