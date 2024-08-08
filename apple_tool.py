import os
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
db = Chroma(
    persist_directory="./chromas/appl",
    embedding_function=embedding_function
    )

retriever = db.as_retriever()

rd_info_tool = create_retriever_tool(
    retriever,
    "appl_reporting_searcher",
    """Search information about Apple's reporting to the SEC"""
)
