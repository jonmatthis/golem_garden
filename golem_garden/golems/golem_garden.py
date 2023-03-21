from typing import Dict, Optional

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem_factory import GolemFactory


class GolemGarden:
    """
    A class representing the Golem Garden, responsible for managing golems and processing user inputs.
    """

    def __init__(self, context_database: ContextDatabase = ContextDatabase()):
        """
        Initialize the Golem Garden with a context database and create all golems.
        """
        self._context_database = context_database
        self._golem_factory = GolemFactory(self._context_database)
        self._golems = self._golem_factory.create_all_golems()

        self._greeter_golem = self._golems["GreeterGolem"]
        self._gardener_golem = self._golems["GardenerGolem"]
        self._expert_golems = {golem.name: golem for golem in self._golems.values() if golem.type == "sub"}

    @property
    def golems(self) -> Dict[str, str]:
        """
        Returns a dictionary of golem names and their corresponding golem instances.
        """
        return self._golems

    def history(self, user_id: Optional[str] = None):
        """
        Returns the context database history for a specific user or the entire history if no user_id is provided.
        """
        # TODO: add ability to pull more specific context/history. Might require moving to a more sophisticated database method like SQL or MongoDB
        if user_id is None:
            return self._context_database.database
        else:
            return self._context_database.database[user_id]

    async def process_input(self, user_input: str, selected_golem: Optional[str] = None) -> str:
        """
        Processes a user input and returns a response from the selected golem or the GreeterGolem if no golem is selected.
        """
        if selected_golem is None:
            return await self._greeter_golem.process_message(user_input)
        else:
            try:
                return await self._expert_golems[selected_golem].process_message(user_input)
            except KeyError:
                return await self._gardener_golem.process_message(user_input)

    def set_user_id(self, user_id: str) -> None:
        """
        Sets the user_id for the context database.
        """
        self._context_database.user_id = user_id
