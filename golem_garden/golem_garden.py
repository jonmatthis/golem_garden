from golem_garden.context_database import ContextDatabase
from golem_garden.golem_factory import GolemFactory


class GolemGarden:
    def __init__(self, context_database: ContextDatabase = ContextDatabase()):
        self._context_database = context_database
        self._golem_factory = GolemFactory(self._context_database)
        self._golems = self._golem_factory.create_all_golems()

        self._greeter_golem = self._golems["GreeterGolem"]
        self._gardener_golem = self._golems["GardenerGolem"]
        self._expert_golems = {golem.name: golem for golem in self._golems.values() if golem.type == "sub"}

    @property
    def golems(self):
        return self._golems

    @property
    def chat_history(self):
        return self._context_database.load_context("chat_history")


    def process_input(self, user_input):
        return self._greeter_golem.process_message(user_input)
