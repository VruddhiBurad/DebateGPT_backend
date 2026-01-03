import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def call_ollama(user_message: str) -> str:
    payload = {
        "model": "phi3",
        "prompt": user_message,
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
                if data.get("done", False):
                    break

        if full_response.strip() == "":
            return "⚠️ Model returned empty response."

        return full_response.strip()

    except Exception as e:
        print("Ollama error:", e)
        return "Sorry, I couldn't process that request."
