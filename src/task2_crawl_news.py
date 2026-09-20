"""Collect public AI20K programme pages as structured JSON.

The selected pages are first-party VinUni/Vingroup sources. A deterministic
``article_NN.json`` is overwritten on reruns, so crawling does not create
timestamped duplicates.

Facebook posts are crawled with a headless Playwright browser because
Facebook requires JavaScript rendering. The playwright package must be
installed (pip install playwright && python -m playwright install chromium).
"""

import asyncio
import json
import re
import hashlib
import unicodedata
from urllib.parse import urljoin, urlsplit, urlunsplit, parse_qsl, urlencode
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_markdown


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLE_URLS = [
    # --- VinUni official website (crawled with requests) ---
    "https://vinuni.edu.vn/aithucchien/",
    (
        "https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-"
        "nhan-tai-ai-thuc-chien-khoa-co-ban/"
    ),
    (
        "https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-"
        "khoa-2-3-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien-cua-"
        "tap-doan-vingroup/"
    ),
    (
        "https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-hanh-trinh-cua-"
        "nhung-nguoi-dam-thu-thach/"
    ),
    (
        "https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-"
        "trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/"
    ),
    (
        "https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao-"
        "the-he-nhan-tai-ai-cho-mot-the-gioi-dang-doi-thay/"
    ),
    # --- Official Facebook page: Đào tạo Nhân tài AI thực chiến (crawled with Playwright) ---
    "https://www.facebook.com/share/p/19VnUE1HCw/",
    "https://www.facebook.com/share/p/19R69XNq9q/",
    (
        "https://www.facebook.com/DaotaoNhantaiAIthucchien/posts/"
        "pfbid0Q84nkwiExfSXfMzGQydHUHhR45eVgcXAxiKLYkwtwpHMeif4zB522WGXfQge1Uzal"
    ),
]

# URLs that require a headless browser (JavaScript-rendered pages)
_BROWSER_URLS: frozenset[str] = frozenset(
    url for url in ARTICLE_URLS if "facebook.com" in url
)


def _clean_markdown(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.replace("\xa0", " ").replace("\u200b", "")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"(?m)^Mục lục\s*$", "", value)
    # Exclude personal contact details; retain the institutional hotline.
    value = re.sub(r"(?im)^.*(?:Ms\. Phương Thảo|email protected|email-protection).*$", "", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()



def expand_tables(content) -> None:
    """Repeat merged cells so Markdown preserves each row's associations."""
    for table in content.select('table'):
        grid = {}
        rows = table.select('tr')
        for row_index, row in enumerate(rows):
            column = 0
            for cell in row.find_all(['td', 'th'], recursive=False):
                while (row_index, column) in grid:
                    column += 1
                text = cell.get_text(' ', strip=True)
                height, width = int(cell.get('rowspan', 1)), int(cell.get('colspan', 1))
                for y in range(height):
                    for x in range(width):
                        grid[row_index + y, column + x] = text
                column += width
        if not grid:
            continue
        replacement = BeautifulSoup('<table></table>', 'html.parser')
        width = max(c for _, c in grid) + 1
        for r in range(len(rows)):
            row = replacement.new_tag('tr')
            for c in range(width):
                cell = replacement.new_tag('th' if r == 0 else 'td')
                cell.string = grid.get((r, c), '')
                row.append(cell)
            replacement.table.append(row)
        table.replace_with(replacement.table)


def _crawl_article_sync(url: str) -> dict[str, str]:
    response = requests.get(
        url,
        timeout=60,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/131 Safari/537.36"
            )
        },
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding

    soup = BeautifulSoup(response.text, "html.parser")
    for node in soup.select(
        "script, style, noscript, svg, iframe, .sidebar, "
        ".related-posts, .social-share, .cookie-notice"
    ):
        node.decompose()

    title_node = soup.select_one("h1")
    metadata_title = soup.select_one('meta[property="og:title"]')
    title = (
        title_node.get_text(" ", strip=True)
        if title_node
        else metadata_title.get("content", "").strip()
        if metadata_title
        else soup.title.get_text(" ", strip=True)
        if soup.title
        else "Unknown"
    )

    candidates = [
        node
        for selector in (
            "article",
            ".entry-content",
            ".article-content",
            ".entry-body",
            ".doc-page",
            ".post-content",
            "main",
            "body",
        )
        if (node := soup.select_one(selector)) is not None
        and len(node.get_text(" ", strip=True)) >= 200
    ]
    if not candidates:
        raise ValueError("No article content found")
    content = candidates[0]

    if url == ARTICLE_URLS[0]:
        # Programme sections only; omit carousel repeats, personal profiles,
        # testimonials, news navigation and the site footer.
        sections = soup.select(
            '.overview-section, .differences-section, .program-info-section, '
            '.admission-section, .faq-section'
        )
        if len(sections) != 5:
            raise ValueError('Programme page structure changed; review selectors')
        content = BeautifulSoup(''.join(str(node) for node in sections), 'html.parser')
        # Remove identical adjacent paragraphs introduced by responsive markup.
        previous = None
        for paragraph in content.select('p'):
            current = paragraph.get_text(' ', strip=True)
            if current and current == previous:
                paragraph.decompose()
            previous = current

    # FAQ questions are buttons: preserve their text alongside the answers.
    for node in content.select('button'):
        node.unwrap()
    for node in content.select('img, picture, video, audio, source, nav, footer, .toc'):
        node.decompose()
    for link in content.select('a[href]'):
        if not link.get_text(' ', strip=True):
            link.decompose()
            continue
        parts = urlsplit(urljoin(url, link['href']))
        query = [(k, v) for k, v in parse_qsl(parts.query) if k != 'fbclid' and not k.startswith('utm_')]
        link['href'] = urlunsplit(parts._replace(query=urlencode(query)))

    expand_tables(content)

    markdown = _clean_markdown(
        html_to_markdown(str(content), heading_style="ATX", strip=["img"])
    )
    if len(markdown) < 200:
        raise ValueError(f"Extracted content is too short ({len(markdown)} chars)")
    if 'thực chiến' not in markdown.lower() or 'vinuni' not in markdown.lower():
        raise ValueError('Page does not explicitly identify the VinUni AI programme')

    def meta(name: str) -> str:
        node = soup.find('meta', attrs={'property': name})
        return str(node.get('content', '')) if node else ''

    return {
        "url": url,
        "title": title,
        "date_crawled": datetime.now(timezone.utc).isoformat(),
        "content_markdown": markdown,
        "date_published": meta('article:published_time'),
        "date_modified": meta('article:modified_time'),
        "publisher": "VinUni",
        "topic": "Thông tin chính thống về chương trình đào tạo Nhân tài AI thực chiến VinUni",
        "content_sha256": hashlib.sha256(markdown.encode('utf-8')).hexdigest(),
        "extraction_version": "2",
    }


def _crawl_facebook_sync(url: str) -> dict[str, str]:
    """Crawl a public Facebook post using a headless Playwright browser.

    Facebook renders content with JavaScript, so requests-based crawling
    returns only a login wall. Playwright loads the full page before extraction.
    """
    from playwright.sync_api import sync_playwright  # lazy import; optional dep

    # Use the system Chrome installation to avoid downloading a separate browser
    _CHROME_PATHS = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_exe = next((p for p in _CHROME_PATHS if Path(p).is_file()), None)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True,
            executable_path=chrome_exe,
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="vi-VN",
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60_000)
        # Wait for the post text to render
        page.wait_for_timeout(5_000)

        # Close login/cookie dialogs if present
        for selector in (
            '[aria-label="Close"]',
            '[data-testid="cookie-policy-manage-dialog-accept-button"]',
        ):
            try:
                btn = page.query_selector(selector)
                if btn:
                    btn.click()
                    page.wait_for_timeout(1_000)
            except Exception:
                pass

        html = page.content()
        context.close()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # Try og:title first (most reliable for FB posts)
    og_title = soup.select_one('meta[property="og:title"]')
    og_desc = soup.select_one('meta[property="og:description"]')
    title = (
        og_title.get("content", "").strip() if og_title
        else soup.title.get_text(" ", strip=True) if soup.title
        else "Facebook – Đào tạo Nhân tài AI thực chiến"
    )

    # Extract visible post text from common FB post containers
    text_parts: list[str] = []
    for selector in (
        '[data-ad-comet-preview="message"]',
        '[data-testid="post_message"]',
        '.userContent',
        'div[dir="auto"]',
    ):
        for node in soup.select(selector):
            part = node.get_text(" ", strip=True)
            if len(part) > 50 and part not in text_parts:
                text_parts.append(part)

    # Fallback: og:description
    if not text_parts and og_desc:
        desc = og_desc.get("content", "").strip()
        if desc:
            text_parts.append(desc)

    if not text_parts:
        raise ValueError(f"No post text found in Facebook page: {url}")

    # Deduplicate while preserving order (FB pages repeat text in responsive markup)
    seen: set[str] = set()
    unique_parts: list[str] = []
    for part in text_parts:
        key = re.sub(r"\s+", " ", part).strip()
        if key not in seen:
            seen.add(key)
            unique_parts.append(part)

    combined = "\n\n".join(unique_parts)
    markdown = _clean_markdown(combined)

    if len(markdown) < 100:
        raise ValueError(f"Facebook post content too short ({len(markdown)} chars): {url}")

    # Relaxed validation for Facebook: programme keyword is sufficient
    lower = markdown.lower()
    if not any(kw in lower for kw in ('thực chiến', 'ai20k', 'vingroup', 'nhân tài ai')):
        raise ValueError(
            f"Facebook post does not appear to be about the AI20K programme: {url}"
        )

    return {
        "url": url,
        "title": title,
        "date_crawled": datetime.now(timezone.utc).isoformat(),
        "content_markdown": markdown,
        "date_published": "",
        "date_modified": "",
        "publisher": "Đào tạo Nhân tài AI thực chiến (Facebook)",
        "topic": "Thông tin chính thống về chương trình đào tạo Nhân tài AI thực chiến VinUni",
        "content_sha256": hashlib.sha256(markdown.encode('utf-8')).hexdigest(),
        "extraction_version": "2",
    }


async def crawl_article(url: str) -> dict[str, str]:
    """Fetch and extract one public page without blocking the event loop."""
    if url in _BROWSER_URLS:
        return await asyncio.to_thread(_crawl_facebook_sync, url)
    return await asyncio.to_thread(_crawl_article_sync, url)


async def crawl_all() -> None:
    """Crawl each source and save one deterministic JSON file per URL."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    failures = []

    for index, url in enumerate(ARTICLE_URLS, 1):
        try:
            article = await crawl_article(url)
            output = DATA_DIR / f"article_{index:02d}.json"
            output.write_text(
                json.dumps(article, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Saved: {output}")
        except Exception as error:
            print(f"Failed: {url} — {error}")
            failures.append(url)
    if failures:
        raise RuntimeError(f'Crawl failed for {len(failures)} source(s): {failures}')


if __name__ == "__main__":
    asyncio.run(crawl_all())
