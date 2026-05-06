import re
import httpx
from scrapling.fetchers import Fetcher
from scrapling.parser import Selector

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
        raise ValueError("Could not extract LinkedIn Job ID from URL")

    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id.group(1)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = httpx.get(api_url, headers=headers, timeout=15)
    response.raise_for_status()

    page = Selector(response.text)
    return page.get_text(strip=True)


def _scrape_normal(url: str) -> str:
    page = Fetcher.get(url, stealthy_headers=True, timeout=15)
    text = page.get_text(strip=True)

    if len(text) < 300:
        raise ValueError(f"Page returned too little text ({len(text)} chars)")

    return text
