import asyncio
from typing import List

import openai

from golem_garden.context_database import ContextDatabase


class Golem:
    def __init__(self,
                 name: str,
                 type: str,
                 context_database: ContextDatabase,
                 api_key: str,
                 golem_string: str = "You are a friendly Golem. We are so glad you're here",
                 model_name: str = "gpt-3.5-turbo",
                 temperature: float = 0.5,
                 max_tokens: int = 150
                 ):
        self.name = name
        self.type = type
        self.model_name = model_name
        self.context_database = context_database
        openai.api_key = api_key
        self.golem_string = golem_string
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _prepare_input(self,  input_message: str) -> List[dict]:
        self.context_database.add_message(golem_name=self.name,
                                          role='user',
                                          content=input_message)
        messages = [{'role': 'system', 'content': self.golem_string}] + self.context_database.get_chat_history(self.name)
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
        input_payload = self._prepare_input(input_message = input_message)
        response_message = await self.return_response(input_payload)
        self.context_database.add_message(golem_name=self.name,
                                          role='assistant',
                                          content=response_message)
        return response_message


#
# class Golem:
#     def __init__(self,
#                  name: str,
#                  type: str,
#                  context_database: ContextDatabase,
#                  golem_string: str = "You are a friendly Golem. We are so glad you're here",
#                  model: str = "gpt-3.5-turbo"):
#         self.name = name
#         self.type = type
#         self.model = model
#         self.golem_string = golem_string
#         self.context_database = context_database
#         self.api_client = OpenAIAPIClient(api_key = OPENAI_API_KEY)
#         self.chat_history = []
#
#     def _prepare_input(self, message: str) -> str:
#         # Prepare the input message for the model
#         self.add_message_to_history('user', message)
#         messages = [{'role': 'system', 'content': self.golem_string}] + self.chat_history
#         # TODO: Add context to the input message, etc etc
#         return messages
#
#     async def process_message(self, input_message) -> str:
#         # Process the message and return the response payload
#         input_payload = self._prepare_input(input_message)
#         response_message = await self.return_response(input_payload)
#         return response_message
#
#     async def return_response(self, input_payload: str) -> str:
#         # Send the response payload to the appropriate recipient
#         response_message = await self.api_client.query(input_payload)
#         return f"Hello, my name is {self.name} - I heard you say: {input_payload} - here is my response: {response_message}"
#

class GreeterGolem(Golem):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            if kwargs["type"] != "greeter":
                raise ValueError("GreeterGolem must have type 'greeter'")
        super().__init__(*args, **kwargs)


class GardenerGolem(Golem):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            if kwargs["type"] != "gardener":
                raise ValueError("GardenerGolem must have type 'gardener'")
        super().__init__(*args, **kwargs)


class ExpertGolem(Golem):
    def __init__(self, *args, **kwargs):
        if "type" in kwargs:
            if kwargs["type"] != "expert":
                raise ValueError("ExpertGolem must have type 'expert'")
        super().__init__(*args, **kwargs)
