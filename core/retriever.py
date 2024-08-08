from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma

def create_retriever(ticker : str, vector_store : Chroma):
    retriever = vector_store.as_retriever()
    return create_retriever_tool(
        retriever,
        ticker + "_filings_searcher",
        "Retrieve information about " + ticker + " filings"
    )