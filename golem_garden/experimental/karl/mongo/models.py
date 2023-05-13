from pydantic import BaseModel

from typing import List, Any

class UpsertPayload(BaseModel):
    ai_question: str
    human_answer: str

    # mongo collection
    collection: Any

    # unique identifier for your model document in mongodb
    query: dict

    # the pydantic model you are storing as a document
    model: BaseModel

class ModelUpdateResponse(BaseModel):
    model: BaseModel
    questions: List[str]

class ModelUpdatePayload(BaseModel):
    ai_question: str
    human_answer: str
    model: BaseModel
    

class InterviewGuidance(BaseModel):
    questions: List[str]




# this is for testing
class ExampleHuman(BaseModel):
    name: str = ''
    age: str = ''
    occupation: str = ''
    