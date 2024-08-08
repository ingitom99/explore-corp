import os
from dotenv import load_dotenv
from tqdm import tqdm

from langchain_mistralai import MistralAIEmbeddings
from langchain_community.document_loaders import JSONLoader
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# Get Mistral API key from environment
mistral_api_key = os.getenv("MISTRAL_API_KEY")

def build_chroma_from_json(

    data_json_path : str,
    chroma_db_path : str,
    ):

    loader = JSONLoader(
        file_path=data_json_path,
    )

    docs = loader.load()
    embedding_func = MistralAIEmbeddings(api_key=mistral_api_key)
    Chroma.from_documents(
            docs,
            embedding_func,
            persist_directory=chroma_db_path
            )

    return None
