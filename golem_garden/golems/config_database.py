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
