from collections import defaultdict
import os

# -------------------------------
# PATHS
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# STT files
INPUT_FILE_STT = os.path.join(BASE_DIR, "debate_final_analysis.txt")
OUTPUT_FILE_STT = os.path.join(BASE_DIR, "debate_final_winner.txt")

# Chatbot files
INPUT_FILE_CHATBOT = os.path.join(BASE_DIR, "chatbot_final_analysis.txt")
OUTPUT_FILE_CHATBOT = os.path.join(BASE_DIR, "chatbot_final_winner.txt")


# -------------------------------
# SCORING RULES
# -------------------------------
SENTIMENT_SCORE = {
    "POSITIVE": 1,
    "NEGATIVE": 1,
    "NEUTRAL": 0
}

ARGUMENT_SCORE = {
    "Claim": 1.5,
    "Evidence": 1.5,
    "Rebuttal": 1,
    "Statement": 0
}


# =====================================================
# MAIN FUNCTION (DUAL MODE)
# =====================================================
def run_winner_analysis(mode: str = "stt"):
    """
    mode:
      - 'stt'     → analyze debate_final_analysis.txt
      - 'chatbot' → analyze chatbot_final_analysis.txt
    """

    # -------------------------------
    # SELECT FILES BASED ON MODE
    # -------------------------------
    if mode == "chatbot":
        INPUT_FILE = INPUT_FILE_CHATBOT
        OUTPUT_FILE = OUTPUT_FILE_CHATBOT
    else:
        INPUT_FILE = INPUT_FILE_STT
        OUTPUT_FILE = OUTPUT_FILE_STT

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    # -------------------------------
    # READ FILE
    # -------------------------------
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # -------------------------------
    # PARSING & SCORING
    # -------------------------------
    scores = defaultdict(float)
    stats = defaultdict(lambda: defaultdict(int))

    current_speaker = None
    current_sentiment = None
    current_argument = None

    for line in lines:
        line = line.strip()

        # Detect speaker
        if "User 1:" in line:
            current_speaker = "User 1"
        elif "User 2:" in line:
            current_speaker = "User 2"

        # Detect sentiment
        if line.startswith("Sentiment"):
            current_sentiment = line.split(":")[1].strip()

        # Detect argument type and score
        if line.startswith("Argument Type"):
            current_argument = line.split(":")[1].strip()

            if current_speaker:
                scores[current_speaker] += SENTIMENT_SCORE.get(current_sentiment, 0)
                scores[current_speaker] += ARGUMENT_SCORE.get(current_argument, 0)

                stats[current_speaker][current_sentiment] += 1
                stats[current_speaker][current_argument] += 1

            current_sentiment = None
            current_argument = None

    # -------------------------------
    # DECIDE WINNER
    # -------------------------------
    user1_score = scores["User 1"]
    user2_score = scores["User 2"]

    if user1_score > user2_score:
        winner = "User 1"
    elif user2_score > user1_score:
        winner = "User 2"
    else:
        winner = "Draw"

    # -------------------------------
    # WRITE OUTPUT
    # -------------------------------
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("DEBATE WINNER & PERFORMANCE ANALYSIS\n")
        f.write("=" * 60 + "\n\n")

        for user in ["User 1", "User 2"]:
            f.write(f"{user} PERFORMANCE SUMMARY:\n")
            f.write(f"Total Score : {scores[user]}\n")

            for k, v in stats[user].items():
                f.write(f"{k:<10} : {v}\n")

            f.write("\n" + "-" * 40 + "\n\n")

        f.write(f"🏆 FINAL RESULT: {winner}\n")

    return {
        "mode": mode,
        "winner": winner,
        "scores": {
            "User 1": user1_score,
            "User 2": user2_score
        },
        "output_file": OUTPUT_FILE
    }


# -------------------------------
# CLI MODE
# -------------------------------
if __name__ == "__main__":
    print("Choose mode:")
    print("1 → STT Debate")
    print("2 → Chatbot Debate")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "2":
        result = run_winner_analysis(mode="chatbot")
    else:
        result = run_winner_analysis(mode="stt")

    print("✅ Winner analysis completed")
    print("🏆 Winner:", result["winner"])
    print("📄 Output file:", result["output_file"])
