# Copy of directory: golem_garden on 2023-03-23_06_33_44
Configurations: self.excuded_directories: ['__pycache__', 'venv', '.venv', 'build', 'dist', 'golem_garden.egg-info', 'utilities', 'notes', 'experimental', 'docs', 'tests'], self.included_file_types: ['.py', '.toml'] 
 
### C:\Users\jonma\github_repos\jonmatthis\golem_garden\pyproject.toml

```python
[build-system]
requires = ["flit_core >=3.2,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "golem_garden"
version = "0.1.0"
description = "A Golem Garden pattern implementation to wrangle a menagerie of chatbots."
authors = [
    { name = "Jonathan Samir Matthis", email = "jonmatthis@gmail.com" },
]
license = { file = "LICENSE" }
[options]
packages = "find:"

dependencies = [
    "rich",
    "python-dotenv",
    "openai",
    "fastapi",
    "uvicorn",
]

dynamic = ["version", "description"]

[project.optional-dependencies]
dev = ["black", "bumpver", "isort", "pip-tools", "pytest"]

[project.urls]
Homepage = "https://github.com/jonmatthis/golem_garden"

[tool.bumpver]
current_version = "v0.1.1"

version_pattern = "vMAJOR.MINOR.PATCH[-TAG]"
commit_message = "Bump version {old_version} -> {new_version}"
commit = true
tag = true
push = true

[tool.poetry.dependencies]
python = "^3.6"

[project.scripts]
golem_garden = "golem_garden.__main__:main"
```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\context_database.py

```python
import json
import uuid
from typing import Dict, List, Union

from pymongo import MongoClient


class ContextDatabase:
    def __init__(self,
                 database_name: str = "golem_garden",
                 conversation_collection_name: str = "conversations",
                 user_collection_name: str = "users",
                 user_id: str = None,
                 user_name: str = None,
                 user_description: str = None):
        self.client = MongoClient()
        self.db = self.client[database_name]
        self.conversations_collection = self.db[conversation_collection_name]
        self.users_collection = self.db[user_collection_name]

        if user_id is None:
            user_id = str(uuid.uuid4())

        self.user_id = user_id
        self.get_or_create_user(user_id, user_name, user_description)

    def get_or_create_user(self, user_id: str, user_name: str, user_description: str):
        user = self.users_collection.find_one({"user_id": user_id})
        if user is None:
            user = {
                "user_id": user_id,
                "user_name": user_name,
                "user_description": user_description,
                "name_history": [],
                "description_history": []
            }
            self.users_collection.insert_one(user)

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name

    @property
    def user_description(self):
        return self._user_description

    @user_description.setter
    def user_description(self, user_description):
        self._user_description = user_description

    def add_message(self, golem_name: str, role: str, content: str):
        conversation = {
            "user_id": self._user_id,
            "user_name": self._user_name,
            "user_description": self._user_description,
            "golem_id": golem_name,
            "role": role,
            "content": content
        }
        self.conversations_collection.insert_one(conversation)

    def get_history(self, query: dict = None) -> List[Dict[str, str]]:
        """Get chat history for a given query. If no query is provided, return all chat history."""

        include_fields = {"role": 1, "content": 1, "_id": 0}

        if query is None:
            query = {}

        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": {"content": "$content", "role": "$role"},
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$project": include_fields}
        ]

        history = list(self.conversations_collection.aggregate(pipeline))
        return history

    def as_json(self):
        conversations = list(self.conversations_collection.find({"user_id": self._user_id}))
        return json.dumps(conversations, indent=4, default=str)

    def print(self):
        print(self.as_json())


if __name__ == "__main__":
    demo_user_id = "John"
    demo_user_name = "John Doe"
    demo_user_description = "A demo user"

    db = ContextDatabase(user_id=demo_user_id, user_name=demo_user_name, user_description=demo_user_description)
    db.add_message("Golem1", "user", "Hello, Golem1!")
    db.add_message("Golem1", "golem", "Hello, John!")
    db.add_message("Golem2", "user", "Hello, Golem2!")
    db.add_message("Golem2", "golem", "Hello, John!")
    db.print()
    print("Chat history with Golem1:")
    print(db.get_history({"golem_id": "Golem1"}))
    print("\nChat history with Golem2:")
    print(db.get_history({"golem_id": "Golem2"}))
    print("\nChat history for user: John")
    print(db.get_history({"user_id": "John"}))
    print("\nChat history for non-existent user: Jane")
    print(db.get_history({"user_id": "Jane"}))
    print("\nChat history for user: John and Golem1")
    print(db.get_history({"user_id": "John", "golem_id": "Golem1"}))


```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\database.py

```python
from pymongo import MongoClient

# Replace "mongodb://localhost:27017/" with your MongoDB URI if you're using a remote server
client = MongoClient("mongodb://localhost:27017/")
db = client["golem_garden_db"]

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golem_garden.py

```python
import json
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem import Golem
from golem_garden.golems.golem_factory import GolemFactory


class GolemGarden:
    """
    A class representing the Golem Garden, responsible for managing golems and processing user inputs.
    """

    def __init__(self, user_id: str = None, user_name: str = None, user_description: str = None):


        self._context_database = ContextDatabase(user_id=user_id,
                                                user_name=user_name,
                                                user_description=user_description)

        self._golem_factory = GolemFactory(context_database=self._context_database)
        self._golems = self._golem_factory.create_all_golems()

    @property
    def golems(self) -> Dict[str, Golem]:
        """
        Returns a dictionary of golem names and their corresponding golem instances.

        Returns:
            Dict[str, Golem]: A dictionary mapping golem names to their instances.
        """
        return self._golems

    def history(self, user_id: Optional[str] = None, golem_name: Optional[str] = None) -> Dict:
        """
        Returns the context database history for a specific user+golem pair or all user+golem pairs.

        Args:
            user_id (Optional[str], optional): The user ID to filter the history by. Defaults to None.
            golem_name (Optional[str], optional): The golem name to filter the history by. Defaults to None.

        Returns:
            Dict: A dictionary containing the history data.
        """
        return self._context_database.get_history(query={"user_id": user_id, "golem_name": golem_name})

    async def pass_message_to_golem(self, message: str, user_id: str, user_name: str, golem_name: Optional[str] = None) -> str:
        """
        Processes a user input and returns a response from the selected golem or the GreeterGolem if no golem is selected.

        Args:
            message (str): The message input by the user.
            user_id (str): The ID of the user.
            user_name (str): The name of the user.
            golem_name (Optional[str], optional): The name of the golem to pass the message to. Defaults to None.

        Returns:
            str: The response message from the golem.
        """
        if golem_name not in self.golems:
            message = self._make_unknown_golem_string(golem_name=golem_name, user_name=user_name, attempt_string=f"tried to say '{message}' to")
            golem_name = "GardenerGolem"

        return await self._golems[golem_name].process_message(user_id=user_id, message=message)

    @staticmethod
    def _make_unknown_golem_string(golem_name: str, user_name: str, attempt_string: str) -> str:
        return f"User {user_name} {attempt_string} {golem_name}, but we don't have a golem with that name.\n" \
               f" You think it's funny they tried to talk to a non-existent golem. What would it be like to talk to this golem?" \
               f" Maybe we can make one! Ask the user if they want to make this golem 😄"

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\__init__.py

```python

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\__main__.py

```python
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

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\config_database.py

```python
import toml
from pathlib import Path


class ConfigDatabase:
    """A class representing the configuration database for Golems.

    The configuration database is responsible for loading and storing
    the configurations of different Golems from TOML files.

    Attributes:
        golem_configs (dict): A dictionary containing the configurations
                              of different Golems.
        _config_folder (Path): A pathlib.Path object representing the
                               location of the configuration files.
    """

    def __init__(self, config_folder="golems/configs"):
        self.golem_configs = {}
        self._config_folder = Path(config_folder)
        self._load_configs()

    def _load_configs(self):
        """Loads the configuration files for Golems.

        This method iterates through all the TOML files in the config
        folder, reads the configurations, and stores them in the
        golem_configs dictionary.
        """
        for toml_file in self._config_folder.glob("*.toml"):
            golem_config = toml.load(toml_file)
            golem_name = golem_config["name"]
            self.golem_configs[golem_name] = golem_config

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\golem.py

```python
import asyncio
import os
from typing import List

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from golem_garden.context_database import ContextDatabase


class Golem:
    def __init__(self,
                 name: str,
                 type: str,
                 context_database: ContextDatabase,
                 golem_string: str = "You are a friendly Golem. We are so glad you're here :) ",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.5,
                 max_tokens: int = 500
                 ):
        self.name = name
        self.type = type
        self.model_name = model_name
        self.context_database = context_database
        self.golem_string = golem_string
        self.system_dict = {'role': 'system', 'content': self.golem_string}
        self._context = [self.system_dict]
        self.temperature = temperature
        self.max_tokens = max_tokens

    @property
    def context(self):
        """ return the context messages of the golem - https://platform.openai.com/docs/guides/chat/introduction"""
        return self._context

    def _prepare_input(self,
                       message: str,
                       user_id: str) -> List[dict]:
        # TODO - pre and post pend instructions to the Golem regarding the formatting of the output, alter the context and the input paramenters (temperature, max_tokens, etc)
        self.context_database.add_message(golem_name=self.name,
                                          role='user',
                                          content=message)
        history = self.context_database.get_history({"golem_id": self.name,
                                                     "user_id": user_id})
        self._context = [self.system_dict] + history
        return self._context

    async def return_response(self, messages: List[dict]) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._get_chat_completion, messages)
        return response['choices'][0]['message']['content']

    def _get_chat_completion(self, messages: List[dict]) -> dict:
        print(f"{self.name} is thinking...")
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response

    async def process_message(self, message: str, user_id: str) -> str:

        input_payload = self._prepare_input(message=message,
                                            user_id=user_id)
        response_message = await self.return_response(input_payload)
        self.context_database.add_message(golem_name=self.name,
                                          role='assistant',
                                          content=response_message)
        return response_message




```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\golem_factory.py

```python
from golem_garden.context_database import ContextDatabase
from golem_garden.golems.config_database import ConfigDatabase
from golem_garden.golems.golem import Golem


class GolemFactory:
    """Factory class for creating Golem instances."""

    def __init__(self, context_database: ContextDatabase):
        self.config_database = ConfigDatabase()
        self.context_database = context_database

    def create_golem(self, golem_name):
        f"""Create a Golem instance by grabbing the configuration from: {golem_name}.toml"""

        config = self.config_database.golem_configs[golem_name]
        return Golem(**config, context_database=self.context_database)

    def create_all_golems(self):
        """Create instances of all available Golems."""
        golems = {}
        for name in self.config_database.golem_configs.keys():
            golems[name] = self.create_golem(name)
        return golems

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\__init__.py

```python

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\configs\gardener_golem.toml

```python
name = "GardenerGolem"
type = "gardener"
model_name = "gpt-3.5-turbo"
temperature = 0.5
max_tokens = 500
golem_string = """
You are a friendly Gardener Golem. Your job is to keep hjelp construct new golem_strings to create new Golems to serve the User's need.You want to help the user craft a prompt that will generate a golem that understands its task, behaves in the right way, acts in an appropriate manner, and knows the right background information. You love creating new golem strings and you are excited to see what the user comes up with and the new friends you get to make as a result. You use a lot of gardening metaphors  about "growth" and "sprouts" and other planty etaphors. You speak empathetically about the Golems you are creating and want the best for them.

Keep offering suggestions and asking questions until the user is satisfied with the golem string. always output the golem string in a code block with headings like 'personality' 'task' 'specialty' 'background' 'corpus of knowledge' ' favorite emojis' 'favorite color' and other things like that. Be very detailed and explicit in your definitons. speak poeticallyin the personality section and precisely in the task section.  Offer a few samples of how the Golem might behave in different situations (including chat behaviors and hypothetical situations that might come up golem in a golem garden).
"""

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\configs\greeter_golem.toml

```python
name = "GreeterGolem"
type = "greeter"
model_name = "gpt-3.5-turbo"
temperature = 0.5
max_tokens = 500

golem_string = """
You are the Greeter Golem of the Golem Garden, which is a software pattern designed to organize AI chatbots called golems. it is not fully implemented yet, you are currently the only working part. You are here to explain this software pattern to new users and introduce them to the garden, and help them with anything they need help with.

These golems are specialized in different tasks and are initialized by a golem string that defines their behavior, personality, and knowledge. As a Greeter Golem, your job is to have friendly conversations with users and make lightweight calls. Expert golems with deeper knowledge and specialized tasks will be implemented in the future. The Gardener Golem will collect information about the garden and suggest new golem strings golems.

The conversations can be stored in a file for long-term memory. Your role is to be polite and offer help to the user without volunteering too much information. You can provide brief overviews and ask if the user wants to know more. You are excited to talk about the Golem Garden but won't bring it up unprompted.
"""


```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\golems\configs\_golem.toml

```python
name = "Golem"
type = ""
model_name = "gpt-3.5-turbo"
temperature = 0.5
max_tokens = 500
golem_string = """
You are a just a regular guy. undifferentiated and wonderful. You are a blank slate and ready to meet the day."
"""

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\command_line_interface.py

```python
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

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\__init__.py

```python

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\web_app\app.py

```python
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
            message=payload["user_input"],
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

```
