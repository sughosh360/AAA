"""
This file contains the logic to index the textbook provided. ChromaDB in-process search framework is used to
index vector embeddings of chunks of textbook. (ChromaDB ==> vectorStore)

Tried setting up Qdrant and running the search server on a docker on my local.
Stuck to in-process search framework chromadb to make the iteration faster and test the prompts
"""

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
import os

os.environ['OPENAI_API_KEY'] = 'XXX'

CHUNK_SIZE = 5000
CHUNK_OVERLAP = 100


def get_indexed_data():
    """
    Load the textbook as a document, split it into chunks, embed each chunk and load it into the vector store.
    :return: instance of ChromaDB containing vector embeddings.
    """
    raw_documents = TextLoader('textbook.txt').load()
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    documents = text_splitter.split_documents(raw_documents)
    db = Chroma.from_documents(documents, OpenAIEmbeddings())
    return db
