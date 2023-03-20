# golem_factory.py
import os

from dotenv import load_dotenv

from golem_garden.config_database import ConfigDatabase
from golem_garden.context_database import ContextDatabase
from golem_garden.golems import GreeterGolem, GardenerGolem, ExpertGolem

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class GolemFactory:
    def __init__(self, context_database: ContextDatabase):
        self.config_database = ConfigDatabase()
        self.context_database = context_database

    def create_golem(self, golem_name):
        config = self.config_database.golem_configs[golem_name]

        golem_type = config["type"]

        if golem_type == "greeter":
            return GreeterGolem(**config, context_database=self.context_database, api_key=OPENAI_API_KEY)
        elif golem_type == "gardener":
            return GardenerGolem(**config, context_database=self.context_database, api_key=OPENAI_API_KEY)
        else:
            return ExpertGolem(**config, context_database=self.context_database, api_key=OPENAI_API_KEY)

    def create_all_golems(self):
        golems = {}
        for name in self.config_database.golem_configs.keys():
            golems[name] = self.create_golem(name)
        return golems
