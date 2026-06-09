# Test Run Log — Thông tin chung

- **Ngày chạy:** 09/06/2026 23:48 → 10/06/2026 00:05
- **File TC:** `03_test-cases/functional/Thông tin chung_result.xlsx`
- **Môi trường:** STG — https://staging.fpt.vn/checkout/{id}/payment
- **Sản phẩm test:** Access Point AC1200T test (https://staging.tongdaiwifi.vn/thiet-bi-thong-minh/access-point-ac1200t-test)
- **Họ tên test:** Chúc ngủ ngon nha
- **Người chạy:** Claude Code (Playwright Python automation)

## Kết quả tổng quan

| Metric | Số lượng | % |
|--------|---------|---|
| **Tổng TC** | 135 | 100% |
| **Pass** | 30 | 22% |
| **Fail** | 1 | 1% |
| **Manual** | 99 | 73% |
| **Skip** | 5 | 4% |

## Danh sách TC Fail

| Row | TC ID | Mô tả lỗi | Evidence |
|-----|-------|-----------|---------|
| 13 | TC_11.x | Icon back có `md:pointer-events-none` trên desktop — không click được | `evidence/screenshots/FAIL_TC_13_*.png` |

## Danh sách TC Skip

| Row | Lý do |
|-----|-------|
| 131 | Bỏ qua theo yêu cầu (ưu đãi) |
| 143 | Bỏ qua theo yêu cầu (ưu đãi) |
| 145 | Bỏ qua theo yêu cầu (ưu đãi) |
| 146 | Bỏ qua theo yêu cầu (ưu đãi) |
| 147 | Bỏ qua theo yêu cầu (ưu đãi) |

## TC Manual (99 rows)

Các TC được đánh Manual do:

| Lý do | Ví dụ rows |
|-------|-----------|
| Yêu cầu điền form đầy đủ để chuyển sang Step 2 | 53-70, 78-88, 93-118, 120-124, 127-130, 132-135 |
| Email field không áp dụng cho AC1200T (chỉ có Hyperfast/UltraFast) | 43-49 |
| Nhà riêng/Chung cư không áp dụng cho AC1200T (SA device) | 72, 73, 75, 77 |
| Dropdown địa chỉ yêu cầu tương tác phức tạp (chọn từng cấp) | 53-70 |
| Timeout 20+ phút, 3rd party payment page | 150-156 |
| Màn hình Hoàn tất đơn hàng (cần hoàn thành thanh toán thực) | 159-168 |
| Màu sắc/visual UI (cần human judgment) | 16, 18 |

## TC Pass chi tiết

| Row | Nội dung | Ghi chú |
|-----|---------|---------|
| 12 | Click Logo FPT Telecom → điều hướng đúng | — |
| 14 | Click back từ tongdaiwifi.vn | — |
| 20 | Block Sản phẩm dịch vụ hiển thị | — |
| 21 | Tên gói dịch vụ hiển thị | — |
| 22 | Chu kỳ gói hiển thị | — |
| 23 | Giá gói hiển thị | — |
| 24 | Icon gói hiển thị | — |
| 27 | Viền xanh khi focus Họ tên | Phát hiện qua `has-[input:focus]:border-brand-blue-primary` |
| 28 | Btn X hiển thị sau nhập Họ tên | — |
| 29 | Click btn X → xóa Họ tên | `button[aria-label='Clear']` |
| 30 | Lỗi khi để trống Họ tên | — |
| 31 | Lỗi khi nhập khoảng trắng Họ tên | — |
| 32 | Chấp nhận họ tên có khoảng trắng đầu cuối | — |
| 33 | Lỗi khi nhập ký tự đặc biệt Họ tên | — |
| 34 | Truncate Họ tên >100 ký tự | — |
| 36 | Btn X hiển thị sau nhập SDT | — |
| 37 | Click btn X → xóa SDT | Clear button thứ 2 trong 2-column grid |
| 38 | Lỗi khi để trống SDT | — |
| 39 | Field chấp nhận/validation ký tự không phải số | — |
| 40 | Lỗi SDT 10 số đầu khác 0 | — |
| 41 | Truncate SDT >10 số | — |
| 52 | Tỉnh/TP mặc định rỗng | Custom combobox, placeholder "Chọn tỉnh thành phố" |
| 90 | Placeholder Ghi chú | "Gọi cho tôi trước 30 phút nhé!" |
| 92 | Truncate Ghi chú >100 ký tự | — |
| 126 | Block Phương thức thanh toán hiển thị | — |
| 139 | Hyperlink điều khoản tồn tại + href hợp lệ | Link `a.text-brand-blue-primary` → fpt.vn/shop/privacy-policy |
| 140 | Tên gói trong Block Thông tin thanh toán | — |
| 144 | Btn Áp dụng enable/disable theo mã KM | — |
| 149 | Validation submit khi chưa điền đủ | 6 lỗi xuất hiện |

## Ghi chú kỹ thuật

- Checkout URL là dynamic, mỗi session có ID riêng → script tự navigate từ product page
- Location HCM + Bến Thành được chọn qua popup khi click "Mua ngay"
- Cookie consent banner có thể che một số elements (điều khoản link)
- Back button có `md:pointer-events-none` → disabled trên desktop (1440px) → **Bug**
- AC1200T là sản phẩm SA/thiết bị, không có field Email và radio Nhà riêng/Chung cư
