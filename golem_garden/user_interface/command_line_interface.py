import time

from rich.console import Console
from rich.prompt import Prompt
from rich.tree import Tree

from golem_garden.golem_garden import GolemGarden


class CommandLineInterface:
    OPTIONS = ["EXIT",
               "OPTIONS",
               "SHOW_GOLEMS",
               "SELECT_GOLEM",
               "SHOW_ALL_HISTORY",
               "SHOW_USER_HISTORY",
               "SHOW_GOLEM_HISTORY",
               "SHOW_USER_GOLEM_HISTORY",
               "POKE"
               ]

    def __init__(self, golem_garden: GolemGarden):
        self._golem_garden = golem_garden
        self._console = Console()
        self._selected_golem = 'GreeterGolem'

    async def run(self):
        self._display_welcome_message()
        self._session_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self._print_golem_message(await self._golem_garden.welcome_user())

        while True:
            self._console.rule("[green]\U0001F331")
            user_input = Prompt.ask("[bold green] Enter your input (or OPTIONS)[/bold green]:", console=self._console)

            if user_input == "EXIT":
                break
            elif user_input == "OPTIONS":
                self._console.print(f"Type any of the following options: {', '.join(self.OPTIONS)}")
            elif user_input == "SHOW_GOLEMS":
                self._print_golem_table()
            elif user_input == "SELECT_GOLEM":
                self._selected_golem = self._golem_garden.select_golem()
                await self._poke_golem(golem=self._selected_golem, waking_up=True)
            elif user_input == "POKE":
                self._console.print(f"You poke {self._selected_golem}")
                await self._poke_golem(self._selected_golem)
            elif user_input == "SHOW_ALL_HISTORY":
                self._print_chat_history()
            elif user_input == "SHOW_USER_HISTORY":
                self._print_chat_history(user=self._golem_garden.get_user_id())
            elif user_input == "SHOW_GOLEM_HISTORY":
                self._print_chat_history(user=None, golem=self._selected_golem)
            elif user_input == "SHOW_USER_GOLEM_HISTORY":
                self._print_chat_history(user=self._golem_garden.get_user_id(), golem=self._selected_golem)
            else:
                await self._send_message_to_garden(user_input)

    def _display_welcome_message(self):
        self._console.rule("[magenta] \U0001F331 [/magenta]")
        self._console.rule("[magenta] Welcome to the Golem Garden! [/magenta]")
        self._console.rule("[magenta] \U0001F331 [/magenta]")
        self._console.print(
            f"Type any of the following options: {', '.join(self.OPTIONS)}", soft_wrap=True)

    async def _send_message_to_garden(self, message: str):
        self._print_golem_message(await self._golem_garden.pass_message_to_golem(message=message,
                                                                                 golem_name=self._selected_golem))

    def _print_golem_message(self, golem_response: str):
        self._console.rule("[blue]\U0001F331")
        self._console.print(f"[bold cyan]{self._selected_golem}:[/bold cyan] {golem_response}")

    def _print_golem_table(self):
        tree = Tree("Golem Garden", style="bold blue")
        for name, golem in self._golem_garden.golems.items():
            tree.add(f"{name}").add(f"Golem Type: ({golem.type})").add(f"Golem Description: ({golem.golem_string})")
        self._console.print(tree)

    def _print_chat_history(self, user=None, golem=None):
        self._console.rule("[blue]\U0001F331")
        self._console.print("[bold blue] Context History [/bold blue]")
        self._console.print_json(self._golem_garden.history(user_id=user, golem_name=golem))

    async def _poke_golem(self, golem: str, waking_up: bool = False):
        self._print_golem_message(await self._golem_garden.poke_golem(golem, waking_up=waking_up))
