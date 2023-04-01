import asyncio
import uuid

from old.database.database_factory import get_database
from golem_garden import GolemConfig, load_golem_config
from golem_garden import OpenAIAPIClient
from golem_garden import OpenaiChatParameters, load_openai_chat_parameters


class Golem:
    def __init__(self,
                 user_id: str,
                 session_id: str = str(uuid.uuid4()),
                 golem_config: GolemConfig = load_golem_config(),
                 openai_chat_parameters: OpenaiChatParameters = load_openai_chat_parameters(),
                 ):
        self._user_id = user_id
        self._session_id = session_id
        self._golem_config = golem_config
        self._openai_chat_parameters = openai_chat_parameters
        self._openai_client = OpenAIAPIClient()
        self._context_database = get_database()

    @property
    def name(self) -> str:
        # TODO - create unique uuid for each golem when it is created
        return self._golem_config.name

    @property
    def type(self) -> str:
        return self._golem_config.type

    @property
    def sub_type(self) -> str:
        return self._golem_config.sub_type

    @property
    def golem_string(self) -> str:
        return self._golem_config.golem_string

    async def chat(self, user_input: str) -> str:
        system = {"role": "system",
                  "content": self._golem_config.golem_string,
                  }
        user_message = {"role": "user",
                       "content": user_input.strip()}

        history = self._context_database.get_history(golem_id=self.name,
                                                     user_id=self._user_id)

        conversation = [system]
        conversation.extend(history)
        conversation.append(user_message)

        response = await self._openai_client.query(conversation=conversation,
                                                   chat_parameters=self._openai_chat_parameters, )

        self._context_database.add_user_message(golem_id=self.name,
                                                user_id=self._user_id,
                                                user_message=user_message)
        self._context_database.add_golem_response(golem_id=self.name,
                                                  user_id=self._user_id,
                                                  response=response)

        return response["choices"][0]["message"]["content"].strip()

    async def poke(self):
        user_input = f"A human just poked you, say the Golem equivalent of 'Hello World!'"

        print(await self.chat(user_input=user_input))

    def __str__(self):
        return (f"\nClass: {self.__class__.__name__}(\n"
                f"  name={self.name},\n"
                f"  type={self.type},\n"
                f"  sub_type={self.sub_type},\n"
                f"  golem_string={self.golem_string})\n"
                )


if __name__ == "__main__":
    print("Creating Golem...")
    golem = Golem()
    print(golem)
    print("\nPoking Golem...")
    asyncio.run(Golem().poke())
    print(f"\n Successfully poked Golem")
