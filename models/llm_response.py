import os
from gpt4all import GPT4All

MODEL_NAME = "orca-mini-3b.q4_0.gguf"
MODEL_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

llm = GPT4All(model_name=MODEL_NAME, model_path=MODEL_DIR, allow_download=False)

def generate_response(prompt):
    try:
        return llm.generate(prompt, max_tokens=256, temp=0.7).strip()
    except Exception as e:
        return f"❌ Error: {e}"
