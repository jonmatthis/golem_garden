import pymongo
from dotenv import load_dotenv
import os
from pprint import pprint
print = pprint

load_dotenv()

def try_mongo_connection():
    mongo_uri = os.getenv('MONGO_URI')
    client = pymongo.MongoClient(mongo_uri)
    db = client.test
    print(f"\n\n\n_________\ndb: {db}\n__________\n\n\n")
    print(f"\n\n\n_________\ndb.list_collection_names(): {db.list_collection_names()}\n__________\n\n\n")
    db.runCommand({"killAllSessions": []})

if __name__ == "__main__":
    try_mongo_connection()
