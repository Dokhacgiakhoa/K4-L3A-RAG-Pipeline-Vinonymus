"""Normalize policy documents and crawled pages into traceable Markdown."""

import hashlib
import json
import re
import unicodedata
from pathlib import Path

import requests
from markitdown import MarkItDown

from src.task1_collect_legal_docs import (
    DOCUMENT_SOURCES,
    _ADMISSIONS_POLICY_ENTRY,
    _ADMISSIONS_POLICY_SOURCES,
    _PROGRAMME_RECORD_ENTRY,
    _PROGRAMME_RECORD_SOURCES,
    _extract_main_text,
)


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/131 Safari/537.36"
    )
}

# The handbook is the only *real* PDF in the legal landing folder.
_REAL_PDF_FILENAME = "vinuni-ai20k-so-tay-hoc-vien-v2.1.pdf"

# Synthesized documents are built from HTML — bypass the PDF intermediate.
_SYNTHESIZED_DOCS = (
    {
        "entry": _ADMISSIONS_POLICY_ENTRY,
        "sources": _ADMISSIONS_POLICY_SOURCES,
    },
    {
        "entry": _PROGRAMME_RECORD_ENTRY,
        "sources": _PROGRAMME_RECORD_SOURCES,
    },
)


def _normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.replace("\x00", "").replace("\r\n", "\n")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{4,}", "\n\n\n", value)
    return value.strip()


def convert_real_pdf_docs() -> None:
    """Convert real (non-synthesized) PDF files using MarkItDown.

    Only ``vinuni-ai20k-so-tay-hoc-vien-v2.1.pdf`` qualifies — it is a
    genuine PDF downloaded directly from VinUni and its font supports proper
    text extraction.  The two synthesized PDFs are intentionally skipped here
    because they were built with a Latin-1 font that strips Vietnamese
    diacritics; ``convert_synthesized_legal_docs()`` handles those instead.
    """
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)
    converter = MarkItDown()
    metadata = {source["filename"]: source for source in DOCUMENT_SOURCES}

    for path in sorted(legal_dir.iterdir()):
        if path.suffix.lower() not in {".pdf", ".doc", ".docx"}:
            continue
        if path.name != _REAL_PDF_FILENAME:
            # Synthesized PDFs are handled by convert_synthesized_legal_docs()
            continue
        if path.name not in metadata:
            raise ValueError(
                f"Unreviewed legal source: {path.name}; add verified provenance first"
            )

        result = converter.convert(str(path))
        content = _normalize_text(result.text_content)
        if len(content) < 200:
            raise ValueError(f"Converted legal document is too short: {path}")

        source = metadata[path.name]
        title = source["title"]
        source_url = source["source_page"]
        header = (
            f"# {title}\n\n"
            f"- **Landing file:** `data/landing/legal/{path.name}`\n"
            f"- **Public source:** {source_url}\n"
            f"- **Original download:** {source['url']}\n"
            f"- **Landing SHA256:** {hashlib.sha256(path.read_bytes()).hexdigest()}\n"
            f"- **Document type:** legal\n\n"
            "---\n\n"
        )
        output = output_dir / f"{path.stem}.md"
        output.write_text(header + content + "\n", encoding="utf-8")
        print(f"Converted (PDF): {path} -> {output}")


def convert_synthesized_legal_docs() -> None:
    """Convert synthesized legal documents directly from their HTML sources.

    The two synthesized PDFs (admissions-policy and programme-record) were
    built by task1 using fpdf2 with a Latin-1 font, which silently replaces
    every Vietnamese character with '?'.  This function bypasses the lossy PDF
    intermediate entirely: it crawls the original HTML pages, extracts clean
    Unicode text, and writes the Markdown output directly — preserving all
    diacritics correctly.
    """
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)
    landing_dir = LANDING_DIR / "legal"

    with requests.Session() as session:
        session.headers.update(_HEADERS)

        for doc in _SYNTHESIZED_DOCS:
            entry = doc["entry"]
            sources = doc["sources"]

            # Collect and concatenate text from all HTML source pages.
            sections: list[str] = []
            all_urls: list[str] = []
            for src in sources:
                response = session.get(src["url"], timeout=60)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or "utf-8"
                text = _extract_main_text(response.text)
                section_heading = f"## {src['section_title']}\n\n"
                sections.append(section_heading + _normalize_text(text))
                all_urls.append(src["url"])
                print(f"  Fetched: {src['url']} ({len(text):,} chars)")

            content = "\n\n---\n\n".join(sections)
            if len(content) < 200:
                raise ValueError(
                    f"Synthesized content too short for: {entry['filename']}"
                )

            # Use the PDF landing file's SHA256 for traceability (still valid
            # as a stable landing-file fingerprint even though we bypass it
            # for text extraction).
            pdf_path = landing_dir / entry["filename"]
            sha256 = (
                hashlib.sha256(pdf_path.read_bytes()).hexdigest()
                if pdf_path.is_file()
                else "n/a (PDF not present)"
            )

            source_urls_md = "\n".join(
                f"  - {u}" for u in all_urls
            )
            header = (
                f"# {entry['title']}\n\n"
                f"- **Landing file:** `data/landing/legal/{entry['filename']}`\n"
                f"- **Public source:** {entry['source_page']}\n"
                f"- **HTML sources (direct):**\n{source_urls_md}\n"
                f"- **Landing SHA256:** {sha256}\n"
                f"- **Document type:** legal\n"
                f"- **Extraction method:** HTML → Markdown (PDF bypassed — Latin-1 font)\n\n"
                "---\n\n"
            )

            stem = entry["filename"].replace(".pdf", "")
            output = output_dir / f"{stem}.md"
            output.write_text(header + content + "\n", encoding="utf-8")
            print(f"Converted (HTML->MD): {entry['filename']} -> {output}")


def convert_news_articles() -> None:
    """Convert article JSON files while retaining required provenance fields."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)
    required = {"url", "title", "date_crawled", "content_markdown"}

    for path in sorted(news_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = required - data.keys()
        if missing:
            raise ValueError(f"{path} is missing fields: {sorted(missing)}")
        if any(not str(data[field]).strip() for field in required):
            raise ValueError(f"{path} contains empty required metadata")

        content = _normalize_text(str(data["content_markdown"]))
        if len(content) < 200:
            raise ValueError(f"Article content is too short: {path}")

        header = (
            f"# {data['title']}\n\n"
            f"- **Landing file:** `data/landing/news/{path.name}`\n"
            f"- **Public source:** {data['url']}\n"
            f"- **Crawled (UTC):** {data['date_crawled']}\n"
            f"- **Published:** {data.get('date_published') or 'Not supplied'}\n"
            f"- **Modified:** {data.get('date_modified') or 'Not supplied'}\n"
            f"- **Content SHA256:** {hashlib.sha256(data['content_markdown'].encode('utf-8')).hexdigest()}\n"
            f"- **Document type:** news\n\n"
            "---\n\n"
        )
        output = output_dir / f"{path.stem}.md"
        output.write_text(header + content + "\n", encoding="utf-8")
        print(f"Converted: {path} -> {output}")


def convert_all() -> None:
    """Convert every supported landing file into standardized Markdown."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_real_pdf_docs()
    convert_synthesized_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
