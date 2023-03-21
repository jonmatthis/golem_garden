import json
import threading
from pathlib import Path
from typing import Dict, List


class ContextDatabase:
    def __init__(self, database_path: str = "user/context_database.json", user_id: str = "UnknownUser"):
        self._database = {}
        self.lock = threading.Lock()
        self.database_path = database_path
        self.user_id = user_id

    @property
    def database(self):
        return self._database

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
        if user_id not in self._database:
            self._database[user_id] = {}

    def add_message(self, golem_name: str, role: str, content: str):
        with self.lock:
            if golem_name not in self._database:
                self._database[self._user_id][golem_name] = []
            self._database[self._user_id][golem_name].append({'role': role, 'content': content})
            self._save_to_file()

    def get_chat_history(self, golem_id: str) -> List[Dict[str, str]]:
        with self.lock:
            return self._database[self._user_id].get(golem_id, [])

    def _save_to_file(self):
        self._create_parent_directory_if_not_exists()
        with open(self.database_path, 'w') as f:
            json.dump(self._database, f, indent=4)

    def _create_parent_directory_if_not_exists(self):
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)

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