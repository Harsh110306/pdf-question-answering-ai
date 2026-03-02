from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings

def get_embedding_model():
    """
    Returns the configured HuggingFace embedding model.
    """
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
