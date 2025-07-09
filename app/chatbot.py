import streamlit as st
import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vectorstore.semantic_search import semantic_search
from models.llm_response import generate_response

st.set_page_config(
    page_title="🛰️ ISRO - MOSDAC Help Bot",
    layout="wide",
    page_icon="🛰️"
)

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/chatbot_queries.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Custom CSS ===
st.markdown("""
    <style>
        body {
            background-color: #f4f8fb;
        }
        .block-container {
            padding-top: 1rem;
        }
        .stTextInput>div>div>input {
            background-color: #1f2c3a;
            color: white;
        }
        .stTextInput>div>div>input::placeholder {
            color: #8ca0b3;
        }
        .stMarkdown {
            font-size: 0.93rem;
        }
        .llm-answer {
            background-color: #e6f7ff;
            border-left: 5px solid #1890ff;
            padding: 10px;
            border-radius: 5px;
        }
        .raw-extract {
            background-color: #fff;
            border-left: 5px solid #888;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# === Sidebar ===
with st.sidebar:
    st.image("assets/isro.jpg", width=200)
    st.markdown("### 🔎 About the Help Bot")
    st.markdown(
        "AI assistant for exploring MOSDAC satellite data and documents using semantic search and embeddings."
    )
    st.markdown("🛰️ Developed for BAH 2025")

st.title("🛰️ ISRO-MOSDAC AI Help Bot")
st.markdown("Ask questions related to Indian satellite missions, data products, or MOSDAC documentation.")

# === Input ===
query = st.text_input("💬 Enter your query:", placeholder="e.g., What is the objective of Megha-Tropiques mission?")

if query:
    st.info(f"🔍 Searching for: **{query}**")
    logging.info(f"User Query: {query}")

    results = semantic_search(query, top_k=3)

    if results:
        st.markdown("### 📚 Retrieved Sources")
        for idx, res in enumerate(results, 1):
            st.markdown(f"📂 **Result {idx}:** {res['source']} → Section: {res['section']}")
            st.markdown(f"📘 **Source Type:** `{res['source_type']}`")
            st.markdown(f"<div class='raw-extract'>📰 <b>Original Extract:</b><br>{res['text']}</div>", unsafe_allow_html=True)

        context = "\n\n".join([res["text"] for res in results])
        prompt = f"Answer the following question using the given context.\n\nContext:\n{context}\n\nQuestion: {query}"

    else:
        st.warning("🚫 No relevant information found.")
        logging.warning("No result found for query.")