import json
from typing import Optional, List

import pandas as pd
from langchain.agents import tool, create_pandas_dataframe_agent
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from pydantic import Field

from golem_garden.data_loaders.async_load_url_with_playwright import async_load_url_with_playwright


def _get_text_splitter():
    return RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )

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


def get_tools(query: str, tools: List[BaseTool]):
    docs = retriever.get_relevant_documents(query)
    return [tools[d.metadata["index"]] for d in docs]


query_website_tool = WebpageQATool(qa_chain=load_qa_with_sources_chain(llm))


@tool
def browse_web_page(url: str) -> str:
    """Verbose way to scrape a whole webpage. Likely to cause issues parsing."""
    return run_async(async_load_url_with_playwright(url))
