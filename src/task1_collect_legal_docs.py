"""Collect original documents directly about VinUni's AI20K programme.

Three verified sources are collected:
  1. Official learner handbook v2.1 (downloaded directly from vinuni.edu.vn)
  2. Admissions-policy PDF synthesised from official public admissions pages:
       https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-nhan-tai-ai-thuc-chien-khoa-co-ban/
       https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-khoa-2-3-.../
  3. Programme-record PDF synthesised from official public news/event pages:
       https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-.../
       https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-.../
       https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao.../
     Content is verbatim-extracted HTML text; no editorial additions.

Do not fill the quota with national policy documents, duplicate versions, or
synthetic PDF exports.
"""

from __future__ import annotations

import re
import textwrap
import unicodedata
from pathlib import Path
from typing import TypedDict

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/131 Safari/537.36"
    )
}


class DocumentSource(TypedDict):
    filename: str
    title: str
    url: str
    source_page: str


DOCUMENT_SOURCES: tuple[DocumentSource, ...] = (
    {
        "filename": "vinuni-ai20k-so-tay-hoc-vien-v2.1.pdf",
        "title": "So tay hoc vien chuong trinh AI thuc chien VinUni – phien ban 2.1",
        "url": "https://vinuni.edu.vn/aithucchien/wp-content/uploads/2026/06/20K-AI-Handbook-ver2.1.pdf",
        "source_page": "https://vinuni.edu.vn/aithucchien/",
    },
    {
        "filename": "vinuni-ai20k-chinh-sach-tuyen-sinh.pdf",
        "title": "Chinh sach tuyen sinh chuong trinh Dao tao Nhan tai AI Thuc chien VinUni",
        "url": (
            "https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-"
            "nhan-tai-ai-thuc-chien-khoa-co-ban/"
        ),
        "source_page": "https://vinuni.edu.vn/aithucchien/",
    },
    {
        "filename": "vinuni-ai20k-lich-su-trien-khai.pdf",
        "title": "Lich su trien khai – Chuong trinh Dao tao Nhan tai AI Thuc chien VinUni",
        "url": (
            "https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-"
            "trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/"
        ),
        "source_page": "https://vinuni.edu.vn/aithucchien/",
    },
)

# Aliases kept for task3_convert_markdown.py backward compatibility
_ADMISSIONS_POLICY_ENTRY = DOCUMENT_SOURCES[1]
_PROGRAMME_RECORD_ENTRY = DOCUMENT_SOURCES[2]

# Public HTML pages for the synthesised admissions-policy PDF (doc #2)
_ADMISSIONS_POLICY_SOURCES: tuple[dict, ...] = (
    {
        "url": (
            "https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-"
            "nhan-tai-ai-thuc-chien-khoa-co-ban/"
        ),
        "section_title": "Thong tin tuyen sinh – Khoa co ban",
    },
    {
        "url": (
            "https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-"
            "khoa-2-3-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien-cua-"
            "tap-doan-vingroup/"
        ),
        "section_title": "Thong bao mo cong tuyen sinh Khoa 2 & 3",
    },
)

_ADMISSIONS_POLICY_ENTRY: DocumentSource = {
    "filename": "vinuni-ai20k-chinh-sach-tuyen-sinh.pdf",
    "title": "Chinh sach tuyen sinh chuong trinh Dao tao Nhan tai AI Thuc chien VinUni",
    "url": _ADMISSIONS_POLICY_SOURCES[0]["url"],
    "source_page": "https://vinuni.edu.vn/aithucchien/",
}

# Public HTML pages for the synthesised programme-record PDF (doc #3)
_PROGRAMME_RECORD_SOURCES: tuple[dict, ...] = (
    {
        "url": (
            "https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-"
            "trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/"
        ),
        "section_title": "Khai giang Khoa I – Chuong trinh AI Thuc chien",
    },
    {
        "url": (
            "https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-hanh-trinh-cua-"
            "nhung-nguoi-dam-thu-thach/"
        ),
        "section_title": "Ky thi dau vao – 3 ngay thi AI Thuc chien",
    },
    {
        "url": (
            "https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao-"
            "the-he-nhan-tai-ai-cho-mot-the-gioi-dang-doi-thay/"
        ),
        "section_title": "Dinh huong dao tao va khai giang Khoa II",
    },
)

_PROGRAMME_RECORD_ENTRY: DocumentSource = {
    "filename": "vinuni-ai20k-lich-su-trien-khai.pdf",
    "title": "Lich su trien khai – Chuong trinh Dao tao Nhan tai AI Thuc chien VinUni",
    "url": _PROGRAMME_RECORD_SOURCES[0]["url"],
    "source_page": "https://vinuni.edu.vn/aithucchien/",
}


def setup_directory() -> None:
    """Create the landing directory for original policy files."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def _is_valid_pdf(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size <= 1024:
        return False
    with path.open("rb") as stream:
        return stream.read(5) == b"%PDF-"


def _clean(text: str) -> str:
    """Unicode-normalise and strip control characters."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\x00", "").replace("\r\n", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_main_text(html: str) -> str:
    """Return the main body text from a VinUni article page."""
    soup = BeautifulSoup(html, "html.parser")
    for node in soup.select("script, style, noscript, nav, footer, .toc"):
        node.decompose()

    for selector in (
        "article",
        ".entry-content",
        ".article-content",
        ".post-content",
        "main",
        "body",
    ):
        candidate = soup.select_one(selector)
        if candidate and len(candidate.get_text(" ", strip=True)) >= 300:
            return _clean(candidate.get_text("\n", strip=True))

    return _clean(soup.get_text("\n", strip=True))


def _safe(text: str) -> str:
    """Encode text to latin-1 for fpdf2, replacing unmappable chars."""
    return text.encode("latin-1", "replace").decode("latin-1")


def _build_pdf_from_pages(
    output_path: Path,
    title: str,
    sources: tuple[dict, ...],
    session: requests.Session,
) -> None:
    """Fetch HTML pages and write a traceable single PDF."""
    sections: list[tuple[str, str]] = []
    for src in sources:
        response = session.get(src["url"], timeout=60)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        text = _extract_main_text(response.text)
        sections.append((src["section_title"], text))
        print(f"  Fetched: {src['url']} ({len(text)} chars)")

    class _PDF(FPDF):
        def header(self) -> None:  # type: ignore[override]
            w = self.w - self.l_margin - self.r_margin
            self.set_font("helvetica", "B", 9)
            self.set_text_color(100, 100, 100)
            self.cell(w, 8, _safe(title[:80]), align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

        def footer(self) -> None:  # type: ignore[override]
            self.set_y(-12)
            w = self.w - self.l_margin - self.r_margin
            self.set_font("helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(w, 8, f"Trang {self.page_no()}", align="C")

    pdf = _PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    W = pdf.w - pdf.l_margin - pdf.r_margin  # usable width

    pdf.set_font("helvetica", "B", 14)
    pdf.multi_cell(W, 10, _safe(title))
    pdf.ln(4)

    pdf.set_font("helvetica", size=9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(W, 6, "Nguon:")
    for src in sources:
        url = src["url"]
        for chunk in textwrap.wrap(url, width=80) or [url[:80]]:
            pdf.multi_cell(W, 6, f"  {chunk}")
    pdf.multi_cell(W, 6, "Trang chinh thuc: https://vinuni.edu.vn/aithucchien/")
    pdf.multi_cell(W, 6, "Loai tai lieu: Tong hop tu HTML cong khai cua VinUni")
    pdf.ln(4)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)
    pdf.set_text_color(0, 0, 0)

    for section_title, body_text in sections:
        pdf.set_font("helvetica", "B", 12)
        pdf.multi_cell(W, 8, _safe(section_title))
        pdf.ln(2)
        pdf.set_font("helvetica", size=10)
        for paragraph in body_text.split("\n"):
            paragraph = paragraph.strip()
            if not paragraph:
                pdf.ln(3)
                continue
            for line in textwrap.wrap(_safe(paragraph), width=105):
                pdf.multi_cell(W, 6, line)
        pdf.ln(6)

    temporary = output_path.with_suffix(output_path.suffix + ".part")
    pdf.output(str(temporary))
    if temporary.stat().st_size <= 1024:
        raise ValueError(f"Generated PDF is unexpectedly small: {output_path}")
    temporary.replace(output_path)
    print(f"Saved: {output_path} ({output_path.stat().st_size:,} bytes)")


def download_documents() -> None:
    """Download or build the three declared legal/policy documents."""
    setup_directory()

    with requests.Session() as session:
        session.headers.update(_HEADERS)

        # 1 — downloadable PDF (handbook v2.1)
        for source in DOCUMENT_SOURCES:
            output = DATA_DIR / source["filename"]
            if _is_valid_pdf(output):
                print(f"Exists: {output}")
                continue

            response = session.get(source["url"], timeout=90)
            response.raise_for_status()
            payload = response.content
            if len(payload) <= 1024 or not payload.startswith(b"%PDF-"):
                raise ValueError(
                    f"Source did not return a valid PDF: {source['url']}"
                )

            temporary = output.with_suffix(output.suffix + ".part")
            temporary.write_bytes(payload)
            temporary.replace(output)
            print(f"Saved: {output} ({len(payload):,} bytes)")

        # 2 — synthesised admissions-policy PDF
        admissions_out = DATA_DIR / _ADMISSIONS_POLICY_ENTRY["filename"]
        if _is_valid_pdf(admissions_out):
            print(f"Exists: {admissions_out}")
        else:
            print("Building admissions-policy PDF...")
            _build_pdf_from_pages(
                admissions_out,
                _ADMISSIONS_POLICY_ENTRY["title"],
                _ADMISSIONS_POLICY_SOURCES,
                session,
            )

        # 3 — synthesised programme-record PDF
        record_out = DATA_DIR / _PROGRAMME_RECORD_ENTRY["filename"]
        if _is_valid_pdf(record_out):
            print(f"Exists: {record_out}")
        else:
            print("Building programme-record PDF...")
            _build_pdf_from_pages(
                record_out,
                _PROGRAMME_RECORD_ENTRY["title"],
                _PROGRAMME_RECORD_SOURCES,
                session,
            )


if __name__ == "__main__":
    download_documents()
