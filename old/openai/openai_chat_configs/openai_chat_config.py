from dataclasses import dataclass
from pathlib import Path
from typing import Union, Dict

import toml

DEFAULT_OPENAI_CHAT_TOML = './_default_openai_chat_config.toml'


@dataclass
class OpenaiChatParameters:
    """
    A dataclass to store the OpenaiChat chatbot golems.
    """
    type: str
    sub_type: str
    model_name: str
    temperature: float
    max_tokens: int
    top_p: float
    n: int
    stream: bool
    stop: Dict[str, str]
    presence_penalty: float
    frequency_penalty: float
    logit_bias: Dict[str, float]
    user: str

    def __str__(self):
        return (f"Class: {self.__class__.__name__}(\n"
                f"  type={self.type},\n"
                f"  sub_type={self.sub_type},\n"
                f"  model_name={self.model_name},\n"
                f"  temperature={self.temperature},\n"
                f"  max_tokens={self.max_tokens},\n"
                f"  top_p={self.top_p},\n"
                f"  n={self.n},\n"
                f"  stream={self.stream},\n"
                f"  stop={self.stop},\n"
                f"  presence_penalty={self.presence_penalty},\n"
                f"  frequency_penalty={self.frequency_penalty},\n"
                f"  logit_bias={self.logit_bias},\n"
                f"  user={self.user}\n"
                ")\n"
                )


def load_openai_chat_parameters(
        config_toml_path: Union[Path, str] = str(Path(__file__).parent / DEFAULT_OPENAI_CHAT_TOML),
        ) -> OpenaiChatParameters:
    """
    Load the OpenaiChat golems from a TOML file.
    """

    with open(config_toml_path, 'r') as toml_file:
        config = toml.load(toml_file)
    return OpenaiChatParameters(**config)


if __name__ == '__main__':
    openai_chat_config = load_openai_chat_parameters()
    print(openai_chat_config)
