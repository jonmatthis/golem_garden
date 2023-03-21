import json
import uuid
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.tree import Tree

from golem_garden.golems.golem_garden import GolemGarden
from golem_garden.system.get_formatted_timestamp import get_formatted_timestamp


class UserInterface:
    OPTIONS = ["EXIT", "SHOW_GOLEMS", "SELECT_GOLEM", "SHOW_HISTORY"]

    def __init__(self, golem_garden: GolemGarden):
        self._golem_garden = golem_garden
        self._console = Console()
        self._selected_golem = None

    async def run(self):
        self._display_welcome_message()
        self._session_timestamp = get_formatted_timestamp()
        await self._welcome_user()

        while True:
            self._console.rule("[green]\U0001F331")
            user_input = Prompt.ask("[bold green] Enter your input [/bold green]:", console=self._console)

            if user_input == "EXIT":
                break
            elif user_input == "SHOW_GOLEMS":
                self._print_golem_table()
            elif user_input == "SELECT_GOLEM":
                self._selected_golem = self._select_golem()
            elif user_input == "SHOW_HISTORY":
                self._print_chat_history()
            else:
                await self._send_message_to_garden(user_input)

    def _display_welcome_message(self):
        self._console.rule("[magenta] \U0001F331 [/magenta]")
        self._console.rule("[magenta] Welcome to the Golem Garden! [/magenta]")
        self._console.rule("[magenta] We are so glad you're here [/magenta]")
        self._console.rule("[magenta] \U0001F331 [/magenta]")
        self._console.print(
            f"Type any of the following options: {', '.join(self.OPTIONS)}", soft_wrap=True)

    async def _send_message_to_garden(self, user_input):
        golem_response = await self._golem_garden.process_input(user_input, self._selected_golem)
        self._console.rule("[blue]\U0001F331")
        golem_name = self._selected_golem if self._selected_golem else "Greeter Golem"
        self._console.print(f"[bold][cyan]{golem_name}:[/bold] {golem_response}")

    def _print_golem_table(self):
        tree = Tree("Golem Garden", style="bold blue")
        for name, golem in self._golem_garden.golems.items():
            tree.add(f"{name}").add(f"Golem Type: ({golem.type})").add(f"Golem Description: ({golem.golem_string})")
        self._console.print(tree)

    def _print_chat_history(self):
        self._console.rule("[blue]\U0001F331")
        self._console.print("[bold blue] Context History [/bold blue]")
        self._console.print_json(self._golem_garden.history())

    def _get_user_id(self):
        user_id_path = "user_id.json"
        user_id_full_path = Path(user_id_path).resolve()
        if user_id_full_path.exists():
            with open(str(user_id_full_path), 'r') as f:
                user_dict = json.load(f)
        else:
            user_dict = self._create_new_user(user_id_full_path)

        self._user_id = user_dict["user_id"]
        self._user_name = user_dict["user_name"]
        self._user_description = user_dict["user_description"]

    def _create_new_user(self, user_id_full_path):
        user_dict = {}
        user_dict["user_name"] = Prompt.ask(f"I don't believe we've met before! What should I call you?")
        user_dict["user_id"] = str(uuid.uuid4())
        self._console.print(
            f"Nice to meet you, {user_dict['user_name']}! I will remember you with the ID: {user_dict['user_id']} in a file at: {user_id_full_path}")
        user_dict["user_description"] = Prompt.ask(f"Tell me a little about yourself, if you like!:",
                                                   default="a nice person")
        with open(str(user_id_full_path), 'w') as f:
            json.dump(user_dict, f)
        return user_dict

    def _select_golem(self):
        golem_names = list(self._golem_garden.golems.keys())
        selected_golem = Prompt.ask("Select a golem to talk to:", choices=golem_names)
        return selected_golem

    async def _welcome_user(self):
        self._get_user_id()

        self._new_user = self._golem_garden.set_user_id(self._user_id)

        welcome_prompt = f"A human user that calls themselvses '{self._user_name}' just approached the Golem Garden Gate. They describe themselves as {self._user_description}. You are excited to see them! Greet them kindly and ask how you may help. "

        await self._send_message_to_garden(welcome_prompt)
