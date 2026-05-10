# ============================================
# CYBERSECURITY RAG CHATBOT USING GROQ + GRADIO
# ============================================

# Install required libraries
!pip install groq gradio sentence-transformers faiss-cpu pypdf

# Imports
import os
import gradio as gr
import faiss
import numpy as np
from groq import Groq
from sentence_transformers import SentenceTransformer

# ============================================
# SET YOUR GROQ API KEY
# ============================================

GROQ_API_KEY = "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"   # Replace with your real API key
client = Groq(api_key=GROQ_API_KEY)

# ============================================
# LOAD EMBEDDING MODEL
# ============================================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ============================================
# SAMPLE CYBERSECURITY KNOWLEDGE BASE
# You can replace these with your own notes/files
# ============================================

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

# ============================================
# CREATE VECTOR DATABASE
# ============================================

doc_embeddings = embedding_model.encode(documents)

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings).astype("float32"))

# ============================================
# RETRIEVAL FUNCTION
# ============================================

def retrieve_context(query, k=2):
    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"), k
    )

    retrieved_docs = [documents[i] for i in indices[0]]
    return "\n".join(retrieved_docs)

# ============================================
# CHAT FUNCTION
# ============================================

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
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )

    answer = completion.choices[0].message.content
    return answer

# ============================================
# GRADIO FRONTEND
# ============================================

interface = gr.Interface(
    fn=cybersecurity_chatbot,
    inputs=gr.Textbox(
        lines=3,
        placeholder="Ask cybersecurity question here..."
    ),
    outputs=gr.Textbox(lines=10),
    title="Cybersecurity RAG Chatbot",
    description="Ask cybersecurity questions using Groq + Llama 3.1 + RAG"
)

interface.launch(share=True)
