import json
import uuid
from pathlib import Path
from typing import Dict, Optional

from rich.prompt import Prompt

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem import Golem
from golem_garden.golems.golem_factory import GolemFactory

TRIED_TO_POKE_GOLEM_THAT_DIDNT_EXIST = "This user tried to poke a golem named {golem_name}, but we don't have a golem with that name. You think it's funny they tried to poke a non-existend golem. What would it be like to poke this golem? Maybe we can make one? 😄"


def create_poke_prompt(user_name:str, waking_up:bool = False):
    if waking_up:
        return f"You wake up to find a human named {user_name} poking you! You wake up in a way that reflects your personality. " \
               f"Introduce yourself to them and say a little bit about yourself :D"

    return  f"The human named {user_name} you are talking to just poked you! Wow, that's wild!!"\
            f" Say the equivalent of 'Hello World' in the language of Golems - it should be brimming with your own distinct personality! " \
           f"Make it yours! Be creative!"


class GolemGarden:
    """
    A class representing the Golem Garden, responsible for managing golems and processing user inputs.
    """

    def __init__(self, context_database: ContextDatabase = ContextDatabase()):
        """
        Initialize the Golem Garden with a context database and create all golems.
        """
        self._context_database = context_database
        self._golem_factory = GolemFactory(context_database=self._context_database)
        self._golems = self._golem_factory.create_all_golems()

    @property
    def golems(self) -> Dict[str, Golem]:
        """
        Returns a dictionary of golem names and their corresponding golem instances.
        """
        return self._golems

    @property
    def greeter(self) -> Golem:
        """
        Returns the GreeterGolem instance.
        """
        return self._golems["GreeterGolem"]

    @property
    def gardener(self) -> Golem:
        """
        Returns the GardenerGolem instance.
        """
        return self._golems["GardenerGolem"]

    def history(self, user_id: Optional[str] = None, golem_name: Optional[str] = None):
        """
        Returns the context database history for a specific user+golem pair or all user+golem pairs.
        """
        return self._context_database.get_history(query={user_id: user_id, golem_name: golem_name})

    async def pass_message_to_golem(self, message: str, golem_name: Optional[str] = None) -> str:
        """
        Processes a user input and returns a response from the selected golem or the GreeterGolem if no golem is selected.
        """

        if not golem_name in self.golems:
            message = self._make_unknown_golem_string(golem_name=golem_name,
                                                      attempt_string=f"tried to say '{message}' to")
            golem_name = "GardenerGolem"

        return await self._golems[golem_name].process_message(user_id=self._user_id,
                                                              message=message)

    def _make_unknown_golem_string(self, golem_name: str, attempt_string: str):
        return f"User {self._user_name} {attempt_string} {golem_name}, but we don't have a golem with that name.\n" \
               f" You think it's funny they tried to talk to a non-existend golem. What would it be like to talk to this golem?" \
               f" Maybe we can make one! Ask the user if they want to make this golem 😄",

    async def poke_golem(self, golem_name: str, waking_up:bool=False) -> str:
        """
        Returns a response from the specified golem.
        """
        return await self._golems[golem_name].process_message(user_id=self._user_id,
                                                              message = create_poke_prompt(user_name=self._user_name,
                                                                                           waking_up=waking_up))

    def set_user_id(self, user_id: str) -> None:
        """
        Sets the user_id for the context database.
        """
        self._context_database.user_id = user_id

    def get_user_id(self):
        user_id_path = "user_id.json"
        user_id_full_path = Path(user_id_path).resolve()
        if user_id_full_path.exists():
            with open(str(user_id_full_path), 'r') as f:
                user_dict = json.load(f)
        else:
            user_dict = self.create_new_user(user_id_full_path)

        self._user_id = user_dict["user_id"]
        self._user_name = user_dict["user_name"]
        self._user_description = user_dict["user_description"]

    def create_new_user(self, user_id_full_path):
        user_dict = {}
        user_dict["user_name"] = Prompt.ask(f"I don't believe we've met before! What should I call you?")
        user_dict["user_id"] = str(uuid.uuid4())
        print(
            f"Nice to meet you, {user_dict['user_name']}! I will remember you with the ID: {user_dict['user_id']} in a file at: {user_id_full_path}")
        user_dict["user_description"] = Prompt.ask(f"Tell me a little about yourself, if you like!:",
                                                   default="a nice person")
        with open(str(user_id_full_path), 'w') as f:
            json.dump(user_dict, f)
        return user_dict

    async def welcome_user(self):
        self.get_user_id()
        return await self.pass_message_to_golem(message=self.create_welcome_prompt(), golem_name="GreeterGolem", )

    def create_welcome_prompt(self):
        return f"A human user that calls themselves '{self._user_name}' " \
               f"just approached the Golem Garden Gate. They describe themselves as {self._user_description}, " \
               f"which you think is interesting. You are excited to see them! Try to briefly mention something from a previous conversation, if you can. " \
               f"Greet them kindly and ask how you may help :D "

    def select_golem(self, golem_name: Optional[str] = None) -> (str, str):
        golem_names = list(self._golems.keys())
        selected_golem = Prompt.ask("Select a golem to talk to:", choices=golem_names)
        print(f"You have selected {selected_golem} to talk to.\n"
              f"They use the following context: {self._context_database.get_history({'golem_id': selected_golem})}\n")
        return selected_golem,

