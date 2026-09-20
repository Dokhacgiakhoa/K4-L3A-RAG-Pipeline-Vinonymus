# Individual contribution report

## Thông tin

- Họ và tên: Trần Nhật Minh
- Mã học viên: 02483
- Nhóm: Vinonymus (K4-3A-E403)
- Repository/branch: `https://github.com/Dokhacgiakhoa/K4-L3A-RAG-Pipeline-Vinonymus/tree/minh`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Data Collection (Facebook Community) | Thu thập, bóc tách và phân loại dữ liệu hỏi đáp tuyển sinh/lộ trình từ Group Facebook Cộng đồng AI Thực chiến VinUni (10 bài viết Markdown kèm permalinks & ảnh) | `data/landing/facebook/`, PR #2 | Done |
| FAQ Integration & Preprocessing | Chuẩn hóa nội dung FAQ các chủ đề P0 (Vibe coding, môi trường Python/Node), P1 (Coding, Git), P2 (Nền tảng AI) và chính sách thực tập doanh nghiệp | `tong-hop-ai-in-action-facebook.md` | Done |
| Database & Vector Indexing Support | Phối hợp rà soát metadata nguồn trích dẫn từ mạng xã hội cho ChromaDB | PR #2 | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Giữ nguyên permalink và URL ảnh gốc trong từng file Markdown trích xuất từ Facebook.  
   **Lý do/evidence:** Đảm bảo tính minh bạch đối soát nguồn thông tin (Grounded Citation), tránh mất nguồn khi phân mảnh chunk.  
   **Trade-off:** Cần xử lý định dạng link cẩn thận để không làm loãng embedding vector.

2. **Quyết định:** Phân tầng mức độ ưu tiên câu hỏi FAQ (P0: Công cụ/vibe coding, P1: Git & coding, P2: Nền tảng AI).  
   **Lý do/evidence:** Phản ánh đúng nhu cầu thực tế của học viên khi tra cứu kinh nghiệm học tập và chuẩn bị trước khóa học.  
   **Trade-off:** Cần tiền xử lý phân loại thủ công kết hợp regex.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: Kiểm tra tính hiển thị và trích xuất đúng link nguồn Facebook trên toàn bộ 10 file Markdown.
- Kết quả trước/sau nếu có: Bổ sung 10 văn bản hỏi đáp thực tế từ cộng đồng giúp RAG pipeline giải đáp được cả các câu hỏi về trải nghiệm học viên.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Facebook API giới hạn luồng comment sâu, một số thread phản hồi dài chưa bóc tách hết toàn bộ 100%.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Tự động hóa crawler qua Graph API hoặc Playwright để tự động sync comment mới nhất.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Trần Nhật Minh
