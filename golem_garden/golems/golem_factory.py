from golem_garden.context_database import ContextDatabase
from golem_garden.golems.config_database import ConfigDatabase
from golem_garden.golems.golems import Golem


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
