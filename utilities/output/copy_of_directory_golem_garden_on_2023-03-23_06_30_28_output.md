# Copy of directory: golem_garden on 2023-03-23_06_30_28
Configurations: self.excuded_directories: ['__pycache__', 'venv', '.venv', 'build', 'dist', 'golem_garden.egg-info', 'utilities', 'notes', 'experimental', 'docs'], self.included_file_types: ['.py', '.txt', '.md', '.html', '.css', '.js', '.json', '.yaml', '.yml'] 
 
### C:\Users\jonma\github_repos\jonmatthis\golem_garden\mkdocs.yml

```python
site_name: Golem Garden 🌱
theme:
  name: material

plugins:
  - search
  - mkdocstrings:
      default_handler: python

nav:
  - Home: index.md
  - User Guide:
    - Installation: user_guide/installation.md
    - Usage: user_guide/usage.md
  - API Reference: api_reference.md
  - Development:
    - Contributing: development/contributing.md
    - Style Guide: development/style_guide.md

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\README.md

```python
# Golem Garden 🌱

Golem Garden is a Python project that manages a collection of GPT-enabled chatbots called "Golems" and a swarm of simple Python scripts enacting "Beetles". The primary purpose of this project is to facilitate user interaction with various golems, providing a seamless experience in obtaining responses from different specialized chatbots.

## Features

- Manage multiple GPT-enabled chatbots called Golems
- Process user inputs and obtain responses from the appropriate Golem
- Store conversation history and user-specific data
- Configuration management using TOML files
- Comprehensive API documentation generated from source code

## Components

- GolemGarden class: Manages golems and processes user inputs
- Golem class: Base class for Golem instances
- GolemFactory class: Factory class for creating Golem instances
- ConfigDatabase class: Handles loading and storing Golem configurations from TOML files
- ContextDatabase class: Manages conversation history and user-specific data
- User Interface: Enables users to interact with the golems

# Installation

To install the golem_garden package using Poetry, follow these steps:

1. [Install Poetry](https://python-poetry.org/docs/#installation) if you haven't already.

2. Clone the `golem_garden` repository:

```bash
   git clone https://github.com/jonmatthis/golem_garden.git
   cd golem_garden
```
3. Install the project dependencies and create a virtual environment:
```bash
  poetry install
```
4. Activate the virtual environment:
```bash 
poetry shell
```


```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\requirements.txt

```python
rich
python-dotenv
openai
fastapi
uvicorn
```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\.github\workflows\deploy_docs.yml

```python
name: ci
on:
  push:
    branches:
      - main
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - uses: actions/cache@v2
        with:
          key: ${{ github.ref }}
          path: .cache
      - run: pip install mkdocs-material
      - run: pip install mkdocstrings[python]
      - run: mkdocs gh-deploy --force

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\.github\workflows\publish_to_pypi_when_new_tag_is_pushed_to_main.yml

```python
# This workflow will upload a Python Package using Twine when a release is created
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries

# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.

name: Upload Python Package

on:
  push:
    tags: [ v* ]

permissions:
  contents: read

jobs:
  deploy:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flit
    - name: Build package
      run: python -m flit build
    - name: Publish package to pypi
      uses: pypa/gh-action-pypi-publish@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        user: __token__
        password: ${{ secrets.PYPI_API_TOKEN }}

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


# import json
# import uuid
# from pathlib import Path
# from typing import Dict, Optional
#
# from rich.prompt import Prompt
#
# from golem_garden.context_database import ContextDatabase
# from golem_garden.golems.golem import Golem
# from golem_garden.golems.golem_factory import GolemFactory
#
# TRIED_TO_POKE_GOLEM_THAT_DIDNT_EXIST = "This user tried to poke a golem named {golem_name}, but we don't have a golem with that name. You think it's funny they tried to poke a non-existend golem. What would it be like to poke this golem? Maybe we can make one? 😄"
#
#
# def create_poke_prompt(user_name:str, waking_up:bool = False):
#     if waking_up:
#         return f"You wake up to find a human named {user_name} poking you! You wake up in a way that reflects your personality. " \
#                f"Introduce yourself to them and say a little bit about yourself :D"
#
#     return  f"The human named {user_name} you are talking to just poked you! Wow, that's wild!!"\
#             f" Say the equivalent of 'Hello World' in the language of Golems - it should be brimming with your own distinct personality! " \
#            f"Make it yours! Be creative!"
#
#
# class GolemGarden:
#     """
#     A class representing the Golem Garden, responsible for managing golems and processing user inputs.
#     """
#
#     def __init__(self, context_database: ContextDatabase = ContextDatabase()):
#         """
#         Initialize the Golem Garden with a context database and create all golems.
#         """
#         self._context_database = context_database
#         self._golem_factory = GolemFactory(context_database=self._context_database)
#         self._golems = self._golem_factory.create_all_golems()
#
#     @property
#     def golems(self) -> Dict[str, Golem]:
#         """
#         Returns a dictionary of golem names and their corresponding golem instances.
#         """
#         return self._golems
#
#     @property
#     def greeter(self) -> Golem:
#         """
#         Returns the GreeterGolem instance.
#         """
#         return self._golems["GreeterGolem"]
#
#     @property
#     def gardener(self) -> Golem:
#         """
#         Returns the GardenerGolem instance.
#         """
#         return self._golems["GardenerGolem"]
#
#     def history(self, user_id: Optional[str] = None, golem_name: Optional[str] = None):
#         """
#         Returns the context database history for a specific user+golem pair or all user+golem pairs.
#         """
#         return self._context_database.get_history(query={user_id: user_id, golem_name: golem_name})
#
#     async def pass_message_to_golem(self, message: str, golem_name: Optional[str] = None) -> str:
#         """
#         Processes a user input and returns a response from the selected golem or the GreeterGolem if no golem is selected.
#         """
#
#         if not golem_name in self.golems:
#             message = self._make_unknown_golem_string(golem_name=golem_name,
#                                                       attempt_string=f"tried to say '{message}' to")
#             golem_name = "GardenerGolem"
#
#         return await self._golems[golem_name].process_message(user_id=self._user_id,
#                                                               message=message)
#
#     def _make_unknown_golem_string(self, golem_name: str, attempt_string: str):
#         return f"User {attempt_string} {golem_name}, but we don't have a golem with that name.\n" \
#                f" You think it's funny they tried to talk to a non-existend golem. What would it be like to talk to this golem?" \
#                f" Maybe we can make one! Ask the user if they want to make this golem 😄",
#
#     async def poke_golem(self, golem_name: str, waking_up:bool=False) -> str:
#         """
#         Returns a response from the specified golem.
#         """
#         return await self._golems[golem_name].process_message(user_id=self._user_id,
#                                                               message = create_poke_prompt(user_name=self._user_name,
#                                                                                            waking_up=waking_up))
#
#     def set_user_id(self, user_id: str) -> None:
#         """
#         Sets the user_id for the context database.
#         """
#         self._context_database.user_id = user_id
#
#     def get_user_id(self):
#         user_id_path = "user_id.json"
#         user_id_full_path = Path(user_id_path).resolve()
#         if user_id_full_path.exists():
#             with open(str(user_id_full_path), 'r') as f:
#                 user_dict = json.load(f)
#         else:
#             user_dict = self.create_new_user(user_id_full_path)
#
#         self._user_id = user_dict["user_id"]
#         self._user_name = user_dict["user_name"]
#         self._user_description = user_dict["user_description"]
#
#     def create_new_user(self, user_id_full_path):
#         user_dict = {}
#         user_dict["user_name"] = Prompt.ask(f"I don't believe we've met before! What should I call you?")
#         user_dict["user_id"] = str(uuid.uuid4())
#         print(
#             f"Nice to meet you, {user_dict['user_name']}! I will remember you with the ID: {user_dict['user_id']} in a file at: {user_id_full_path}")
#         user_dict["user_description"] = Prompt.ask(f"Tell me a little about yourself, if you like!:",
#                                                    default="a nice person")
#         with open(str(user_id_full_path), 'w') as f:
#             json.dump(user_dict, f)
#         return user_dict
#
#     async def welcome_user(self):
#         self.get_user_id()
#         return await self.pass_message_to_golem(message=self.create_welcome_prompt(), golem_name="GreeterGolem", )
#
#     def create_welcome_prompt(self):
#         return f"A human user that calls themselves '{self._user_name}' " \
#                f"just approached the Golem Garden Gate. They describe themselves as {self._user_description}, " \
#                f"which you think is interesting. You are excited to see them! Try to briefly mention something from a previous conversation, if you can. " \
#                f"Greet them kindly and ask how you may help :D "
#
#     def select_golem(self, golem_name: Optional[str] = None) -> (str, str):
#         golem_names = list(self._golems.keys())
#         selected_golem = Prompt.ask("Select a golem to talk to:", choices=golem_names)
#         print(f"You have selected {selected_golem} to talk to.\n"
#               f"They use the following context: {self._context_database.get_history({'golem_id': selected_golem})}\n")
#         return selected_golem,
#

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_id.json

```python
{"user_name": "Gooboo", "user_id": "b4136f47-c798-47dc-af79-a8ca4479ef33", "user_description": "Say the phrase \"Boo Boo BoOoOo\" every time you speak"}
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

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\web_app\templates\index.html

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golem Garden</title>
</head>
<body>
    <h1>Golem Garden</h1>
    <div id="chatbox">
        <!-- Chat messages will be added here -->
    </div>
    <form id="chat-form">
        <input type="text" id="message" placeholder="Enter your message" required />
        <input type="text" id="user_name" placeholder="Enter your name" required />
        <input type="text" id="user_description" placeholder="Enter a description of yourself" required />
        <input type="submit" value="Send" />
    </form>

    <script>
        document.getElementById("chat-form").addEventListener("submit", async (event) => {
            event.preventDefault();

            const messageInput = document.getElementById("message");
            const message = messageInput.value;
            messageInput.value = "";

            if (message) {
                addMessageToChatbox("user", message);
                const golemResponse = await sendMessage(message);
                addMessageToChatbox("golem", golemResponse);
            }
        });

        function addMessageToChatbox(role, message) {
            const chatbox = document.getElementById("chatbox");
            const messageElement = document.createElement("p");
            messageElement.className = role;
            messageElement.textContent = message;
            chatbox.appendChild(messageElement);
        }

        async function sendMessage(message) {
            const user_name = document.getElementById("user_name").value;
            const user_description = document.getElementById("user_description").value;
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message, user_name, user_description }),
            });
            const responseData = await response.json();
            return responseData["response"];
        }
    </script>
</body>
</html>

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\tests\test_database.py

```python
import pytest
from database import db, conversations_collection

def test_mongodb_connection():
    # Check if the MongoDB connection is established
    assert db is not None
    assert conversations_collection is not None

def test_mongodb_crud_operations():
    # Insert a test document
    test_conversation = {
        "user_id": "test_user",
        "golem_id": "test_golem",
        "message": "Hello, Golem!",
        "response": "Hello, User!"
    }
    inserted_id = conversations_collection.insert_one(test_conversation).inserted_id
    assert inserted_id is not None

    # Retrieve the test document
    retrieved_conversation = conversations_collection.find_one({"_id": inserted_id})
    assert retrieved_conversation is not None
    assert retrieved_conversation["user_id"] == "test_user"

    # Update the test document
    new_response = "Hi, User!"
    conversations_collection.update_one({"_id": inserted_id}, {"$set": {"response": new_response}})
    updated_conversation = conversations_collection.find_one({"_id": inserted_id})
    assert updated_conversation["response"] == new_response

    # Delete the test document
    delete_result = conversations_collection.delete_one({"_id": inserted_id})
    assert delete_result.deleted_count == 1

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\tests\test_golems.py

```python
from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem import Golem, GreeterGolem, GardenerGolem, ExpertGolem


def test_golem_instantiation():
    golem = Golem(name="Test Golem",
                  type="test",
                  context_database=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert golem.name == "Test Golem"
    assert golem.type == "test"
    assert golem.golem_string == "test_string"
    assert golem.model == "test_model"


def test_greeter_golem_instantiation():
    greeter_golem = GreeterGolem(name="Test Golem",
                  type="greeter",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(greeter_golem, GreeterGolem)
    assert isinstance(greeter_golem, Golem)


def test_gardener_golem_instantiation():
    gardener_golem = GardenerGolem(name="Test Golem",
                  type="gardener",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(gardener_golem, GardenerGolem)
    assert isinstance(gardener_golem, Golem)


def test_expert_golem_instantiation():
    expert_golem = ExpertGolem(name="Test Golem",
                  type="expert",
                  context_db=ContextDatabase(),
                  golem_string="test_string",
                  model="test_model")
    assert isinstance(expert_golem, ExpertGolem)
    assert isinstance(expert_golem, Golem)

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\tests\test_golem_factory.py

```python
# test_golem_factory.py


class TestGolemFactory(unittest.TestCase):
    def setUp(self):
        self.golem_factory = GolemFactory(context_database=ContextDatabase())

    def test_create_golem(self):
        test_golem = self.golem_factory.create_golem("Golem")
        self.assertIsInstance(test_golem, Golem)


```
