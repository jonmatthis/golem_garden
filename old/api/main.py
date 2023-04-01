from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import asyncio
import uuid

from golem_garden import Golem

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
async def health():
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
