# MOSDAC AI Help Bot – Starter

This project crawls the MOSDAC portal to download PDF, DOCX, XLSX files, and parses them into clean JSON text. It serves as the first stage for building an AI-powered knowledge-based assistant.

## Folder Structure
- `crawler/`: Downloads files from the MOSDAC site
- `parser/`: Extracts readable content from downloaded files
- `data/mosdac_docs/`: Folder where files are saved
- `data/parsed_docs.json`: Combined output of parsed documents

## How to Run
1. `cd mosdac_help_bot`
2. Install dependencies: `pip install -r requirements.txt`
3. Run crawler: `python crawler/crawl_documents.py`
4. Run parser: `python parser/parse_documents.py`
