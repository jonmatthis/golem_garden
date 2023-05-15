from pydantic import BaseModel

from langchain import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from golem_garden.experimental.karl.mongo.models import ModelUpdatePayload

MODEL_UPDATE_TEMPLATE = '''
    You are updating an incomplete data model based on information extracted from a human by an AI.
    
    Given this current model state:
    {current_model}

    Update it according to this AI question / human answer
    
    AI asked:{ai_question}
    Human responded:{human_response}

    Format your output like this:
    {format_instructions}
'''

llm = ChatOpenAI(model_name = 'gpt-4')

def update_model(input_payload: ModelUpdatePayload) -> BaseModel:
    print(input_payload)
    pydantic_class_constructor = input_payload.model.__class__

    extractor_parser = PydanticOutputParser(pydantic_object=pydantic_class_constructor)

    extractor_prompt = PromptTemplate(
        template = MODEL_UPDATE_TEMPLATE,
        input_variables = ['current_model','ai_question', 'human_response'],
        partial_variables={'format_instructions': extractor_parser.get_format_instructions()}
    )

    extractor_chain = LLMChain(
        prompt=extractor_prompt,
        llm = llm
    )

    fixer = OutputFixingParser.from_llm(
        llm = llm,
        parser = extractor_parser
    )

    raw_response = extractor_chain.predict(
        ai_question = input_payload.ai_question,
        human_response = input_payload.human_answer,
        current_model = input_payload.model
    )

    updated_model = fixer.parse(
        raw_response
    )

    return updated_model

