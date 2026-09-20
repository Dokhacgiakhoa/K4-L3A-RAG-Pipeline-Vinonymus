"""
Task 1 — Thu thập tài liệu chính sách/quy định/cẩm nang đào tạo.

Thu thập tối thiểu 3 tài liệu PDF từ các nguồn dữ liệu chính thức của chương trình:
1. 20k-ai-handbook-ver2.1.pdf: Sổ tay chương trình Đào tạo Nhân tài AI Thực chiến (Vingroup & VinUni).
2. ai-mentor-blueprint.pdf: Bản thiết kế kiến trúc hệ thống AI Mentor & Khung đánh giá.
3. demo-slides.pdf: Slide quy chuẩn và lộ trình đào tạo chuyên sâu.
"""

from pathlib import Path
import shutil


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "landing" / "legal"
VINONYMUS_DIR = Path("D:/Github/K4-3A-e403-Vinonymus")


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Sao chép và thiết lập 3 tài liệu PDF từ nguồn dữ liệu thực tế."""
    setup_directory()

    sources = [
        # File 1: Sổ tay cẩm nang đào tạo 20K AI Handbook ver 2.1
        (ROOT_DIR / "data" / "20K-AI-Handbook-ver2.1.pdf", DATA_DIR / "20k-ai-handbook-ver2.1.pdf"),
        # File 2: AI Mentor Blueprint & Kiến trúc chương trình
        (VINONYMUS_DIR / "docs" / "hackathon" / "cp5" / "ai-mentor-blueprint.pdf", DATA_DIR / "ai-mentor-blueprint.pdf"),
        # File 3: Slide thuyết trình và chuẩn đánh giá
        (VINONYMUS_DIR / "demo-slides.pdf", DATA_DIR / "demo-slides.pdf"),
    ]

    copied_count = 0
    for src_path, dest_path in sources:
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            print(f"[OK] Đã nạp tài liệu: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
            copied_count += 1
        else:
            print(f"[WARN] Nguồn chưa sẵn sàng: {src_path}")

    # Đảm bảo có tối thiểu 3 file PDF hợp lệ
    pdf_files = [f for f in DATA_DIR.glob("*.pdf") if f.is_file() and f.stat().st_size > 1024]
    print(f"\nTổng số tài liệu legal/policy PDF hiện có: {len(pdf_files)}")
    if len(pdf_files) < 3:
        raise RuntimeError(f"Chưa đủ 3 file PDF hợp lệ trong {DATA_DIR} (hiện có: {len(pdf_files)})")


if __name__ == "__main__":
    download_documents()
