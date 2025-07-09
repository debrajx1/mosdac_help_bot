# txt_to_json_converter.py (Updated with sub-section support)

import os
import json
import re

# Input/Output paths
TXT_DIR = "data/static_pages"
OUTPUT_JSON = "data/static_pages/parsed_static_pages.json"

# Regex to match markdown-style headers: # Header or ## Subheader
header_pattern = re.compile(r'^(#+)\s*(.+)')

def parse_txt_file(filepath):
    sections = {}
    current_main = None
    current_sub = None
    content_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            match = header_pattern.match(stripped)
            if match:
                # Save existing content before switching
                if current_sub and content_lines:
                    key = f"{current_main} - {current_sub}"
                    sections[key] = " ".join(content_lines).strip()
                elif current_main and content_lines:
                    sections[current_main] = " ".join(content_lines).strip()

                content_lines = []
                level, title = len(match.group(1)), match.group(2).strip()

                if level == 1:
                    current_main = title
                    current_sub = None
                elif level == 2 and current_main:
                    current_sub = title
            else:
                content_lines.append(stripped)

    # Save last section
    if current_sub and content_lines:
        key = f"{current_main} - {current_sub}"
        sections[key] = " ".join(content_lines).strip()
    elif current_main and content_lines:
        sections[current_main] = " ".join(content_lines).strip()

    return sections

# Parse all .txt files
parsed_data = {}
for filename in os.listdir(TXT_DIR):
    if filename.endswith(".txt"):
        filepath = os.path.join(TXT_DIR, filename)
        doc_key = filename.replace(".txt", "").lower()
        parsed_data[doc_key] = parse_txt_file(filepath)
        print(f"✅ Parsed: {filename}")

# Write to JSON
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

print(f"\n📁 JSON written to: {OUTPUT_JSON}")
