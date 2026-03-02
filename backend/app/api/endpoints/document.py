from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Document
from app.models.schemas import DocumentResponse
from app.services.pdf_parser import extract_text_from_pdf
from app.services.chunker import create_chunks
from app.services.vector_store import vector_store_manager
from app.services.rag_pipeline import rag_pipeline
from pydantic import BaseModel
from typing import List, Optional
import shutil
import tempfile
import os

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    try:
        # 1. Create DB record
        db_doc = Document(filename=file.filename)
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        
        # 2. Extract Text
        pages_data = extract_text_from_pdf(temp_file_path)
        
        if not pages_data:
            # Rollback
            db.delete(db_doc)
            db.commit()
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            
        # 3. Chunk Text
        chunks = create_chunks(pages_data)
        
        # 4. Generate Embeddings & Store in FAISS
        vector_store_manager.add_documents(db_doc.id, chunks)
        
    except Exception as e:
        if 'db_doc' in locals():
            db.delete(db_doc)
            db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_file_path)
        
    return db_doc

class SummaryResponse(BaseModel):
    summary: str
    
class CompareRequest(BaseModel):
    document_ids: List[str]
    question: str
    
class CompareResponse(BaseModel):
    answer: str
    sources: List[dict]

@router.get("/{document_id}/summary", response_model=SummaryResponse)
def get_document_summary(document_id: str, db: Session = Depends(get_db)):
    # Verify doc exists
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    question = "Provide a comprehensive summary of this document."
    result = rag_pipeline.query(document_id, question)
    return {"summary": result["answer"]}

@router.post("/compare", response_model=CompareResponse)
def compare_documents(req: CompareRequest, db: Session = Depends(get_db)):
    if len(req.document_ids) < 2:
        raise HTTPException(status_code=400, detail="Provide at least two document IDs for comparison")
        
    combined_contexts = []
    combined_sources = []
    
    # Retrieve context from each document
    for doc_id in req.document_ids:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document {doc_id} not found")
            
        context_str, sources = rag_pipeline._get_context_and_sources(doc_id, req.question)
        if context_str:
            combined_contexts.append(f"--- From Document {doc.filename} ---\n{context_str}")
            # Add document filename to sources
            for source in sources:
                source["filename"] = doc.filename
                combined_sources.append(source)
                
    if not combined_contexts:
        return {"answer": "No relevant info found in any document.", "sources": []}
        
    full_context = "\n\n".join(combined_contexts)
    
    # Generate final answer
    if rag_pipeline.chain:
        answer = rag_pipeline.chain.invoke({"context": full_context, "question": req.question})
    else:
        answer = f"[MOCK LLM] Comparing the documents based on context: {full_context[:300]}..."
        
    return {
        "answer": answer,
        "sources": combined_sources
    }

@router.get("/{document_id}/search")
def keyword_search(document_id: str, keyword: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # We can just use the vector store to find the chunks containing similar keywords
    # Vector search is robust enough to act as semantic keyword search
    results = vector_store_manager.search(document_id, keyword, k=5)
    
    sources = []
    for d, score in results:
        sources.append({
            "page_num": d.metadata.get("page_num", 0),
            "similarity_score": float(score),
            "text_snippet": d.page_content[:200]
        })
        
    return {"results": sources}
