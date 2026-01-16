from fastapi import FastAPI
from api.stt_api import router as stt_router
from api.analysis_api import router as analysis_router
from api.winner_api import router as winner_router
from api.chatbot_api import router as chatbot_router
app = FastAPI(title="DebateGPT Backend")

app.include_router(stt_router)
app.include_router(analysis_router)
app.include_router(winner_router)
app.include_router(chatbot_router)
@app.get("/")
def root():
    return {"message": "DebateGPT FastAPI server is running"}
