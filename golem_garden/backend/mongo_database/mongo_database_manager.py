import json
import logging
import os
import traceback
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Union, Any

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from system.filenames_and_paths import clean_path_string, get_default_database_json_save_path

load_dotenv()

logger = logging.getLogger(__name__)
def get_mongo_uri() -> str:
    remote_uri = os.getenv('MONGO_URI_MONGO_CLOUD')
    if remote_uri:
        return remote_uri

    is_docker = os.getenv('IS_DOCKER', False)
    if is_docker:
        return os.getenv('MONGO_URI_DOCKER')
    else:
        return os.getenv('MONGO_URI_LOCAL')


def get_mongo_database_name():
    return os.getenv('MONGODB_DATABASE_NAME')


def get_mongo_chat_history_collection_name():
    return os.getenv('MONGODB_CHAT_HISTORY_COLLECTION_NAME')


TEST_MONGO_QUERY = {"student_id": "test_student",
                    "student_name": "test_student_name",
                    "thread_title": "test_thread_title",
                    "thread_id": f"test_session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"}


def default_serialize(o: Any) -> str:
    if isinstance(o, datetime):
        return o.isoformat()
    elif hasattr(o, "dict"):
        return o.dict()
    elif hasattr(o, "to_dict"):
        return o.to_dict()
    elif hasattr("__dict__") and not isinstance(o, dict):
        return o.__dict__
    return str(o)

class MongoDatabaseManager:
    def __init__(self, ):
        self._client = AsyncIOMotorClient(get_mongo_uri())
        self._database = self._client.get_default_database(get_mongo_database_name())


    def get_collection(self, collection_name: str):
        return self._database[collection_name]

    def get_collection_as_dict(self, collection_name: str):
        return self._database[collection_name].find().to_dict()
    async def insert(self, collection, document):
        return await self._database[collection].insert_one(document)

    async def upsert(self, collection, query, data):
        return await self._database[collection].update_one(query, data, upsert=True)

    async def save_json(self,
                  collection_name: str,
                  query: dict = None,
                  save_path: Union[str, Path] = None):
        try:
            query = query if query is not None else defaultdict()
            collection = self._database[collection_name]
            if save_path is not None:
                file_name = Path(save_path).name
                if file_name.endswith(".json"):
                    file_name = file_name[:-5]
                file_name = clean_path_string(file_name)
                save_path = Path(save_path).parent / file_name
            else:
                save_path =  get_default_database_json_save_path(filename=collection_name,
                                                    timestamp=True)


            data = [doc async for doc in collection.find(query)]

            save_path = str(save_path)
            if save_path[-5:] != ".json":
                save_path += ".json"

            for document in data:
                document["_id"] = str(document["_id"])
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'w') as file:
                json.dump(data, file, indent=4, default=default_serialize)
        except Exception as e:
            traceback.print_exc()
            print(f"Error saving json: {e}")
            raise e

        logger.info(f"Saved {len(data)} documents to {save_path}")

    async def close(self):
        self._client.close()



if __name__ == "__main__":
    import asyncio
    # Replace 'your_mongodb_uri' with your actual MongoDB URI
    mongodb_manager = MongoDatabaseManager()  # run locally

    test_document = {
        'name': 'Test',
        'description': 'This is a test document',
        'timestamp': datetime.now().isoformat(),
    }

    async def main():
        # Insert the test document into a 'test' collection
        insert_result = await mongodb_manager.insert('test', test_document)
        print(f'Inserted document with ID: {insert_result.inserted_id}')

        # Retrieve all documents from the 'test' collection
        find_result = [doc async for doc in mongodb_manager.get_collection('test').find()]

        print("Documents in 'test' collection:")
        for document in find_result:
            print(document)

    asyncio.run(main())
