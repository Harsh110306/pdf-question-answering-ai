from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from typing import List, Dict
from langchain_core.documents import Document

def create_chunks(pages_data: List[Dict]) -> List[Document]:
    """
    Splits page text into smaller semantic chunks while retaining metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    docs = []
    for page in pages_data:
        # Avoid creating empty chunks if page has no text
        if not page["text"].strip():
            continue
            
        chunks = text_splitter.create_documents(
            texts=[page["text"]],
            metadatas=[{"page_num": page["page_num"]}]
        )
        docs.extend(chunks)
        
    return docs
