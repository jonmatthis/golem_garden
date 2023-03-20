from golem_garden.context_database import ContextDatabase


class Golem:
    def __init__(self,
                 name: str,
                 type: str,
                 context_db: ContextDatabase,
                 golem_string: str = "You are a friendly Golem. We are so glad you're here",
                 model: str = "gpt-3.5-turbo"):
        self.name = name
        self.type = type
        self.model = model
        self.golem_string = golem_string
        self.context_db = context_db

    async def receive_message(self, message: str):
        input_payload = self.prepare_input(message)
        response_payload = await self.process_message(input_payload)
        success = self.return_response(response_payload)
        return success


    async def process_message(self, input_payload) -> str:
        # Process the message and return the response payload
        return input_payload

    def return_response(self, response_payload: str) -> bool:
        # Send the response payload to the appropriate recipient
        print(f"I heard you say: {response_payload}")



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
