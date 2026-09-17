from typing import Optional
from langchain_core.vectorstores import VectorStoreRetriever

from .vectorstore import HospitalVectorStore
from .config import TOP_K_RESULTS

def get_retriever(collection_name: str, filter_dict: Optional[dict] = None) -> VectorStoreRetriever:
    """
    Creates and returns a LangChain Retriever for a specific collection.
    
    While the VectorStore is the actual database, the Retriever is the tool 
    that knows HOW to search it (e.g., how many results to bring back, and what filters to apply).
    """
    vector_store = HospitalVectorStore()
    
    # Get the raw Chroma collection (like 'patients' or 'doctors')
    chroma_collection = vector_store.get_collection(collection_name)
    
    # Configuration for our search
    search_kwargs = {
        "k": TOP_K_RESULTS  # This tells the retriever to bring back the top 5 most relevant chunks
    }
    
    # If we only want to search inside a specific patient's record, we apply a filter.
    if filter_dict:
        search_kwargs["filter"] = filter_dict
        
    # We convert the Chroma collection into a LangChain Retriever
    # "similarity" means it will look for text that mathematically means the same thing as the user's question.
    retriever = chroma_collection.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs
    )
    
    return retriever
