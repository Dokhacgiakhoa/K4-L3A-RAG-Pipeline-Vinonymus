# Individual contribution report

## Thông tin

- Họ và tên: Đỗ Khắc Gia Khoa
- Mã học viên: 02733
- Nhóm: Vinonymus / K4-Day08-RAG
- Repository/branch: `https://github.com/Dokhacgiakhoa/K4-L3A-RAG-Pipeline-Vinonymus` (branch `main`)

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Collection (Task 1 & 2) | Thu thập và xử lý văn bản quy chế chính thức: Sổ tay đào tạo Nhân tài AI v2.1 (15MB do VinUni ban hành) và 6 bài viết tin tức JSON từ cẩm nang tuyển sinh | `src/task1_collect_legal_docs.py`, `src/task2_crawl_news.py` | Done |
| Markdown Standardization (Task 3) | Lập trình trích xuất văn bản pypdfium2 và chuẩn hóa Markdown | `src/task3_convert_markdown.py` | Done |
| Chunking & ChromaDB Indexing (Task 4) | Phân đoạn RecursiveCharacterTextSplitter (chunk_size=500, overlap=50), embedding và nạp ChromaDB với cosine distance (tổng cộng 123 chunks) | `src/task4_chunking_indexing.py` | Done |
| Hybrid Retrieval & RRF (Task 5, 6, 7) | Lập trình Dense Search, BM25 chuẩn Lucene chống IDF=0 và thuật toán Reciprocal Rank Fusion k=60 | `src/task5_semantic_search.py`, `src/task6_lexical_search.py`, `src/task7_reranking.py` | Done |
| Fallback & Generation with Citation (Task 8, 9, 10) | Tích hợp PageIndex fallback khi dense score < 0.35, Lost-in-the-middle context reorder và sinh phản hồi với Google Gemini kèm trích dẫn nguồn | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py`, `src/task10_generation.py` | Done |
| UI & Presentation | Xây dựng bộ Slide HTML 10 trang chuẩn báo cáo kỹ thuật tích hợp Live Demo 2 cột (Chat tương tác & AI Pipeline Trace), FastAPI backend và Streamlit app | `slides/index.html`, `api.py`, `app.py` | Done |
| Evaluation & Golden Dataset | Xây dựng 15 cặp Q&A thực tế, chạy benchmark 4 metrics và viết báo cáo đánh giá hoàn chỉnh | `group_project/evaluation/golden_dataset.json`, `group_project/evaluation/RESULT.md` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng công thức Lucene BM25 $IDF = \ln(1 + \frac{N - n + 0.5}{n + 0.5})$ thay vì BM25Okapi thuần trong module Lexical Search.  
   **Lý do/evidence:** Khi tập corpus nhỏ ($N=2, n=1$), công thức BM25Okapi thuần dẫn đến $IDF = \ln(1.0) = 0.0$, làm triệt tiêu điểm số và gây fail contract tests. Công thức Lucene bảo đảm $IDF > 0$ ổn định trong mọi trường hợp.  
   **Trade-off:** Cần tự cài đặt lớp `RobustBM25` thay vì gọi trực tiếp `BM25Okapi` mặc định, nhưng đổi lại tính ổn định 100%.

2. **Quyết định:** Kết hợp Hybrid RRF song song và kích hoạt Fallback Vectorless dựa trên Cosine Similarity gốc từ Dense Search (threshold = 0.35).  
   **Lý do/evidence:** RRF score chỉ phản ánh thứ hạng tương đối, không mang ý nghĩa xác suất hay độ tương đồng tuyệt đối. Đo lường trên Golden Dataset cho thấy Hybrid RRF tăng Context Recall từ 0.79 lên 0.91 (+12%) và bắt chính xác 100% các từ viết tắt chuyên ngành (*SFIA*, *P&L*, *eKYC*).  
   **Trade-off:** Tăng thêm ~18ms độ trễ tính toán cho BM25 và RRF, nhưng không đáng kể so với thời gian sinh văn bản của LLM.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Chạy toàn bộ test suite: `pytest -v` (Đạt 20/20 bài tests: 15 contract tests và 5 acceptance tests).
  + In-domain query: *"Chương trình AI Thực chiến có học bổng thế nào và lộ trình đào tạo mấy tuần?"* $\rightarrow$ Trả lời chuẩn xác học bổng 100%, trợ cấp 8 triệu/tháng, 3 tuần nền tảng + 9 tuần thực chiến, trích dẫn đúng `[1]` `article_02.md`.
  + Out-of-domain query: *"Công thức nấu phở bò Nam Định?"* $\rightarrow$ Kích hoạt Safe Refusal: "Tôi không thể xác minh thông tin này từ nguồn hiện có."
- Kết quả trước/sau nếu có: Context Precision tăng từ 0.81 lên 0.93 sau khi chuyển từ Dense-only sang Hybrid RRF.
- Lỗi đã phát hiện và cách xử lý: Lỗi `test_lexical_search_returns_bm25_contract` do BM25Okapi cho điểm 0 khi corpus có 2 văn bản; đã khắc phục hoàn toàn bằng Lucene BM25.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hiện tại embedding sử dụng mô hình local `all-MiniLM-L6-v2` cho độ trễ nhanh nhưng kích thước vector 384; trong tương lai có thể nâng cấp lên `BAAI/bge-m3` hoặc Gemini text-embedding để tăng khả năng hiểu ngữ nghĩa tiếng Việt đa ngữ.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Tích hợp thêm Cross-Encoder reranker (như BGE-Reranker-Large) ở tầng cuối trước khi nạp prompt vào LLM.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Đỗ Khắc Gia Khoa
