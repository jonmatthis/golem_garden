from textual.app import App
from textual import events
from textual.widgets import Table, ScrollView, Placeholder

from golem_garden.golem_garden import GolemGarden


class GolemGardenUI(App):
    def __init__(self, golem_garden: GolemGarden):
        super().__init__()
        self.golem_garden = golem_garden

    async def on_load(self, event: events.Load) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_ready(self, event: events.Ready) -> None:
        self.status.update("Press 'q' to quit")

        self.golem_status_table = Table(
            "Name", "Model", "Golem String", title="Golem Garden Status"
        )
        self.chat_history_table = Table(
            "Message ID", "Sent", "Received", title="Chat History"
        )

        for golem in self.golem_garden.golems.values():
            self.golem_status_table.add_row(
                golem.name,
                golem.model,
                golem.golem_string,
            )

        self.golem_status_view = ScrollView(self.golem_status_table)
        self.chat_history_view = ScrollView(self.chat_history_table)

        await self.view.dock(self.golem_status_view, edge="left", size=50)
        await self.view.dock(self.chat_history_view, edge="right", size=50)

    async def update_chat_history(self):
        chat_history = self.golem_garden.get_chat_history()

        self.chat_history_table.clear()

        for message in chat_history:
            self.chat_history_table.add_row(
                str(message['id']),
                message['sent'],
                message['received']
            )

    async def process_input(self, user_input: str) -> None:
        response = self.golem_garden.process_input(user_input)
        await self.update_chat_history()
        self.status.update(f"Golem Garden: {response}")


if __name__ == "__main__":
    golem_garden = GolemGarden()
    app = GolemGardenUI(golem_garden)
    app.run()
