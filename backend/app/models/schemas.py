from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Document Schemas
class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: str
    upload_date: datetime
    
    class Config:
        from_attributes = True

# Chat Schemas
class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class ChatMessageResponse(MessageBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionCreate(BaseModel):
    document_id: str

class ChatSessionResponse(BaseModel):
    id: str
    document_id: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True

class QueryInput(BaseModel):
    session_id: str
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    sources: List[dict] = []
