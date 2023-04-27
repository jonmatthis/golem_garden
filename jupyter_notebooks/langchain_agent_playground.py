import asyncio
import functools
import os

import faiss
import nest_asyncio
from dotenv import load_dotenv
from langchain import LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.human.tool import HumanInputRun
from langchain.vectorstores import FAISS

from golem_garden.prompts import task_completion_prompt_template, CustomPromptTemplate
from golem_garden.output_parsers.output_parser import CustomOutputParser
from golem_garden.tools.tools import web_search, process_csv, query_website_tool, get_tools

load_dotenv()
os.environ["LANGCHAIN_HANDLER"] = "langchain"



OBJECTIVE = "I want to create personalized emails to send to high schools in Massachusetts that have dog or dog breeds " \
            "as their mascots asking them to contact their state representative to support a dog welfare bill. " \
            "Format your emails to be personalized to each school and save them out to file when you are done." \
            " You can use the following template:" \
            " Dear [school name], We are reaching out to [your school name] to ask you to contact your state" \
            " representative to support a dog welfare bill. [Insert a paragraph about why you think this bill is " \
            "important and why you think your school should support it. ]. I am writing to you because" \
            " [insert a reason why you think your school should support this bill that mentions their mascot]. I " \
            "hope you will consider contacting your state representative to support this bill" \
            " [include contact information for the state representive for people who live near that school]. " \
            "Thank you!"

def run_async(coroutine):
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coroutine)


if __name__ == "__main__":
    nest_asyncio.apply()

    # llm

    output_parser = CustomOutputParser()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1.0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    # tools

    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

    tools = [
        web_search,
        WriteFileTool(),
        ReadFileTool(),
        process_csv,
        query_website_tool,
        HumanInputRun(),  # Activate if you want the permit asking for help from the human
    ]

    tool_documentations = [Document(page_content=t.description, metadata={"index": i}) for i, t in enumerate(tools)]
    tool_vector_store = FAISS.from_documents(tool_documentations, OpenAIEmbeddings())
    retriever = tool_vector_store.as_retriever()
    tool_names = [tool.name for tool in tools]

    # task
    new_todo_bool = False

    # prompt
    task_completion_prompt = CustomPromptTemplate(
        template=task_completion_prompt_template,
        tools_getter=functools.partial(get_tools, tools=tools),
        input_variables=["input", "intermediate_steps"]
    )

    # llm_chain
    llm_chain = LLMChain(llm=llm, prompt=task_completion_prompt)

    # agent
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nFinal Answer:"],
        allowed_tools=tool_names
    )

    # agent_executor

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                        tools=tools,
                                                        verbose=True, )

    agent_executor.run(OBJECTIVE)
