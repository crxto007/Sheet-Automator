import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    """
    Fetches a URL and returns clean text content.
    """
    try:
        # Set a User-Agent to avoid being blocked by some websites
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove elements that typically don't contain useful job info
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        # Extract text and clean up whitespace
        text = soup.get_text(separator=" ")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        clean_text = " ".join(lines)
        
        return clean_text
    except Exception as e:
        print(f"Scraping error: {e}")
        return None
