# web_app/app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from golem_garden.golem_garden import GolemGarden

templates = Jinja2Templates(directory="templates")


class WebApp:
    """
    The WebApp class provides the functionality of the Golem Garden web application.
    """

    def __init__(self, golem_garden: GolemGarden):
        """
        Initializes a WebApp instance with a GolemGarden object.

        Args:
            golem_garden (GolemGarden): The GolemGarden instance used to manage golems.
        """
        self.golem_garden = golem_garden
        self.app = FastAPI()
        self.app.get("/")(self.index)
        self.app.post("/chat")(self.chat)

    async def index(self, request: Request):
        """
        Handles the root route and renders the index page.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            TemplateResponse: The index.html template with the request context.
        """
        return templates.TemplateResponse("index.html", {"request": request})

    async def chat(self,payload: dict):
        golem_response = await self.golem_garden.pass_message_to_golem(
            message=payload["message"],
            user_id=self.golem_garden.user_id,
            user_name=payload["user_name"],
            golem_name="GreeterGolem",
        )
        return JSONResponse(content={"golem_response": golem_response})


def get_web_app(golem_garden: GolemGarden) -> FastAPI:
    return WebApp(golem_garden).app

if __name__ == "__main__":
    from golem_garden.golem_garden import GolemGarden
    golem_garden = GolemGarden()
    app = get_web_app(golem_garden)
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
