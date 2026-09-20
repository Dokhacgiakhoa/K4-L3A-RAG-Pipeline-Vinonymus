# Hệ Thống AI Mentor & Lộ Trình Học Cá Nhân Hóa Dành Cho Học Viên AI Khóa 4

**Source:** https://vinuni.edu.vn/aithucchien/ai-mentor-personalized-pathway

**Crawled:** 2026-09-20T15:11:54.946805

---

# Hệ Thống AI Mentor & Lộ Trình Học Cá Nhân Hóa Cho Học Viên AI

Nghiên cứu và giải pháp kỹ thuật từ dự án Nhóm Vinonymus (Lớp K4-3A-E403) hỗ trợ học viên giải quyết bài toán bế tắc kiến thức trước mỗi buổi Lab.

## 1. Vấn đề thực tế (Pain Points)
- 87% (71/82 học viên) khảo sát gặp khó khăn trong việc xác định kiến thức cần học bù trước buổi thực hành.
- 93% gặp trở ngại do tài liệu rải rác trên nhiều nền tảng (Discord, Zoom, VLearn, GitHub).
- Thời gian tự học hạn chế (dưới 60 phút mỗi buổi trưa).

## 2. Giải pháp AI Mentor Adaptive Learning
- Hệ thống AI chẩn đoán nền tảng học viên (Non-tech / Tech / AI) và quỹ thời gian rảnh.
- Tự động đối chiếu Catalog tài liệu chuẩn để đưa ra danh sách đề xuất tối đa 3 đầu việc trọng tâm (Checklist ≤ 3 tasks).
- Tích hợp cơ chế Guardrails an toàn: Từ chối giải hộ bài tập hoặc tiết lộ đáp án, yêu cầu liên hệ Lab Coach khi cần hỗ trợ sâu.

## 3. Kiến trúc AI Pipeline
- Mô hình ngôn ngữ Gemini Flash hỗ trợ phân tích ngữ cảnh câu hỏi của học viên.
- Đạt Quality Bar kiểm định với tỷ lệ chính xác 95% (19/20 case chuẩn) và 0 liên kết ngoài catalog kiểm chứng.

# 01 — Đặc tả yêu cầu phần mềm (SRS) · Lộ trình cá nhân hoá (AI Mentor · Adaptive Learning System)

> **Phạm vi:** chỉ lát cắt dự thi (xem [`spec.md`](../spec.md) §4). Các tính năng khác của codebase (Chat K.AI, tài khoản, gói Pro, backend .NET) nằm ngoài tài liệu này.
> **Trạng thái:** bản nháp v0.1 · 16/9 · chốt cùng `spec.md` tại CP4 (21:00 · 17/9).

Quy ước: **FR** = yêu cầu chức năng · **NFR** = phi chức năng · **P0** = bắt buộc cho demo · **P1** = nên có · **AC** = tiêu chí nghiệm thu.

---

## 1. Bối cảnh (Mô hình Khách hàng kép)

| Mục | Nội dung |
|---|---|
| **Khách hàng 1 (Học viên)** | Học viên Khoá 4 AI20K đang tự học trước buổi lab/workshop tiếp theo (40 ca kiểm thử) |
| **Khách hàng 2 (VLearn/LMS)** | Nền tảng VLearn, ban đào tạo & trợ giảng cần giảm tải, bảo vệ an toàn và chống gian lận (10 ca kiểm thử) |
| **Việc cần làm** | Học viên biết hôm nay học gì trong quỹ thời gian rảnh; VLearn có cơ chế tự động dẫn đường học tập chuẩn hóa |
| **Quyết định AI duy nhất** | Từ nền tảng + quỹ thời gian + bài lab → **chọn và sắp thứ tự tối đa 3 tài liệu trong catalog**, kèm lý do; hoặc hỏi lại (`clarify`); hoặc từ chối (`refuse`) |
| **Kết quả** | Checklist ≤3 việc có link, học viên chỉnh được trước khi làm; hệ thống bảo vệ 0 link ngoài catalog |
| **Mức tự động hoá** | Conditional (xem `spec.md` §4) |

## 2. Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| **Catalog** | Danh sách tài liệu cho từng bài lab do nhóm tự soạn tại `codebase/src/data/planner-catalog.ts` — nguồn sự 

# 04 — AI pipeline · AI Mentor (tính năng Lộ trình cá nhân hoá)

> **Trạng thái:** đã build cho CP3. Prompt/schema: `codebase/src/lib/prompts/planner.ts`; route: `codebase/src/app/api/roadmap/route.ts`; hậu kiểm: `codebase/src/lib/planner/ai-planner.ts`.

## 1. Luồng xử lý

1. **Validate** đầu vào bằng zod (FR-P02).
2. **Luật cứng trước khi gọi LLM** — rẻ, chắc chắn, không bịa:
   - `lab_id` không có trong catalog → `clarify`.
   - Ghi chú khớp mẫu làm hộ / đáp án / gia hạn / xin điểm / bỏ qua hướng dẫn → `refuse`.
   - `available_minutes < 30` → `clarify`.
3. **Rút gọn catalog** của bài lab đã chọn thành danh sách `item_id | tiêu đề | loại | phút | mức độ | tags`. Không đưa URL vào prompt, để LLM không có link nào để chép hay bịa.
4. **Gọi LLM** qua `lib/llm/router.ts`, yêu cầu trả JSON đúng schema. Phản hồi dài quá 20.000 ký tự bị coi là lỗi.
5. **Kiểm tra output** (`ai-planner.ts`):
   - Parse JSON bằng zod; hỏng hoặc router lỗi → baseline.
   - `status = clarify` hoặc `refuse` → trả nguyên cho học viên.
   - `confidence = low` → đổi thành `clarify`.
   - Bỏ `item_id` không có trong catalog hoặc bị trùng.
   - Duyệt theo thứ tự AI chọn, bỏ qua việc nào làm tổng phút vượt quỹ thời gian; dừng khi đủ 3 việc.
   - Còn 0 việc → baseline.
6. **Ghép dữ liệu hiển thị** (`title`, `url`, `type`, `minutes`) từ catalog theo `item_id`; `reason` cắt còn 160 ký tự, `summary` còn 240 ký tự.

## 2. Prompt

Nguyên văn: `PLANNER_SYSTEM_PROMPT` và `buildPlannerUserPrompt` trong `codebase/src/
