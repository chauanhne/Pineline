---
name: vibe-test
description: Thực thi test case tự động bằng Playwright dựa trên file TC đã gen ra. Đọc file test case (.xlsx), spec/URD để hiểu context, yêu cầu user cung cấp test data, sau đó dùng Playwright chạy từng TC và ghi kết quả Pass (xanh lá) / Fail (đỏ) vào cột H "Kết Quả Thực Hiện (Actual Result)". Trigger khi user nhắc đến: vibe test, chạy test, execute TC, run test case, test tự động, kiểm thử playwright, chạy playwright, auto test.
---

# Vibe Test — Thực thi TC tự động bằng Playwright

## Vị trí trong Pipeline

```
init-project → create-test-plan → analyze-req → generate-manual-tc → ★ vibe-test ★ → log-bug
   (00_)           (01_)            (02_)              (03_)               (execute)    (05_)
```

| Hướng | Skill | Đọc / Ghi |
|-------|-------|-----------|
| **Upstream** | generate-manual-tc | Đọc file Excel TC từ `03_test-cases/` |
| **Upstream** | analyze-req / 00_input/ | Đọc spec/URD để hiểu context |
| **Downstream** | log-bug | Cung cấp danh sách TC Fail + evidence |

---

## NGUYÊN TẮC CỐT LÕI

- **Đọc TC trước, hỏi data sau** — không thực thi khi chưa có đủ test data
- **Chạy từng TC** theo thứ tự trong file Excel, không bỏ qua TC nào
- **Ghi kết quả trực tiếp vào file Excel** — cột H, màu xanh lá (Pass) / đỏ (Fail)
- **Lưu evidence** (screenshot/video) cho mỗi TC Fail
- **Không sửa nội dung TC** — chỉ điền cột H

---

## WORKFLOW

### Step 1: Đọc File TC & Spec

**1a. Tìm file TC:**
Scan thư mục `03_test-cases/` để liệt kê các file `.xlsx`:
```
Tìm thấy:
- 03_test-cases/functional/AI_ClaudeCode_DangNhap.xlsx (25 TC)
- 03_test-cases/functional/AI_ClaudeCode_ThanhToan.xlsx (18 TC)
```

Hỏi user: **"Bạn muốn chạy file TC nào? (Chọn 1 hoặc nhiều file)"**

**1b. Đọc file TC được chọn:**
Với mỗi file, extract toàn bộ TC:
- Sheet name → tên feature
- Cột B (Testcase ID), C (Priority), D (Test Title), E (Pre-condition), F (Steps), G (Expected Results)
- Bỏ qua các dòng section title (không có Testcase ID)
- Ghi nhận dòng nào đã có giá trị ở cột H (đã chạy trước đó)

**1c. Đọc context (nếu có):**
- `00_input/` — đọc URD/spec liên quan để hiểu business rules
- `02_analyze-requirements/MEMORY.md` — đọc context nếu có
- `CLAUDE.md` — đọc project info (URL, môi trường)

**Tóm tắt sau khi đọc:**
```
📋 Đã đọc file TC:
- File: AI_ClaudeCode_DangNhap.xlsx
- Tổng TC: 25 (High: 10, Medium: 10, Low: 5)
- Môi trường: STG — https://stg.example.com
- TC đã chạy: 0 / 25
```

---

### Step 2: Yêu cầu Test Data

Trước khi chạy, tổng hợp **toàn bộ data cần thiết** từ cột E (Pre-condition / Test Data) của tất cả TC và hỏi user cung cấp **1 lần duy nhất**.

Trình bày dạng bảng:

```
📝 Để thực thi 25 TC, tôi cần bạn cung cấp các thông tin sau:

| # | Dữ liệu cần | Dùng cho TC | Ví dụ |
|---|-------------|-------------|-------|
| 1 | Tài khoản admin hợp lệ (username + password) | TC_01.1, TC_01.2, TC_01.5 | admin@fpt.vn / Pass@123 |
| 2 | Tài khoản user KHÔNG có quyền | TC_01.3 | user_norole@fpt.vn / ... |
| 3 | Số điện thoại đã đăng ký FPT Play | TC_01.8 | 0901234567 |
| 4 | URL môi trường test | Tất cả TC | https://stg.example.com |
| 5 | [CẦN BA CONFIRM] — OTP expire time | TC_01.12 | Confirm trước khi chạy TC này |

Vui lòng cung cấp đầy đủ trước khi bắt đầu chạy test.
```

**Quy tắc:**
- **Gộp data trùng lặp** — mỗi loại data chỉ hỏi 1 lần
- **TC có `[CẦN BA CONFIRM]`** → cảnh báo, hỏi user có muốn skip hay dừng để confirm trước
- **KHÔNG bắt đầu chạy** khi chưa nhận đủ data từ user

---

### Step 3: Khởi tạo Playwright & Xác nhận Môi trường

Sau khi nhận đủ test data từ user:

```python
# Khởi tạo Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False để user thấy quá trình
    context = browser.new_context(
        record_video_dir="evidence/videos/",      # Ghi video toàn bộ session
        viewport={"width": 1366, "height": 768}
    )
    page = context.new_page()
```

**Kiểm tra môi trường trước khi chạy:**
1. Navigate đến URL môi trường
2. Kiểm tra trang load thành công (status 200, không có error page)
3. Thông báo: **"Môi trường [URL] đang hoạt động. Bắt đầu chạy [N] TC..."**

Nếu môi trường không accessible → dừng, thông báo lỗi, KHÔNG chạy tiếp.

---

### Step 4: Thực thi Từng TC

Chạy TC **theo thứ tự** từ trên xuống trong file Excel. Với mỗi TC:

#### 4a. Parse TC
- Đọc TC ID, Priority, Steps (cột F), Expected Results (cột G), Pre-condition (cột E)
- Bỏ qua TC đã có kết quả ở cột H (trừ khi user yêu cầu chạy lại)

#### 4b. Thực thi Steps
- Chuyển từng step thành Playwright action:

| Từ khóa trong Steps | Playwright action |
|---------------------|------------------|
| `Truy cập vào màn hình [X]` | `page.goto(url_of_screen)` |
| `Nhập [value] vào [field]` | `page.fill(selector, value)` |
| `Click button [X]` | `page.click(selector)` |
| `Check [element]` | Assert + screenshot |
| `Chọn [option] từ dropdown` | `page.select_option(selector, value)` |
| `Upload file [X]` | `page.set_input_files(selector, file_path)` |

- Sau mỗi step có `"Check"` → chụp screenshot tự động
- Dùng **Playwright locator strategies**: text, role, label, placeholder — ưu tiên semantic locator trước CSS/XPath

#### 4c. Verify Expected Results
So sánh kết quả thực tế với cột G (Expected Results):
- Kiểm tra text hiển thị, toast message, URL redirect, element visible/hidden
- Nếu **tất cả** expected đều đúng → **PASS**
- Nếu **bất kỳ** expected nào sai → **FAIL**

#### 4d. Ghi kết quả vào cột H
Sau mỗi TC, cập nhật ngay vào file Excel:

**PASS:**
- Giá trị: `"Pass"`
- Fill color: `#00B050` (xanh lá)
- Font: Trắng, Bold
- Thêm timestamp: `"Pass — HH:MM DD/MM/YYYY"`

**FAIL:**
- Giá trị: `"Fail — [mô tả ngắn lỗi]"`
- Fill color: `#FF0000` (đỏ)
- Font: Trắng, Bold
- Thêm timestamp: `"Fail — HH:MM DD/MM/YYYY"`

#### 4e. Lưu Evidence khi FAIL
Với mỗi TC Fail:
- **Screenshot**: `evidence/screenshots/FAIL_[TC_ID]_[timestamp].png`
- **Video clip**: cắt đoạn video tương ứng TC đó (nếu ghi video): `evidence/videos/FAIL_[TC_ID].mp4`
- Ghi nhận: URL hiện tại, error message (nếu có), actual behavior

**Thư mục evidence:**
```
08_test-runs/[YYYY-MM-DD_HH-MM]/
  ├── evidence/
  │   ├── screenshots/
  │   │   ├── FAIL_TC_01.3_1430.png
  │   │   └── FAIL_TC_01.8_1445.png
  │   └── videos/
  │       ├── FAIL_TC_01.3.mp4
  │       └── FAIL_TC_01.8.mp4
  └── run-log.md
```

#### 4f. Progress update
Sau mỗi TC, hiển thị tiến độ trong chat:
```
[TC_01.1] ✅ Pass — Check nhập email hợp lệ
[TC_01.2] ✅ Pass — Check nhập email sai format
[TC_01.3] ❌ Fail — Check quyền truy cập: Không hiển thị thông báo lỗi đúng
[TC_01.4] ✅ Pass — ...
Tiến độ: 4/25 TC (16%) — Pass: 3 | Fail: 1
```

---

### Step 5: Tạo Run Log

Sau khi chạy xong tất cả TC, tạo file `08_test-runs/[YYYY-MM-DD]/run-log.md`:

```markdown
# Test Run Log

- **Ngày chạy:** [DD/MM/YYYY HH:MM]
- **File TC:** [tên file xlsx]
- **Môi trường:** [ENV] — [URL]
- **Người chạy:** Claude Code (Playwright automation)

## Kết quả tổng quan

| Metric | Số lượng | % |
|--------|---------|---|
| Tổng TC | 25 | 100% |
| Pass | 20 | 80% |
| Fail | 4 | 16% |
| Blocked/Skip | 1 | 4% |

## Danh sách TC Fail

| TC ID | Tên TC | Lỗi ngắn | Evidence |
|-------|--------|----------|---------|
| TC_01.3 | Check quyền truy cập không có quyền | Không hiển thị thông báo lỗi | [screenshot](evidence/screenshots/FAIL_TC_01.3_1430.png) |
| TC_01.8 | Check SDT đã đăng ký FPT Play | Toast message sai nội dung | [screenshot](evidence/screenshots/FAIL_TC_01.8_1445.png) |

## Danh sách TC Blocked/Skip

| TC ID | Lý do |
|-------|-------|
| TC_01.12 | [CẦN BA CONFIRM] — chưa có data OTP expire |

## Ghi chú
[Ghi chú thêm nếu có]
```

---

### Step 6: Thông báo kết quả & Handoff

```
✅ Vibe Test hoàn tất!

📊 Kết quả:
  - Tổng: 25 TC | Pass: 20 ✅ | Fail: 4 ❌ | Skip: 1 ⏭️
  - Pass rate: 80%
  - File TC đã cập nhật kết quả: 03_test-cases/functional/AI_ClaudeCode_DangNhap.xlsx
  - Evidence lưu tại: 08_test-runs/2026-06-06/evidence/

📋 Có 4 TC Fail. Bạn muốn:
  (a) Tạo bug report cho tất cả TC Fail → chạy skill log-bug
  (b) Xem chi tiết từng TC Fail
  (c) Chạy lại các TC Fail sau khi fix
```

---

## XỬ LÝ CÁC TRƯỜNG HỢP ĐẶC BIỆT

### TC không thể automate
Một số TC không phù hợp để automate (ví dụ: UI cosmetic, human judgment):
- Đánh dấu: `"Manual required"` ở cột H
- Fill màu: `#FFC000` (vàng cam)
- Liệt kê cho user xem xét thủ công

### Playwright không tìm được element
Khi locator không match:
1. Thử các locator thay thế (text, role, CSS)
2. Chờ tối đa 10 giây (timeout)
3. Nếu vẫn fail → đánh là **Fail** với ghi chú: `"Element not found: [selector]"`
4. Chụp screenshot trạng thái hiện tại làm evidence

### TC phụ thuộc nhau
Nếu TC_01.2 phụ thuộc kết quả TC_01.1:
- Nếu TC_01.1 Fail → TC_01.2 tự động **Blocked**
- Ghi chú: `"Blocked — TC_01.1 failed"`

### Môi trường lỗi giữa chừng
Nếu môi trường down khi đang chạy:
- Dừng tại TC hiện tại
- Đánh TC đó là **Blocked**
- Lưu progress đã có vào file Excel
- Thông báo user, đề xuất retry

---

## CHECKLIST TRƯỚC KHI BẮT ĐẦU

- [ ] Đã đọc file TC và hiểu context
- [ ] Đã đọc spec/URD liên quan
- [ ] Đã thu thập đủ test data từ user
- [ ] Đã kiểm tra môi trường accessible
- [ ] Đã xác nhận thư mục evidence sẽ lưu tại đâu
- [ ] User đã xác nhận bắt đầu chạy

## CHECKLIST SAU KHI CHẠY XONG

- [ ] Tất cả TC đã có giá trị ở cột H (Pass/Fail/Blocked/Manual required)
- [ ] File Excel đã lưu với kết quả mới nhất
- [ ] Evidence (screenshot/video) đã lưu cho tất cả TC Fail
- [ ] run-log.md đã tạo trong 08_test-runs/
- [ ] Đã thông báo kết quả tổng quan và handoff cho log-bug
