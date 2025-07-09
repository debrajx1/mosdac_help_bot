import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of MOSDAC
BASE_URL = "https://www.mosdac.gov.in"

# Allowed extensions 
ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.xlsx']

# Where to save files
DOWNLOAD_DIR = "mosdac_docs"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to download a file
def download_file(file_url):
    local_filename = os.path.join(DOWNLOAD_DIR, file_url.split("/")[-1])
    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except Exception as e:
        print(f"Failed to download {file_url}: {e}")

# Crawl all document links from the page
def crawl_documents(start_url):
    visited = set()
    to_visit = [start_url]

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all links
            for link_tag in soup.find_all("a", href=True):
                href = link_tag['href']
                file_url = urljoin(current_url, href)

                # If it's a document link
                if any(file_url.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                    download_file(file_url)

                # Internal page? Add to queue
                elif BASE_URL in file_url and file_url not in visited:
                    to_visit.append(file_url)

        except Exception as e:
            print(f"Error visiting {current_url}: {e}")

# Start crawling
if __name__ == "__main__":
    crawl_documents(BASE_URL)
