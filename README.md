# WebDocTruyen Performance Testing

Một repository chứa mã nguồn và tài liệu cho kiểm thử hiệu năng (performance testing) của dự án WebDocTruyen.

## Mô tả

Repository này tổng hợp mã frontend, backend, dữ liệu cơ sở dữ liệu và bộ kiểm thử hiệu năng để đo và tối ưu hóa hiệu năng của WebDocTruyen. Mục tiêu là cung cấp các kịch bản, cấu hình và tài liệu để chạy thử tải, thu thập số liệu và tìm điểm nghẽn hiệu năng.

## Ngôn ngữ & Công nghệ chính
- CSS, SCSS, HTML, JavaScript — giao diện & tài nguyên frontend
- PHP — backend (API / server-side)
- Python — scripts kiểm thử/performance nhỏ

(Tỷ lệ ngôn ngữ theo phân tích repository: CSS 23.4%, JavaScript 22.7%, SCSS 20.9%, PHP 16.6%, HTML 15.3%, Python 1.1%)

## Cấu trúc thư mục
- `.vscode/` — cấu hình editor (tùy chọn)
- `frontend/` — mã nguồn frontend (HTML/CSS/JS/SCSS)
- `backend/` — mã nguồn server (PHP)
- `database/` — các script / dump liên quan tới cơ sở dữ liệu
- `tests/` — kịch bản kiểm thử hiệu năng, script tự động
- `docs/` — tài liệu bổ sung (ví dụ: `comment-change-log.md`)

## Hướng dẫn nhanh (Quick start)
Các bước dưới đây mang tính hướng dẫn chung; hãy điều chỉnh theo cấu hình thực tế trong repo.

1. Clone repository

```bash
git clone https://github.com/ductien1904/WebDocTruyen_PerformanceTesting.git
cd WebDocTruyen_PerformanceTesting
```

2. Backend (PHP)
- Nếu backend là các file PHP thuần, bạn có thể chạy máy chủ PHP built-in cho môi trường phát triển:

```bash
# Từ thư mục gốc (hoặc vào thư mục backend nếu cần)
php -S localhost:8000 -t backend/
```

- Nếu dự án dùng Docker, Composer hoặc framework (Laravel, Symfony...), dùng lệnh tương ứng (docker-compose up, composer install, v.v.). Xem nội dung trong `backend/` để biết lệnh chính xác.

3. Frontend
- Nếu frontend là static site: mở `frontend/index.html` trong trình duyệt hoặc host bằng một HTTP server tĩnh.
- Nếu có `package.json` (Node.js), cài phụ thuộc và chạy:

```bash
cd frontend
npm install
npm run dev # hoặc npm start
```

4. Cơ sở dữ liệu
- Import các script SQL hoặc cấu hình từ `database/`. Ví dụ:

```bash
# Ví dụ (MySQL)
mysql -u <user> -p <database_name> < database/dump.sql
```

5. Chạy kiểm thử hiệu năng
- Thư mục `tests/` chứa các kịch bản kiểm thử. Nếu có file `requirements.txt` hoặc phụ thuộc Python:

```bash
cd tests
python -m venv .venv
source .venv/bin/activate  # trên macOS/Linux
pip install -r requirements.txt  # nếu có

# Chạy pytest nếu dùng pytest
pytest

# Hoặc chạy Locust nếu repo cung cấp locustfile
locust -f locustfile.py
```

Lưu ý: Điều chỉnh theo nội dung thực tế trong `tests/`. Nếu bạn không thấy các file yêu cầu, mở `tests/` để kiểm tra README hoặc script cụ thể.

## Ghi chú về đo đạc & thu thập số liệu
- Bật logging và thu thập metrics (CPU, memory, response times, error rates) khi chạy các bài kiểm thử.
- Có thể sử dụng các công cụ như Locust, JMeter, k6, Gatling hoặc custom Python scripts.
- Lưu trữ kết quả ở thư mục `tests/results/` (hoặc nơi phù hợp) và đính kèm file log / báo cáo vào PR khi chia sẻ kết quả.

## Tài liệu
- Xem `docs/comment-change-log.md` để biết lịch sử thay đổi liên quan tới comment hoặc ghi chú phát triển.

## Cách đóng góp
1. Fork repository
2. Tạo branch feature: `git checkout -b feature/my-change`
3. Commit thay đổi, push và tạo Pull Request

Vui lòng mô tả rõ: cách tái tạo, bước chạy test, kết quả trước/sau và bất kỳ ảnh hưởng hiệu năng nào.

## Liên hệ
- Tác giả / chủ repo: @ductien1904

## License
Thêm thông tin license nếu cần — nếu chưa có, cân nhắc thêm file `LICENSE` với giấy phép mong muốn (MIT, Apache 2.0, v.v.).

---

Bạn muốn mình thêm badge (CI / coverage / license) hay hướng dẫn chi tiết từ file cấu hình cụ thể trong repo không?