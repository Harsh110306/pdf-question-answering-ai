from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db, SessionLocal
from app.models.schemas import ChatSessionCreate, ChatSessionResponse, QueryInput, QueryResponse, ChatMessageResponse
from app.services.chat_history import create_session, get_session, add_message, get_history
from app.services.rag_pipeline import rag_pipeline
from app.services.pdf_generator import create_chat_pdf
import json
import os
import tempfile
from typing import List

router = APIRouter()

@router.post("/session", response_model=ChatSessionResponse)
def create_chat_session(session_in: ChatSessionCreate, db: Session = Depends(get_db)):
    session = create_session(db, session_in.document_id)
    return session

@router.get("/session/{session_id}", response_model=ChatSessionResponse)
def get_chat_session(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/message", response_model=QueryResponse)
def send_message(query: QueryInput, db: Session = Depends(get_db)):
    """
    Standard blocking endpoint for chat.
    """
    session = get_session(db, query.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Add user message
    add_message(db, query.session_id, "user", query.question)
    
    # Query RAG
    result = rag_pipeline.query(session.document_id, query.question)
    
    # Add AI message
    add_message(db, query.session_id, "ai", result["answer"])
    
    return result

@router.post("/message/stream")
def send_message_stream(query: QueryInput, db: Session = Depends(get_db)):
    """
    Streaming endpoint using SSE.
    """
    session = get_session(db, query.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Add user message to DB
    add_message(db, query.session_id, "user", query.question)
    
    def event_stream():
        full_answer = ""
        sources = []
        for chunk in rag_pipeline.query_stream(session.document_id, query.question):
            if chunk.startswith("__SOURCES__:"):
                sources = json.loads(chunk.split("__SOURCES__:")[1])
            else:
                full_answer += chunk
                yield chunk
                
        # Save AI message in a new session to avoid closed transaction issues inside generator
        with SessionLocal() as local_db:
            add_message(local_db, query.session_id, "ai", full_answer)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@router.get("/session/{session_id}/history", response_model=List[ChatMessageResponse])
def get_chat_history_endpoint(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return get_history(db, session_id)

@router.get("/session/{session_id}/download")
def download_chat_pdf(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    messages = get_history(db, session_id)
    if not messages:
        raise HTTPException(status_code=400, detail="No messages in this chat session")
        
    # Generate PDF in a temporary file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, f"chat_history_{session_id}.pdf")
    
    create_chat_pdf(messages, pdf_path)
    
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"Chat_Summary_{session.document.filename}.pdf"
    )
