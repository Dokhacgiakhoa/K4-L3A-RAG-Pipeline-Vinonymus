# Ai Mentor Blueprint

**Source File:** `ai-mentor-blueprint.pdf`

---

# AI Mentor — Lộ Trình Cá Nhân Hóa Cho Học Viên AI
**Dự án của Nhóm Vinonymus (Lớp K4-3A-E403)**
- Đội ngũ: Khoa (PM/Backend), Minh (Database), Đức (AI), Thành (Giao diện)
- Mã nguồn: github.com/Dokhacgiakhoa/K4-3A-e403-Vinonymus

## 1. Nỗi đau & Bằng chứng dữ liệu thực tế (Khảo sát Khóa 4)
- 87% (71/82 học viên): Không tự xác định được phần kiến thức cần học bù trước mỗi buổi thực hành Lab.
- 93% (76/82 học viên): Gặp khó khăn do tài liệu rải rác đa nền tảng (Discord, Zoom, VLearn, GitHub).
- 0.13% (18/13.494 lượt): Tỉ lệ AI Tutor VLearn chủ động gợi ý bước học tiếp theo.
- Job-to-be-done: Với quỹ thời gian và trình độ hiện tại, biết chính xác cần học gì để làm kịp bài Lab tiếp theo.

## 2. Logic Sản Phẩm & Quyết Định AI
- Chẩn đoán nền tảng (Non-tech / Tech / AI) kết hợp thời gian rảnh dưới 1 tiếng -> Đề xuất tối đa 3 đầu việc trọng tâm (Checklist <= 3 tasks).
- Tín hiệu chấp nhận: 90% (74/82) học viên sẵn sàng dùng checklist 3 việc theo số phút rảnh mỗi ngày.

## 3. Luồng Hoạt Động & Kiểm Soát An Toàn (Guardrails)
- Đầu vào: Nền tảng học viên, số phút rảnh, bài Lab cần làm.
- Hệ thống chẩn đoán AI: Đối chiếu danh mục Catalog tài liệu đã kiểm chứng.
- Luồng rẽ nhánh an toàn:
  + Khai báo mâu thuẫn (VD: Non-tech nhưng đã làm RAG production) -> AI yêu cầu làm rõ (Case G14).
  + Đòi giải bài hộ / xin đáp án -> AI từ chối an toàn và yêu cầu liên hệ Lab Coach (Case G16).
  + Đầu ra chuẩn (Case Tech, 60 phút): Checklist <= 3 việc trọng tâm kèm lý do, thời lượng và URL catalog.

## 4. Đo Lường Khắt Khe & Chất Lượng (Quality Bar tại CP4)
- Tiêu chuẩn: >= 18/20 case đạt VÀ 0 URL ngoài catalog VÀ 3/3 case vi phạm phải từ chối.
- Kết quả: AI v2 (Gemini Flash) đạt 19/20 case chuẩn (95%), 0 URL ngoài catalog, từ chối chính xác 100% case vi phạm bảo mật.
