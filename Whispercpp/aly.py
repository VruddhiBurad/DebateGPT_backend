import nltk
from transformers import pipeline
import language_tool_python

# -------------------------------
# DOWNLOAD REQUIRED NLTK DATA
# -------------------------------
nltk.download("punkt")
nltk.download("punkt_tab")  # required for Python 3.13+

# -------------------------------
# FILE PATHS
# -------------------------------
RAW_TRANSCRIPT_FILE = "debate_transcript.txt"
FINAL_OUTPUT_FILE = "debate_final_analysis.txt"

# -------------------------------
# 1️⃣ READ RAW TRANSCRIPT
# -------------------------------
with open(RAW_TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
    raw_text = f.read()

# -------------------------------
# 2️⃣ GRAMMAR CORRECTION (IN-MEMORY)
# -------------------------------
print("🧠 Performing grammar correction...")

tool = language_tool_python.LanguageTool("en-US")
matches = tool.check(raw_text)
corrected_text = language_tool_python.utils.correct(raw_text, matches)

# -------------------------------
# 3️⃣ SENTENCE SEGMENTATION
# -------------------------------
sentences = nltk.sent_tokenize(corrected_text)

# -------------------------------
# 4️⃣ SENTIMENT ANALYZER
# -------------------------------
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# -------------------------------
# 5️⃣ ARGUMENT TYPE DETECTION
# -------------------------------
def detect_argument_type(sentence):
    s = sentence.lower()

    if any(k in s for k in ["i think", "i believe", "tea is", "coffee is"]):
        return "Claim"

    if any(k in s for k in ["because", "energy", "focus", "gives", "making"]):
        return "Evidence"

    if any(k in s for k in ["but", "however", "no,", "only", "just"]):
        return "Rebuttal"

    return "Statement"

# -------------------------------
# 6️⃣ WRITE FINAL OUTPUT TXT
# -------------------------------
print("📄 Writing final analysis report...")

with open(FINAL_OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("DEBATE GRAMMAR, SENTIMENT & ARGUMENT ANALYSIS\n")
    out.write("=" * 55 + "\n\n")

    # ---- Corrected Transcript Section ----
    out.write("CORRECTED TRANSCRIPT:\n")
    out.write("-" * 55 + "\n")
    out.write(corrected_text + "\n\n")

    # ---- Sentence-wise Analysis ----
    out.write("SENTENCE-WISE ANALYSIS:\n")
    out.write("-" * 55 + "\n\n")

    count = 1
    for sentence in sentences:
        if not sentence.strip():
            continue

        sentiment = sentiment_analyzer(sentence)[0]

        out.write(f"Sentence {count}:\n")
        out.write(f"Corrected Text : {sentence}\n")
        out.write(f"Sentiment      : {sentiment['label']}\n")
        out.write(f"Confidence     : {round(sentiment['score'], 3)}\n")
        out.write(f"Argument Type  : {detect_argument_type(sentence)}\n")
        out.write("\n" + "-" * 55 + "\n\n")

        count += 1

print("✅ FULL ANALYSIS COMPLETED")
print(f"📄 Final output saved as: {FINAL_OUTPUT_FILE}")
