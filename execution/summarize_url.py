"""
Summarize URL — Execution Script
Fetches a webpage, extracts its text content, and returns an LLM-generated summary.

Usage:
    python execution/summarize_url.py <url>

Requires:
    pip install requests beautifulsoup4 openai python-dotenv
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MAX_CHARS = 32_000  # ~8k tokens — keeps us well within context limits


def fetch_page_text(url: str) -> str:
    """Fetch a URL and extract its visible text content."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DOE-Framework/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove non-content elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return text[:MAX_CHARS]


def summarize_text(text: str, url: str) -> str:
    """Send extracted text to OpenAI and return a concise summary."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise summarizer. Given the text content of a webpage, "
                    "produce a clear, bullet-pointed summary capturing the key points. "
                    "Keep it under 300 words."
                ),
            },
            {
                "role": "user",
                "content": f"Summarize this page ({url}):\n\n{text}",
            },
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python execution/summarize_url.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Fetching: {url}")

    try:
        text = fetch_page_text(url)
        print(f"Extracted {len(text)} characters. Summarizing...\n")
        summary = summarize_text(text, url)
        print(summary)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
