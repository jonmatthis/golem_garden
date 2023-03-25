import json
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple, List

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem import Golem
from golem_garden.golems.golem_factory import GolemFactory


class GolemGarden:
    """
    A class representing the Golem Garden, responsible for managing golems and processing user inputs.
    """

    def __init__(self, session_id: str = None, user_name: str = None, user_description: str = None):

        if session_id is None:
            session_id = str(uuid.uuid4())
        self._session_id = session_id

        self._context_database = ContextDatabase(session_id=self._session_id,
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

    @property
    def session_id(self) -> str:
        """A unique ID for the user session """
        return self._session_id


    def history(self,
                session_id: Optional[str] = None,
                user_name: Optional[str] = None,
                golem_name: Optional[str] = None) -> List[Dict]:
        """
        Returns the context database history for a specific user+golem pair or all user+golem pairs.

        Args:
            session_id (Optional[str], optional): The session ID to filter the history by. Defaults to None.
            user_name (Optional[str], optional): The user name to filter the history by. Defaults to None.
            golem_name (Optional[str], optional): The golem name to filter the history by. Defaults to None.

        Returns:
            Dict: A dictionary containing the history data.
        """
        return self._context_database.get_history(query={"session_id": session_id, "user_name":user_name, "golem_name": golem_name})

    async def pass_message_to_golem(self, message: str, session_id: str, user_name: str, golem_name: Optional[str] = None) -> str:
        """
        Processes a user input and returns a response from the selected golem or the GreeterGolem if no golem is selected.

        Args:
            message (str): The message input by the user.
            session_id (str): The ID of the user.
            user_name (str): The name of the user.
            golem_name (Optional[str], optional): The name of the golem to pass the message to. Defaults to None.

        Returns:
            str: The response message from the golem.
        """
        if golem_name not in self.golems:
            message = self._make_unknown_golem_string(golem_name=golem_name, user_name=user_name, attempt_string=f"tried to say '{message}' to")
            golem_name = "GardenerGolem"

        return await self._golems[golem_name].process_message(session_id=session_id, message=message)

    @staticmethod
    def _make_unknown_golem_string(golem_name: str, user_name: str, attempt_string: str) -> str:
        return f"User {user_name} {attempt_string} {golem_name}, but we don't have a golem with that name.\n" \
               f" You think it's funny they tried to talk to a non-existent golem. What would it be like to talk to this golem?" \
               f" Maybe we can make one! Ask the user if they want to make this golem 😄"
