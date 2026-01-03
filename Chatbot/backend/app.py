from fastapi import FastAPI
from backend.ollama_client import call_ollama
from backend.prompts import debate_prompt
from backend.models import ChatRequest, ChatResponse

app = FastAPI(title="DebateGPT Chatbot API")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    prompt = debate_prompt(request.message)
    reply = call_ollama(prompt)
    return ChatResponse(reply=reply)
