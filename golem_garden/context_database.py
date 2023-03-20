import threading
import json
from typing import List, Dict

class ContextDatabase:
    def __init__(self, database_path: str = "context_database.json"):
        self._database = {}
        self.lock = threading.Lock()
        self.database_path = database_path

    @property
    def database(self):
        return self._database

    def add_message(self, golem_name: str, role: str, content: str):
        with self.lock:
            if golem_name not in self._database:
                self._database[golem_name] = []
            self._database[golem_name].append({'role': role, 'content': content})
            self._save_to_file()

    def get_chat_history(self, golem_id: str) -> List[Dict[str, str]]:
        with self.lock:
            return self._database.get(golem_id, [])

    def _save_to_file(self):
        with open(self.database_path, 'w') as f:
            json.dump(self._database, f, indent=2)

    def load_from_file(self):
        try:
            with open(self.database_path, 'r') as f:
                self._database = json.load(f)
        except FileNotFoundError:
            pass

    def as_json(self):
        with self.lock:
            return json.dumps(self._database, indent=4)

    def print(self):
        print(self.as_json())


if __name__ == "__main__":
    context_database = ContextDatabase()
    context_database.load_from_file()
    context_database.print()
