# Corpus: thông tin chính thống về AI thực chiến VinUni

## Phạm vi và nguồn

Bao gồm nội dung trực tiếp về chương trình đào tạo Nhân tài AI thực chiến do
VinUni phối hợp với Vingroup triển khai: cấu trúc đào tạo, điều kiện tham gia,
quyền lợi, nghĩa vụ, FAQ, sự kiện, định hướng và kết quả chương trình.
Các trang hiện được chọn đều do VinUni công bố. Chưa xem tập nguồn này là đầy đủ
mọi thông tin đã được công bố trên mọi kênh.

| Landing | Nguồn công khai | Nội dung |
| --- | --- | --- |
| `news/article_01.json` | [Trang chương trình](https://vinuni.edu.vn/aithucchien/) | Tổng quan, đào tạo, quyền lợi, tuyển chọn, FAQ |
| `news/article_02.json` | [Thông tin khóa cơ bản](https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-nhan-tai-ai-thuc-chien-khoa-co-ban/) | Điều kiện, lịch, nghĩa vụ; trang có cập nhật sau ngày đăng |
| `news/article_03.json` | [Khóa II–III](https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-khoa-2-3-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien-cua-tap-doan-vingroup/) | Thông báo lịch sử, lịch dự kiến từng khóa |
| `news/article_04.json` | [Kỳ thi khóa I](https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-hanh-trinh-cua-nhung-nguoi-dam-thu-thach/) | Hoạt động đánh giá đầu vào |
| `news/article_05.json` | [Khai giảng khóa I](https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/) | Mô hình 3+3+6, hướng chuyên môn, triển khai |
| `news/article_06.json` | [Định hướng và khai giảng khóa II](https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao-the-he-nhan-tai-ai-cho-mot-the-gioi-dang-doi-thay/) | Đào tạo, đối thoại chuyên gia, định hướng thực hành |
| `news/article_07.json` | [Facebook post 19VnUE1HCw](https://www.facebook.com/share/p/19VnUE1HCw/) | Bài đăng chính thức trang Đào tạo Nhân tài AI thực chiến (thông báo tuyển sinh/chương trình) |
| `news/article_08.json` | [Facebook post 19R69XNq9q](https://www.facebook.com/share/p/19R69XNq9q/) | Bài đăng chính thức: thông tin mở đơn ứng tuyển, tiêu chí tuyển chọn, quyền lợi |
| `news/article_09.json` | [Facebook post pfbid0Q84...](https://www.facebook.com/DaotaoNhantaiAIthucchien/posts/pfbid0Q84nkwiExfSXfMzGQydHUHhR45eVgcXAxiKLYkwtwpHMeif4zB522WGXfQge1Uzal) | Bài đăng chính thức: Vingroup chính thức mở tuyển sinh khóa mới |
| `legal/vinuni-ai20k-so-tay-hoc-vien-v2.1.pdf` | [Sổ tay v2.1](https://vinuni.edu.vn/aithucchien/wp-content/uploads/2026/06/20K-AI-Handbook-ver2.1.pdf) được liên kết từ trang chương trình | Sổ tay học viên chính thức; PDF gốc tải trực tiếp |
| `legal/vinuni-ai20k-chinh-sach-tuyen-sinh.pdf` | Tổng hợp từ [trang tuyển sinh khóa cơ bản](https://vinuni.edu.vn/vi/thong-tin-tuyen-sinh-chuong-trinh-dao-tao-nhan-tai-ai-thuc-chien-khoa-co-ban/) + [trang khóa 2-3](https://vinuni.edu.vn/vi/chinh-thuc-mo-cong-nhan-ho-so-tuyen-sinh-khoa-2-3-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien-cua-tap-doan-vingroup/) | Chính sách tuyển sinh: điều kiện, quyền lợi, nghĩa vụ, lịch |
| `legal/vinuni-ai20k-lich-su-trien-khai.pdf` | Tổng hợp từ 3 trang VinUni: [khai giảng khóa I](https://vinuni.edu.vn/vi/vingroup-khai-giang-khoa-dau-tien-chuong-trinh-dao-tao-20-000-nhan-tai-ai-thuc-chien/) + [kỳ thi đầu vào](https://vinuni.edu.vn/vi/3-ngay-thi-ai-thuc-chien-hanh-trinh-cua-nhung-nguoi-dam-thu-thach/) + [định hướng khóa II](https://vinuni.edu.vn/vi/dao-tao-nhan-tai-ai-thuc-chien-kien-tao-the-he-nhan-tai-ai-cho-mot-the-gioi-dang-doi-thay/) | Lịch sử triển khai, mô hình đào tạo thực tế |

## Cách tạo tài liệu legal tổng hợp

Hai PDF tổng hợp (`chinh-sach-tuyen-sinh` và `lich-su-trien-khai`) được tạo tự động
từ nội dung HTML công khai của VinUni bằng hàm `_build_pdf_from_pages()` trong
`src/task1_collect_legal_docs.py`. Nội dung được trích xuất nguyên văn từ HTML,
không thêm thông tin biên tập. Nguồn gốc (URL, ngày thu thập) được ghi trong tiêu đề PDF.

Cách tra lại nguồn: mở PDF → xem phần "Nguon:" ở đầu tài liệu → truy cập URL đó.

## Thu thập bài viết Facebook (Playwright)

Các bài viết trên fanpage chính thức **Đào tạo Nhân tài AI thực chiến** của Vingroup/VinUni
được thu thập tự động qua `_crawl_facebook_sync()` trong `src/task2_crawl_news.py`.
Do Facebook yêu cầu JavaScript rendering và chặn requests tĩnh:
- Sử dụng Playwright kết hợp trình duyệt Chrome hệ thống (`chrome.exe`) ở chế độ headless.
- Đợi DOM tải hoàn tất, trích xuất text từ các container bài viết chính (`[data-ad-comet-preview="message"]`, `div[dir="auto"]`), loại bỏ văn bản trùng lặp và làm sạch bằng `_clean_markdown()`.
- Tự động đóng các modal/dialog (chính sách cookie, yêu cầu đăng nhập) để lấy toàn văn bài viết công khai mà không cần đăng nhập.

## Quy tắc làm sạch và truy vết

- Chỉ lấy phần bài viết hoặc các mục chương trình đã chọn; bỏ điều hướng, tin
  gợi ý khác chủ đề, ảnh/video rỗng và carousel. Trang tổng quan không thu thập
  danh sách hồ sơ cá nhân, lời chứng thực của học viên và thông tin liên hệ cá nhân.
- Giữ câu hỏi FAQ cùng câu trả lời; mở rộng ô gộp trong bảng để không lệch lịch
  giữa khóa, đợt và ngày. Chuẩn hóa Unicode NFC, bỏ tracking trong URL.
- Bài lịch sử vẫn được giữ, không xem lịch dự kiến cũ là thông báo hiện hành.
  Lưu riêng `date_published`, `date_modified`, `date_crawled`; không suy diễn ngày
  đăng khi trang không cung cấp metadata.
- Mỗi Markdown ghi đường dẫn landing, URL và SHA256. Tên file giữ cố định khi
  chạy lại; thay đổi corpus đòi hỏi chạy lại index/evaluation về sau.
- Nguồn công khai không đồng nghĩa giấy phép mở. Các trang VinUni có thông báo
  bản quyền; chưa xác minh được giấy phép tái phân phối toàn văn. Cần kiểm tra
  quyền sử dụng trước khi xuất bản corpus ra ngoài phạm vi bài tập.

## Nguồn loại khỏi corpus

Ba PDF Nghị quyết 57, Nghị quyết 71 và Quyết định 127 là chính sách quốc gia,
không phải quy định riêng của AI20K. Chúng được chuyển sang
`archive/excluded-national-policies/` ngoài `data/` để có thể khôi phục, và đã
loại khỏi cấu hình tải. Không dùng chúng để trả lời về nghĩa vụ học viên.

Trang Vingroup trả 403/timeout trong lần thử. Không dùng bản tin đăng lại của Bộ
VHTTDL vì trùng sự kiện khai giảng đã có nguồn VinUni trực tiếp.

PDF Handbook v2.0 từ `registrar.vinuni.edu.vn` không dùng vì server timeout liên tục
dù HEAD request trả 200; kết nối TCP từ Python không ổn định.

## Trạng thái acceptance

- **Corpus phase:** 6/8 tests PASS ✅ (test_acceptance × 3, test_corpus_quality × 3)
- **Evaluation phase:** 2 tests FAIL — chờ giai đoạn sau (golden_dataset.json, RESULT.md)

Chạy kiểm tra corpus: `python -m pytest tests/test_acceptance.py tests/test_corpus_quality.py -q`
