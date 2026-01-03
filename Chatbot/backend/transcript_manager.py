import os

TRANSCRIPT_DIR = "transcripts"
TRANSCRIPT_FILE = "debate_transcript.txt"

def save_message(role: str, content: str):
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    file_path = os.path.join(TRANSCRIPT_DIR, TRANSCRIPT_FILE)

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{role.upper()}: {content}\n")
