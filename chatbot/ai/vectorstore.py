"""
vectorstore.py

Production-ready ChromaDB Vector Store
--------------------------------------

Responsibilities:
- Create Chroma collections
- Store LangChain Documents
- Update vectors
- Delete vectors
- Perform similarity search
- Manage persistent vector database

Author: Vaibhav
"""

from typing import List, Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .config import (
    CHROMA_DB_PATH,
    TOP_K_RESULTS,
)

from .embedder import get_embedding_model


class HospitalVectorStore:
    """
    Wrapper around Chroma Vector Database.
    """

    COLLECTIONS = {
        "patients": "hospital_patients",
        "doctors": "hospital_doctors",
        "appointments": "hospital_appointments",
        "bills": "hospital_bills",
        "payments": "hospital_payments",
    }

    def __init__(self):
        """
        Initialize embedding model.
        """

        self.embedding_model = get_embedding_model()

        self._stores = {}

    # ---------------------------------------------------------
    # Collection
    # ---------------------------------------------------------

    def get_collection(self, collection_name: str) -> Chroma:
        """
        Return existing collection.
        Creates one automatically if it doesn't exist.
        """

        if collection_name not in self.COLLECTIONS:
            raise ValueError(
                f"Unknown collection: {collection_name}"
            )

        if collection_name not in self._stores:

            self._stores[collection_name] = Chroma(
                collection_name=self.COLLECTIONS[
                    collection_name
                ],
                embedding_function=self.embedding_model,
                persist_directory=str(CHROMA_DB_PATH),
            )

        return self._stores[collection_name]

    # ---------------------------------------------------------
    # Add Documents
    # ---------------------------------------------------------

    def add_documents(
        self,
        collection_name: str,
        documents: List[Document],
        ids: Optional[List[str]] = None,
    ):
        """
        Store LangChain documents.
        """

        if not documents:
            return

        collection = self.get_collection(collection_name)

        collection.add_documents(
            documents=documents,
            ids=ids,
        )

    # ---------------------------------------------------------
    # Update Documents
    # ---------------------------------------------------------

    def update_documents(
        self,
        collection_name: str,
        documents: List[Document],
        ids: List[str],
    ):
        """
        Update vectors.

        Chroma has no direct update.

        Delete old

        Add new
        """

        self.delete_documents(
            collection_name,
            ids,
        )

        self.add_documents(
            collection_name,
            documents,
            ids,
        )

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete_documents(
        self,
        collection_name: str,
        ids: List[str],
    ):
        """
        Delete vectors.
        """

        collection = self.get_collection(
            collection_name
        )

        collection.delete(
            ids=ids,
        )

    # ---------------------------------------------------------
    # Similarity Search
    # ---------------------------------------------------------

    def similarity_search(
        self,
        collection_name: str,
        query: str,
        k: int = TOP_K_RESULTS,
        filter: Optional[dict] = None,
    ) -> List[Document]:
        """
        Search similar documents.
        """

        collection = self.get_collection(
            collection_name
        )

        return collection.similarity_search(
            query=query,
            k=k,
            filter=filter,
        )

    # ---------------------------------------------------------
    # Search With Score
    # ---------------------------------------------------------

    def similarity_search_with_score(
        self,
        collection_name: str,
        query: str,
        k: int = TOP_K_RESULTS,
        filter: Optional[dict] = None,
    ):
        """
        Search documents with similarity score.
        """

        collection = self.get_collection(
            collection_name
        )

        return collection.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter,
        )

    # ---------------------------------------------------------
    # Count
    # ---------------------------------------------------------

    def count_documents(
        self,
        collection_name: str,
    ) -> int:
        """
        Return total vectors.
        """

        collection = self.get_collection(
            collection_name
        )

        return collection._collection.count()

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset_collection(
        self,
        collection_name: str,
    ):
        """
        Delete all vectors.
        """

        collection = self.get_collection(
            collection_name
        )

        ids = collection.get()["ids"]

        if ids:
            collection.delete(ids=ids)

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def document_exists(
        self,
        collection_name: str,
        document_id: str,
    ) -> bool:
        """
        Check document exists.
        """

        collection = self.get_collection(
            collection_name
        )

        result = collection.get(
            ids=[document_id]
        )

        return len(result["ids"]) > 0