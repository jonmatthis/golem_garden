from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uuid

from golem_garden.golems.golem import Golem

app = FastAPI()



class IncomingRequest(BaseModel):

    session_id: str
    user_id: str
    golem_id: str
    user_input: str


class ChatResponse(BaseModel):
    session_id: str
    user_id: str
    golem_id: str
    response: str


@app.get("/")
async def return_hello_world():
    return {"message": "Hello World"}

@app.post("/" , response_model=ChatResponse)
async def receive_hello_world():
    return {"message": "Hello World"}


@app.post("/poke", response_model=ChatResponse)
async def poke_golem(chat_request: IncomingRequest):
    """
    Poke a Golem instance.

    Args:
        chat_request (IncomingRequest): A Pydantic model containing the user_input and session_id.

    Returns:
        ChatResponse: A Pydantic model containing the Golem's name and response.
    """
    golem = Golem(session_id=chat_request.session_id,
                  user_id="UnknownUser")

    await golem.poke()

    return {"golem_name": golem.name,
            "response": "Golem poked successfully."}
@app.post("/chat", response_model=ChatResponse)
async def chat_with_golem(chat_request: IncomingRequest):
    """
    Chat with a Golem instance based on the user input.

    Args:
        chat_request (IncomingRequest): A Pydantic model containing the user_input and session_id.

    Returns:
        ChatResponse: A Pydantic model containing the Golem's name and response.


    Raises:
        HTTPException: An exception with status_code 400 if the user_input is "quit" or "exit".
    """
    golem = Golem(session_id=chat_request.session_id,
                  user_id="UnknownUser")

    await golem.poke()

    if chat_request.user_input.lower() in ["quit", "exit"]:
        raise HTTPException(status_code=400, detail="Invalid user input.")
    elif chat_request.user_input.lower() in ["poke"]:
        await golem.poke()
    elif chat_request.user_input.lower() in ["golem"]:
        return {"golem_name": golem.name, "response": str(golem)}

    response = await golem.chat(chat_request.user_input)
    return {"golem_name": golem.name, "response": response}


if __name__ == "__main__":
    import requests
    import json

    # Test the FastAPI endpoint
    url = "http://127.0.0.1:8000/chat"
    headers = {'Content-Type': 'application/json'}

    # Test case 0: Hello World
    response = requests.get(url)
    if response.status_code == 200:
        print("Test case 0: Success!")
        print(response.json())

    # Test case 1: Simple chat interaction
    chat_request = {"user_input": "Hello Golem!", "session_id": str(uuid.uuid4())}
    response = requests.post(url, data=json.dumps(chat_request), headers=headers)

    if response.status_code == 200:
        print("Test case 1: Success!")
        print(response.json())
    else:
        print("Test case 1: Failed!")
        print(response.status_code, response.text)

    # Test case 2: Invalid user input (quit)
    chat_request = {"user_input": "quit", "session_id": str(uuid.uuid4())}
    response = requests.post(url, data=json.dumps(chat_request), headers=headers)

    if response.status_code == 400:
        print("Test case 2: Success!")
        print(response.json())
    else:
        print("Test case 2: Failed!")
        print(response.status_code, response.text)
