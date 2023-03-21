from typing import Dict, List

from golem_garden.context_database import ContextDatabase
from golem_garden.golems.golem_factory import GolemFactory


class GolemGarden:
    def __init__(self, context_database: ContextDatabase = ContextDatabase()):
        self._context_database = context_database
        self._golem_factory = GolemFactory(self._context_database)
        self._golems = self._golem_factory.create_all_golems()

        self._greeter_golem = self._golems["GreeterGolem"]
        self._gardener_golem = self._golems["GardenerGolem"]
        self._expert_golems = {golem.name: golem for golem in self._golems.values() if golem.type == "sub"}

    @property
    def golems(self) -> List[Dict[str, str]]:
        return self._golems

    def history(self, user_id: str = None):
        if user_id is None:
            return self._context_database.database
        else:
            return self._context_database.database[user_id]

    async def process_input(self, user_input, selected_golem=None):
        if selected_golem is None:
            return await self._greeter_golem.process_message(user_input)
        else:
            try:
                return await self._expert_golems[selected_golem].process_message(user_input)
            except KeyError:
                return await self._gardener_golem.process_message(user_input)

    def set_user_id(self, user_id):
        self._context_database.user_id = user_id
