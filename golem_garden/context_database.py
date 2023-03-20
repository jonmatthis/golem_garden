# context_database.py
import asyncio
import json
import threading


class ContextDatabase:
    def __init__(self):
        try:
            self.data = self.load_context_database()
        except FileNotFoundError:
            self.data = {"chat_history": []}
        self.lock = threading.Lock()

    def update_context(self, context_key, context_value):
        with self.lock:
            self.data[context_key] = context_value


    def load_context(self, context_key):
        with self.lock:
            return self.data.get(context_key, None)

    def load_context_database(self):
        with open("context_database.json", "r") as f:
            return json.load(f)
