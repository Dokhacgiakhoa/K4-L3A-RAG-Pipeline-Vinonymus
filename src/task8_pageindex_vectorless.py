"""
Task 8 — PageIndex vectorless fallback.

1. Tìm kiếm theo cấu trúc cây văn bản / mục lục (vectorless retrieval).
2. Nếu có PAGEINDEX_API_KEY, gọi service ngoài; nếu không hoặc lỗi, fallback sang
   tìm kiếm theo tiêu đề tài liệu và đoạn mục lục chuẩn hóa.
3. Parse kết quả thành SearchResult có retrieval_method = "pageindex".
"""

import os
from pathlib import Path
import re
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
STANDARDIZED_DIR = ROOT_DIR / "data" / "standardized"
PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs (nếu dùng service PageIndex bên ngoài)."""
    print(f"PageIndex API key configured: {'Yes' if PAGEINDEX_API_KEY else 'No (using local vectorless index)'}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Tìm kiếm vectorless dựa trên cấu trúc tài liệu / mục lục và từ khóa tiêu đề."""
    if not query.strip():
        return []

    query_lower = query.lower()
    query_terms = [t for t in query_lower.split() if len(t) > 2]

    candidates = []
    
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        if not path.is_file():
            continue

        raw = path.read_text(encoding="utf-8")
        sections = re.split(r"\n(?=##?\s+)", raw)
        doc_type = "legal" if "legal" in path.parts else "news"

        for sec_idx, sec in enumerate(sections):
            sec_clean = sec.strip()
            if not sec_clean:
                continue

            sec_lower = sec_clean.lower()
            # Tính điểm tương đồng theo số lượng từ khóa xuất hiện trong tiêu đề/đoạn
            matches = sum(1 for term in query_terms if term in sec_lower)
            if matches > 0:
                score = min(1.0, 0.5 + (matches * 0.1))
                candidates.append({
                    "id": f"{path.stem}-pageindex-{sec_idx}",
                    "content": sec_clean[:800],
                    "score": round(score, 6),
                    "metadata": {
                        "source": path.name,
                        "title": path.stem.replace("-", " ").title(),
                        "doc_type": doc_type,
                        "url": None,
                        "chunk_index": sec_idx,
                    },
                    "retrieval_method": "pageindex",
                })

    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[:top_k]


if __name__ == "__main__":
    upload_documents()
    res = pageindex_search("SFIA", top_k=2)
    print(f"Found {len(res)} results with pageindex method")
