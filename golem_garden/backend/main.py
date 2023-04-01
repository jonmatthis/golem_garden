from fastapi import FastAPI
from datetime import datetime
from .openai_chat import load_openai_chat_parameters, OpenaiChatParameters

app = FastAPI()
openai_chat_config = load_openai_chat_parameters()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/message/{msg}")
def read_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Received message at {timestamp}: {msg}")
    return {"timestamp": timestamp, "message": msg, "config": str(openai_chat_config)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
