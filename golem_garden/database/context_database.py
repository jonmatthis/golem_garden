import uuid
from typing import Dict, List, Union

from pymongo import MongoClient


class ContextDatabase:
    # TODO - integrate with new refactor of Golem class
    def __init__(self,
                 database_name: str = "golem_garden",
                 collection_name: str = "conversations",
                 session_id: str = str(uuid.uuid4())):
        self._mongo_client = MongoClient()
        self._database = self._mongo_client[database_name]
        self._conversations_collection = self._database[collection_name]
        self._session_id = session_id

    def add_message(self,
                    golem_name: str,
                    user_id: str,
                    message: Dict[str, str]):

        self._validate_incoming_message(message)

        conversation = {
            "session_id": self._session_id,
            "user_id": user_id,
            "golem_id": golem_name,
            "message": message,
        }
        self._conversations_collection.insert_one(conversation)

    def _validate_incoming_message(self, message):
        if not "role" in message.keys():
            raise ValueError("Message must have a 'role' key.")
        if not "content" in message.keys():
            raise ValueError("Message must have a 'content' key.")
        if not message["role"] in ["user", "system", "assistant"]:
            raise ValueError("Message role must be either 'user' or 'system' or 'assistant'.")

    def add_response(self,
                     golem_name: str,
                     user_id: str,
                     response: List[Dict[str, Union[str, float]]]):

        conversation = {
            "session_id": self._session_id,
            "user_id": user_id,
            "golem_id": golem_name,
            "response": response,
        }
        self._conversations_collection.insert_one(conversation)

    def get_history(self, query: dict = None, only_this_session: bool = True) -> List[Dict[str, str]]:
        """Get chat history for a given query. If no query is provided, return all chat history."""

        include_fields = {"role": 1, "content": 1, "_id": 0}

        if query is None:
            query = {}

        if only_this_session:
            query["session_id"] = self._session_id

        # Add aggregation stages
        pipeline = [
            {"$match": query},  # Filter by query
            {"$group": {
                "_id": {"content": "$content", "role": "$role"},  # Group by content and role
                "doc": {"$first": "$$ROOT"}  # Get the first document in the group (i.e. remove duplicates)
            }},
            {"$replaceRoot": {"newRoot": "$doc"}},  # Replace the root with the first document in the group
            {"$project": include_fields}  # Only include the fields specified in include_fields
        ]

        history = list(self._conversations_collection.aggregate(pipeline))
        return history
