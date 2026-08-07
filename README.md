# WebDocTruyen — Performance Testing (Tập trung vào kiểm thử)

> Repository này chuyên cho mục đích kiểm thử hiệu năng (performance testing) của dự án WebDocTruyen. Nếu bạn chủ yếu làm về kiểm thử, README này sẽ tóm tắt cách thiết lập, chạy kịch bản kiểm thử (Locust), xuất kết quả và quy trình đóng góp test case.

## Tổng quan
Repository chứa:
- `frontend/` — mã frontend (tham khảo giao diện real requests)
- `backend/` — mã server (PHP) để target trong kiểm thử
- `database/` — script/dump DB dùng cho môi trường test
- `tests/` — tất cả kịch bản kiểm thử, helper scripts và thư mục kết quả
- `docs/` — tài liệu phụ trợ (ví dụ `comment-change-log.md`)

Mục tiêu chính: nhanh chóng chạy các bài kiểm thử tải/độ bền, thu thập số liệu (latency, throughput, errors), và dễ chia sẻ kết quả để phân tích.

---

## Tập trung kiểm thử (Testing-first)
Nếu bạn chủ yếu làm kiểm thử, hãy chú ý đến thư mục `tests/`. Hiện tại repo có các file sau (liên quan đến kiểm thử):
- `tests/test_locust.py` — kịch bản Locust (locustfile) chứa các hành vi người dùng mẫu (tham khảo `tests/test_locust.py` trong repo).
- `tests/export_testcase.py` — (nếu tồn tại) script hỗ trợ xuất/import test case (mở file để xem chi tiết).
- `tests/results/` — nơi lưu kết quả/CSV/ báo cáo khi chạy headless.

Mình đã xem `tests/test_locust.py` và kịch bản thực hiện các thao tác cơ bản như login, truy cập trang chủ và một nhóm route liên quan tới chapter management.

---

## Cài đặt nhanh cho kiểm thử (Locust)
1. Tạo virtualenv và cài dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\.venv\Scripts\activate   # Windows (PowerShell)
pip install -U pip
pip install locust
# Nếu repo có requirements.txt trong tests/:
# pip install -r tests/requirements.txt
```

2. Chạy Locust ở chế độ tương tác (UI):

```bash
# host là địa chỉ backend / ứng dụng đang chạy, ví dụ http://localhost:8000
locust -f tests/test_locust.py --host http://localhost:8000
# sau đó mở http://localhost:8089 để cấu hình số lượng users (spawn) và chạy
```

3. Chạy Locust headless (thường dùng cho CI / thu thập kết quả tự động):

```bash
# ví dụ chạy 200 user, spawn rate 20 user/s, trong 10 phút, lưu CSV vào tests/results/
locust -f tests/test_locust.py --host http://localhost:8000 --headless -u 200 -r 20 -t 10m --csv=tests/results/run1
```

Các file CSV tạo ra: `run1_stats.csv`, `run1_failures.csv`, `run1_requests.csv` — dùng để phân tích sau.

4. Thực thi trong Docker / CI
- Nếu muốn chạy trong container, tạo Dockerfile/compose nhỏ với Locust image hoặc cài đặt Python + locust trong CI job, rồi chạy lệnh headless trên.

---

## Hướng dẫn đọc kịch bản (test_locust.py)
- `UTTPortalUser(HttpUser)` xác định hành vi người dùng: `on_start()` gọi login bằng POST.
- Các task như `trangChu`, `chuongManagement` mô phỏng các endpoint truy cập.
- Bạn có thể thêm tags (`@tag('...')`) để nhóm test và chạy subset task bằng `-t tagname` hoặc trong UI chọn tag.

Ví dụ chạy chỉ tag `chuong_management`:

```bash
locust -f tests/test_locust.py --host http://localhost:8000 -t chuong_management --headless -u 50 -r 5 -t 5m --csv=tests/results/chuong_management
```

---

## Xuất test case / Tích hợp script helpers
- Nếu repo có `tests/export_testcase.py`, mở file đó để biết mục đích (export test case ra định dạng JSON/CSV hoặc tạo testcases động). Sử dụng script đó để:
  - Tích hợp test case từ hệ thống khác,
  - Tạo test case cho Locust tự động,
  - Lưu test case mẫu vào `tests/testcases/`.

---

## Thu thập metrics & phân tích
- Kết quả Locust CSV là nguồn chính để tính:
  - P50/P95/P99 latencies
  - Requests per second (RPS)
  - Lỗi / request failures
- Kết hợp thu thập metrics hệ thống (CPU, memory, network) bằng Prometheus/Grafana hoặc `sar`, `top`, `vmstat` khi chạy bài kiểm thử để tìm nghẽn cổ chai.
- Lưu kết quả mỗi lần chạy vào `tests/results/<timestamp>/` để dễ so sánh.

---

## Mẫu quy trình kiểm thử (recommended)
1. Chuẩn bị môi trường test: seed DB (database/), deploy backend dev (port cố định), đảm bảo frontend static hoặc server chạy.
2. Triển khai kịch bản Locust: chỉnh URL trong `tests/test_locust.py` (hoặc dùng `--host`).
3. Chạy Locust headless với cấu hình load step (tăng dần user để tìm điểm phá vỡ).
4. Thu thập logs, CSV, và metrics hệ thống.
5. Phân tích: latency percentiles, error rates, throughput; xác định bottleneck.
6. Tối ưu và lặp lại.

---

## Góp phần (Contributing)
- Nếu bạn thêm test case mới, tạo PR vào thư mục `tests/testcases/` kèm hướng dẫn/tập tin ví dụ.
- Mô tả rõ kịch bản: mục tiêu test, endpoint, dữ liệu mẫu, và bước chạy.

Commit message mẫu: `tests: add locust testcase for chapter management`.

---

## Tài liệu thêm
- Xem `docs/comment-change-log.md` để biết ghi chú phát triển.
- Xem `tests/test_locust.py` trực tiếp để hiểu chi tiết hành vi đã được mô tả.

---

## Liên hệ
- Chủ repo / liên hệ: @ductien1904
- Email: boyndt1904@gmail.com


2. Tạo template test case trong `tests/testcases/` và ví dụ cách export bằng `export_testcase.py` (mình sẽ đọc file và tạo template phù hợp).
3. Dịch README sang tiếng Anh hoặc làm song ngữ.

Bạn muốn mình làm tiếp bước nào?
