from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    retrieval_mode: str = "keyword"
    embedding_provider: str = "local_hashing"
