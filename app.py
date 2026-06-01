# =========================================================
# ASP CHATBOT - PROFESSIONAL UI UPGRADE VERSION
# =========================================================

import streamlit as st
from groq import Groq
import json
import time

# =========================================================
# API KEY
# =========================================================
client = Groq(
    api_key=""
)

# =========================================================
# MODEL
# =========================================================
MODEL = "llama-3.3-70b-versatile"

# =========================================================
# LOAD MEMORY
# =========================================================
with open("memory.json", "r", encoding="utf-8") as f:
    memory = json.load(f)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ASP Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CUSTOM UI (PROFESSIONAL ANIMATIONS)
# =========================================================
st.markdown("""
<style>

/* ===== GLOBAL ===== */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ===== BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #0b1220);
    color: white;
}

/* ===== HEADER ANIMATION ===== */
@keyframes fadeInDown {
    from {opacity: 0; transform: translateY(-20px);}
    to {opacity: 1; transform: translateY(0);}
}

.title {
    font-size: 44px;
    font-weight: 700;
    animation: fadeInDown 0.8s ease-in-out;
    color: #ffffff;
}

.subtitle {
    color: #94a3b8;
    margin-top: -10px;
    animation: fadeInDown 1s ease-in-out;
}

/* ===== LOGO STYLING ===== */
.logo {
    border-radius: 50%;
    box-shadow: 0px 0px 25px rgba(14,165,233,0.4);
    transition: 0.3s;
}

.logo:hover {
    transform: scale(1.05);
}

/* ===== CHAT ANIMATION ===== */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

[data-testid="stChatMessage"] {
    animation: fadeIn 0.4s ease-in-out;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 10px;
    transition: 0.3s;
}

/* Hover effect */
[data-testid="stChatMessage"]:hover {
    transform: scale(1.01);
}

/* ===== CHAT INPUT ===== */
.stChatInput input {
    border-radius: 12px !important;
    border: 2px solid #0ea5e9 !important;
    box-shadow: 0px 0px 15px rgba(14,165,233,0.2);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #0b1220;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.5);
}

/* ===== BUTTON ===== */
.stButton>button {
    border-radius: 10px;
    background-color: #0f766e;
    color: white;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background-color: #14b8a6;
}

/* ===== TYPING DOTS ===== */
.dot {
  width: 8px;
  height: 8px;
  background-color: #0ea5e9;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.2s infinite ease-in-out;
  margin-right: 3px;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image("star_logo.png", width=160)

    st.title("ASP Chatbot")

    st.markdown("""
### Features
- Smart AI Responses  
- Career Inference  
- Memory-Based Chat  
- Cybersecurity Focus  
- Smooth UI Animations  
""")

    st.divider()

    st.markdown("""
### About ASP
ASP Chatbot is an AI assistant designed for learning, cybersecurity guidance, and personal development.
""")

# =========================================================
# HEADER (PROFESSIONAL LAYOUT)
# =========================================================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("star_logo.png", width=90)

with col2:
    st.markdown('<p class="title">ASP Chatbot</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Personal AI Assistant of Ali Shehzan Punjwani</p>', unsafe_allow_html=True)

st.divider()

# =========================================================
# AI FUNCTION (UNCHANGED)
# =========================================================
def ask_ai(user_input):

    system_prompt = f"""
You are ASP Chatbot.

Memory:
{json.dumps(memory, indent=2)}

Be natural, human-like, and professional.
Never mention memory.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# INPUT
# =========================================================
user_input = st.chat_input("Ask ASP Chatbot anything...")

# =========================================================
# PROCESS
# =========================================================
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        # typing animation
        st.markdown("""
        <div>
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
            <span style="margin-left:10px;">ASP is thinking...</span>
        </div>
        """, unsafe_allow_html=True)

        response = ask_ai(user_input)

        placeholder = st.empty()
        typed = ""

        for char in response:
            typed += char
            time.sleep(0.01)
            placeholder.markdown(typed)

    st.session_state.messages.append({"role": "assistant", "content": response})