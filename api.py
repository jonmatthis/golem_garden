from pathlib import Path

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from golem_garden.golems.golem import Golem



app = FastAPI()

GOLEM = Golem()

class Message(BaseModel):
    content: str

@app.post("/api/chat")
async def chat(message: Message):
    response = GOLEM.process_message(message.content)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)
