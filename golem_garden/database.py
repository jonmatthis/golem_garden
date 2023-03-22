from pymongo import MongoClient

# Replace "mongodb://localhost:27017/" with your MongoDB URI if you're using a remote server
client = MongoClient("mongodb://localhost:27017/")
db = client["golem_garden_db"]
