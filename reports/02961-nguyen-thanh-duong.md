# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Thành Dương
- Mã học viên: 02961
- Nhóm: Vinonymus (K4-3A-E403)
- Repository/branch: `https://github.com/Dokhacgiakhoa/K4-L3A-RAG-Pipeline-Vinonymus/tree/feat/collect-standardize-ai20k-corpus`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Collection (Legal & News) | Thu thập tài liệu văn bản quy chế chính thức: Sổ tay học viên v2.1 (15MB do VinUni ban hành) và các bài viết tin tức tuyển sinh | `src/task1_collect_legal_docs.py`, `src/task2_crawl_news.py`, PR #1 | Done |
| Markdown Standardization & Fix Encoding | Chuẩn hóa Markdown, xử lý triệt để lỗi encoding tiếng Việt có dấu, bổ sung metadata header nguồn trích dẫn | `src/task3_convert_markdown.py`, `docs/CORPUS_SOURCES.md` | Done |
| Corpus Quality Testing | Viết bài test chất lượng dữ liệu đầu vào kiểm tra độ dài và tính toàn vẹn | `tests/test_acceptance.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chuẩn hóa toàn bộ văn bản sang định dạng UTF-8 và bổ sung Metadata Header chuẩn (`Title`, `Source`, `Date`).  
   **Lý do/evidence:** Tránh lỗi Unicode/mojibake khi đọc tiếng Việt có dấu trên Windows và bảo toàn tính minh bạch khi trích dẫn nguồn (Grounded Citations).  
   **Trade-off:** Cần tiền xử lý regex làm sạch khoảng trắng và dấu ngắt dòng thừa.

2. **Quyết định:** Viết bài test nghiệm thu chất lượng dữ liệu trong `tests/test_acceptance.py` để validate tập tài liệu trước khi đưa vào chunking.  
   **Lý do/evidence:** Phát hiện sớm các văn bản bị rỗng hoặc thiếu ký tự (ngưỡng &ge; 200 ký tự), ngăn ngừa lỗi ở các tầng pipeline sau.  
   **Trade-off:** Tăng thêm thời gian chạy kiểm thử CI/CD ban đầu.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_acceptance.py -v`.
- Kết quả trước/sau nếu có: 100% tài liệu pháp quy và bài viết tin tức vượt qua kiểm tra chất lượng và độ dài.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Quá trình thu thập tin tức một phần vẫn dựa trên crawler tĩnh, chưa tự động re-crawl khi có bài viết mới.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Xây dựng webhook tự động kích hoạt cập nhật tài liệu và re-index vào ChromaDB.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Thành Dương
