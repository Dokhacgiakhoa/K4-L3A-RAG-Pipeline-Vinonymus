"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

1. Trích xuất văn bản từ PDF trong data/landing/legal/ sang data/standardized/legal/.
2. Đọc JSON từ data/landing/news/ và sinh Markdown có header nguồn sang data/standardized/news/.
3. Đảm bảo mỗi file Markdown đều có nội dung hoàn chỉnh (>= 200 ký tự).
"""

import json
from pathlib import Path
import pypdfium2


ROOT_DIR = Path(__file__).resolve().parent.parent
LANDING_DIR = ROOT_DIR / "data" / "landing"
OUTPUT_DIR = ROOT_DIR / "data" / "standardized"

def convert_legal_docs() -> None:
    """Convert toàn bộ PDF trong data/landing/legal sang data/standardized/legal."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in legal_dir.iterdir():
        if path.suffix.lower() not in {".pdf", ".doc", ".docx"}:
            continue

        md_path = output_dir / f"{path.stem}.md"
        extracted_text = ""

        try:
            doc = pypdfium2.PdfDocument(path)
            pages_text = []
            for page_idx, page in enumerate(doc, 1):
                text_page = page.get_textpage()
                page_content = text_page.get_text_range().strip()
                if page_content:
                    pages_text.append(f"<!-- Page {page_idx} -->\n{page_content}")
            extracted_text = "\n\n".join(pages_text).strip()
        except Exception as err:
            print(f"[WARN] Lỗi đọc PDF {path.name}: {err}")

        header = f"# {path.stem.replace('-', ' ').title()}\n\n**Source File:** `{path.name}`\n\n---\n\n"
        md_content = header + extracted_text
        md_path.write_text(md_content, encoding="utf-8")
        print(f"[OK] Legal MD: {md_path.name} ({len(md_content):,} chars)")


def convert_news_articles() -> None:
    """Convert toàn bộ JSON trong data/landing/news sang data/standardized/news."""
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in news_dir.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        header = (
            f"# {data['title']}\n\n"
            f"**Source:** {data.get('url', '')}\n\n"
            f"**Crawled:** {data.get('date_crawled', '')}\n\n---\n\n"
        )
        md_content = header + data.get("content_markdown", "")
        md_path = output_dir / f"{path.stem}.md"
        md_path.write_text(md_content, encoding="utf-8")
        print(f"[OK] News MD: {md_path.name} ({len(md_content):,} chars)")


def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"\nChuẩn hóa hoàn tất! Thư mục đích: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
