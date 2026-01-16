from fastapi import APIRouter, HTTPException
from Analyzer.winner import run_winner_analysis

router = APIRouter(prefix="/winner", tags=["Winner"])


@router.post("/stt")
def run_winner_stt():
    """
    Runs winner analysis for STT debate
    """
    try:
        result = run_winner_analysis(mode="stt")
        return {
            "status": "success",
            "data": result
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="debate_final_analysis.txt not found. Run analysis first."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chatbot")
def run_winner_chatbot():
    """
    Runs winner analysis for Chatbot debate
    """
    try:
        result = run_winner_analysis(mode="chatbot")
        return {
            "status": "success",
            "data": result
        }

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="chatbot_final_analysis.txt not found. Run chatbot analysis first."
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
