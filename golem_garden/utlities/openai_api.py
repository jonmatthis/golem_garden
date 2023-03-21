import asyncio
import openai


class OpenAIAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    async def query(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant golem :D"
            }, {
                "role": "user",
                "content": prompt
            }],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.8,
        ))
        message = response.choices[0].message['content'].strip()
        return message
