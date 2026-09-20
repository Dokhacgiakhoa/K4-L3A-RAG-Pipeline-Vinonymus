# Nguồn Gốc Xuất Xứ Tập Dữ Liệu (Corpus Sources) — Sổ Tay Nhân Tài AI Thực Chiến

## 1. Phạm Vi & Mục Tiêu Tập Dữ Liệu

Corpus bao gồm toàn bộ dữ liệu văn bản chính thống liên quan đến chương trình đào tạo **20.000 Nhân tài AI thực chiến** do Tập đoàn Vingroup phối hợp cùng Trường Đại học VinUni triển khai. Dữ liệu phục vụ hệ thống RAG tra cứu điều kiện tuyển sinh, quy chế học bổng, trợ cấp sinh hoạt 8 triệu, chuẩn năng lực SFIA, nội quy thực tập P&L doanh nghiệp và kinh nghiệm học tập thực tế từ cộng đồng.

100% dữ liệu gốc được thu thập từ nguồn xác thực, không sử dụng dữ liệu giả lập.

---

## 2. Bảng Danh Mục Dữ Liệu Thực Tế

### A. Tài Liệu Pháp Lý & Quy Chế Đào Tạo (`data/landing/legal/`)

| Tên File | Dung Lượng | Nguồn Gốc Xuất Xứ | Nội Dung Cốt Lõi |
|---|:---:|---|---|
| `20k-ai-handbook-ver2.1.pdf` | ~15.0 MB | [VinUni 20K AI Handbook v2.1](https://vinuni.edu.vn/aithucchien/wp-content/uploads/2026/06/20K-AI-Handbook-ver2.1.pdf) | 22 trang quy chế chính thức: Tài trợ học bổng 100%, trợ cấp sinh hoạt 8.000.000 VNĐ/tháng, điều kiện duy trì chuyên cần &ge; 90%, cam kết làm việc tại VinFast/VinAI. |
| `ai-mentor-blueprint.pdf` | ~8.4 MB | Đề tài AI Mentor Nhóm Vinonymus (K4-3A-E403) | Khảo sát thực tế 82 học viên Khóa 4, kiến trúc AI Mentor, Guardrails an toàn và Quality Bar CP4. |
| `demo-slides.pdf` | ~142 KB | Tài liệu nghiệm thu & chuẩn năng lực SFIA VinUni | 7 bậc năng lực AI SFIA, tiêu chuẩn nghiệm thu đồ án và lộ trình đào tạo 12 tuần. |

### B. Bài Viết & Cẩm Nang Tuyển Sinh (`data/landing/news/`)

| Tên File | Nguồn Gốc URL | Tiêu Đề & Chủ Đề |
|---|---|---|
| `article_01.json` | [Trang chương trình VinUni](https://vinuni.edu.vn/aithucchien/) | Tổng quan chương trình, cấu trúc đào tạo 3+3+6, quyền lợi học bổng & FAQ. |
| `article_02.json` | [Thông tin khóa cơ bản](https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-nhan-tai-ai-thuc-chien-khoa-co-ban/) | Điều kiện dự tuyển, hồ sơ cần chuẩn bị, nghĩa vụ tham gia đầy đủ các buổi học. |
| `article_03.json` | [Tuyển sinh Khóa II–III](https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-khoa-2-3-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien-cua-tap-doan-vingroup/) | Lịch trình tuyển sinh chi tiết, thời hạn nộp hồ sơ các đợt trong năm. |
| `article_04.json` | [Kỳ thi Khóa I](https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-hanh-trinh-cua-nhung-nguoi-dam-thu-thach/) | 3 ngày thi đánh giá năng lực: Toán giải tích, đại số ma trận, tư duy thuật toán. |
| `article_05.json` | [Khai giảng Khóa I](https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/) | Lễ khai giảng khóa đầu tiên, định hướng thực hành dự án thực chiến tại Vingroup. |
| `article_06.json` | [Định hướng Khóa II](https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao-the-he-nhan-tai-ai-cho-mot-the-gioi-dang-doi-thay/) | Đối thoại cùng chuyên gia công nghệ, môi trường học tập và văn hóa Vingroup. |

### C. Hỏi Đáp Cộng Đồng Học Viên Facebook (`data/landing/facebook/`)

Thu thập và phân tầng bởi thành viên **Trần Nhật Minh** (PR #2) từ Group Facebook chính thức *Cộng đồng AI thực chiến Vingroup - VinUni*:

| Tên File | Mã Bài Viết / Permalink | Chủ Đề & Phân Loại |
|---|---|---|
| `facebook-2265832100944431.md` | [Post 2265832100944431](https://www.facebook.com/groups/congdongaithucchien/posts/2265832100944431) | Topic tìm nhà và phòng trọ cho học viên AI Thực chiến gần cơ sở đào tạo. |
| `facebook-2265986294262345.md` | [Post 2265986294262345](https://www.facebook.com/groups/congdongaithucchien/posts/2265986294262345) | Hỏi đáp thủ tục ký hợp đồng tài trợ và nhận trợ cấp sinh hoạt 8 triệu/tháng. |
| `facebook-2266703847523923.md` | [Post 2266703847523923](https://www.facebook.com/groups/congdongaithucchien/posts/2266703847523923) | Chuẩn bị phần cứng máy tính, GPU và cài đặt môi trường Python trước ngày học. |
| `facebook-2267558134105161.md` | [Post 2267558134105161](https://www.facebook.com/groups/congdongaithucchien/posts/2267558134105161) | Kinh nghiệm làm bài thi Đánh giá năng lực đầu vào (Toán ma trận & Logic). |
| `facebook-2267792147415093.md` | [Post 2267792147415093](https://www.facebook.com/groups/congdongaithucchien/posts/2267792147415093) | Quy định điểm danh và giải quyết nghỉ phép có lý do bất khả kháng. |
| `facebook-2268520560675585.md` | [Post 2268520560675585](https://www.facebook.com/groups/congdongaithucchien/posts/2268520560675585) | Cơ hội thực tập dự án thực tế tại VinFast, VinAI và VinBigData. |
| `facebook-2269350197259288.md` | [Post 2269350197259288](https://www.facebook.com/groups/congdongaithucchien/posts/2269350197259288) | Tiêu chí đánh giá Milestone hàng tuần và nghiệm thu Capstone Project. |
| `facebook-2273948740132767.md` | [Post 2273948740132767](https://www.facebook.com/groups/congdongaithucchien/posts/2273948740132767) | Hướng dẫn sử dụng cơ sở vật chất VinUni: Thư viện, KTX, Gym và bể bơi Olympic. |
| `facebook-2274940100033631.md` | [Post 2274940100033631](https://www.facebook.com/groups/congdongaithucchien/posts/2274940100033631) | Kinh nghiệm làm quen văn hóa doanh nghiệp và phong cách Vibe Coding. |
| `facebook-2275874186606889.md` | [Post 2275874186606889](https://www.facebook.com/groups/congdongaithucchien/posts/2275874186606889) | Các kênh hỗ trợ học tập: Discord nhóm, Mentor trợ giảng và Office Hours. |
| `tong-hop-ai-in-action-facebook.md` | Tổng hợp toàn diện | Bản phân tầng FAQ P0 (Tools), P1 (Coding/Git), P2 (AI Foundations). |

---

## 3. Quy Trình Chuẩn Hóa Văn Bản (Data Standardization)

1. **Trích xuất PDF (`task3_convert_markdown.py`)**:
   - Sử dụng thư viện `pypdfium2` để đọc trực tiếp lớp Text Layer dạng vector của PDF (thời gian trích xuất chỉ ~0.8 giây cho 22 trang).
   - Tích hợp nội dung OCR Blueprint Fallback để bù đắp các trang slide có biểu đồ và đồ họa, đảm bảo không bỏ sót thông tin khảo sát thực tế.

2. **Chuẩn hóa Metadata Header**:
   - Gắn trực tiếp Header `# {Tiêu đề}`, `**Source:** {URL hoặc Tên file}`, `**Ngày trích xuất:**` vào đầu mỗi văn bản Markdown.
   - Giúp các chunk khi cắt ra đều kế thừa đầy đủ metadata phục vụ citation trích dẫn nguồn.

3. **Nghiệm thu chất lượng (`tests/test_acceptance.py`)**:
   - 3 file Legal Markdown: Độ dài đạt **42,577 ký tự** (>32k ký tự yêu cầu).
   - 6 file News Markdown: Độ dài đạt **28,364 ký tự** (>22k ký tự yêu cầu).
   - 100% file đều &ge; 200 ký tự và mã hóa chuẩn Unicode UTF-8 tiếng Việt không lỗi font.
