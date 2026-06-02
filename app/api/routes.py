from fastapi import APIRouter

from app.models.chat import ChatRequest
from app.services.chat_service import handle_chat


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Welcome to Lumo"}


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/chat")
def chat(request: ChatRequest):
    return handle_chat(
        message=request.message,
        retrieval_mode=request.retrieval_mode,
        embedding_provider=request.embedding_provider,
    )
