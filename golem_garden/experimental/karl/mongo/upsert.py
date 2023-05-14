import logging

from dotenv import load_dotenv
from langchain import OpenAI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

from golem_garden.experimental.karl.mongo.guidance import get_questions
from golem_garden.experimental.karl.mongo.models import ModelUpdatePayload, ModelUpdateResponse, ExampleHuman
from golem_garden.experimental.karl.mongo.models import UpsertPayload
from golem_garden.experimental.karl.mongo.retrieve import retrieve
from golem_garden.experimental.karl.mongo.updater import update_model

from rich import print

load_dotenv()

logging.basicConfig(level=logging.INFO)


def mongo_update(collection: Collection, query: dict, model: BaseModel):
    collection.update_one(query, {"$set": model.dict()}, upsert=True)


def handle_model_update(input: UpsertPayload) -> ModelUpdateResponse:
    updated_model = update_model(ModelUpdatePayload(
        ai_question=input.ai_question,
        human_answer=input.human_answer,
        model=input.model
    ))

    new_questions = get_questions(updated_model)

    mongo_update(input.collection, input.query, updated_model)

    output_payload = ModelUpdateResponse(
        questions=new_questions,
        model=updated_model
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
        'id': '12345'
    }

    model = retrieve(collection, query, ExampleHuman)

    payload = UpsertPayload(
        ai_question="what is your name",
        human_answer="my name is bob",
        collection=collection,
        model=model,
        query=query
    )

    payloads = {}
    payloads[0] = payload

    loop = 5
    for loop_index in range(loop):
        print(f'------loop index: {loop_index}------\n')

        model_update_response = handle_model_update(payloads[loop_index])

        print(f'\n--Updated model: {model_update_response.model.dict()}--\n')

        print(f'new questions: {model_update_response.questions}-\n')

        print(f"Asking question: {model_update_response.questions[0]}-\n")

        human_answer = input("Human answer: ")

        payloads[loop_index + 1] = UpsertPayload(
            ai_question=model_update_response.questions[0],
            human_answer=human_answer,
            collection=collection,
            model=model_update_response.model,
            query=query
        )

    best_guess_model = model_update_response.model

    print(f"=========\n+++++++++++\n==========\nBest guess model:\n {best_guess_model}\n==========\n+++++++++++\n==========\n")