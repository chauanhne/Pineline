---
name: analyze-requirements
description: Phân tích tài liệu yêu cầu (URD, SRS, specs, user stories) từ thư mục 00_input/ và tạo các deliverable phân tích trong 02_analyze-requirements/. Sử dụng skill này khi user muốn phân tích requirement, tạo scenario map, xác định test data, đánh giá rủi ro, hoặc chuẩn bị context cho việc viết test case (manual hoặc automation). Trigger khi user nhắc đến "phân tích yêu cầu", "analyze requirements", "đọc SRS", "đọc URD", "tạo scenario", "review specs", "chuẩn bị test analysis", hoặc bất kỳ yêu cầu nào liên quan đến việc hiểu và phân rã tài liệu đầu vào thành test artifacts.
---

# Analyze Requirements

Đọc tài liệu requirement từ `00_input/`, phân tích và tạo các deliverable trong `02_analyze-requirements/` làm nền tảng cho việc viết test case (manual + automation).

## Nguyên tắc cốt lõi

- **Chỉ phân tích, không tạo code.** Đây là bước context building — output là markdown files.
- **Traceability bắt buộc.** Mọi scenario phải trace ngược về requirement ID/section gốc.
- **Viết tiếng Việt**, giữ tiếng Anh cho thuật ngữ kỹ thuật và keywords.
- **TUYỆT ĐỐI KHÔNG**: không tạo Java/Python code, không thêm scenario ngoài requirement.

---

---

## Vị trí trong Pipeline

```
init-project → create-test-plan → ★ analyze-req ★ → generate-tc → review-tc
   (00_)           (01_)              (02_)            (03_)        (11_)
                                                          ↓
                                           scan-source → implement-auto
                                              (10_)        (10_)
                                                             ↓
                                                       execute-maintain → log-bug
                                                          (10_§15)      (05_)
```

| Hướng | Skill | Đọc / Ghi |
|-------|-------|-----------|
| **Upstream** | create-test-plan | Đọc §2 Scope (modules in-scope) |
| **Upstream** | 00_input/ | Đọc tài liệu yêu cầu (BRD, SRS, wireframe) |
| **Downstream** | generate-tc | Đọc MEMORY.md, test_scenario_map.md, test_data_catalog.md |
| **Downstream** | implement-auto | Đọc MEMORY.md §4 Scenario Index, §7 Automation Context |
| **Downstream** | review-tc | Đọc MEMORY.md để đối chiếu coverage |

---

## Cách gọi Skill & Entry Modes

Skill này có **3 chế độ** — tự detect dựa trên message của user:

### Mode 1: INIT — Phân tích lần đầu
**Khi nào:** Chưa có file nào trong `02_analyze-requirements/`, hoặc user chỉ định tài liệu mới.

**Cách gọi (ví dụ):**
```
"Phân tích tài liệu trong 00_input/"
"Analyze requirements cho file URD_login.pdf"  
"Đọc SRS và tạo scenario map"
"Phân tích thêm file SRS_dashboard.docx"        ← có MEMORY.md rồi nhưng thêm DOC mới
```

**Flow:** Step 1 → 2 → 3 → 4 → 5 → 6 (đầy đủ)

**Detect:** Không có MEMORY.md HOẶC user nhắc đến file/tài liệu cụ thể chưa có trong Document Registry.

---

### Mode 2: UPDATE — Cập nhật từ feedback
**Khi nào:** Đã có kết quả phân tích, nhận feedback từ tester/BA/dev cần sửa.

**Cách gọi (ví dụ):**
```
"BA confirm OTP expire sau 5 phút, cập nhật lại"
"Sửa scenario SC-LOGIN-003: expected result sai"
"Thêm scenario cho trường hợp đăng nhập bằng SSO"
"Dev nói API đổi endpoint từ /auth sang /v2/auth"
"Xóa module Report khỏi scope"
"Cập nhật risk: module Payment nên là High thay vì Medium"
```

**Flow:** Đọc MEMORY.md → xác định file cần sửa → sửa → đồng bộ MEMORY.md

**Detect:** Có MEMORY.md VÀ user nhắc đến sửa/cập nhật/thêm/xóa/feedback + scenario ID hoặc module cụ thể.

**Chi tiết xử lý theo loại feedback:**

| User nói | Skill hiểu | Files cần cập nhật |
|----------|-----------|-------------------|
| "BA confirm [câu trả lời]" | Resolve clarification | `requirement_traceability.md` (answer + status) → `test_scenario_map.md` (thêm/sửa scenario nếu cần) → `test_data_catalog.md` → `MEMORY.md` |
| "Sửa scenario SC-xxx" | Sửa scenario cụ thể | `test_scenario_map.md` → `MEMORY.md` section 4 |
| "Thêm scenario cho [feature]" | Thêm scenario mới | `test_scenario_map.md` (append) → `MEMORY.md` section 3+4 |
| "Xóa scenario SC-xxx" | Xóa scenario | `test_scenario_map.md` (remove) → `MEMORY.md` section 3+4 |
| "Dev nói [thay đổi kỹ thuật]" | Technical change | `test_scenario_map.md` (sửa steps) → `test_data_catalog.md` → `MEMORY.md` |
| "Đổi priority/risk module X" | Điều chỉnh risk | `risk_assessment.md` → `test_scenario_map.md` (priority) → `MEMORY.md` section 3 |
| "Xóa module X khỏi scope" | Thu hẹp scope | Tất cả files: xóa rows liên quan → `MEMORY.md` → `CLAUDE.md` |
| "Thêm Figma link [url]" | Thêm UI input | Chạy Figma extract → `ui_design_specs.md` → thêm UI scenarios → `MEMORY.md` |

**Quy tắc quan trọng cho Mode UPDATE:**
- **KHÔNG tạo lại file từ đầu** — chỉ sửa phần bị ảnh hưởng
- **Luôn đồng bộ MEMORY.md** sau mỗi thay đổi
- **Ghi log** vào MEMORY.md header: `> Cập nhật lần cuối: [date] — [lý do: "BA confirm OTP 5 phút"]`
- Nếu thay đổi ảnh hưởng TC đã generate → cảnh báo: `"⚠️ Thay đổi này ảnh hưởng [N] TC đã tạo. Cần re-generate TC cho module [X]."`

---

### Mode 3: REVIEW — Xem lại kết quả
**Khi nào:** User muốn xem tổng quan kết quả phân tích hiện tại.

**Cách gọi (ví dụ):**
```
"Xem lại kết quả phân tích"
"Tổng quan MEMORY.md"
"Còn bao nhiêu clarification chưa resolve?"
"Module nào risk cao nhất?"
"Liệt kê scenario của module Login"
```

**Flow:** Đọc MEMORY.md → trình bày thông tin user cần → KHÔNG sửa file.

**Detect:** User hỏi/xem nhưng không yêu cầu sửa đổi.

---

### Detect Logic (cho Claude)

```
User message → kiểm tra:

1. Có MEMORY.md trong 02_analyze-requirements/?
   ├── KHÔNG → Mode 1: INIT
   └── CÓ → kiểm tra tiếp:
       │
       2. User nhắc đến file mới chưa có trong Document Registry?
       │  ├── CÓ → Mode 1: INIT (thêm document mới, append vào MEMORY.md)
       │  └── KHÔNG → kiểm tra tiếp:
       │
       3. User yêu cầu sửa/cập nhật/thêm/xóa/feedback?
       │  ├── CÓ → Mode 2: UPDATE
       │  └── KHÔNG → kiểm tra tiếp:
       │
       4. User hỏi/xem/review?
          ├── CÓ → Mode 3: REVIEW
          └── KHÔNG RÕ → Hỏi user: "Bạn muốn phân tích thêm tài liệu mới,
                          cập nhật kết quả hiện tại, hay xem lại tổng quan?"
```

---

## Workflow

### Step 1: Đọc Project Context

Đọc `CLAUDE.md` ở root project để hiểu:
- Tên dự án, môi trường, URL
- Quy ước đặt tên, workflow
- Các convention đã thiết lập

Nếu không tìm thấy `CLAUDE.md`, hỏi user về project context trước khi tiếp tục.

### Step 2: Quét và Đọc Tài Liệu Input

Scan thư mục `00_input/` để liệt kê tất cả file có sẵn:

```
Tìm thấy trong 00_input/:
- URD_module_login.pdf
- SRS_v2.1.docx
- wireframe_dashboard.png
```

Hỏi user: **"Tôi tìm thấy các file sau trong 00_input/. Phân tích tất cả hay chỉ một số file cụ thể?"**

Sau đó hỏi thêm: **"Có link Figma design liên quan không? (nếu có, tôi sẽ đọc design specs để tạo thêm UI test scenarios)"**

Sau khi user xác nhận, đọc từng file. Với mỗi file:
- PDF/DOCX: đọc nội dung text
- Image (wireframe, mockup): mô tả các UI element nhìn thấy
- Excel/CSV: đọc data structure

#### Đọc Figma Design (nếu có link Figma + MCP Figma đã kết nối)

Nếu user cung cấp link Figma và MCP Figma server đã kết nối, đọc design theo flow:

```
1. get_metadata(figma_link)       → lấy node map tổng quan (các frame, page)
2. get_design_context(node_id)    → lấy chi tiết từng frame: components, layout, spacing, colors
3. get_screenshot(node_id)        → lấy visual reference để mô tả
```

Với mỗi frame/page trong Figma, extract:
- **UI Components**: button, input, dropdown, modal, table, card... + trạng thái (default, hover, disabled, error)
- **Layout**: spacing, alignment, responsive breakpoints
- **Design Tokens**: colors, fonts, sizes (để verify trên UI thực)
- **Component States**: active/inactive, expanded/collapsed, loading, empty state
- **Navigation Flow**: frame nào link đến frame nào

Ghi nhận vào Document Registry trong MEMORY.md:
```
| DOC ID | File | Loại | ...
| DOC-FIG-01 | Figma: Login Flow (link) | Figma Design | ...
```

**Nếu KHÔNG có MCP Figma:**
- User có thể screenshot từng màn hình → lưu vào `00_input/` dạng image
- Hoặc export Figma sang PDF → đặt vào `00_input/`
- Skill sẽ phân tích image/PDF như bình thường

**Nếu có MCP Figma nhưng rate limit:**
Figma MCP free tier chỉ có ~6 tool calls/tháng. Ưu tiên:
1. `get_metadata` cho toàn bộ file (1 call) → biết cấu trúc
2. `get_design_context` cho các frame chính (1 call/frame) → biết components
3. `get_screenshot` chỉ khi cần verify visual → dùng tiết kiệm

### Step 3: Phân Tích và Phân Rã Requirement

Phân rã tài liệu theo cấu trúc:

```
Module → Feature → Requirement → Acceptance Criteria → Test Scenario
```

Với mỗi requirement, xác định:
- **Requirement ID** (nếu tài liệu có sẵn ID thì dùng, nếu không thì tạo: REQ-[MODULE]-[NNN])
- **Loại**: Functional / Non-functional / **UI** / Business Rule / Integration
- **Mức độ rủi ro**: High / Medium / Low (dựa trên complexity + business impact)
- **Testability**: requirement có đủ rõ ràng để viết test case không? Nếu mơ hồ → ghi vào danh sách clarification.

#### Phân tích UI scenarios (khi có Figma hoặc wireframe)

Nếu có Figma design hoặc wireframe images, tạo thêm **UI scenarios** bên cạnh functional scenarios:

| Loại UI Scenario | Từ Figma extract gì | Ví dụ Scenario |
|-----------------|---------------------|----------------|
| **Layout/Display** | Frame structure, component list | SC-LOGIN-UI-001: Kiểm tra trang Login hiển thị đúng layout (logo, email input, password input, button Đăng nhập, link Quên mật khẩu) |
| **Component State** | Component variants (default, hover, disabled, error) | SC-LOGIN-UI-002: Kiểm tra button Đăng nhập disabled khi chưa nhập đủ thông tin |
| **Design Token** | Colors, fonts, spacing values | SC-LOGIN-UI-003: Kiểm tra màu button Đăng nhập = #1890FF, font = Roboto 14px |
| **Responsive** | Breakpoints, layout changes | SC-LOGIN-UI-004: Kiểm tra trang Login hiển thị đúng trên mobile (375px) |
| **Empty/Error State** | Empty state frames, error message designs | SC-LOGIN-UI-005: Kiểm tra hiển thị khi nhập sai password 5 lần (account locked state) |
| **Navigation** | Frame-to-frame connections, prototype links | SC-LOGIN-UI-006: Kiểm tra nhấn "Quên mật khẩu" chuyển đến trang Reset Password |

**Naming convention cho UI scenarios:** `SC-[MODULE]-UI-[NNN]`

**Trong test_scenario_map.md**, UI scenarios có `Test Type = UI` và `DOC Source = DOC-FIG-XX`:

```
| SC-LOGIN-UI-001 | Layout trang Login | REQ-LOGIN-001 | DOC-FIG-01 | ... | P2 | UI |
```

**Lưu ý quan trọng:**
- UI scenarios chỉ tạo từ design có trong Figma/wireframe — không tự sáng tạo
- Nếu Figma chỉ có 1 state (default) → chỉ tạo TC cho default state, không đoán hover/disabled
- Nếu Figma có design token nhưng không specify → ghi clarification: "Figma design tokens chưa được document"

### Step 4: Tạo Deliverables

Tạo các file sau trong `02_analyze-requirements/`. Output path cố định — không thay đổi.

### Step 5: Review & Cập Nhật Kết Quả

Sau khi tạo deliverables, trình bày tóm tắt cho user review:

```
📊 Kết quả phân tích:
- Tổng requirements: [N]
- Tổng scenarios: [N] (P1: [n] | P2: [n] | P3: [n])
- Clarifications cần xử lý: [N]
- Modules: [list]

Bạn muốn review file nào trước?
```

**Vòng lặp review:** Hỏi user từng phần, nhận feedback và cập nhật. Có 5 loại feedback:

| Loại feedback | Cập nhật vào đâu | Ví dụ |
|---------------|-------------------|-------|
| Sửa/bổ sung scenario | `test_scenario_map.md` → đồng bộ MEMORY.md | "Thêm scenario logout timeout" |
| Trả lời clarification | Xem chi tiết bên dưới ↓ | "OTP expire sau 5 phút" |
| Điều chỉnh priority/risk | `risk_assessment.md` + `test_scenario_map.md` → đồng bộ MEMORY.md | "Module Payment nên là P1" |
| Bổ sung test data | `test_data_catalog.md` → đồng bộ MEMORY.md | "Thêm case email có dấu tiếng Việt" |
| Thay đổi scope | Cập nhật tất cả file liên quan + MEMORY.md + CLAUDE.md | "Bỏ module Report khỏi scope" |

> Tất cả file trong bảng trên đều nằm tại `02_analyze-requirements/`

#### Chi tiết: Cập nhật Clarification Answers

Khi BA/Dev trả lời các clarification, cập nhật theo chuỗi sau:

```
BA/Dev trả lời clarification
        │
        ▼
┌─ FILE 1: requirement_traceability.md ─────────────────────────────┐
│  Section "Clarifications Needed":                                  │
│  - Đổi Status: Open → Resolved                                    │
│  - Thêm cột Answer: ghi nguyên văn câu trả lời                    │
│  - Thêm cột Ngày resolve                                          │
│                                                                    │
│  | Req ID | Câu hỏi | Answer | Status | Ngày | Ảnh hưởng |        │
│  | REQ-PREDICT-005 | OTP expire? | 5 phút | Resolved | 07/04 | → │─┐
└────────────────────────────────────────────────────────────────────┘ │
        │                                                              │
        ▼                                                              │
┌─ FILE 2: test_scenario_map.md ────────────────────────────────────┐ │
│  NẾU answer tạo ra scenario mới hoặc thay đổi scenario hiện có:   │ │
│  - Thêm row scenario mới (ví dụ: SC-PREDICT-010 OTP expire 5p)   │◄┘
│  - Hoặc sửa Given/When/Then của scenario bị ảnh hưởng             │
│  - Hoặc xóa scenario nếu answer cho thấy không cần test           │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ FILE 3: test_data_catalog.md ────────────────────────────────────┐
│  NẾU answer ảnh hưởng test data:                                   │
│  - Thêm boundary values mới (ví dụ: OTP = 4:59, 5:00, 5:01)      │
│  - Thêm business rule data                                         │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ FILE 4: risk_assessment.md ──────────────────────────────────────┐
│  NẾU answer thay đổi risk:                                         │
│  - Cập nhật risk score nếu complexity thay đổi                     │
│  - Cập nhật thứ tự test nếu priority thay đổi                     │
└────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─ FILE 5: MEMORY.md ──────────────────────────────────────────────┐
│  LUÔN cập nhật sau mỗi lần resolve clarification:                  │
│  - Section 3 (Module Summary): cập nhật số scenario nếu thay đổi  │
│  - Section 4 (Scenario Index): thêm/sửa/xóa scenario              │
│  - Section 5 (Test Data Summary): cập nhật nếu data thay đổi      │
│  - Section 6 (Clarifications): đổi Status Open → Resolved          │
│  - Header: cập nhật timestamp "Cập nhật lần cuối"                  │
└────────────────────────────────────────────────────────────────────┘
```

**Ví dụ thực tế** (từ dự án NHA):

```
Clarification #1: "Màn hình login IAM: popup hay redirect?"
BA trả lời: "Redirect sang IAM, sau đó callback về trang chủ"

Cập nhật:
1. requirement_traceability.md → Status: Resolved, Answer: "Redirect IAM + callback"
2. test_scenario_map.md → Sửa SC-LOGIN-001: 
   Given: "Người dùng ở trang chủ" 
   When: "Nhấn Đăng nhập → Redirect sang IAM → Nhập credentials → Callback"
   Then: "Quay về trang chủ, đã đăng nhập"
3. test_data_catalog.md → Thêm: callback_url, IAM session token
4. MEMORY.md → Cập nhật section 6: Clarification #1 = Resolved
```

**Ví dụ thực tế #2:**

```
Clarification #3: "Làm tròn 2 số thập phân: áp dụng cho điểm từng trận hay tổng vòng/mùa?"
BA trả lời: "Chỉ làm tròn tổng điểm mùa, điểm từng trận giữ nguyên"

Cập nhật:
1. requirement_traceability.md → Resolved
2. test_scenario_map.md → Thêm SC-BXH-012: kiểm tra điểm từng trận KHÔNG làm tròn
3. test_data_catalog.md → Thêm boundary: 9.995 (tổng mùa → 10.00), 9.994 (→ 9.99)
4. risk_assessment.md → BXH complexity +1 (do logic làm tròn phức tạp hơn dự kiến)
5. MEMORY.md → Cập nhật tất cả sections liên quan
```

**Quy tắc cập nhật:**
- Mọi thay đổi ở file chi tiết → **phải đồng bộ lại MEMORY.md** (cập nhật số liệu, scenario index, clarification status)
- MEMORY.md luôn phản ánh trạng thái mới nhất — vì các bước sau chỉ đọc MEMORY.md để lấy context
- Ghi timestamp cập nhật vào header MEMORY.md: `> Cập nhật lần cuối: [date]`

Lặp lại cho đến khi user xác nhận: **"OK, kết quả phân tích đã đúng, tiếp tục viết test case."**

### Step 6: Handoff — Sẵn sàng cho bước tiếp theo

Khi user approve kết quả, tổng kết data flow cho bước viết TC:

```
📋 Analyze hoàn tất. Data sẵn sàng cho bước viết test case:

Manual tester đọc:
  → 02_analyze-requirements/MEMORY.md          (tổng quan + index)
  → 02_analyze-requirements/test_scenario_map.md (Given/When/Then → convert thành TC)
  → 02_analyze-requirements/test_data_catalog.md (data cho từng TC)

Automation tester đọc:
  → 02_analyze-requirements/MEMORY.md          (tổng quan + automation context)
  → 02_analyze-requirements/pom_analysis.md    (page class + elements)
  → 02_analyze-requirements/test_scenario_map.md
  → 02_analyze-requirements/test_data_catalog.md

Output test case sẽ ghi vào:
  → 03_test-cases/[loại]/TC-[MODULE]-[NNN]-[short-title].md
```

---

## Data Flow: Folder nào đọc, folder nào ghi

```
00_input/                        ← INPUT (read-only, không sửa)
  URD, SRS, specs...
        │
        ▼
02_analyze-requirements/         ← OUTPUT của skill này (đọc + ghi)
  requirement_traceability.md
  test_scenario_map.md
  test_data_catalog.md
  risk_assessment.md
  MEMORY.md                      ★ Bridge file — luôn cập nhật mới nhất
  pom_analysis.md (optional)
        │
        ▼
03_test-cases/                   ← OUTPUT của bước viết TC (skill tiếp theo ghi vào)
  functional/
  regression/
  smoke/
  ...
```

**Nguyên tắc:**
- `00_input/` — chỉ đọc, không bao giờ sửa file gốc
- `02_analyze-requirements/` — skill này sở hữu, đọc + ghi + cập nhật khi có feedback
- `03_test-cases/` — skill viết TC sở hữu, skill này không ghi vào
- `CLAUDE.md` (root) — append summary, không ghi đè

---

## Deliverables (6 files + 1 optional)

### 1. `requirement_traceability.md`
Ma trận truy vết từ requirement gốc đến scenario.

```markdown
# Requirement Traceability Matrix

## Tài liệu nguồn
| # | File | Loại | Phiên bản | Ghi chú |
|---|------|------|-----------|---------|

## Ma trận truy vết
| Req ID | Mô tả requirement | DOC Source | Nguồn (file + section) | Loại | Scenarios liên quan | Mức rủi ro |
|--------|-------------------|-----------|----------------------|------|---------------------|------------|
| REQ-LOGIN-001 | Đăng nhập bằng email + password | DOC-01 | URD_login.pdf §3.1 | Functional | SC-LOGIN-001, SC-LOGIN-002 | High |

## Requirement cần làm rõ (Clarifications Needed)
| # | Req ID | Câu hỏi | Answer | Status | Ngày resolve | Ảnh hưởng |
|---|--------|---------|--------|--------|-------------|-----------|
| 1 | REQ-LOGIN-003 | OTP expire sau bao lâu? | — | Open | — | Không viết được TC cho OTP timeout |
```

### 2. `test_scenario_map.md`
Bản đồ scenario chi tiết theo format Given/When/Then.

```markdown
# Test Scenario Map

## Tổng quan
- Tổng số scenarios: [N]
- Phân bổ theo priority: P1: [n] | P2: [n] | P3: [n]
- Phân bổ theo module: [module]: [n] | ...

## Scenarios

### [Module Name]

| Scenario ID | Feature | Req ID | DOC Source | Given | When | Then | Priority | Test Type |
|-------------|---------|--------|-----------|-------|------|------|----------|-----------|
| SC-LOGIN-001 | Đăng nhập | REQ-LOGIN-001 | DOC-01 | Người dùng ở trang login | Nhập email + password hợp lệ và nhấn Đăng nhập | Chuyển đến trang Dashboard | P1 | Functional |
| SC-LOGIN-002 | Đăng nhập | REQ-LOGIN-001 | DOC-01 | Người dùng ở trang login | Nhập email sai format | Hiển thị thông báo lỗi "Email không hợp lệ" | P1 | Negative |
```

Quy tắc:
- **Scenario ID**: `SC-[MODULE]-[NNN]` (bắt đầu từ 001)
- **Req ID**: link ngược về requirement_traceability.md
- **Priority**: P1 (critical path), P2 (important), P3 (nice-to-have)
- **Test Type**: Functional / Negative / Boundary / UI / Integration / Performance
- Mỗi acceptance criteria tạo tối thiểu 1 positive + 1 negative scenario

### 3. `test_data_catalog.md`
Catalog dữ liệu test cần chuẩn bị.

```markdown
# Test Data Catalog

## Tổng quan
Dữ liệu kiểm thử cần chuẩn bị cho các scenario trong test_scenario_map.md.

## Theo Module

### [Module Name]

| Field | Data Type | DOC Source | Ràng buộc | Valid (ví dụ) | Invalid (ví dụ) | Boundary | Scenarios sử dụng |
|-------|-----------|-----------|-----------|---------------|-----------------|----------|-------------------|
| Email | String (email format) | DOC-01 | Required, max 255 chars | user@example.com | user@, @domain.com, (empty) | 255 chars, 256 chars | SC-LOGIN-001, SC-LOGIN-002 |

## Test Accounts cần chuẩn bị
| Vai trò | Mục đích | Scenarios |
|---------|----------|-----------|
| Admin | Test chức năng quản lý | SC-ADMIN-001..005 |

## Dữ liệu đặc biệt
| Loại | Mô tả | Cách chuẩn bị |
|------|-------|--------------|
| Ảnh > 5MB | Test upload limit | Tạo file test |
```

### 4. `risk_assessment.md`
Đánh giá rủi ro và đề xuất ưu tiên test.

```markdown
# Risk Assessment & Test Priority

## Ma trận rủi ro
| Module / Feature | Business Impact (1-5) | Complexity (1-5) | Risk Score | Đề xuất |
|-----------------|----------------------|-------------------|------------|---------|
| Login | 5 | 2 | 10 | Test đầu tiên, smoke test bắt buộc |

## Vùng rủi ro cao
- [Liệt kê các area cần focus test]

## Dependencies & Integration Points
| Feature A | Phụ thuộc vào | Ảnh hưởng nếu fail |
|-----------|--------------|-------------------|

## Đề xuất thứ tự test
1. [Smoke test critical path]
2. [Module có risk score cao nhất]
3. ...
```

### 5. `MEMORY.md`
File tracking kết quả phân tích — **bridge** giữa bước analyze → manual viết TC → automation generate code. Lưu tại `02_analyze-requirements/MEMORY.md`. Các skill/agent ở bước sau (viết TC manual, generate automation code) sẽ đọc file này để lấy context thay vì đọc lại toàn bộ requirement.

**Thiết kế cho multi-document:** Dự án có thể có nhiều tài liệu input (file 01, 02, 03...) được phân tích ở các thời điểm khác nhau. MEMORY.md phải track **theo từng document** để:
- Biết scenario nào thuộc document nào
- Generate-tc có thể filter "chỉ tạo TC cho document 02"
- Phân tích thêm document mới → append, không ghi đè kết quả cũ

```markdown
# MEMORY — Analyze Requirements Output

> File này được tạo tự động bởi skill analyze-requirements.
> Mục đích: cung cấp context cho các bước tiếp theo (viết TC manual, generate automation code).
> Cập nhật lần cuối: [date]

## 1. Project Overview
- **Dự án:** [tên]
- **Mô tả:** [2-3 câu tóm tắt dự án đang test cái gì]
- **Môi trường:** [DEV/STG/UAT] — URL: [url]

## 2. Document Registry
Danh sách tài liệu đã phân tích. Mỗi document có **DOC ID** dùng để filter ở các bước sau.

| DOC ID | File | Loại | Ngày phân tích | Status | Modules liên quan |
|--------|------|------|---------------|--------|-------------------|
| DOC-01 | URD_module_login.pdf | URD | 2026-04-06 | ✅ Analyzed | Login, Register |
| DOC-02 | SRS_dashboard_v2.docx | SRS | 2026-04-07 | ✅ Analyzed | Dashboard, Report |
| DOC-03 | wireframe_payment.png | Wireframe | — | ⏳ Chưa phân tích | — |

> Khi chạy generate-tc, có thể chỉ định: "Tạo TC cho DOC-02" → filter scenarios có Source DOC = DOC-02

## 3. Module Summary (tổng hợp tất cả documents)
| Module | DOC Source | Tổng Requirements | Tổng Scenarios | P1 | P2 | P3 | Risk Level |
|--------|-----------|-------------------|----------------|----|----|----|-----------:|
| Login  | DOC-01    | 5                 | 12             | 4  | 5  | 3  | High       |
| Dashboard | DOC-02 | 8                | 15             | 6  | 5  | 4  | Medium     |
| Register | DOC-01  | 3                 | 8              | 3  | 3  | 2  | Medium     |
| Report | DOC-02    | 4                 | 7              | 2  | 3  | 2  | Low        |
| **Tổng** | | **20** | **42** | | | | |

## 4. Scenario Index (quick reference)
Mỗi scenario gắn DOC Source — dùng để filter khi generate-tc.

| Scenario ID | Tên ngắn | Module | DOC Source | Priority | Test Type | TC Status |
|-------------|----------|--------|-----------|----------|-----------|-----------|
| SC-LOGIN-001 | Đăng nhập hợp lệ | Login | DOC-01 | P1 | Functional | ⏳ Chưa tạo TC |
| SC-LOGIN-002 | Email sai format | Login | DOC-01 | P1 | Negative | ⏳ Chưa tạo TC |
| SC-DASH-001 | Xem dashboard tổng quan | Dashboard | DOC-02 | P1 | Functional | ⏳ Chưa tạo TC |

> Chi tiết Given/When/Then → xem `test_scenario_map.md`
> **TC Status**: ⏳ Chưa tạo TC / ✅ Đã tạo TC / 🚫 Blocked

## 5. Test Data Summary
| Module | DOC Source | Fields chính | Số bộ valid | Số bộ invalid | Có boundary? |
|--------|-----------|-------------|-------------|---------------|-------------|
| Login  | DOC-01    | email, password | 3 | 5 | Có |
| Dashboard | DOC-02 | date_range, filter_type | 2 | 3 | Có |

> Chi tiết → xem `test_data_catalog.md`

## 6. Clarifications & Blockers
| # | Req ID | DOC Source | Vấn đề | Status | Ảnh hưởng |
|---|--------|-----------|--------|--------|-----------|
| 1 | REQ-LOGIN-003 | DOC-01 | Chưa rõ OTP expire sau bao lâu | Open | Không viết được TC cho OTP timeout |

## 7. Automation Context (nếu có)
Phần này chỉ điền khi dự án có automation framework.

- **Framework:** [Java 21 + TestNG 7 + Selenium 4 + Maven]
- **POM path:** [src/main/java/page/]
- **BaseTest:** [src/test/java/testcase/BaseTest.java]
- **Naming convention:** [buttonLogin, textBoxEmail, popupError, labelTitle]

### Page Classes cần cho scenarios
| Page Class | Status | DOC Source | Scenarios sử dụng |
|------------|--------|-----------|-------------------|
| LoginPage  | Update | DOC-01    | SC-LOGIN-001..005 |
| DashboardPage | New | DOC-02   | SC-DASH-001..003 |

> Chi tiết elements/methods → xem `pom_analysis.md` (nếu có)

## 8. Deliverable Files Reference
| File | Đường dẫn | Mô tả |
|------|-----------|-------|
| Requirement Traceability | `02_analyze-requirements/requirement_traceability.md` | Ma trận truy vết req → scenario |
| Test Scenario Map | `02_analyze-requirements/test_scenario_map.md` | Chi tiết Given/When/Then |
| Test Data Catalog | `02_analyze-requirements/test_data_catalog.md` | Dữ liệu test valid/invalid/boundary |
| Risk Assessment | `02_analyze-requirements/risk_assessment.md` | Đánh giá rủi ro + thứ tự test |
| POM Analysis | `02_analyze-requirements/pom_analysis.md` | (nếu có) Page class structure |

## 9. TC Generation Log
Tracking file nào đã được generate TC — cập nhật bởi skill generate-tc.

| DOC ID | Ngày generate | Tổng TC | File output | Ghi chú |
|--------|--------------|---------|-------------|---------|
| DOC-01 | 2026-04-06 | 25 | `03_test-cases/functional/TC-LOGIN.xlsx` | Đã hoàn thành |
| DOC-02 | — | — | — | Chưa generate |
```

**Quy tắc cập nhật MEMORY.md khi phân tích thêm document:**
- **KHÔNG ghi đè** nội dung cũ. Append thêm rows vào Document Registry, Module Summary, Scenario Index, v.v.
- Mỗi row mới phải có `DOC Source` = DOC ID của document vừa phân tích
- Cập nhật dòng tổng (Tổng) ở Module Summary
- Cập nhật `Cập nhật lần cuối` ở header

### 6. Cập nhật `CLAUDE.md`
Append thông tin phân tích vào `CLAUDE.md` hiện có ở root project (không thay thế nội dung cũ):

```markdown
## Kết quả phân tích requirement (Requirement Analysis)
- **Ngày phân tích:** [date]
- **Tài liệu đã phân tích:** [list files]
- **Figma design:** [có/không] — [link nếu có]
- **Tổng requirement:** [N]
- **Tổng scenario:** [N] (Functional: [n], UI: [n], Business Rule: [n])
- **Module chính:** [list modules]
- **Vùng rủi ro cao:** [list]
- **Clarification cần xử lý:** [N items]
- **MEMORY file:** `02_analyze-requirements/MEMORY.md`
```

### 7. `ui_design_specs.md` (optional — chỉ khi có Figma/wireframe input)

Tạo khi có Figma link hoặc wireframe images. File này chứa **UI specs đã extract** để manual tester biết chính xác cần verify gì trên giao diện.

Lưu tại: `02_analyze-requirements/ui_design_specs.md`

```markdown
# UI Design Specs

> Extract từ: [Figma link / wireframe files]
> DOC Source: DOC-FIG-01
> Ngày extract: [date]

## Tổng quan
- Số screens/pages: [N]
- Số components unique: [N]
- Có responsive design: Có/Không
- Design system: [tên nếu có]

## Theo Screen

### [Screen Name] — [Figma Frame ID/Link]

#### Layout & Components
| # | Component | Type | Vị trí | States có trong design |
|---|-----------|------|--------|----------------------|
| 1 | Logo | Image | Top-left | Default |
| 2 | Email input | Text Input | Center | Default, Focus, Error, Disabled |
| 3 | Password input | Text Input | Center | Default, Focus, Error |
| 4 | Button "Đăng nhập" | Button | Center-bottom | Default, Hover, Disabled, Loading |
| 5 | Link "Quên mật khẩu" | Link | Below button | Default, Hover |

#### Design Tokens (từ Figma)
| Property | Value | Áp dụng cho |
|----------|-------|-------------|
| Primary Color | #1890FF | Button background, Links |
| Error Color | #FF4D4F | Error messages, Error state borders |
| Font Family | Roboto | All text |
| Font Size - Body | 14px | Input labels, body text |
| Font Size - Heading | 24px | Page title |
| Spacing - Input gap | 16px | Giữa các input fields |
| Border Radius | 8px | Buttons, Inputs |

#### Navigation
| Từ | Hành động | Đến | Ghi chú |
|----|-----------|-----|---------|
| Login screen | Nhấn "Đăng nhập" thành công | Dashboard | Redirect |
| Login screen | Nhấn "Quên mật khẩu" | Reset Password | New page |

#### Responsive (nếu có)
| Breakpoint | Thay đổi layout |
|-----------|-----------------|
| Desktop (>1024px) | 2 columns: illustration + form |
| Tablet (768-1024px) | 1 column, form centered |
| Mobile (<768px) | 1 column, full width inputs |
```

**Lưu ý:**
- File này là **reference** cho manual tester khi verify UI — không phải test case
- UI scenarios (SC-xxx-UI-xxx) trong `test_scenario_map.md` sẽ reference file này
- Nếu không có MCP Figma, user có thể tự điền hoặc extract từ screenshot

---

## Quy tắc quan trọng

### Về nội dung
- Chỉ tạo scenario từ requirement có trong tài liệu. Không sáng tạo thêm feature.
- Nếu requirement mơ hồ → ghi vào "Clarifications Needed", không đoán.
- Mỗi scenario phải trace được ngược về requirement source (file + section/page).
- Ưu tiên viết Given/When/Then rõ ràng, cụ thể, có thể convert trực tiếp thành test case.

### Về format
- Mọi file bắt đầu bằng `# heading`
- Dùng bảng markdown cho dữ liệu có cấu trúc
- Viết tiếng Việt, giữ tiếng Anh cho: field names, status, priority, technical terms
- ID format nhất quán: `REQ-[MODULE]-[NNN]`, `SC-[MODULE]-[NNN]`

### Về automation context (nếu dự án có automation)
Nếu `CLAUDE.md` chứa thông tin về automation framework (Java, Selenium, POM structure):

1. **MEMORY.md section 6** — tự động điền Automation Context (framework, POM path, naming convention, page class list)
2. **test_scenario_map.md** — bổ sung thêm cột `Page Class (suggested)`
3. **Tạo thêm `pom_analysis.md`** (file thứ 7, optional) — chi tiết elements/methods cho từng page class

Automation tester / generate_TC skill sẽ đọc: `MEMORY.md` (tổng quan) → `pom_analysis.md` (chi tiết POM) → `test_scenario_map.md` (scenarios) → `test_data_catalog.md` (data).

```markdown
# POM Structure Analysis

## Page Classes hiện có
(Đọc từ source code nếu có access, hoặc từ CLAUDE.md)

| Page Class | File path | Status |
|------------|-----------|--------|

## Page Classes cần tạo/cập nhật
| Page Class | Status (New/Update) | Elements cần thêm | Methods cần thêm | Từ Scenarios |
|------------|--------------------|--------------------|-------------------|-------------|
| LoginPage | Update | textBoxOTP, buttonResendOTP | enterOTP(), clickResend() | SC-LOGIN-003 |

## Naming Convention nhắc lại
- Element: [type][Name] → buttonLogin, textBoxEmail, popupError, labelTitle
- Method: [action][Target] → clickLogin(), enterEmail(), getErrorMessage()
```

---

## Checklist trước khi hoàn thành

Trước khi present output cho user, tự kiểm tra:
- [ ] Mọi scenario có Req ID trỏ về requirement_traceability.md
- [ ] Mọi requirement có ít nhất 1 scenario (positive) + 1 scenario (negative) nếu applicable
- [ ] test_data_catalog.md cover tất cả input fields từ scenarios
- [ ] risk_assessment.md có risk score cho mọi module
- [ ] MEMORY.md có đầy đủ: module summary, scenario index, test data summary, clarifications
- [ ] MEMORY.md section "Automation Context" chỉ điền khi CLAUDE.md có automation info
- [ ] CLAUDE.md đã được append kết quả phân tích (không ghi đè nội dung cũ)
- [ ] Không có Java/Python code trong bất kỳ file nào
- [ ] Tất cả file nằm trong `02_analyze-requirements/` (trừ CLAUDE.md ở root)
