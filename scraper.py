import re
import httpx
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    try:
        if "linkedin.com/jobs/view" in url:
            return _scrape_linkedin(url)
        return _scrape_normal(url)
    except Exception as e:
        print(f"Scraping error: {e}")
        return None


def _scrape_linkedin(url: str) -> str:
    job_id = re.search(r'/jobs/view/(\d+)', url)
    if not job_id:
        raise ValueError("Could not extract LinkedIn Job ID")

    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id.group(1)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = httpx.get(api_url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def _scrape_normal(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text if len(text) > 300 else None
