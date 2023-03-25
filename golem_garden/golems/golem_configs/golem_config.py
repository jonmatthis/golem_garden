from dataclasses import dataclass
from pathlib import Path
from typing import Union

import toml

DEFAULT_GOLEM_TOML = './_default_golem.toml'


@dataclass
class GolemConfig:
    """
    A dataclass to store the Golem chatbot golems.
    """
    name: str
    type: str
    sub_type: str
    golem_string: str

    def __str__(self):
        return (f"Class: {self.__class__.__name__}(\n"
                f"  name={self.name},\n"
                f"  type={self.type},\n"
                f"  sub_type={self.sub_type},\n"
                f"  golem_string='''\n"
                f"{self.golem_string}\n"
                "'''\n"
                )


def load_golem_config(config_toml_path: Union[Path, str] = str(Path(__file__).parent / DEFAULT_GOLEM_TOML),
                      ) -> GolemConfig:
    """
    Load the Golem golems from a TOML file.
    """
    with open(config_toml_path, 'r') as toml_file:
        config = toml.load(toml_file)
    return GolemConfig(**config)


if __name__ == '__main__':
    golem_config = load_golem_config()
    print(golem_config)
