# models/llm_response.py

import os
import streamlit as st
from gpt4all import GPT4All

# ✅ Set correct model name and path for Mistral GGUF model
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

# ✅ Check if model exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file not found: {MODEL_PATH}")

# ✅ Cache the model load so it's not reloaded on every Streamlit rerun
@st.cache_resource
def load_model():
    return GPT4All(model_name=MODEL_NAME, model_path=MODEL_DIR, allow_download=False)

# ✅ Load model only once
llm = load_model()

# ✅ Generate response wrapper
def generate_response(prompt):
    try:
        response = llm.generate(prompt, max_tokens=256, temp=0.7)
        return response.strip()
    except Exception as e:
        return f"❌ Error generating response: {e}"