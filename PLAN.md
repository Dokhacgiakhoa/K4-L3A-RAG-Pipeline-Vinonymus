# Kế hoạch Triển khai Dự án: Hệ thống RAG "Sổ tay Nhân tài AI Thực chiến VinUni & Vingroup"

Tài liệu kế hoạch tổng thể triển khai đồ án Day 8 RAG Pipeline cho nhóm và cá nhân.

---

## 1. Thông tin đồ án
- **Đề tài**: Hệ thống Chatbot RAG Sổ tay Đào tạo Nhân tài AI Thực chiến (AI in Action - VinUni & Vingroup).
- **Phạm vi tra cứu**:
  - Cẩm nang chương trình, lộ trình đào tạo 3 tuần nền tảng + 9 tuần thực chiến với dự án thật tại Vingroup.
  - Chính sách tuyển sinh, tiêu chí xét chọn, học bổng 100% và cơ hội việc làm tại VinFast, VinAI, VinBrain,...
  - Khung chuẩn năng lực SFIA quốc tế ứng dụng trong chương trình.
  - 9 nguyên tắc nghiên cứu & phát triển AI có trách nhiệm theo Quyết định 1290/QĐ-BKHCN của Bộ Khoa học và Công nghệ.
- **Công nghệ cốt lõi**:
  - LLM Provider: **Google Gemini** (Gemini 2.5 Flash / 1.5 Flash).
  - Embeddings: `sentence-transformers` (`BAAI/bge-m3`) hoặc `gemini-embedding`.
  - Vector DB: `ChromaDB`.
  - Lexical Search: `BM25Okapi`.
  - Reranker: `Reciprocal Rank Fusion (RRF)`.
  - Vectorless Fallback: `PageIndex`.
  - Giao diện duy nhất (Primary UI): **Next.js 15 + Tailwind CSS + Lucide Icons + PWA (Progressive Web App)** (Chatbot UI cao cấp, installable trên điện thoại & desktop, offline fallback, citation cards, source inspector, dark/light mode).
  - Backend API: **FastAPI** (`api.py`) tích hợp trực tiếp với pipeline `src.task10_generation`.
  - Báo cáo & Thuyết trình: **Slide HTML tương tác** (`slides/index.html`).

---

## 2. Danh mục Nguồn dữ liệu Thực tế (100% Verified)

### A. Tài liệu chính sách / quy chuẩn (`data/landing/legal/` — $\ge 3$ file PDF)
1. **`20k-ai-handbook-ver2.1.pdf`**: Cẩm nang Sổ tay Nhân tài AI Thực chiến chính thức (sẵn có trong repo, chuyển vào `data/landing/legal/`).
2. **`quyet-dinh-1290-qd-bkhcn-nguyen-tac-phat-trien-ai.pdf`**: Quyết định số 1290/QĐ-BKHCN ngày 11/06/2024 của Bộ Khoa học & Công nghệ về hướng dẫn nguyên tắc phát triển AI có trách nhiệm.
3. **`sfia-skills-framework-for-information-age.pdf`**: Tài liệu định nghĩa chuẩn khung năng lực kỹ năng SFIA toàn cầu mà chương trình VinUni áp dụng.

### B. Bài viết / Tin tức (`data/landing/news/` — $\ge 5$ file JSON)
1. **`news_01_tong_quan_va_diem_khac_biet.json`**: Tổng quan chương trình, triết lý đào tạo, đội ngũ giảng viên VinUni và chuyên gia Vingroup.
2. **`news_02_thong_tin_tuyen_sinh_va_quy_trinh.json`**: Lộ trình thi tuyển, các vòng phỏng vấn, đối tượng tham gia.
3. **`news_03_giai_dap_thac_mac_qa.json`**: Bộ câu hỏi giải đáp chi tiết cho học viên về thời gian biểu, trợ cấp, cam kết làm việc.
4. **`news_04_vingroup_khoi_dong_ai_in_action.json`**: Tin tức báo chí chính thức về việc Tập đoàn Vingroup phối hợp VinUni đào tạo nhân tài AI thực chiến.
5. **`news_05_kenh_ho_tro_va_cong_dong.json`**: Thông tin Fanpage Đào tạo Nhân tài AI Thực chiến, Group Cộng đồng học viên, hotline, email liên hệ.

---

## 3. Lộ trình Phân chia Công việc (Task Breakdown)

| Giai đoạn | Nhiệm vụ | File phụ trách | Deliverable |
|---|---|---|---|
| **Phase 1: Setup** | Cài môi trường Python 3.13, cài thư viện, cấu hình `.env` với `GEMINI_API_KEY` | `.env`, `pyproject.toml` | Môi trường ảo `.venv` hoàn chỉnh |
| **Phase 2: Data** | Tải và chuyển 3 PDF vào `data/landing/legal/`<br>Crawl 5 tin tức JSON vào `data/landing/news/`<br>Convert toàn bộ sang Markdown | `src/task1_collect_legal_docs.py`<br>`src/task2_crawl_news.py`<br>`src/task3_convert_markdown.py` | Pass `test_corpus_has_required_legal_documents`<br>Pass `test_corpus_has_required_news_with_metadata`<br>Pass `test_standardized_output_covers_both_source_types` |
| **Phase 3: Index & Search** | Chunking văn bản, index ChromaDB<br>Semantic Search (Dense)<br>Lexical Search (BM25)<br>Rerank RRF | `src/task4_chunking_indexing.py`<br>`src/task5_semantic_search.py`<br>`src/task6_lexical_search.py`<br>`src/task7_reranking.py` | Pass contract tests cho SearchResult và ordering |
| **Phase 4: Pipeline & Generation** | Vectorless fallback (PageIndex)<br>Retrieval pipeline & Cosine threshold<br>Generation có citation với Gemini & Safe Refusal | `src/task8_pageindex_vectorless.py`<br>`src/task9_retrieval_pipeline.py`<br>`src/task10_generation.py` | Pass toàn bộ `test_contracts.py` |
| **Phase 5: UI & Presentation** | Next.js Chatbot UI hiện đại & FastAPI backend<br>Slide thuyết trình HTML tương tác | `api.py`<br>`frontend/`<br>`slides/index.html` | Chatbot Next.js mượt mà, citation cards & slide demo chuyên nghiệp |
| **Phase 6: Evaluation & Report** | Soạn 15+ Q&A Golden Dataset<br>Đo 4 metrics, so sánh A/B<br>Hoàn thành RESULT.md & Individual Report | `group_project/evaluation/golden_dataset.json`<br>`group_project/evaluation/RESULT.md`<br>`reports/02733-do-khac-gia-khoa.md` | Pass `test_acceptance.py`<br>Không còn TODO |

---

## 4. Kế hoạch Kiểm thử & Đo kiểm Chất lượng

### A. Kiểm thử Hợp đồng & Nghiệm thu
```powershell
# Kiểm tra hợp đồng kiểu dữ liệu và chữ ký hàm
.\.venv\Scripts\pytest tests/test_contracts.py -v

# Kiểm tra tiêu chí nghiệm thu dữ liệu và báo cáo
.\.venv\Scripts\pytest tests/test_acceptance.py -v

# Chạy toàn bộ test suite
.\.venv\Scripts\pytest -v
```

### B. Kiểm tra Truy vấn Thực tế
1. **Câu hỏi đúng domain (In-domain)**:
   - *"Quy trình tuyển chọn chương trình Nhân tài AI Thực chiến của Vingroup gồm những vòng nào?"*
   - *"Chuẩn SFIA áp dụng trong chương trình như thế nào?"*
   - $\rightarrow$ Kỳ vọng: Trả lời chính xác, trích dẫn rõ ràng nguồn tài liệu.
2. **Câu hỏi ngoài domain (Out-of-domain)**:
   - *"Cho tôi biết công thức làm món phở bò Nam Định?"*
   - $\rightarrow$ Kỳ vọng: Kích hoạt cơ chế Fallback và Safe Refusal an toàn, không hallucinate.
