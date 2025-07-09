# crawler/crawl_static_pages.py

import requests
from bs4 import BeautifulSoup
import os
import json
import time

MOSDAC_URLS = {
    # Satellite Missions
    "insat_3d": "https://mosdac.gov.in/insat-3d",
    "insat_3dr": "https://mosdac.gov.in/insat-3dr",
    "insat_3a": "https://mosdac.gov.in/insat-3a",
    "insat_3ds": "https://mosdac.gov.in/insat-3ds",
    "kalpana_1": "https://mosdac.gov.in/kalpana-1",
    "meghatropiques": "https://mosdac.gov.in/megha-tropiques",
    "saral_altika": "https://mosdac.gov.in/saral-altika",
    "oceansat_2": "https://mosdac.gov.in/oceansat-2",
    "oceansat_3": "https://mosdac.gov.in/oceansat-3",
    "scatsat_1": "https://mosdac.gov.in/scatsat-1",

    # Applications
    "weather_applications": "https://mosdac.gov.in/weather",
    "energy_applications": "https://mosdac.gov.in/energy",

    # Others
    "validation": "https://mosdac.gov.in/validation",
    "data_quality": "https://mosdac.gov.in/data-quality",
    "weather_reports": "https://mosdac.gov.in/weather-reports",
    "tools": "https://mosdac.gov.in/tools",
    "faq": "https://mosdac.gov.in/faq-page"
}

os.makedirs("data/static_pages", exist_ok=True)
parsed_data = {}

def extract_sections(soup):
    sections = {}
    current_heading = "Introduction"
    buffer = []

    for tag in soup.find_all(['h2', 'h3', 'p', 'li']):
        if tag.name in ['h2', 'h3']:
            if buffer:
                sections[current_heading] = "\n".join(buffer).strip()
                buffer = []
            current_heading = tag.get_text(strip=True)
        elif tag.name in ['p', 'li']:
            text = tag.get_text(strip=True)
            if text and len(text) > 30:
                buffer.append(text)

    if buffer:
        sections[current_heading] = "\n".join(buffer).strip()

    return sections

# Crawl each URL
for name, url in MOSDAC_URLS.items():
    print(f"⏳ Crawling: {url}")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Skipped {name}: {e}")
        continue

    soup = BeautifulSoup(resp.content, "html.parser")

    # Remove unwanted tags
    for tag in soup(['nav', 'header', 'footer', 'script', 'style', 'noscript']):
        tag.decompose()

    sections = extract_sections(soup)
    parsed_data[name] = sections

    with open(f"data/static_pages/{name}.json", "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved: {name} ({len(sections)} sections)")
    time.sleep(1)

# Save combined JSON
with open("data/static_pages/parsed_static_pages.json", "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)

print("✅ Done crawling and saving section-wise content.")
