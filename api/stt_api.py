from fastapi import APIRouter, UploadFile, File, HTTPException
from Whispercpp.debate_whispercpp import run_whisper_file
import tempfile
import os

router = APIRouter(prefix="/stt", tags=["Speech To Text"])

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Receives WAV file from Android,
    runs STT,
    saves transcript to debate_transcript.txt
    """

    try:
        # -----------------------
        # 1. Save uploaded audio
        # -----------------------
        suffix = os.path.splitext(file.filename)[1] or ".wav"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            wav_path = tmp.name

        # -----------------------
        # 2. Run STT
        # -----------------------
        transcript = run_whisper_file(wav_path)

        # -----------------------
        # 3. Save transcript
        # -----------------------
        transcript_file = "debate_transcript.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)

        # -----------------------
        # 4. Cleanup
        # -----------------------
        os.remove(wav_path)

        return {
            "status": "success",
            "message": "Transcription completed",
            "transcript_file": transcript_file
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
