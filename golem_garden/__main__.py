
from pathlib import Path
import sys

base_package_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path

from rich.console import Console

rich_console = Console()

from golem_garden import Golem



class GolemGarden:
    def __init__(self):

        self._golem = Golem()

        # self._golem = GolemDocumentEditor()
    def run(self):
        rich_console.print(f"[bold cyan] {self._golem.intake_message('A human is here and said Hello')}")

        while True:
            message = input("Enter message (or `quit`): ")
            if message == "quit":
                break
            rich_console.print(self._golem.intake_message(message))




def main():
    rich_console.rule("Welcome to Golem Garden 🌱", style="bold green")
    golem_garden = GolemGarden()
    golem_garden.run()


if __name__ == "__main__":
    main()
