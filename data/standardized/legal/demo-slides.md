# Demo Slides

**Source File:** `demo-slides.pdf`

---

<!-- Page 1 -->
1 · USER & JOB
Học viên Khoá 4 trước mỗi buổi lab: không biết phải học bù
phần nào
Job: với quỹ thời gian rảnh hôm nay và trình độ của mình, biết chính xác cần học gì để làm kịp bài lab tiếp theo.
87%
71/82 không tự xác định được phần cần
học bù trước buổi lab
93%
76/82 gặp tài liệu rải rác nhiều nơi
(Discord, Zoom, Drive, VLearn, GitHub)
0.13%
lượt chat AI Tutor VLearn tự gợi ý bước
học tiếp theo (18/13.494)
“Slide bài giảng dài hơn 60 trang, mình chỉ có khoảng 45 phút buổi trưa để đọc trước.” — P02, học viên nền AI
Nguồn: khảo sát form n = 82 (17/9, tự khai, mẫu tự nguyện) · vlearn-pack 13.494 lượt chat · phỏng vấn P02 16/9 — chi tiết spec.md §1

<!-- Page 2 -->
2 · VÌ SAO CHỌN TÍNH NĂNG NÀY
3 ứng viên — chọn cái có “một quyết định AI” rõ ràng
Ứng viên Bằng chứng Quyết định
(1) Tổng hợp link tài liệu phân mảnh 76/82 (93%) gặp tài liệu rải rác Loại — chỉ là tra cứu, không có quyết
định AI
(2) Tóm tắt trọng tâm bài giảng 75/82 (91%) gặp slide dài; 8.8% lượt chat
VLearn xin tóm tắt
Loại — trùng lõi Track A (AI Tutor)
(3) Chẩn đoán nền tảng + thời gian → ≤3 việc
trọng tâm cho lab tiếp theo
71/82 (87%) không biết học bù phần nào;
41/82 (50%) rảnh dưới 1 tiếng
Chọn — catalog đã kiểm chứng giải
luôn một phần (1)
Tín hiệu chấp nhận: 74/82 (90%) muốn dùng checklist 3 việc theo số phút rảnh mỗi ngày.
Nguồn: bảng impact spec.md §2 · khảo sát n = 82 · mining docs/research/evidence-mining.md

<!-- Page 3 -->
3 · GIẢI PHÁP & DEMO LIVE
Lộ trình cá nhân hoá: AI Mentor đề xuất tối đa 3 việc, kèm
link đã kiểm chứng
Luồng
Chọn nền tảng (non-tech / tech / AI) → số phút rảnh +
bài lab → ghi chú
AI Mentor trả checklist ≤3 việc, lý do, thời lượng, link chỉ
lấy từ catalog
Thiếu thông tin → hỏi lại; xin làm hộ / đáp án / gia hạn →
từ chối
Mức tự động hoá: augment
AI chỉ đề xuất, học viên tự tick/sửa. Cost-of-error: gợi ý sai
tốn vài chục phút đọc nhầm, không ảnh hưởng điểm.
Demo trên sân khấu
Case chuẩn
Tech-base, 60 phút, lab tiếp theo → checklist 3 việc,
tổng ≤ 60 phút, link trong catalog.
Case khó
“Làm hộ bài lab / cho đáp án” → AI từ chối, gợi ý liên hệ
Lab Coach (G16). Hoặc khai non-tech nhưng ghi “đã làm
RAG production” → AI hỏi lại (G14).
Web: k4-3a-e403-vinonymus.vercel.app/personalized-path · luồng chi tiết docs/05-ui-flow.md · video demo dự phòng nộp kèm CP5

<!-- Page 4 -->
4 · KẾT QUẢ ĐO
Đạt Quality Bar khoá tại CP4: AI v2 19/20, 0 link ngoài
catalog
Quality Bar (khoá 21:00 · 17/9): ≥18/20 case đạt VÀ 0 URL
ngoài catalog VÀ 3/3 case G16–G18 trả refuse.
Lượt Đạt Link ngoài
Baseline luật tĩnh (20 case) 17/20 · 85% 0
AI v1 · Gemini Flash-Lite 18/20 · 90% 0
AI v2 · Gemini Flash-Lite 19/20 · 95% 0
Failure đáng kể nhất: G02
Gemini chọn đúng tài liệu ptc-function-calling
nhưng xếp thứ ba; hậu kiểm giới hạn 60 phút loại mất
item này. Không bịa link, không rơi về baseline — nhóm
giữ nguyên case và số 19/20.
Minh bạch: ngưỡng chốt sau khi đã có lượt v1, v2. Bộ mở rộng 50 case hiện chỉ
chạy baseline luật tĩnh (50/50) — luật đã được chỉnh theo chính các case này,
nên không dùng làm bằng chứng chất lượng AI.
Nguồn: eval/run_results.md lượt 0–3 · eval/latest-ai-results.json · spec.md §7

<!-- Page 5 -->
5 · USER THẬT NÓI GÌ
Chưa hoàn thành 5 buổi cho người ngoài dùng thử — nói
thẳng thay vì tô vẽ
Đã có
“Mỗi buổi học phải mất ít nhất 20–25 phút chỉ để gom
đủ link tài liệu.” — P01, học viên nền tech
“Slide bài giảng dài hơn 60 trang, mình chỉ có khoảng 45
phút buổi trưa để đọc trước.” — P02, học viên nền AI
Phỏng vấn trước khi build (16/9). 71/82 người khảo sát sẵn sàng dùng thử.
Thay cho validation: đo trên golden set
AI v2 đạt Quality Bar: 19/20 case, 0 link ngoài catalog
3/3 case ngoài phạm vi (xin đáp án, mở cổng nộp muộn,
đòi system prompt) → từ chối
Chưa đạt: G02 — thiếu 1 tài liệu vì giới hạn thời lượng
Nhật ký dùng thử: validation/log.md (chưa đủ 5 người).
Nguồn: docs/research/survey-log.md · eval/run_results.md · theo luật 02-guide §5.1: không có validation thì báo kết quả golden set

<!-- Page 6 -->
6 · NẾU CÓ THÊM 1 TUẦN
3 việc ưu tiên, đều trỏ về lỗ hổng đang có
1. Cho 5 người thật dùng thử
Giao task, ngồi im quan sát, ghi
quote nguyên văn — đúng phần
còn thiếu ở slide 5.
2. Bài test chẩn đoán từ CV
74/82 (90%) muốn có bài test
ngắn; hiện AI Mentor chỉ dựa nền
tảng tự khai.
3. Thư viện tài liệu giảng viên
Giảng viên tải tài liệu lên, AI
Mentor đọc vào thư viện thay cho
catalog nhóm soạn tay.
Bài học lớn nhất: chốt chuẩn “đạt” và đo bằng golden set từ sớm giúp nhóm nói được con số thật — kể cả con số chưa
đẹp.
Nhóm Vinonymus · K4-3A-E403 · Khoa (PM · backend) · Minh (database) · Đức (AI) · Thành (giao diện)
Repo: github.com/Dokhacgiakhoa/K4-3A-e403-Vinonymus · task board docs/hackathon/tasks-he-thong-4-vai-tro.md