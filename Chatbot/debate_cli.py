import ollama
import os
from datetime import datetime

# -----------------------------
# FILE SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "chatbot_debate_transcript.txt")


def get_chatbot_reply(topic: str, stance: str, user_msg: str) -> str:
    """
    Generates debate reply using Ollama and saves transcript.
    """

    # create file if not exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== DEBATE GPT TRANSCRIPT ===\n")

    # save user input
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\n")
        f.write("USER:\n")
        f.write(user_msg + "\n\n")

    prompt = f"""
You are Debate GPT.

STRICT RULES:
- Do NOT use any greetings or formal openings.
- Give ONLY 2–3 short sentences.
- Be clear, simple, and direct.
- No headings, no bullet points.

Debate topic: {topic}
User stance: {stance}
User argument: {user_msg}

Now write a very short debate response that goes AGAINST the user's stance.
"""

    # -----------------------------
    # CALL OLLAMA (API MODE → no streaming)
    # -----------------------------
    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role": "system", "content": "You are a debate assistant. Follow rules strictly."},
            {"role": "user", "content": prompt}
        ]
    )

    bot_reply = response["message"]["content"]

    # save bot output
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("DEBATE GPT:\n")
        f.write(bot_reply + "\n")
        f.write("=" * 60 + "\n")

    return bot_reply

# -----------------------------
# TEST MODE (run from terminal)
# -----------------------------
if __name__ == "__main__":
    print("=== Debate GPT (Terminal Mode) ===")
    print("Type 'exit' to stop the debate.\n")

    topic = input("Enter debate topic: ")
    stance = input("Choose your side (favor / against): ")

    while True:
        msg = input("\nYour argument:\n> ")

        if msg.lower() == "exit":
            break

        reply = get_chatbot_reply(topic, stance, msg)

        print("\nDebate GPT says:")
        print(reply)

    # -----------------------------
    # SAVE FINAL COPY IN PROJECT ROOT
    # -----------------------------
    CHATBOT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(CHATBOT_DIR, ".."))

    FINAL_FILE = os.path.join(PROJECT_ROOT, "chatbot_debate_transcript.txt")

    # copy content from chatbot folder log to project root
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as src:
            content = src.read()

        with open(FINAL_FILE, "w", encoding="utf-8") as dest:
            dest.write(content)

        print("\nDebate saved in project root as:")
        print(FINAL_FILE)
    else:
        print("\n No debate log found to save.")


