"""
Task 1 — Thu thập tài liệu chính sách/quy định/cẩm nang đào tạo.

Thu thập tối thiểu 3 tài liệu PDF từ các nguồn dữ liệu chính thức của chương trình:
1. 20k-ai-handbook-ver2.1.pdf: Sổ tay chương trình Đào tạo Nhân tài AI Thực chiến (Vingroup & VinUni).
2. vinuni-ai20k-chinh-sach-tuyen-sinh.pdf: Chính sách tuyển sinh khóa cơ bản và khóa 2-3.
3. vinuni-ai20k-lich-su-trien-khai.pdf: Lịch sử triển khai và mô hình đào tạo 3+3+6.
"""

from pathlib import Path
import shutil


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "landing" / "legal"


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Xác thực và nạp 3 tài liệu PDF pháp lý chính thức từ VinUni."""
    setup_directory()

    # Kiểm tra 3 file PDF chính sách pháp quy chính thức
    required_pdfs = [
        "20k-ai-handbook-ver2.1.pdf",
        "vinuni-ai20k-chinh-sach-tuyen-sinh.pdf",
        "vinuni-ai20k-lich-su-trien-khai.pdf",
    ]

    for filename in required_pdfs:
        filepath = DATA_DIR / filename
        if filepath.exists() and filepath.stat().st_size > 1024:
            print(f"[OK] Đã sẵn sàng tài liệu: {filename} ({filepath.stat().st_size:,} bytes)")
        else:
            print(f"[WARN] Cần kiểm tra lại file: {filename}")

    # Đảm bảo có tối thiểu 3 file PDF hợp lệ
    pdf_files = [f for f in DATA_DIR.glob("*.pdf") if f.is_file() and f.stat().st_size > 1024]
    print(f"\nTổng số tài liệu legal/policy PDF hiện có: {len(pdf_files)}")
    if len(pdf_files) < 3:
        raise RuntimeError(f"Chưa đủ 3 file PDF hợp lệ trong {DATA_DIR} (hiện có: {len(pdf_files)})")


if __name__ == "__main__":
    download_documents()
