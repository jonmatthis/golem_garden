import asyncio
import os
from typing import List

import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from golem_garden.context_database import ContextDatabase


class Golem:
    def __init__(self,
                 name: str,
                 type: str,
                 context_database: ContextDatabase,
                 golem_string: str = "You are a friendly Golem. We are so glad you're here",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.5,
                 max_tokens: int = 500
                 ):
        self.name = name
        self.type = type
        self.model_name = model_name
        self.context_database = context_database
        self.golem_string = golem_string
        self.system_dict = {'role': 'system', 'content': self.golem_string}
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _prepare_input(self,  input_message: str) -> List[dict]:
        #TODO - pre and post pend instructions to the Golem regarding the formatting of the output
        self.context_database.add_message(golem_name=self.name,
                                          role='user',
                                          content=input_message)
        history = self.context_database.get_chat_history(self.name)
        messages = [self.system_dict]+history
        return messages

    async def return_response(self, messages: List[dict]) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._get_chat_completion, messages)
        return response['choices'][0]['message']['content']

    def _get_chat_completion(self, messages: List[dict]) -> dict:
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response

    async def process_message(self, input_message) -> str:
        self._update_chat_history(input_message)
        input_payload = self._prepare_input(input_message = input_message)
        response_message = await self.return_response(input_payload)
        self.context_database.add_message(golem_name=self.name,
                                          role='assistant',
                                          content=response_message)
        return response_message

    def _update_chat_history(self, input_message: str):
        self.context_database.add_message(golem_name=self.name,
                                            role='user',
                                            content=input_message)

