"""Scrape Logicbroker KB articles into structured markdown files."""

import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
import html2text

logger = logging.getLogger(__name__)

KB_BASE = "https://support.logicbroker.com"
CATEGORY_SLUGS = [
    "quick-start-guides",
    "supplier-onboarding",
    "retailer-onboarding",
    "document-standards",
    "platform",
    "logicbroker-updates",
]
OUTPUT_DIR = Path("data/kb_articles")

# Polite delay between requests
REQUEST_DELAY = 0.5


def _make_client() -> httpx.Client:
    return httpx.Client(
        timeout=30,
        follow_redirects=True,
        headers={"User-Agent": "LogicbrokerAgent/0.1 (support-kb-indexer)"},
    )


def _extract_article_links(html: str) -> list[str]:
    """Extract article links from a category page."""
    soup = BeautifulSoup(html, "html.parser")
    links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Article URLs have a numeric prefix pattern like 208610377484-slug
        if re.search(r"/kb/logicbroker/\d+-", href):
            full = urljoin(KB_BASE, href.split("?")[0])
            links.add(full)
    return sorted(links)


def _slug_from_url(url: str) -> str:
    """Extract a filename-safe slug from an article URL."""
    path = url.rstrip("/").split("/")[-1]
    # Remove hsLang param if present
    path = path.split("?")[0]
    return path


def _extract_article_content(html: str) -> tuple[str, str]:
    """Extract title and body content from an article page.

    Returns (title, markdown_body).
    """
    soup = BeautifulSoup(html, "html.parser")

    # Title from the page heading
    title_el = soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else "Untitled"

    # Body from .knowledgebase-post container
    body_el = soup.find(class_="knowledgebase-post")
    if not body_el:
        # Fallback: try main content area
        body_el = soup.find("article") or soup.find(class_="hs-kb-content-wrapper")

    if not body_el:
        return title, ""

    converter = html2text.HTML2Text()
    converter.body_width = 0  # Don't wrap lines
    converter.ignore_links = False
    converter.ignore_images = True
    converter.ignore_emphasis = False
    body_md = converter.handle(str(body_el))

    return title, body_md.strip()


def _category_from_url(url: str, category_slug: str) -> str:
    """Map a category slug to a human-readable category name."""
    return category_slug.replace("-", " ").title()


def scrape_category(client: httpx.Client, slug: str) -> list[str]:
    """Fetch a category page and return article URLs found."""
    url = f"{KB_BASE}/kb/logicbroker/{slug}"
    logger.info(f"Fetching category: {slug}")
    try:
        resp = client.get(url)
        resp.raise_for_status()
        links = _extract_article_links(resp.text)
        logger.info(f"  Found {len(links)} articles in {slug}")
        return links
    except httpx.HTTPError as e:
        logger.error(f"  Failed to fetch category {slug}: {e}")
        return []


def scrape_article(
    client: httpx.Client, url: str, category: str, output_dir: Path
) -> bool:
    """Scrape a single article and save as markdown with YAML frontmatter."""
    slug = _slug_from_url(url)
    out_path = output_dir / f"{slug}.md"

    if out_path.exists():
        logger.debug(f"  Skipping (already exists): {slug}")
        return True

    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"  Failed to fetch article {url}: {e}")
        return False

    title, body = _extract_article_content(resp.text)
    if not body:
        logger.warning(f"  No content extracted from {url}")
        return False

    # Write with YAML frontmatter
    frontmatter = (
        f"---\n"
        f"title: \"{title}\"\n"
        f"url: \"{url}\"\n"
        f"category: \"{category}\"\n"
        f"---\n\n"
    )
    out_path.write_text(frontmatter + body, encoding="utf-8")
    return True


def scrape_all(output_dir: Path | None = None) -> dict:
    """Scrape all KB articles across all categories.

    Returns a summary dict with counts.
    """
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    client = _make_client()
    all_urls: dict[str, str] = {}  # url -> category

    # Phase 1: collect all article URLs from category pages
    for slug in CATEGORY_SLUGS:
        links = scrape_category(client, slug)
        category = _category_from_url(slug, slug)
        for link in links:
            if link not in all_urls:
                all_urls[link] = category
        time.sleep(REQUEST_DELAY)

    logger.info(f"Total unique articles found: {len(all_urls)}")

    # Phase 2: scrape each article
    success = 0
    failed = 0
    for url, category in all_urls.items():
        ok = scrape_article(client, url, category, output_dir)
        if ok:
            success += 1
        else:
            failed += 1
        time.sleep(REQUEST_DELAY)

    summary = {
        "total_found": len(all_urls),
        "success": success,
        "failed": failed,
        "output_dir": str(output_dir),
    }
    logger.info(
        f"Scraping complete: {success} saved, {failed} failed out of {len(all_urls)} articles"
    )
    return summary


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    result = scrape_all()
    print(f"\nSummary: {result['success']} saved, {result['failed']} failed "
          f"out of {result['total_found']} articles")
    print(f"Output: {result['output_dir']}")
