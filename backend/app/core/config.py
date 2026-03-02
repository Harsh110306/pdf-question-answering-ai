import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF QA System"
    API_V1_STR: str = "/api/v1"
    
    # DB Configuration
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    
    # Vector DB
    VECTOR_STORE_PATH: str = "./.faiss_store"
    
    # Embedding model
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"

settings = Settings()
