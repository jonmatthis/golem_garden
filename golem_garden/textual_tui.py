from textual.app import App
from textual.widgets import Header, Footer, TextLog
from textual import events

class ChatBot(App):
    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        self.text_log = await self.view.dock(TextLog(), edge="left", size=80)

    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.text_log.write("You: " + self.text_log.get_input())
            self.text_log.clear_input()
            # Implement your chatbot logic here and send the chatbot's response
            chatbot_response = "Chatbot: This is a sample response."
            self.text_log.write(chatbot_response)

    def on_resize(self, event: events.Resize) -> None:
        self.console.clear()

if __name__ == "__main__":
    app = ChatBot()
    app.run()
