import os
import streamlit as st
import faiss
import numpy as np
from groq import Groq
from sentence_transformers import SentenceTransformer

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="STAR AI Cybersecurity Assistant")
st.title("STAR - AI Cybersecurity Assistant")
st.write("Ask cybersecurity questions using RAG + Groq + Llama 3.1")

# -----------------------------
# API KEY
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found. Add it in Streamlit secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()

# -----------------------------
# KNOWLEDGE BASE
# -----------------------------
documents = [
    """
    Risk assessment is the process of identifying vulnerabilities,
    threats, and weaknesses in a system.
    """,

    """
    Risk management is the process of reducing, controlling,
    and handling identified risks after assessment.
    """,

    """
    Firewall is a network security device that monitors
    incoming and outgoing traffic.
    """,

    """
    IDS stands for Intrusion Detection System.
    IPS stands for Intrusion Prevention System.
    """,

    """
    VPN stands for Virtual Private Network.
    It encrypts communication over public networks.
    """,

    """
    CIA Triad includes Confidentiality, Integrity, and Availability.
    """
]

# -----------------------------
# VECTOR DATABASE
# -----------------------------
@st.cache_resource
def build_vectorstore():
    doc_embeddings = embedding_model.encode(documents)

    dimension = doc_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(doc_embeddings).astype("float32"))
    return index

index = build_vectorstore()

# -----------------------------
# RETRIEVAL
# -----------------------------
def retrieve_context(query, k=2):
    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), k
    )

    retrieved_docs = [documents[i] for i in indices[0]]
    return "\n".join(retrieved_docs)

# -----------------------------
# CHATBOT
# -----------------------------
def cybersecurity_chatbot(user_question):
    context = retrieve_context(user_question)

    prompt = f"""
You are a cybersecurity assistant chatbot.

Use the provided cybersecurity context to answer clearly
in easy wording.

Context:
{context}

Question:
{user_question}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )

    return completion.choices[0].message.content

# -----------------------------
# UI
# -----------------------------
question = st.text_input("Ask your cybersecurity question:")

if st.button("Submit"):
    if question:
        with st.spinner("Generating answer..."):
            response = cybersecurity_chatbot(question)
            st.success(response)
    else:
        st.warning("Please enter a question.")
