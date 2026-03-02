from sqlalchemy.orm import Session
from app.models.domain import ChatSession, ChatMessage
from typing import List

def create_session(db: Session, document_id: str) -> ChatSession:
    db_session = ChatSession(document_id=document_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: str) -> ChatSession:
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()

def add_message(db: Session, session_id: str, role: str, content: str) -> ChatMessage:
    msg = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_history(db: Session, session_id: str) -> List[ChatMessage]:
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
