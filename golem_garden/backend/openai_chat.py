from dataclasses import dataclass
from pathlib import Path
from typing import Union, Dict
import asyncio
import os
from typing import Dict, List, Any

import openai
from dotenv import load_dotenv

import toml

DEFAULT_OPENAI_CHAT_TOML = './open_ai_chat_configs/_default_openai_chat_config.toml'



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


class OpenAIAPIClient:
    # TODO - integrate with new impelementation fo Golem and use openai_chat_config
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def query(self,
                    conversation: List[Dict[str, str]],
                    chat_parameters: OpenaiChatParameters = load_openai_chat_parameters(),
                    only_return_message_content: bool = False) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()

        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            messages=conversation,
            model=chat_parameters.model_name,
            # temperature=chat_parameters.temperature,
            # top_p=chat_parameters.top_p,
            # n=chat_parameters.n,
            # # stream=chat_config.stream, #TODO - figure out how this works lol
            # # stop=chat_config.stop, #TODO - figure out how this works lol
            # max_tokens=chat_parameters.max_tokens,
            # presence_penalty=chat_parameters.presence_penalty,
            # frequency_penalty=chat_parameters.frequency_penalty,
            # logit_bias=chat_parameters.logit_bias,
            # user=chat_parameters.user,
        ))

        if only_return_message_content:
            return response.choices[0].message['content'].strip()

        return dict(response)


if __name__ == '__main__':
    openai_chat_config = load_openai_chat_parameters()
    print(openai_chat_config)
