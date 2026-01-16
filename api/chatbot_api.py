from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Chatbot.debate_cli import get_chatbot_reply

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class ChatRequest(BaseModel):
    topic: str
    stance: str
    message: str


@router.post("/respond")
def chatbot_respond(data: ChatRequest):
    """
    Returns chatbot debate response
    """
    try:
        reply = get_chatbot_reply(
            topic=data.topic,
            stance=data.stance,
            user_msg=data.message
        )

        return {
            "status": "success",
            "reply": reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
