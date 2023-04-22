import asyncio
import functools
import json
import os
import re
from typing import List, Union
from typing import Optional

import faiss
import nest_asyncio
# %%
# General
import pandas as pd
from dotenv import load_dotenv
from duckduckgo_search import ddg
from langchain import PromptTemplate, LLMChain, OpenAI
from langchain.agents import tool, AgentExecutor, AgentOutputParser, LLMSingleActionAgent
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain, BaseCombineDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.base import BaseTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.human.tool import HumanInputRun
from langchain.vectorstores import FAISS
from pydantic import Field

load_dotenv()
os.environ["LANGCHAIN_HANDLER"] = "langchain"

# # %%
# %pip install bs4
# %pip install nest_asyncio
# %pip install pandas
# %pip install langchain
# %pip install duckduckgo_search
# %pip install playwright


@tool
def process_csv(csv_file_path: str, instructions: str, output_path: Optional[str] = None) -> str:
    """Process a CSV by with pandas in a limited REPL. Only use this after writing data to disk as a csv file. Any figures must be saved to disk to be viewed by the human. Instructions should be written in natural language, not code. Assume the dataframe is already loaded."""
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        return f"Error: {e}"
    agent = create_pandas_dataframe_agent(llm, df, max_iterations=30, verbose=True)
    if output_path is not None:
        instructions += f" Save output to disk at {output_path}"
    try:
        return agent.run(instructions)
    except Exception as e:
        return f"Error: {e}"


@tool
def web_search(query: str, num_results: int = 8) -> str:
    """Useful for general internet search queries."""
    search_results = []
    if not query:
        return json.dumps(search_results)

    results = ddg(query, max_results=num_results)
    if not results:
        return json.dumps(search_results)

    for j in results:
        search_results.append(j)

    return json.dumps(search_results, ensure_ascii=False, indent=4)


async def async_load_playwright(url: str) -> str:
    """Load the specified URLs using Playwright and parse using BeautifulSoup."""
    from bs4 import BeautifulSoup
    from playwright.async_api import async_playwright

    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()
            soup = BeautifulSoup(page_source, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            results = "\n".join(chunk for chunk in chunks if chunk)
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


def run_async(coro):
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coro)


@tool
def browse_web_page(url: str) -> str:
    """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
    return run_async(async_load_playwright(url))


def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )


class WebpageQATool(BaseTool):
    name = "query_webpage"
    description = "Browse a webpage and retrieve the information relevant to the question."
    text_splitter: RecursiveCharacterTextSplitter = Field(default_factory=_get_text_splitter)
    qa_chain: BaseCombineDocumentsChain

    def _run(self, url: str, question: str) -> str:
        """Useful for browsing websites and scraping the text information."""
        result = browse_web_page.run(url)
        docs = [Document(page_content=result, metadata={"source": url})]
        web_docs = self.text_splitter.split_documents(docs)
        results = []
        # TODO: Handle this with a MapReduceChain
        for i in range(0, len(web_docs), 4):
            input_docs = web_docs[i:i + 4]
            window_result = self.qa_chain({"input_documents": input_docs, "question": question},
                                          return_only_outputs=True)
            results.append(f"Response from window {i} - {window_result}")
        results_docs = [Document(page_content="\n".join(results), metadata={"source": url})]
        return self.qa_chain({"input_documents": results_docs, "question": question}, return_only_outputs=True)

    async def _arun(self, url: str, question: str) -> str:
        raise NotImplementedError


# Set up the base template
task_completion_prompt_template = """
 Complete the following tasks as best you can. You have access to the following tools. You should stop to ask the Human before taking each step:

{tools}

Use the following format:

Task: The task you must complete
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have everything I need to complete the task
Final Answer: What I will do to complete the task

task: {input}
{agent_scratchpad}"""

from typing import Callable


# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str

    # The list of tools available
    tools_getter: Callable

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts

        tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
        return self.template.format(**kwargs)

def get_tools(query: str, tools: List[BaseTool]):
    docs = retriever.get_relevant_documents(query)
    return [tools[d.metadata["index"]] for d in docs]




class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

if __name__ == "__main__":

    nest_asyncio.apply()

    #llm

    output_parser = CustomOutputParser()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1.0, openai_api_key=os.getenv("OPENAI_API_KEY"))






    #tools

    query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))

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



    #task
    new_todo_bool = False
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


    #prompt
    task_completion_prompt = CustomPromptTemplate(
        template=task_completion_prompt_template,
        tools_getter=functools.partial(get_tools, tools=tools),
        input_variables=["input", "intermediate_steps"]
    )

    #llm_chain
    llm_chain = LLMChain(llm=llm, prompt=task_completion_prompt)

    #agent
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nFinal Answer:"],
        allowed_tools=tool_names
    )

    #agent_executor

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                        tools=tools,
                                                        verbose=True,)


    agent_executor.run(OBJECTIVE)
