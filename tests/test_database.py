import pytest
from database import db, conversations_collection

def test_mongodb_connection():
    # Check if the MongoDB connection is established
    assert db is not None
    assert conversations_collection is not None

def test_mongodb_crud_operations():
    # Insert a test document
    test_conversation = {
        "user_id": "test_user",
        "golem_id": "test_golem",
        "message": "Hello, Golem!",
        "response": "Hello, User!"
    }
    inserted_id = conversations_collection.insert_one(test_conversation).inserted_id
    assert inserted_id is not None

    # Retrieve the test document
    retrieved_conversation = conversations_collection.find_one({"_id": inserted_id})
    assert retrieved_conversation is not None
    assert retrieved_conversation["user_id"] == "test_user"

    # Update the test document
    new_response = "Hi, User!"
    conversations_collection.update_one({"_id": inserted_id}, {"$set": {"response": new_response}})
    updated_conversation = conversations_collection.find_one({"_id": inserted_id})
    assert updated_conversation["response"] == new_response

    # Delete the test document
    delete_result = conversations_collection.delete_one({"_id": inserted_id})
    assert delete_result.deleted_count == 1
