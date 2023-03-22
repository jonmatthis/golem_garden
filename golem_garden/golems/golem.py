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
                 golem_string: str = "You are a friendly Golem. We are so glad you're here :) ",
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
        self._context = [self.system_dict]
        self.temperature = temperature
        self.max_tokens = max_tokens

    @property
    def context(self):
        """ return the context messages of the golem - https://platform.openai.com/docs/guides/chat/introduction"""
        return self._context

    def _prepare_input(self,
                       message: str,
                       user_id: str) -> List[dict]:
        # TODO - pre and post pend instructions to the Golem regarding the formatting of the output, alter the context and the input paramenters (temperature, max_tokens, etc)
        self.context_database.add_message(golem_name=self.name,
                                          role='user',
                                          content=message)
        history = self.context_database.get_history({"golem_id": self.name,
                                                     "user_id": user_id})
        self._context = [self.system_dict] + history
        return self._context

    async def return_response(self, messages: List[dict]) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self._get_chat_completion, messages)
        return response['choices'][0]['message']['content']

    def _get_chat_completion(self, messages: List[dict]) -> dict:
        print(f"{self.name} is thinking...")
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

        return response

    async def process_message(self, message: str, user_id: str) -> str:

        input_payload = self._prepare_input(message=message,
                                            user_id=user_id)
        response_message = await self.return_response(input_payload)
        self.context_database.add_message(golem_name=self.name,
                                          role='assistant',
                                          content=response_message)
        return response_message



