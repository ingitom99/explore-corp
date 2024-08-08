from uuid import uuid4

from dotenv import load_dotenv

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


# Load environment variables
load_dotenv()

def build_vdb(
    data : dict,
    company_name : str,
    info_source : str
    ) -> Chroma:

    documents = []
    for key, value in data.items():
        # Convert the value to a string if it's not already
        content = str(value)
        # Create a Document object
        doc = Document(page_content=content, id=key, metadata={
            "source": info_source,
            "company": company_name,
            "tag": key
            })
        documents.append(doc)

    embedding_func = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = Chroma(
        collection_name=company_name + "_" + info_source,
        embedding_function=embedding_func,
        persist_directory="./chromas/" + company_name + "_" + info_source  
    )

    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)

    return vector_store

def load_vdb(persist_directory : str) -> Chroma:
    
