import asyncio
from typing import Dict, List, Any

import openai

from golem_garden.openai.openai_chat_configs.openai_chat_config import OpenaiChatParameters, load_openai_chat_parameters


class OpenAIAPIClient:
    # TODO - integrate with new impelementation fo Golem and use openai_chat_config
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    async def query(self,
                    conversation: List[Dict[str, str]],
                    chat_parameters: OpenaiChatParameters = load_openai_chat_parameters(),
                    only_return_message_content: bool = False) -> Dict[str, Any]:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            messages=conversation,
            model=chat_parameters.model_name,
            temperature=chat_parameters.temperature,
            top_p=chat_parameters.top_p,
            n=chat_parameters.n,
            # stream=chat_config.stream, #TODO - figure out how this works lol
            # stop=chat_config.stop, #TODO - figure out how this works lol
            max_tokens=chat_parameters.max_tokens,
            presence_penalty=chat_parameters.presence_penalty,
            frequency_penalty=chat_parameters.frequency_penalty,
            logit_bias=chat_parameters.logit_bias,
            user=chat_parameters.user,
        ))

        if  only_return_message_content:
            return response.choices[0].message['content'].strip()

        return dict(response)
