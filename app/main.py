from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.services.chat_service import handle_chat

app = FastAPI(
    title="Lumo",
    description="AI Engineering Companion",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Welcome to Lumo"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = handle_chat(
        mode=request.mode,
        message=request.message
    )

    return response
   