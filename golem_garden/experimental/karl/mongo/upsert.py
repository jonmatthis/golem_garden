from pymongo.collection import Collection
from pymongo import MongoClient

from pydantic import BaseModel

from golem_garden.experimental.karl.mongo.models import UpsertPayload

from golem_garden.experimental.karl.mongo.guidance import get_questions
from golem_garden.experimental.karl.mongo.updater import update_model

from golem_garden.experimental.karl.mongo.models import ModelUpdatePayload, ModelUpdateResponse, ExampleHuman
from golem_garden.experimental.karl.mongo.retrieve import retrieve

from dotenv import load_dotenv
load_dotenv()

def mongo_update(collection: Collection, query: dict, model: BaseModel):

    collection.update_one(query, {"$set": model.dict()}, upsert=True)

def handle_model_update(input: UpsertPayload ) -> ModelUpdateResponse:
    
    updated_model = update_model(ModelUpdatePayload(
        ai_question = input.ai_question,
        human_answer = input.human_answer,
        model = input.model
    ))

    new_questions = get_questions(updated_model)

    mongo_update(input.collection, input.query, updated_model)

    output_payload = ModelUpdateResponse(
        questions = new_questions,
        model = updated_model
    )

    return output_payload

if __name__ == '__main__':
        # Create a client instance
    client = MongoClient("mongodb://localhost:27017/")

    # Select a database
    db = client["test"]
    # Select a collection
    collection = db["test"]

    query = {
        'id': '123'
    }

    model = retrieve(collection, query, ExampleHuman)

    payload = UpsertPayload(
        ai_question = "what is your name",
        human_answer = "my name is bob",
        collection = collection,
        model = model,
        query = query
    )

    model_update_response = handle_model_update(payload)

    print(f'Updated model: {model_update_response.model}')
    print(f'new questions: {model_update_response.questions}')