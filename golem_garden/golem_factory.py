# golem_factory.py

from golem_garden.golems import GreeterGolem, GardenerGolem, SubGolem
from golem_garden.config_database import ConfigDatabase
from golem_garden.context_database import ContextDatabase

class GolemFactory:
    def __init__(self, context_db:ContextDatabase):
        self.config_db = ConfigDatabase()
        self.context_db = context_db

    def create_golem(self, golem_name):
        config = self.config_db.golem_configs[golem_name]

        golem_type = config["type"]

        if golem_type == "greeter":
            return GreeterGolem(**config, context_db=self.context_db)
        elif golem_type == "gardener":
            return GardenerGolem(**config, context_db=self.context_db)
        else:
            return SubGolem(**config, context_db=self.context_db)

    def create_all_golems(self):
        golems  = {}
        for name in self.config_db.golem_configs.keys():
            golems[name] = self.create_golem(name)
        return golems
