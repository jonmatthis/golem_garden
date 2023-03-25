import json
from typing import Dict, List, Union

from pymongo import MongoClient


class ContextDatabase:
    #TODO - integrate with new refactor of Golem class
    def __init__(self, database_name: str = "golem_garden", collection_name: str = "conversations",
                 user_id: str = "UnknownUser"):
        self.client = MongoClient()
        self.db = self.client[database_name]
        self.conversations_collection = self.db[collection_name]
        self.user_id = user_id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    def add_message(self,
                    golem_name: str,
                    user_id: str,
                    message: Dict[str, str]):

        if not message["role"] in ["user", "system", "assistant"]:
            raise ValueError("Message role must be either 'user' or 'system' or 'assistant'.")

        conversation = {
            "user_id": self._user_id,
            "golem_id": golem_name,
            "message": message,
        }
        self.conversations_collection.insert_one(conversation)

    def add_response(self,
                        golem_name: str,
                        user_id: str,
                        response: str):
            conversation = {
                "user_id": self._user_id,
                "golem_id": golem_name,
                "response": response,
            }
            self.conversations_collection.insert_one(conversation)
    def get_history(self, query: dict = None, ) -> List[Dict[str, str]]:
        """Get chat history for a given query. If no query is provided, return all chat history."""

        include_fields = {"role": 1, "content": 1, "_id": 0}

        if query is None:
            query = {}

        # Add aggregation stages
        pipeline = [
            {"$match": query}, # Filter by query
            {"$group": {
                "_id": {"content": "$content", "role": "$role"}, # Group by content and role
                "doc": {"$first": "$$ROOT"} # Get the first document in the group (i.e. remove duplicates)
            }},
            {"$replaceRoot": {"newRoot": "$doc"}}, # Replace the root with the first document in the group
            {"$project": include_fields} # Only include the fields specified in include_fields
        ]

        history = list(self.conversations_collection.aggregate(pipeline))
        return history

    def as_json(self):
        conversations = list(self.conversations_collection.find({"user_id": self._user_id}))
        return json.dumps(conversations, indent=4, default=str)

    def print(self):
        print(self.as_json())


if __name__ == "__main__":
    db = ContextDatabase(user_id="John")
    db.add_message("Golem1", "user", "Hello, Golem1!")
    db.add_message("Golem1", "golem", "Hello, John!")
    db.add_message("Golem2", "user", "Hello, Golem2!")
    db.add_message("Golem2", "golem", "Hello, John!")
    db.print()
    print("Chat history with Golem1:")
    print(db.get_history("Golem1"))
