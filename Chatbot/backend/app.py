from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()   # 🔴 THIS LINE IS REQUIRED

OLLAMA_URL = "http://localhost:11434/api/generate"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    payload = {
        "model": "phi3",
        "prompt": req.message,
        "stream": True
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            stream=True,
            timeout=300
        )

        full_response = ""

        for line in response.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                if "response" in data:
                    full_response += data["response"]
                if data.get("done"):
                    break

        if not full_response.strip():
            return {"reply": "⚠️ Model returned no response."}

        return {"reply": full_response.strip()}

    except Exception as e:
        print("Backend error:", e)
        return {"reply": "Sorry, I couldn't process that request."}
