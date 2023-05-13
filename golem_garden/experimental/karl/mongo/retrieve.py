from pydantic import BaseModel

from typing import Type

from pymongo import MongoClient
from pymongo.collection import Collection

from golem_garden.experimental.karl.mongo.models import ExampleHuman

def retrieve(collection: Collection, query, pydantic_model: Type[BaseModel]) -> BaseModel:

    document = collection.find_one(query)

    return pydantic_model(**document) if document else pydantic_model()

if __name__ == '__main__':
    
    # Create a client instance
    client = MongoClient("mongodb://localhost:27017/")

    # Select a database
    db = client["test"]
    # Select a collection
    collection = db["test"]

    test = retrieve(collection, {'id':'123'}, ExampleHuman)

    print(test)