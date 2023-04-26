import json
import re
from typing import Optional, Union

import pandas as pd
from duckduckgo_search import ddg
from langchain.agents import tool, create_pandas_dataframe_agent, AgentOutputParser
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.schema import Document, AgentAction, AgentFinish
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from pydantic import Field

from jupyter_notebooks.langchain_agent_playground import llm, _get_text_splitter, browse_web_page


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


query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))
