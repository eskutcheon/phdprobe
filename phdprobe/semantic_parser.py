import os
import json
from transformers import pipeline
from bs4 import BeautifulSoup
import re

# Initialize a Hugging Face QA pipeline (this downloads or uses a local model).
# You can swap for a summarization pipeline if you prefer.
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def extract_text_from_html(html_content):
    """ Simple text extraction from HTML. Might remove scripts/styles and combine text """
    soup = BeautifulSoup(html_content, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    # Get raw text
    text = soup.get_text(separator="\n")
    return text.strip()


def find_admissions_requirements(text, chunk_size=500):
    """ Use a QA pipeline to search for "What are the admission requirements?" across large text. Because text can be huge, we chunk it.
        Returns:
            List[str] - answers or relevant text segments
    """
    # Normalize text
    text = text.replace("\n", " ")
    # Split into chunks of ~chunk_size tokens (naive splitting by words)
    words = text.split()
    segments = []
    for i in range(0, len(words), chunk_size):
        seg = " ".join(words[i:i+chunk_size])
        segments.append(seg)
    answers = []
    for seg in segments:
        # If the segment doesn't even contain "require" or "admission", skip to save time
        if not re.search(r"(requirement|admission|gre|toefl)", seg.lower()):
            continue
        # Attempt QA
        try:
            res = qa_pipeline({
                "context": seg,
                "question": "What are the admission requirements?"
            })
            # The QA model might not always find a relevant answer, check the score
            if res["score"] > 0.2:  # threshold is arbitrary, adjust as needed
                answers.append(res["answer"])
        except Exception as e:
            # The pipeline may fail on certain text, skip gracefully
            continue
    # Combine answers or keep them separate
    if not answers:
        return None
    return answers

def parse_html_files(file_paths, university_name):
    """ Go through each local HTML file, parse the text, run QA for "requirements," and store results in a JSON (one overall file or one per page) """
    results = []
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        text = extract_text_from_html(html_content)
        qa_answers = find_admissions_requirements(text)
        # Basic data structure
        if not qa_answers:
            continue
        page_data = {
            "file_path": file_path,
            "requirements_text": qa_answers,
        }
        results.append(page_data)
    # Save a consolidated JSON
    output_path = os.path.join("data", university_name, "requirements_parsed.json")
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"[INFO] Parsed data saved to {output_path}")
    return results
