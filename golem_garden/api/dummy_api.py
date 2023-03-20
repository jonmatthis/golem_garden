from fastapi import FastAPI

app = FastAPI()

@app.post("/api/v1/endpoint")
async def process_golem_message(message: str):
    # Simulate processing time
    await asyncio.sleep(1)
    return {"response": f"Message received: {message}"}
