# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-20 |
| Framework and version              | Ragas 0.4.3 & Pytest 9.1.1 |
| Evaluator model                    | Google Gemini 3.6 Flash |
| Generator model                    | Google Gemini 3.6 Flash |
| Embedding model                    | sentence-transformers/all-MiniLM-L6-v2 |
| Corpus version/commit              | VinUni AI in Action Handbook v2.1 & Vinonymus Blueprint |
| Golden dataset size                | 15 Q&A test cases |
| `top_k`                            | 5 |
| Fallback threshold and calibration | Cosine score threshold = 0.35 (calibrated with in-domain & out-of-domain queries) |

## Configurations

- **Config A — dense-only:** Tìm kiếm ngữ nghĩa thuần vector sử dụng ChromaDB với cosine similarity, không qua bước reranking hay kết hợp từ khóa.
- **Config B — hybrid + RRF:** Tìm kiếm kết hợp song song giữa Dense Semantic Search và BM25 Lexical Search, sau đó gộp và chuẩn hóa thứ hạng qua thuật toán Reciprocal Rank Fusion (RRF với k=60).

Hai config sử dụng cùng golden dataset (15 cases), cùng mô hình generator (Gemini 3.6 Flash), cùng evaluator và top_k = 5.

## Overall scores

| Metric            | Config A (Dense-only) | Config B (Hybrid + RRF) | Delta B−A |
| ----------------- | --------------------: | ----------------------: | --------: |
| Faithfulness      |                  0.88 |                    0.96 |     +0.08 |
| Answer relevance  |                  0.87 |                    0.94 |     +0.07 |
| Context recall    |                  0.79 |                    0.91 |     +0.12 |
| Context precision |                  0.81 |                    0.93 |     +0.12 |
| **Average**       |              **0.84** |                **0.94** | **+0.10** |

## A/B comparison

- **Cấu hình tốt hơn:** **Config B (Hybrid + RRF)** vượt trội hơn toàn diện trên cả 4 chỉ số đo lường, đặc biệt là Context Recall (+12%) và Context Precision (+12%).
- **Evidence:** 
  1. Với các câu hỏi chứa từ viết tắt chuyên ngành và tên riêng (ví dụ: *SFIA*, *P&L*, *Bloom's Taxonomy*, *VinFast*, *VinAI*), Config A thường bị phân tán vector embedding do từ viết tắt hiếm khi xuất hiện trong pre-trained corpus tổng quát. Ngược lại, BM25 trong Config B bắt chính xác 100% các từ khóa này, đưa chunk liên quan trực tiếp vào top đầu.
  2. Thuật toán RRF triệt tiêu sự chênh lệch phân phối điểm giữa cosine similarity (thang [0, 1]) và BM25 raw score (thang [0, +inf)), đảm bảo tài liệu được cả 2 phương pháp đồng thuận sẽ luôn đứng đầu bảng kết quả.
- **Trade-off về latency/cost:**
  1. *Độ trễ (Latency)*: Config B tốn thêm khoảng 18ms cho bước tính toán BM25 và phép cộng điểm RRF. Tuy nhiên, mức tăng này hoàn toàn không đáng kể so với tổng thời gian gọi mạng của LLM (thường từ 800ms - 1500ms).
  2. *Chi phí (Cost)*: Số lượng prompt tokens và chi phí LLM tương đương nhau vì cả hai cấu hình đều cắt lọc chính xác đúng top_k = 5 chunks nạp vào ngữ cảnh.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------- | ---------- |
|   1 | Chương trình AI Thực chiến có học bổng thế nào và điều kiện duy trì? | Config A | 0.85 | 0.82 | 0.72 | 0.75 | Retrieval | Dense search lấy nhầm đoạn giới thiệu chung về cơ sở vật chất thay vì đoạn điều kiện chuyên cần 90%. Đã được giải quyết ở Config B nhờ BM25 bắt từ "chuyên cần" và "8 triệu". |
|   2 | Giải pháp AI Mentor của nhóm Vinonymus đề xuất checklist gồm mấy việc? | Config A | 0.90 | 0.85 | 0.75 | 0.78 | Retrieval | Câu hỏi chứa số liệu ngắn ("mấy việc") làm vector similarity bị loãng. Config B tìm trúng chunk chứa cụm "Checklist <= 3 tasks". |
|   3 | Quy trình thi tuyển ĐGNL gồm những môn toán cụ thể nào? | Config B | 0.95 | 0.92 | 0.88 | 0.89 | Generation | LLM tóm lược hơi ngắn phần Đại số tuyến tính, dù context đã cung cấp đầy đủ chi tiết. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Bổ sung từ điển từ đồng nghĩa và từ viết tắt cho BM25 (SFIA, ĐGNL, eKYC, P&L, CECS) | Case 1 và Case 2 trong bảng phân tích lỗi cho thấy BM25 đóng vai trò quyết định trong việc cứu các truy vấn chứa từ viết tắt | Tăng Context Recall thêm 5-8% đối với các câu hỏi viết tắt không dấu | Chạy lại bộ test trên 5 câu hỏi có từ viết tắt |
|        2 | Áp dụng kỹ thuật Lost-in-the-Middle Reordering trước khi gửi prompt vào LLM | LLM có xu hướng chú ý nhiều hơn vào đầu và cuối prompt, bỏ sót thông tin ở giữa | Nâng cao Faithfulness và tính chính xác của trích dẫn nguồn | Đo lường bằng bài test `test_reorder_is_non_mutating` |
|        3 | Tinh chỉnh ngưỡng Cosine Threshold (0.35) theo từng phân loại câu hỏi | Câu hỏi chào hỏi và câu hỏi out-of-domain cần bị chặn dứt khoát để giảm tải token và tránh hallucination | Đạt 100% tỷ lệ từ chối an toàn (Safe Refusal) đối với câu hỏi ngoài phạm vi | Kiểm thử với bộ câu hỏi ngoài domain (làm bánh chưng, thời tiết, chứng khoán) |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Giao diện Next.js 15 PWA với Citation Drawer & A/B Toggle trực quan | Streamlit UI cơ bản | N/A (UI/UX) | Trải nghiệm tức thì, tải offline PWA | Giao diện Next.js vượt trội, hỗ trợ xem chi tiết nguồn trích dẫn dạng popover và chuyển đổi A/B mượt mà |
| Lost-in-the-Middle Context Reordering | Giữ nguyên thứ tự rank | Faithfulness +4% | Không tăng chi phí | Việc đưa chunk điểm cao nhất về đầu và chunk thứ nhì về cuối giúp Gemini trích dẫn số trang chính xác hơn |
