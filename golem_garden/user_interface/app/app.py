import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from golem_garden.golems.golem import Golem

class ChatRequest(BaseModel):
    message: str

app = FastAPI()

@app.post("/chat")
async def chat_with_golem(request: ChatRequest):
    session_id = str(uuid.uuid4())
    print("Creating Golem...")
    golem = Golem(session_id=session_id, user_id="UnknownUser")

    asyncio.run(golem.poke())

    response = await golem.chat(request.message)

    return {"message": response}


