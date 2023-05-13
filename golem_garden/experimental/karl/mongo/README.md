# how to call
see example usage in `mongo/upsert.py`.

import `handle_model_update` (`mongo/upsert.py`) and `retrieve` (`mongo/retrieve.py`)

Use `retrieve` to get the existing model first (this will create a new instance of your pydantic object if it doesn't exist yet)


pass in an `UpsertPayload` to `handle_model_update`
you will get back a `ModelUpdateResponse`
(see `mongo/models.py`)


```
class UpsertPayload(BaseModel):
    ai_question: str
    human_answer: str

    # mongo collection
    collection: Any

    # unique identifier for your model document in mongodb
    query: dict

    # the pydantic model you are storing as a document
    model: BaseModel
```

```
class ModelUpdateResponse(BaseModel):
    model: BaseModel
    questions: List[str]
```

# what does it do?

The current model + the AI / Human exchange is passed to an LLM which will update the model.
Another LLM will then examine the updated model, and generate questions that will help populate missing fields.

The updated model as well as new questions to ask are returned in `ModelUpdateResponse`

In addition, the updated model is written to the mongo DB
