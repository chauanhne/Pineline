---
name: log-bug
description: Tạo bug report file .xlsx từ các TC Fail sau khi chạy vibe-test bằng Playwright. Mỗi bug là 1 file riêng theo format [TC_XX - Tên sheet - Tên chức năng/Tên Block]. Trigger khi user nhắc đến: log bug, tạo bug report, báo cáo lỗi, bug từ playwright, export bug, bug report excel, TC fail report.
---

# Log Bug — Tạo Bug Report từ TC Fail (Playwright)

## Vị trí trong Pipeline

```
init-project → ... → generate-manual-tc → vibe-test → ★ log-bug ★
                           (03_)           (execute)    (05_bug-reports/)
```

| Hướng | Skill | Đọc / Ghi |
|-------|-------|-----------|
| **Upstream** | vibe-test | Đọc file TC xlsx (cột H = Fail) + evidence (screenshots/videos) |
| **Upstream** | generate-manual-tc | Đọc nội dung Steps (cột F) + Expected (cột G) |
| **Ghi** | `05_bug-reports/` | Tạo file `.xlsx` cho từng bug |

---

## NGUYÊN TẮC CỐT LÕI

- **1 TC Fail = 1 file bug report** `.xlsx` riêng
- **Tên file** theo format chuẩn: `[TC_XX - Tên sheet - Tên chức năng/Tên Block].xlsx`
- **Evidence bắt buộc** — đính kèm screenshot/video vào file bug report
- **Nội dung lấy từ file TC** — không tự bịa description hay expected
- **Không merge nhiều bug vào 1 file** — trừ khi user yêu cầu rõ ràng

---

## GIẢI THÍCH FORMAT TÊN FILE

**Format:** `[TC_XX - Tên sheet - Tên chức năng/Tên Block].xlsx`

| Thành phần | Ý nghĩa | Ví dụ |
|-----------|---------|-------|
| `TC_XX` | XX = số phần đầu của Testcase ID (trước dấu chấm) | TC_11.3 → XX = **11** |
| `Tên sheet` | Tên sheet trong file Excel TC chứa TC bị fail | `Thông tin chung` |
| `Tên chức năng/Tên Block` | Tên section title (block UI) chứa TC bị fail, hoặc tên chức năng | `Validate Link Báo Giá` |

**Ví dụ đầy đủ:**
- TC_11.3 fail, nằm trong sheet "Thông tin chung", block "Thông tin người dùng" → `TC_11 - Thông tin chung - Thông tin người dùng.xlsx`
- TC_02.7 fail, nằm trong sheet "Đăng nhập", block "Validate Form" → `TC_02 - Đăng nhập - Validate Form.xlsx`

---

## WORKFLOW

### Step 1: Đọc Danh Sách TC Fail

**1a. Tìm file TC đã chạy:**
Scan file `.xlsx` trong `03_test-cases/` có cột H chứa giá trị bắt đầu bằng `"Fail"`:

```
Tìm thấy các TC Fail:
| TC ID   | Sheet           | Block               | Lỗi ngắn |
|---------|----------------|---------------------|----------|
| TC_11.3 | Thông tin chung | Thông tin người dùng | Toast message sai nội dung |
| TC_02.7 | Đăng nhập       | Validate Form        | Không hiển thị thông báo lỗi |
| TC_05.1 | Thanh toán      | Xử lý đơn hàng      | Button disabled không đúng state |
```

**1b. Đọc run-log.md** (nếu có trong `08_test-runs/`) để lấy thêm chi tiết lỗi.

**1c. Xác nhận với user:**
```
❌ Tìm thấy 3 TC Fail. Tôi sẽ tạo 3 file bug report:
  1. TC_11 - Thông tin chung - Thông tin người dùng.xlsx
  2. TC_02 - Đăng nhập - Validate Form.xlsx
  3. TC_05 - Thanh toán - Xử lý đơn hàng.xlsx

Bạn muốn tạo tất cả hay chỉ một số bug?
```

---

### Step 2: Thu thập Thông tin cho Từng Bug

Với mỗi TC Fail, collect đầy đủ:

| Trường | Lấy từ đâu |
|--------|-----------|
| **TC_XX** | Testcase ID (cột B) — lấy phần XX trước dấu chấm |
| **Tên sheet** | Sheet name của file TC xlsx |
| **Tên chức năng/Block** | Section title (dòng block) phía trên TC đó trong file TC |
| **Title** | Tóm tắt ngắn lỗi — tổng hợp từ cột H (Fail description) |
| **Description** | Các bước từ cột F (Test Steps), giữ nguyên đánh số 1,2,3,4... |
| **Bug** | Mô tả cụ thể lỗi thực tế — từ cột H + run-log |
| **Expected** | Nội dung từ cột G (Kết Quả Mong Đợi / Expected Results) |
| **Evidence** | File screenshot/video từ `08_test-runs/.../evidence/` |

---

### Step 3: Tạo File Bug Report Excel

Với mỗi TC Fail, tạo 1 file `.xlsx` lưu vào `05_bug-reports/`:

#### Cấu trúc file Excel (1 sheet duy nhất)

**Row 1:** Tiêu đề — `"Bug Report: [TC_XX - Tên sheet - Tên chức năng/Block]"` (merge A:B, fill `#C00000`, font trắng Bold 14)

**Row 2:** Ngày tạo — `"Ngày tạo: [DD/MM/YYYY HH:MM]"` (merge A:B)

**Row 3-9:** Các trường nội dung bug:

| Row | Cột A (Label) | Cột B (Nội dung) |
|-----|--------------|-----------------|
| 3 | **TC ID** | `TC_XX.YY` (Testcase ID đầy đủ) |
| 4 | **Title** | Tóm tắt lỗi ngắn gọn |
| 5 | **Description** | Các bước thực hiện (đánh số 1,2,3,4...) |
| 6 | **Bug** | Mô tả lỗi cụ thể hơn title |
| 7 | **Expected** | Kết quả mong đợi (từ cột G file TC) |
| 8 | **Severity** | Critical / High / Medium / Low |
| 9 | **Status** | `New` (mặc định khi tạo) |

**Row 10:** Label `"Evidence"` (cột A), đính kèm hình ảnh screenshot (cột B)

#### Quy tắc điền từng trường

**Title:**
- Tóm tắt lỗi trong 1 câu ngắn gọn, rõ ràng
- Không bắt đầu bằng "Bug" hay "Lỗi"
- ✅ Đúng: `"Toast message không hiển thị khi nhập SDT đã đăng ký FPT Play"`
- ❌ Sai: `"Bug toast message sai"`

**Description:**
- Lấy từ cột F (Các Bước Thực Hiện) của TC — giữ **nguyên thứ tự và nội dung**
- Đánh số từ 1, mỗi bước 1 dòng
- Format:
  ```
  1. Truy cập vào màn hình Thanh toán dịch vụ FPL SA
  2. Tại block Thông tin cá nhân, nhập Số điện thoại là SDT đã đăng ký FPT Play
  3. Nhập đầy đủ các trường bắt buộc khác
  4. Click button Thanh toán
  ```

**Bug:**
- Mô tả **hành vi thực tế** của hệ thống (khác với Expected)
- Chi tiết hơn Title — nêu rõ element nào bị lỗi, text gì hiển thị sai
- ✅ Ví dụ: `"Hệ thống không hiển thị toast message cảnh báo. Thay vào đó, form được submit thành công và chuyển sang trang xác nhận đơn hàng."`

**Expected:**
- Copy nguyên văn từ cột G (Kết Quả Mong Đợi) của TC
- Không chỉnh sửa nội dung

**Severity mapping từ Priority:**
| TC Priority | Bug Severity |
|------------|-------------|
| High | High |
| Medium | Medium |
| Low | Low |
| High (core flow bị break) | Critical |

**Evidence:**
- Đính kèm ảnh screenshot từ `08_test-runs/.../evidence/screenshots/FAIL_[TC_ID]_*.png` vào cột B row 10
- Nếu có video: ghi đường dẫn video vào dòng tiếp theo: `"Video: evidence/videos/FAIL_TC_01.3.mp4"`
- Nếu không có evidence → ghi: `"[Không có evidence — chạy lại vibe-test để capture]"`

#### Formatting Excel

| Thuộc tính | Giá trị |
|-----------|---------|
| Font toàn bộ | Arial 11 |
| Cột A (Label) | Width 20, Bold, fill `#D6E4F0`, align right |
| Cột B (Nội dung) | Width 80, wrap text, align top-left |
| Border | Thin border tất cả cells có data |
| Row height (nội dung dài) | Auto-fit hoặc min 40px |
| Row 1 (tiêu đề) | Fill `#C00000`, font trắng Bold 14 |

---

### Step 4: Tổ chức File trong 05_bug-reports/

**Cấu trúc thư mục:**
```
05_bug-reports/
├── [YYYY-MM-DD]/                              ← nhóm theo ngày chạy test
│   ├── TC_11 - Thông tin chung - Thông tin người dùng.xlsx
│   ├── TC_02 - Đăng nhập - Validate Form.xlsx
│   └── TC_05 - Thanh toán - Xử lý đơn hàng.xlsx
└── bug-index.md                               ← index tổng hợp tất cả bug
```

**Cập nhật `bug-index.md`** sau mỗi lần log bug:

```markdown
# Bug Index

| # | File | TC ID | Sheet | Block | Severity | Status | Ngày tạo |
|---|------|-------|-------|-------|---------|--------|---------|
| 1 | [TC_11 - Thông tin chung - Thông tin người dùng.xlsx](2026-06-06/TC_11...) | TC_11.3 | Thông tin chung | Thông tin người dùng | High | New | 06/06/2026 |
| 2 | [TC_02 - Đăng nhập - Validate Form.xlsx](2026-06-06/TC_02...) | TC_02.7 | Đăng nhập | Validate Form | Medium | New | 06/06/2026 |
```

---

### Step 5: Thông báo kết quả

```
✅ Đã tạo 3 bug report:

📁 05_bug-reports/2026-06-06/
  ├── TC_11 - Thông tin chung - Thông tin người dùng.xlsx  [High]
  ├── TC_02 - Đăng nhập - Validate Form.xlsx               [Medium]
  └── TC_05 - Thanh toán - Xử lý đơn hàng.xlsx            [High]

📋 bug-index.md đã cập nhật (tổng 3 bug mới)

Bạn muốn:
(a) Xem chi tiết nội dung 1 bug cụ thể
(b) Export tổng hợp tất cả bug vào 1 file (bug summary)
(c) Chạy lại các TC Fail sau khi dev fix
```

---

## VÍ DỤ FILE BUG REPORT HOÀN CHỈNH

**Tên file:** `TC_11 - Thông tin chung - Thông tin người dùng.xlsx`

| Label | Nội dung |
|-------|---------|
| **TC ID** | TC_11.3 |
| **Title** | Toast message không hiển thị khi nhập SDT đã đăng ký FPT Play |
| **Description** | 1. Truy cập màn hình Thanh toán dịch vụ FPL SA<br>2. Tại block Thông tin cá nhân, nhập Số điện thoại là SDT đã đăng ký FPT Play (0901234567)<br>3. Nhập đầy đủ các trường bắt buộc khác<br>4. Click button Thanh toán |
| **Bug** | Hệ thống không hiển thị toast message cảnh báo. Form được submit thành công và chuyển sang trang xác nhận, bỏ qua validation SDT đã đăng ký FPT Play. |
| **Expected** | Hệ thống show thông báo lỗi: "Số điện thoại đã đăng ký dịch vụ FPT Play." |
| **Severity** | High |
| **Status** | New |
| **Evidence** | [Hình ảnh screenshot đính kèm] |

---

## CHECKLIST TRƯỚC KHI HOÀN THÀNH

- [ ] Mỗi TC Fail có 1 file bug report riêng
- [ ] Tên file đúng format `[TC_XX - Tên sheet - Tên chức năng/Block].xlsx`
- [ ] XX trong tên file = số trước dấu chấm của Testcase ID
- [ ] Description lấy nguyên văn từ cột F (Steps), đánh số đúng thứ tự
- [ ] Expected lấy nguyên văn từ cột G, không chỉnh sửa
- [ ] Evidence được đính kèm (ảnh) hoặc ghi đường dẫn (video)
- [ ] bug-index.md đã cập nhật
- [ ] Tất cả file nằm trong `05_bug-reports/[YYYY-MM-DD]/`
