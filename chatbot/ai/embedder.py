"""
embedder.py

Responsible for creating and managing the embedding model.
This module loads the embedding model only once and reuses it
throughout the application.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from .config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_embedding_model():
    """
    Returns a singleton embedding model.

    The model is loaded only once during the application lifetime.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )