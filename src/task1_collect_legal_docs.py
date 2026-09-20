"""
Task 1 — Thu thập tài liệu chính sách/quy định/cẩm nang đào tạo.

Nạp tài liệu chính thức của chương trình:
20k-ai-handbook-ver2.1.pdf: Sổ tay chương trình Đào tạo Nhân tài AI Thực chiến (Vingroup & VinUni).
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
    """Xác thực và nạp tài liệu PDF Sổ tay học viên chính thức từ VinUni."""
    setup_directory()

    handbook_path = DATA_DIR / "20k-ai-handbook-ver2.1.pdf"
    if handbook_path.exists() and handbook_path.stat().st_size > 1024:
        print(f"[OK] Đã sẵn sàng tài liệu Sổ tay chính thức: {handbook_path.name} ({handbook_path.stat().st_size:,} bytes)")
    else:
        # Dự phòng sao chép từ data/ nếu có
        source_handbook = ROOT_DIR / "data" / "20K-AI-Handbook-ver2.1.pdf"
        if source_handbook.exists():
            shutil.copy2(source_handbook, handbook_path)
            print(f"[OK] Đã sao chép Sổ tay: {handbook_path.name}")
        else:
            raise FileNotFoundError(f"Không tìm thấy Sổ tay chính thức tại {handbook_path}")

    pdf_files = [f for f in DATA_DIR.glob("*.pdf") if f.is_file() and f.stat().st_size > 1024]
    print(f"\nTổng số tài liệu legal/policy PDF chính thức hiện có: {len(pdf_files)}")


if __name__ == "__main__":
    download_documents()
