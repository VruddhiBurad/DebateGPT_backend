from fastapi import APIRouter, HTTPException
from Analyzer.aly import analyze_debate

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("/stt")
def analyze_stt():
    """
    Analyze STT debate transcript
    """
    try:
        result = analyze_debate(mode="stt")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbot")
def analyze_chatbot():
    """
    Analyze chatbot debate transcript
    """
    try:
        result = analyze_debate(mode="chatbot")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

