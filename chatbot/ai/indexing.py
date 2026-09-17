from typing import Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_SIZE, CHUNK_OVERLAP
from .vectorstore import HospitalVectorStore

def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Returns a configured text splitter to break large text into smaller chunks.
    We use the chunk size and overlap defined in config.py.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )

def index_text_data(collection_name: str, text_content: str, metadata: Dict[str, Any], doc_id: str):
    """
    Takes raw text, splits it into smaller chunks, and saves it to the vector store.
    
    Args:
        collection_name: The Chroma collection to store data in (e.g., 'patients').
        text_content: The raw string of text you want the AI to learn.
        metadata: A dictionary of extra info (like {'patient_id': 1}). 
        doc_id: A unique identifier for this document.
    """
    # 1. Initialize the text splitter
    splitter = get_text_splitter()
    
    # 2. Split the raw text into manageable pieces
    chunks = splitter.split_text(text_content)
    
    if not chunks:
        return
        
    # 3. Create LangChain Document objects for each chunk
    documents = []
    chunk_ids = []
    
    for i, chunk in enumerate(chunks):
        # Attach the metadata to the chunk so the AI knows where it came from
        doc = Document(page_content=chunk, metadata=metadata)
        documents.append(doc)
        
        # Create a unique ID for each chunk (e.g., "patient_45_chunk_0")
        chunk_ids.append(f"{doc_id}_chunk_{i}")
        
    # 4. Save the chunks to the ChromaDB vector database
    vector_store = HospitalVectorStore()
    vector_store.add_documents(
        collection_name=collection_name, 
        documents=documents, 
        ids=chunk_ids
    )
    
    print(f"Successfully indexed {len(chunks)} chunks into '{collection_name}'.")
