from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma

def create_retriever(
    vector_store : Chroma,
    name : str, 
    description : str
    ):
    retriever = vector_store.as_retriever()
    return create_retriever_tool(
        retriever,
        name,
        description
    )