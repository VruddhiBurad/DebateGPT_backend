from fastapi import APIRouter, HTTPException
from Whispercpp.winner import run_winner_analysis

router = APIRouter(prefix="/winner", tags=["Winner"])


@router.post("/run")
def run_winner():
    """
    Runs winner analysis and returns result
    """
    try:
        result = run_winner_analysis()
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
