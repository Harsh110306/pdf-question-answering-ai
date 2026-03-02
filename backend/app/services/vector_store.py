import os
from typing import List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.core.config import settings
from app.services.embedder import get_embedding_model
import shutil

class VectorStoreManager:
    def __init__(self):
        self.embeddings = get_embedding_model()
        self.store_path = settings.VECTOR_STORE_PATH
        
        # Ensure directory exists
        os.makedirs(self.store_path, exist_ok=True)
        
    def _get_doc_path(self, document_id: str) -> str:
        return os.path.join(self.store_path, document_id)

    def add_documents(self, document_id: str, chunks: List[Document]) -> None:
        """
        Creates a new FAISS index for the document and saves it locally.
        Each document gets its own namespace/subdirectory.
        """
        doc_path = self._get_doc_path(document_id)
        
        # Create new vector store
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        # Save locally
        vector_store.save_local(doc_path)
        
    def search(self, document_id: str, query: str, k: int = 3) -> List[Tuple[Document, float]]:
        """
        Loads the FAISS index and performs similarity search with scores.
        Returns a list of (Document, score) tuples.
        """
        doc_path = self._get_doc_path(document_id)
        if not os.path.exists(doc_path):
            raise ValueError(f"Vector index not found for document {document_id}")
            
        vector_store = FAISS.load_local(
            doc_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True # Required for local loading in newer LangChain versions
        )
        
        # L2 distance (lower is better, depending on normalization)
        results = vector_store.similarity_search_with_score(query, k=k)
        return results

    def delete_document_index(self, document_id: str) -> bool:
        doc_path = self._get_doc_path(document_id)
        if os.path.exists(doc_path):
            shutil.rmtree(doc_path)
            return True
        return False

# Global instance
vector_store_manager = VectorStoreManager()
