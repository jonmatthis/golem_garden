import json
import logging
import uuid
from pathlib import Path
from typing import Union, Dict

from golem_garden.database._strategies.base_database import BaseDatabase

DATABASE_PATH = Path(__file__).parent.parent / "database.json"

logger = logging.getLogger(__name__)


class JSONDatabase(BaseDatabase):
    def __init__(self,
                 database_path: Union[Path, str] = str(DATABASE_PATH),
                 session_id: str = str(uuid.uuid4())):

        self._database_path = Path(database_path).resolve()
        self._data = self._load_data()

        if session_id:
            self.session_id = session_id
        else:
            self.session_id = self._create_session_id()

    def _load_data(self):
        if self._database_path.is_file():
            with self._database_path.open() as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    logger.warning("Warning: Invalid JSON format. Initializing an empty database.")
                    return {}
        else:
            return {}

    def _create_session_id(self):
        return str(uuid.uuid4())

    def _save_data(self):
        with self._database_path.open(mode="w") as file:
            json.dump(self._data, file, indent=4)

    def add_user_message(self,
                         user_id: str,
                         golem_id: str,
                         user_message: Dict[str, str]):
        if not user_id in self._data:
            self._data[user_id] = {}
        if not golem_id in self._data[user_id]:
            self._data[user_id][golem_id] = {}
        if not self.session_id in self._data[user_id][golem_id]:
            self._data[user_id][golem_id][self.session_id] = []

        self._data[user_id][golem_id][self.session_id].append(user_message)
        self._save_data()

    def add_golem_response(self,
                           user_id: str,
                           golem_id: str,
                           response: Union[str, dict]):
        if not user_id in self._data:
            self._data[user_id] = {}
        if not golem_id in self._data[user_id]:
            self._data[user_id][golem_id] = {}
        if not self.session_id in self._data[user_id][golem_id]:
            self._data[user_id][golem_id][self.session_id] = []

        if isinstance(response, str):
            response_message = {"type":"assistant", "content":response}
        else:
            try:
                response_message = response['choices'][0]['message']
            except Exception as e:
                logger.error(f"Error: {e}")
                raise e
        self._data[user_id][golem_id][self.session_id].append(response_message)
        self._save_data()

    def get_history(self,
                    user_id: str,
                    golem_id: str,
                    this_session_only: bool = True):

        try:
            if this_session_only:
                return self._data[user_id][golem_id][self.session_id]
            else:
                return self._data[user_id][golem_id]
        except KeyError:
            # logger.warning(f"Warning: No history found for the given query: {query_dict}")
            return []


if __name__ == "__main__":
    test_user_id = "test_user1"
    golem1_id = "test_golem1"
    golem2_id = "test_golem2"
    test_session_id = "test_session1"

    test_database_path = Path(__file__).parent.parent / "test_database.json"
    database = JSONDatabase(database_path=test_database_path, session_id=test_session_id)

    database.add_user_message(test_user_id, golem1_id, {"role":"user", "content": "Hello Golem1!"})
    database.add_golem_response(test_user_id, golem1_id, "Hello,Wow!, how can I help you?")

    database.add_user_message(test_user_id, golem2_id, {"role":"user", "content": "Hello Golem2!"})
    database.add_golem_response(test_user_id, golem2_id, "Hello, Jeez! how can I help you?")

    query_dict = {
        "user_id": test_user_id,
        "golem_id": golem1_id
    }

    print(f"History for {query_dict}:\n {database.get_history(user_id=test_user_id, golem_id=golem1_id)}")

    query_dict = {
        "user_id": test_user_id,
        "golem_id": golem2_id
    }
    print(f"History for {query_dict}:\n {database.get_history(user_id=test_user_id, golem_id=golem2_id)}")
