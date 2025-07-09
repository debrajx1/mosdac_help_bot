# 🛰️ ISRO-MOSDAC AI Help Bot

An AI-powered chatbot built for the [MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre)](https://mosdac.gov.in/) portal. It intelligently answers user queries using live crawled content, scientific documents, semantic search, and optionally a local LLM like Orca-Mini.

---

## ✅ Features

- 🌐 Crawl static and PDF content from the MOSDAC portal
- 📄 Parse documents into structured JSON
- 🔍 Semantic search using Sentence-BERT + FAISS
- 🤖 Optionally use local LLMs (via GPT4All) for fluent responses
- 💬 Streamlit-based chatbot UI with ISRO theme
- 🔁 Hybrid retrieval: combines static page + document results
- 📝 Logs all user queries and answers

---

## 📁 Project Structure

```plaintext
mosdac_help_bot/
├── app/                        → Streamlit chatbot UI
├── assets/                    → Logo and static images
├── crawler/                   → Static & document crawling scripts
├── data/                      → Parsed data and downloaded PDFs
├── logs/                      → Query logs
├── models/                   → Local LLM handler (GPT4All)
├── parser/                   → PDF parsing module
├── vectorstore/              → Semantic embedding & FAISS search
├── txt_to_json.py            → Converts sectioned .txt to JSON
├── requirements.txt          → Dependencies
└── README.md                 → This file

## How to Run
1. `cd mosdac_help_bot`
2. Install dependencies: `pip install -r requirements.txt`
3. Run crawler: `python crawler/crawl_documents.py`
4. Run parser: `python parser/parse_documents.py`
5. Convert Static Texts to JSON: `python txt_to_json.py`
6. Create Vector Index: `python vectorstore/embed_and_index.py`
7. Run the Chatbot (Streamlit UI): `streamlit run app/chatbot.py`