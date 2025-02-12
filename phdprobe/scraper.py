import os
import re
import json
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm



# A naive dictionary for subdomain "tagging" or classification.
# You might expand this to do more advanced clustering or use an NLP approach.
SUBDOMAIN_KEYWORDS = {
    "robotics": ["robotics", "robot", "autonomous systems"],
    "deep learning": ["deep learning", "neural networks"],
    "data science": ["data science", "data analytics"],
    "theoretical ml": ["theoretical ml", "theory of machine learning", "theoretical computer science"]
}



def is_valid_url(url, base_domain):
    """ Check if a URL is valid and points to the same domain (or subdomain) """
    # TODO: extend to check for specific paths or patterns
    if not url.startswith("http") or not url.startswith("/".join(base_domain.split("/")[:-1])):
        return False
    parsed_base = urlparse(base_domain)
    parsed_url = urlparse(url)
    # Only follow links within the same domain or subdomain
    return parsed_url.netloc.endswith(parsed_base.netloc)

def fetch_html(url):
    """ Fetch HTML content from a given URL with error handling. """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except (requests.HTTPError, requests.Timeout, requests.ConnectionError) as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

def parse_program_info(html_text):
    """ Extract minimal data points from the HTML; extractors should be customized to match the structure of each site """
    soup = BeautifulSoup(html_text, 'html.parser')
    # Example data we might want:
    program_name = soup.find("h1")  # Very naive approach
    acceptance_rate = None
    funding_info = None
    # Example: parse acceptance rate if you find a pattern like "Acceptance Rate: XX%"
    # This is naive; you'll need site-specific logic or more robust patterns.
    text_content = soup.get_text(separator=" ").lower()
    match_rate = re.search(r"acceptance rate:\s*([\d.]+)\s*%", text_content)
    if match_rate:
        acceptance_rate = float(match_rate.group(1))
    # Example: parse funding info if there's a heading "Funding" followed by text
    # (This is a placeholder; actual logic will vary.)
    if "funding" in text_content:
        # Do further extraction or just store a flag for demonstration
        funding_info = "Available (exact details not parsed)"
    if program_name:
        program_name = program_name.get_text(strip=True)
    else:
        program_name = "Unknown Program"
    return {
        "program_name": program_name,
        "acceptance_rate": acceptance_rate,
        "funding_info": funding_info,
    }

def classify_subdomains(text):
    """ Very naive approach: look for keywords in the text to tag the program. TODO: use embeddings and a similarity search instead """
    tags = []
    lower_text = text.lower()
    for domain, keywords in SUBDOMAIN_KEYWORDS.items():
        if any(k in lower_text for k in keywords):
            tags.append(domain)
    return tags

def scrape_phd_program(url, university_name):
    """ Main function to fetch a program page, parse the data, classify subdomains, and return a dictionary. """
    html = fetch_html(url)
    if not html:
        return None  # Skip if failed to fetch
    program_data = parse_program_info(html)
    # Use entire page text for subdomain classification
    tags = classify_subdomains(html)
    program_data["subdomains"] = tags
    # You might also store the source URL for reference:
    program_data["source_url"] = url
    return program_data

def save_program_data(program_data, university_name):
    """ Save a single program's data in a local subdirectory: data/<university_name>/, storing as a JSON for now """
    # Ensure directory exists
    output_dir = os.path.join("data", university_name)
    os.makedirs(output_dir, exist_ok=True)
    # Create a filename from the program name (sanitized).
    # Alternatively, you might create a unique ID.
    file_name = program_data["program_name"].replace(" ", "_").lower() + ".json"
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(program_data, f, indent=2)
    print(f"[INFO] Saved data to {file_path}")


def scrape_all_links(start_url, university_name, max_depth=2):
    """ Scrape recursively up to `max_depth` levels of links, saving each page's HTML. Return a list of file paths for offline parsing. """
    visited = set()       # Keep track of visited URLs to avoid duplication
    to_visit = [(start_url, 0)]  # Queue or stack for BFS/DFS
    saved_files = []
    # Prepare output directory
    output_dir = os.path.join("data", university_name)
    html_out_dir = os.path.join(output_dir, "html")
    os.makedirs(html_out_dir, exist_ok=True)
    while to_visit:
        current_url, depth = to_visit.pop(0)
        if depth > max_depth:
            break
        if current_url in visited:
            continue
        visited.add(current_url)
        html_content = fetch_html(current_url)
        if not html_content:
            continue
        # Save locally
        file_id = len(saved_files) + 1
        file_name = f"{file_id}.html"
        file_path = os.path.join(html_out_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        saved_files.append(file_path)
        # Find links for next depth level
        soup = BeautifulSoup(html_content, "html.parser")
        for link_tag in tqdm(soup.find_all("a", href=True), desc=f"Processing links from {current_url}"):
            next_url = urljoin(current_url, link_tag['href'])
            # Keep only valid internal URLs
            if is_valid_url(next_url, start_url):
                if next_url not in visited:
                    to_visit.append((next_url, depth+1))
    return saved_files