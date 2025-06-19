import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

BASE_URL = "https://dharashiv.maharashtra.gov.in/"
SAVE_DIR = "docs"
TIMEOUT = 20  # Increased timeout for slower pages

def is_valid_link(url):
    # Skip links that are not useful or problematic
    invalid_keywords = [".pdf", "#", "tel:", "mailto:"]
    return not any(keyword in url.lower() for keyword in invalid_keywords)

def scrape_all_pages(base_url):
    visited = set()
    to_visit = [base_url]
    os.makedirs(SAVE_DIR, exist_ok=True)
    all_text = ""

    while to_visit:
        url = to_visit.pop()
        if url in visited or not url.startswith(base_url) or not is_valid_link(url):
            continue
        try:
            print(f"Crawling: {url}")
            response = requests.get(url, timeout=TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            all_text += f"\n\n=== {url} ===\n\n{text}"
            visited.add(url)

            # Collect internal links
            links = [urljoin(url, link.get("href")) for link in soup.find_all("a", href=True)]
            to_visit.extend(links)
        except requests.exceptions.ReadTimeout:
            print(f"Timeout: {url}")
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    with open(f"{SAVE_DIR}/dharashiv_all.txt", "w", encoding="utf-8") as f:
        f.write(all_text)

if __name__ == "__main__":
    scrape_all_pages(BASE_URL)
