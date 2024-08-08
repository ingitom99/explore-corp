from langchain.docstore.document import Document
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def build_db(
    data : dict,
    ticker : str,
    source : str = "sec_filings"
    ):

    documents = []
    for key, value in data.items():
        # Convert the value to a string if it's not already
        content = str(value)
        # Create a Document object
        doc = Document(page_content=content, id=key, metadata={
            "source": source,
            "ticker": ticker,
            "tag": key
            })
        documents.append(doc)

    embedding_func = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name=ticker + "_" + source,
        embedding_function=embedding_func,
        persist_directory="./chromas/" + ticker + "_" + source,  
    )

    
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store.add_documents(documents=documents, ids=uuids)

    return vector_store