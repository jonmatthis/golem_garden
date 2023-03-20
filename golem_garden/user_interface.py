from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from golem_garden.golem_garden import GolemGarden


class UserInterface:
    def __init__(self, golem_garden:GolemGarden):
        self._golem_garden = golem_garden
        self._console = Console()

    async def run(self):

        self._console.rule("[magenta]")
        self._console.rule("[magenta] Welcome to the Golem Garden \U0001F5FF \U0001F331 [/magenta]")


        while True:
            self._console.rule("[green]")
            user_input = Prompt.ask("[bold green] Enter your input [/bold green] (type 'EXIT' to quit, 'SHOW_GOLEMS' to display golems, or 'SHOW_HISTORY' to display history):", console=self._console)
            self._console.rule("[green]")

            if user_input == "EXIT":
                break
            elif user_input == "SHOW_TABLE":
                self.print_golem_table()
            elif user_input == "SHOW_HISTORY":
                self.print_chat_history()
            else:
                # Process the user input and get the bot's response
                with self._console.status("[bold blue] Awaiting Greeter Golem response..."):
                    bot_response = await self._golem_garden.process_input(user_input)

                # Print the bot's response using Rich formatting
                self._console.rule("[blue]")
                self._console.print(f"[bold][cyan]Greeter Golem:[/bold] {bot_response}")
                self._console.rule("[blue]")

    def print_golem_table(self):
        table = Table(title="Golem Garden Status")

        # Define table columns
        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Model", justify="left", style="magenta")
        table.add_column("Golem String", justify="left", style="green")

        # Add golems to the table
        for golem in self._golem_garden.golems.values():
            table.add_row(
                golem.name,
                golem.model,
                golem.golem_string)

        return table

    def print_chat_history(self):
        table = Table(title="Chat History")

        # Define table columns
        table.add_column("Message ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Sent", justify="left", style="magenta")
        table.add_column("Received", justify="left", style="green")

        # Add chat messages to the table
        for message in self._golem_garden.history:
            table.add_row(
                str(message['id']),
                message['sent'],
                message['received']
            )

        return table
