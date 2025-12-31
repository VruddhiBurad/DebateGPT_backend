import streamlit as st
import requests

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="DebateGPT Chatbot",
    layout="centered"
)

API_URL = "http://localhost:8000/chat"

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello, I am DebateGPT 🤖. How can I help you practice debating?"
        }
    ]

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🗣️ DebateGPT – Practice Chatbot")
st.markdown("Enter a statement and receive a counter-argument.")

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
st.subheader("Chat")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.info(msg["content"])
    else:
        st.success(msg["content"])

# Typing indicator
if st.session_state.is_typing:
    st.warning("🤖 DebateGPT is typing...")

st.markdown("---")

# --------------------------------------------------
# SEND MESSAGE FUNCTION
# --------------------------------------------------
def send_message():
    user_text = st.session_state.input_text.strip()
    if not user_text:
        return

    # 1. Show user message immediately
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )

    # 2. Clear input box
    st.session_state.input_text = ""

    # 3. Show typing indicator
    st.session_state.is_typing = True

# --------------------------------------------------
# INPUT AREA
# --------------------------------------------------
st.subheader("Your Statement")

st.text_input(
    "Type your argument here",
    placeholder="Example: Artificial Intelligence will replace human jobs.",
    key="input_text",
    on_change=send_message
)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📨 Send"):
        send_message()

with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello, I am DebateGPT 🤖. How can I help you practice debating?"
            }
        ]
        st.session_state.input_text = ""
        st.session_state.is_typing = False

# --------------------------------------------------
# BOT RESPONSE
# --------------------------------------------------
if st.session_state.is_typing:
    last_user_message = st.session_state.messages[-1]["content"]

    try:
        response = requests.post(
            API_URL,
            json={"message": last_user_message},
            timeout=120
        )

        if response.status_code == 200:
            bot_reply = response.json().get("reply", "")
        else:
            bot_reply = "Sorry, I couldn't process that request."

    except Exception as e:
        bot_reply = "Error connecting to the chatbot backend."

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    st.session_state.is_typing = False
    st.rerun()