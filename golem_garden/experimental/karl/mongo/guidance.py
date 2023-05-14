from pydantic import BaseModel
from typing import List

from langchain import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from golem_garden.experimental.karl.mongo.models import InterviewGuidance
from dotenv import load_dotenv
load_dotenv()

QUESTION_GUIDANCE = '''
    You are generating questions for an interviewer to ask to get missing information to populate an incomplete data model.
    
    Given this current model state:
    {current_model}

    What information is missing? Are you filling in a blank, or adding details to an existing field?
    
    Try to think of some interesting and conversational questions that could help you learn the things you want to learn about this Human!  Try not to ask for the information directly, instead Gently guide the conversation via socratic questioning and try to get the human to talk more about the things that interest them.

    What are some questions you could ask to help you fill out the model?
       
    Format your output like this:
    {format_instructions}
'''

llm = ChatOpenAI(model_name = 'gpt-4')

def get_questions(current_model: BaseModel) -> List[str]:

    guidance_parser = PydanticOutputParser(pydantic_object=InterviewGuidance)

    guidance_prompt = PromptTemplate(
        template = QUESTION_GUIDANCE,
        input_variables = ['current_model'],
        partial_variables={'format_instructions': guidance_parser.get_format_instructions()}
    )

    guidance_chain = LLMChain(
        prompt=guidance_prompt,
        llm = llm
    )

    fixer = OutputFixingParser.from_llm(
        llm = llm,
        parser = guidance_parser
    )

    raw_response = guidance_chain.predict(
        current_model = current_model
    )

    question_list = fixer.parse(
        raw_response
    )

    return question_list.questions

