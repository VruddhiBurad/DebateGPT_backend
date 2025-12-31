import sounddevice as sd
import numpy as np
import noisereduce as nr
import wave
import subprocess
import tempfile
import os
import keyboard
import uuid

sr = 16000  # sample rate used by whisper.cpp
WHISPER_CLI = r"C:\Users\siddh\OneDrive\Desktop\Documents\megaproject\whisper.cpp\Release\whisper-cli.exe"     # your whisper.cpp binary
WHISPER_MODEL = r"C:\Users\siddh\OneDrive\Desktop\Documents\megaproject\whisper.cpp\Release\ggml-small.en.bin"    # your ggml model file


# Write 16-bit WAV for whisper.cpp
def write_wav_int16(path: str, samples: np.ndarray, samplerate: int):
    clipped = np.clip(samples, -1.0, 1.0)
    int16 = (clipped * 32767).astype(np.int16)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(int16.tobytes())


# Run whisper.cpp on WAV → return plain transcript
def transcribe_with_whispercpp(wav_path: str) -> str:
    cmd = [
        WHISPER_CLI,
        "-m", WHISPER_MODEL,
        "-f", wav_path,
        "--no-timestamps"   # ⭐ NO TIMESTAMPS
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = proc.stdout.strip()
    except subprocess.CalledProcessError as e:
        output = ((e.stdout or "") + "\n" + (e.stderr or "")).strip()

    # Clean up: remove empty lines → single clean text line
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    return " ".join(lines)


# RECORD ONE USER TURN
def record_turn(user_id):
    print(f"\n🎤 User {user_id}, start speaking…")
    print("➡ Press CTRL + C to end your turn.\n")

    audio_chunks = []

    try:
        with sd.InputStream(samplerate=sr, channels=1, dtype="float32") as stream:
            while True:
                audio_chunks.append(stream.read(1024)[0])
    except KeyboardInterrupt:
        print("🛑 Turn ended.\n")

    if not audio_chunks:
        print("⚠️ No audio captured.")
        return

    audio = np.concatenate(audio_chunks, axis=0).flatten()

    print("🔇 Reducing noise…")
    cleaned = nr.reduce_noise(y=audio, sr=sr)

    tmp_wav = os.path.join(tempfile.gettempdir(), f"debate_{uuid.uuid4().hex}.wav")
    write_wav_int16(tmp_wav, cleaned, sr)
    print(f"💾 WAV saved: {tmp_wav}")

    print("🧠 Transcribing with whisper.cpp…")
    transcript = transcribe_with_whispercpp(tmp_wav)

    try:
        os.remove(tmp_wav)
    except:
        pass

    print(f"\n===== USER {user_id} TRANSCRIPT =====")
    print(transcript)
    print("=====================================\n")

    debate_log.append({"user": f"User {user_id}", "text": transcript})


# -------------------------------------
# MAIN DEBATE LOOP
# -------------------------------------
debate_log = []

# ------------------- NEW: Ask for debate topic -------------------
topic = input("📝 Enter the debate topic: ").strip()
print(f"\n🎙 The debate topic is: '{topic}'\n")

print("🎙 TWO-USER DEBATE MODE (whisper.cpp)")
print("CTRL + C → End user turn")
print("CTRL + D → Save & Exit\n")
print("User 1 starts.\n")

current_user = 1

while True:
    print(f"👉 Press ENTER to start User {current_user}'s turn…")

    try:
        input()

        if keyboard.is_pressed("ctrl+d"):
            raise EOFError

        record_turn(current_user)

        current_user = 2 if current_user == 1 else 1

        if keyboard.is_pressed("ctrl+d"):
            raise EOFError

    except EOFError:
        print("\n🟥 CTRL + D detected — Ending debate.\n")
        break


# -------------------------------------
# SAVE TRANSCRIPT
# -------------------------------------
filename = "debate_transcript.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"========== FULL DEBATE ==========\n")
    f.write(f"Topic: {topic}\n\n")
    for entry in debate_log:
        f.write(f"{entry['user']}:\n{entry['text']}\n\n")
    f.write("=================================\n")

print(f"📄 Transcript saved as: {filename}")
