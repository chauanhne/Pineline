---
name: create-test-plan
description: Tạo Test Plan tổng thể cho dự án/release/sprint dựa trên input docs (00_input/) và thông tin project (CLAUDE.md). Xác định scope, test approach, entry/exit criteria, resources, schedule, risks trước khi phân tích chi tiết requirement. Trigger khi user nhắc đến "tạo test plan", "create test plan", "viết kế hoạch test", "test strategy", "test approach", "lập kế hoạch kiểm thử", "TP", "planning test", hoặc trước khi chạy analyze-requirements mà chưa có test plan. Skill này ghi vào 01_test-plans/ và là bước #2 sau init-project.
---

# Create Test Plan

Tạo Test Plan tổng thể — xác định scope, approach, criteria, resources, schedule, risks — làm kim chỉ nam cho toàn bộ quá trình testing.

---

## Nguyên tắc cốt lõi

- **Quick scan, không deep analysis.** Đọc 00_input/ để xác định scope/modules — phân tích chi tiết là việc của analyze-requirements.
- **User-driven decisions.** Test approach, priority, schedule — hỏi user, không tự quyết.
- **Living document.** Test plan được update khi scope thay đổi, không viết 1 lần rồi bỏ.
- **Downstream contract.** Exit criteria từ test plan → trở thành Quality Gates trong test-report GO/NO-GO.

---

## Vị trí trong Pipeline

```
init-project → ★ create-test-plan ★ → analyze-req → generate-tc → review-tc
   (00_)              (01_)              (02_)         (03_)        (11_)
                                                         ↓
                                          scan-source → implement-auto
                                             (10_)        (10_)
                                                            ↓
                                                      execute-maintain → log-bug
                                                         (10_§15)      (05_)
```

| Hướng | Skill | Đọc / Ghi |
|-------|-------|-----------|
| **Upstream** | init-project | Đọc cấu trúc thư mục, CLAUDE.md |
| **Downstream** | analyze-req | Đọc §2 Scope để filter modules phân tích |
| **Downstream** | implement-auto | Đọc §3 Approach để biết modules cần auto |
| **Downstream** | test-report | Đọc §4 Exit Criteria làm Quality Gates cho GO/NO-GO |

---

## Cách gọi Skill & Entry Modes

### Mode CREATE — Tạo test plan mới (từ đầu)
**Khi nào:** Bắt đầu dự án, chưa có test plan, chưa chạy analyze.

```
"Tạo test plan"
"Lập kế hoạch test cho release v1.0"
"Create test plan cho sprint 5"
"Viết test plan"
```

**Flow:** Step 1 → 2 → 3 → 4 → 5 → 6 → 7

---

### Mode RETRO — Tạo test plan cho project đã chạy
**Khi nào:** Project đã chạy analyze/generate-tc/implement-auto TRƯỚC khi có test plan. Cần bổ sung retroactive.

```
"Tạo test plan cho project đang chạy"
"Bổ sung test plan, đã có MEMORY rồi"
"Create test plan retroactive"
```

**Flow:** Step 1-RETRO (đọc existing artifacts) → Step 2-RETRO (confirm + hỏi thiếu) → 3 → 4 → 5 → 6 → 7

**Khác biệt với CREATE:**

| Aspect | CREATE | RETRO |
|--------|--------|-------|
| Scope | Hỏi user, scan 00_input/ | Auto-extract từ MEMORY.md §3 |
| Test types | Hỏi user | Auto-detect từ MEMORY.md §4 |
| Approach | Hỏi manual/auto | Detect từ 10_source-code/ |
| Schedule | Hỏi all dates | Past = actual timestamps, hỏi future only |
| Risks | Hỏi user | Merge từ risk_assessment.md |
| Progress | Empty | Pre-fill ✅/⏳ per phase |
| Questions | ~9 câu | ~5 câu (~50% giảm) |

---

### Mode UPDATE — Cập nhật test plan
**Khi nào:** Scope thay đổi, thêm/bớt module, đổi schedule.

```
"Cập nhật test plan: thêm module Payment"
"Đổi schedule test plan"
"Bỏ module Report khỏi scope"
```

**Flow:** Đọc test plan hiện tại → sửa sections bị ảnh hưởng → increment version → cảnh báo downstream impact

---

### Mode REVIEW — Xem test plan hiện tại

```
"Xem test plan"
"Review test plan"
```

**Flow:** Đọc → trình bày → KHÔNG sửa

---

### Detect Logic

```
User message → kiểm tra:

1. Có test plan trong 01_test-plans/?
   ├── KHÔNG → kiểm tra tiếp:
   │   ├── Có 02_analyze-requirements/MEMORY.md? → Mode RETRO
   │   └── Không có MEMORY.md → Mode CREATE
   └── CÓ → kiểm tra tiếp:
       │
       2. User nói "cập nhật" / "thêm" / "bỏ" / "đổi"?  → Mode UPDATE
       3. User nói "xem" / "review"?                       → Mode REVIEW
       4. User nói "tạo mới" / "tạo lại"?                  → Mode CREATE (new version)
```

---

## Workflow

### Step 1: Đọc Project Context

**Mode CREATE:**
```
1. CLAUDE.md (root)          → project name, env, team, automation info
2. 07_environments/          → environment URLs, configs
3. 00_input/ (quick scan)    → list files, identify document types & modules
```

Quick scan 00_input/ chỉ extract:
- Danh sách files (tên + loại: URD, SRS, BRD, wireframe, Figma...)
- Modules/features gợi ý từ file names hoặc headings
- **KHÔNG đọc chi tiết nội dung** — đó là việc của analyze-requirements

**Mode RETRO — Đọc existing artifacts:**
```
1. CLAUDE.md (root)
2. 02_analyze-requirements/MEMORY.md        → modules, scenarios, test types, clarifications
3. 02_analyze-requirements/risk_assessment.md → risks, priorities
4. 03_test-cases/**/*.xlsx (scan)            → TC counts
5. 11_tc-review/review-report.md            → review score (nếu có)
6. 10_source-code/MEMORY.md                 → automation status (nếu có)
7. 05_bug-reports/bug-index.md              → bug status (nếu có)
8. 00_input/                                → original doc list
9. 07_environments/                         → env config
```

**RETRO auto-extraction mapping:**

| Test Plan Section | Extracted From | Fallback if not found |
|-------------------|---------------|-----------------------|
| §2.1 Scope (In) | MEMORY §3 Module Summary | Hỏi user |
| §2.1 Test Types | MEMORY §4 unique Test Type values | Hỏi user |
| §2.2 Out-of-scope | MEMORY §6 Blocked + not-analyzed docs | Hỏi user |
| §3.2 Test Types table | MEMORY §3 + §4 cross-reference | Hỏi user |
| §3.3 Manual vs Auto | 10_source-code/MEMORY.md existence | Hỏi user |
| §5 Environment | CLAUDE.md + 07_environments/ | Hỏi user |
| §6.2 Schedule (past) | MEMORY timestamps ("Cập nhật lần cuối") | Leave blank |
| §7 Risks | risk_assessment.md | Hỏi user |
| §8 Progress | All folders scanned | Detect ✅/⏳ |

**RETRO progress detection logic:**

```
Check each phase:
  02_analyze-requirements/MEMORY.md exists?     → analyze = ✅
  03_test-cases/**/*.xlsx exists?                → tc_design = ✅
  11_tc-review/review-report.md exists?          → tc_review = ✅
  10_source-code/MEMORY.md exists + §7 has data? → automation = ✅
  10_source-code/MEMORY.md §15 has runs?         → execution = ✅
  05_bug-reports/bug-index.md exists?             → bug_logging = ✅
  09_reports/*.md exists?                         → reporting = ✅
  Else                                           → ⏳ Not started
```

### Step 2: Thu thập thông tin từ User

**Mode CREATE:** Hỏi **từng câu một**, skip câu đã có từ CLAUDE.md.

**Mode RETRO:** Trình bày dữ liệu đã extract, **chỉ hỏi phần còn thiếu**.

---

#### CREATE Questions (Q1-Q9)

**Q1 — Test plan type**
```
"Test plan cho level nào?"
  (a) Master Test Plan — toàn bộ dự án
  (b) Release Test Plan — cho release/version cụ thể
  (c) Sprint Test Plan — cho sprint cụ thể
  (d) Feature Test Plan — cho 1 feature/module
```

**Q2 — Objectives**
```
"Mục tiêu testing là gì? (Có thể chọn nhiều)"
  (a) Verify requirements implemented đúng
  (b) Regression testing sau thay đổi
  (c) UAT trước go-live
  (d) Performance/load testing
  (e) Security testing
  (f) Khác: [user nhập]
```

**Q3 — Scope**
```
"Tôi phát hiện modules sau từ 00_input/:
  - [module list từ file scan]
Modules nào IN scope? Cần BỎ hoặc THÊM?"
```

**Q4 — Test types**
```
"Các loại test sẽ thực hiện?"
  Functional / UI / Integration / Regression / Smoke / UAT / Performance / Security / Exploratory
```

**Q5 — Test approach**
```
"Manual testing, Automation testing, hay kết hợp?
Nếu automation: framework gì? Modules nào ưu tiên auto?"
```

**Q6 — Entry/Exit criteria**
```
"Entry criteria (bắt đầu test khi):"
  Defaults: Requirements approved, env ready, test data prepared, code deployed

"Exit criteria (kết thúc test khi):"
  Defaults: Pass rate ≥ 90%, P1 bugs = 0, P1 TC 100% executed, report created

Thêm/sửa?
```

**Q7 — Schedule**
```
"Timeline: start date → end date?
Milestones: analyze complete, TC ready, execution done, report delivery?"
```

**Q8 — Resources** (chỉ hỏi nếu Team mode)
```
"Team members: Test Lead, Testers, Automation, BA/Dev support?"
```

**Q9 — Risks**
```
"Rủi ro testing: timeline gấp? thiếu người? env chưa sẵn? requirement thay đổi?"
```

---

#### RETRO Questions (reduced set)

Trình bày extracted data trước:
```
📋 Auto-extracted từ project hiện tại:

Project: [name] | Env: [env — url]
Scope: [N] modules — [list] = [N] scenarios
Test types: [auto-detected list]
Risks: [from risk_assessment.md]
Progress: [✅/⏳ per phase with dates and counts]
```

Rồi chỉ hỏi:

| # | Question | Lý do cần hỏi |
|---|---------|---------------|
| RQ1 | Test plan type? | MEMORY không chứa |
| RQ2 | Objectives? | MEMORY không chứa |
| RQ3 | Confirm scope OK? | Confirm, không hỏi từ đầu |
| RQ4 | Exit criteria targets? | Defaults cần user confirm |
| RQ5 | Future schedule dates? | Past dates auto-fill, future cần user |
| RQ6 | Automation plan? | Chỉ hỏi nếu 10_source-code/ unclear |
| RQ7 | Additional risks? | Confirm extracted + thêm nếu cần |

**Skipped in RETRO:** test types (auto), resources (từ CLAUDE.md), past dates (from timestamps).

---

After collecting all answers (CREATE or RETRO), **confirm summary** trước khi generate.

### Step 3: Generate Test Plan Document

Tạo file trong `01_test-plans/`:

**File name:** `TP-[type]-[project]-[version].md`

```markdown
# Test Plan — [Project Name] [Type] [Version]

| Field | Value |
|-------|-------|
| Document ID | TP-[NNN] |
| Version | 1.0 |
| Ngày tạo | [date] |
| Tạo bởi | [name / Claude AI] |
| Trạng thái | Draft |
| Dự án | [project name] |
| Release/Sprint | [release or sprint ID] |

---

## 1. Giới thiệu

### 1.1. Mục đích
[1-2 câu mô tả mục đích test plan]

### 1.2. Tài liệu tham khảo
| # | Tài liệu | Vị trí | Phiên bản |
|---|----------|--------|-----------|
| 1 | [file từ 00_input/] | 00_input/ | [version] |

### 1.3. Thuật ngữ
| Thuật ngữ | Giải thích |
|-----------|-----------|
| TC | Test Case |
| TP | Test Plan |
| UAT | User Acceptance Testing |

---

## 2. Phạm vi (Scope)

### 2.1. Trong phạm vi (In-Scope)
| # | Module / Feature | Mô tả ngắn | Test Types | Priority |
|---|-----------------|-------------|------------|----------|
| 1 | [module] | [mô tả] | [types] | [High/Med/Low] |

### 2.2. Ngoài phạm vi (Out-of-Scope)
| # | Module / Feature | Lý do |
|---|-----------------|-------|
| 1 | [module] | [lý do] |

### 2.3. Assumptions & Constraints
**Assumptions:**
- [list]

**Constraints:**
- [list]

---

## 3. Test Approach

### 3.1. Test Levels
| Level | Applicable | Mô tả |
|-------|-----------|-------|
| Unit Testing | [Có/Không] | Dev responsibility |
| Integration Testing | [Có/Không] | Module interaction |
| System Testing | Có | End-to-end trên [env] |
| UAT | [Có/Không] | User acceptance |

### 3.2. Test Types
| Test Type | Modules | Approach | Tool |
|-----------|---------|----------|------|
| Functional | [modules] | Manual + Auto | Excel TC + Selenium |
| UI/UX | [modules] | Manual | Verify vs Figma |
| Regression | [modules] | Automation | Selenium suite |
| Smoke | Critical path | Automation | Smoke suite |

### 3.3. Manual vs Automation Strategy
```
Manual: [scope description]
Automation: [framework] — [modules] — [priority order]
```

---

## 4. Entry & Exit Criteria

### 4.1. Entry Criteria
| # | Criteria | Verified by |
|---|---------|-------------|
| 1 | Requirements reviewed và approved | BA + PM |
| 2 | Code deployed lên [env] | Dev |
| 3 | Test environment accessible | Tester |
| 4 | Test data chuẩn bị | Tester |
| 5 | Test cases reviewed | Test Lead |

### 4.2. Exit Criteria
| # | Criteria | Metric | Target |
|---|---------|--------|--------|
| 1 | Pass rate | % TC pass / total | ≥ [N]% |
| 2 | P1 bugs | P1 bugs open | 0 |
| 3 | P1 TC coverage | % P1 TC executed | 100% |
| 4 | Bug fix rate | % bugs closed / total | ≥ [N]% |
| 5 | Test report | Created and reviewed | Yes |

> Exit criteria → truyền vào CLAUDE.md → test-report dùng làm Quality Gates.

### 4.3. Suspension & Resumption
**Tạm dừng:** Env down >2h, blocker bug >50% scope, requirement thay đổi >30%.
**Tiếp tục:** Issue resolved, env restored, requirements confirmed.

---

## 5. Test Environment

| Environment | URL | Mục đích |
|-------------|-----|---------|
| [env] | [url] | [purpose] |

### 5.1. Test Accounts
| Vai trò | Username | Mục đích |
|---------|----------|---------|
| [role] | [TBD] | [purpose] |

### 5.2. Tools
| Tool | Purpose |
|------|---------|
| Claude Code | AI-assisted analysis + TC generation |
| Playwright MCP | Locator extraction + env health check |
| [Selenium/TestNG] | Automation execution |
| [openpyxl] | Excel TC generation |

---

## 6. Resources & Schedule

### 6.1. Team
| Vai trò | Tên | Trách nhiệm | Allocation |
|---------|-----|-------------|-----------|
| Test Lead | [name] | Planning, review, reporting | [%] |
| Tester | [name] | Execution, bug logging | [%] |

### 6.2. Schedule
| Phase | Start | End | Deliverable | Skill |
|-------|-------|-----|-------------|-------|
| Test Planning | [date] | [date] | Test Plan | create-test-plan |
| Requirement Analysis | [date] | [date] | Scenarios | analyze-req |
| TC Design | [date] | [date] | TC Excel | generate-tc |
| TC Review | [date] | [date] | Review Report | review-tc |
| Automation Setup | [date] | [date] | Source code | scan + implement |
| Execution Cycle 1 | [date] | [date] | Run log | execute-maintain |
| Bug Fix & Retest | [date] | [date] | Bug updates | log-bug |
| Execution Cycle 2 | [date] | [date] | Run log | execute-maintain |
| Test Report | [date] | [date] | Summary | test-report |

### 6.3. Milestones
| Milestone | Target Date | Gate |
|-----------|-------------|------|
| Analyze complete | [date] | — |
| TC ready + reviewed | [date] | Review score ≥ 70 |
| Execution done | [date] | Pass rate tracked |
| All P1 bugs fixed | [date] | Required for release |
| Final report | [date] | GO/NO-GO |

---

## 7. Risk Assessment

| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|-----------|------------|
| 1 | Timeline gấp | High | [H/M/L] | Ưu tiên P1, skip P3 nếu cần |
| 2 | Thiếu test data | Medium | [H/M/L] | Chuẩn bị data song song TC design |
| 3 | Env không ổn định | High | [H/M/L] | Smoke check trước mỗi run |
| 4 | Requirement thay đổi | High | [H/M/L] | Impact analysis + re-plan |
| 5 | Locator thay đổi | Medium | [H/M/L] | Playwright recheck, report only |

---

## 8. Deliverables

| # | Deliverable | Folder | Skill | Status |
|---|------------|--------|-------|--------|
| 1 | Test Plan | 01_test-plans/ | create-test-plan | ✅ / ⏳ |
| 2 | Requirement Analysis | 02_analyze-requirements/ | analyze-req | ✅ / ⏳ |
| 3 | Test Cases (Excel) | 03_test-cases/ | generate-tc | ✅ / ⏳ |
| 4 | TC Review Report | 11_tc-review/ | review-tc | ✅ / ⏳ |
| 5 | Automation Code | 10_source-code/ | implement-auto | ✅ / ⏳ |
| 6 | Execution Logs | 08_test-runs/ | test-report | ✅ / ⏳ |
| 7 | Bug Reports | 05_bug-reports/ | log-bug | ✅ / ⏳ |
| 8 | Summary Report | 09_reports/ | test-report | ✅ / ⏳ |

> **Mode RETRO:** Status column auto-populated from progress detection.

### 8.1. Current Progress (RETRO mode only)

> Section này chỉ xuất hiện khi tạo test plan bằng Mode RETRO.

| Phase | Status | Date | Metrics |
|-------|--------|------|---------|
| [phase] | [✅/⏳] | [date or —] | [counts] |

**Remaining work:**
- [list incomplete phases + estimated effort]

---

## 9. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | | | |
| PM | | | |
| BA | | | |

---

## 10. Revision History

| Version | Date | Changed By | Changes |
|---------|------|-----------|---------|
| 1.0 | [date] | [name] | Initial creation |
```

### Step 4: Generate Excel Version (optional)

Nếu user cần .xlsx: `view /mnt/skills/public/xlsx/SKILL.md`

**Sheets:** Overview, Scope Matrix (module × test type × priority), Schedule, Risk Register, RACI (Team mode).

### Step 5: Update CLAUDE.md

Append test plan contract vào CLAUDE.md — downstream skills đọc từ đây:

```markdown
## Test Plan
- **Document:** `01_test-plans/[filename]`
- **Type:** [Master / Release / Sprint / Feature]
- **Scope IN:** [list modules]
- **Scope OUT:** [list modules + reason]
- **Test types:** [list]
- **Approach:** Manual: [modules] | Automation: [modules]
- **Entry criteria:** [summary]
- **Exit criteria (= Quality Gates for test-report):**
  - G1: TC Review score ≥ [N]
  - G2: P1 pass rate = 100%
  - G3: Overall pass rate ≥ [N]%
  - G4: No P1 bugs open
  - G5: Bug fix rate ≥ [N]%
  - G6: Blocked items ≤ [N]
- **Schedule:** [start] → [end]
```

### Step 6: Present to User

```
📋 Test Plan Created:

📄 File: 01_test-plans/TP-[type]-[project]-[version].md
📊 Excel: 01_test-plans/TP-[type]-[project]-[version].xlsx (nếu có)

Summary:
  Type: [type]
  Scope: [N] modules ([list])
  Test types: [list]
  Approach: [manual/auto/combined]
  Schedule: [start] → [end]
  Exit: Pass ≥ [N]%, P1 bugs = 0

Status: Draft — chờ approval.

Bạn muốn:
(a) Review chi tiết từng section
(b) Adjust scope hoặc schedule
(c) Mark Approved và tiếp tục bước tiếp theo
(d) Export cho stakeholder
```

### Step 7: Handoff to Next Step

**Mode CREATE:**
```
✅ Test Plan approved.
Bước tiếp: "Phân tích tài liệu trong 00_input/"
→ analyze-requirements sẽ đọc scope từ test plan.
```

**Mode RETRO:**
Detect phase nào chưa done, handoff tương ứng:
```
Nếu chưa analyze    → "Chạy: Phân tích tài liệu trong 00_input/"
Nếu chưa TC         → "Chạy: Tạo test case"
Nếu chưa review     → "Chạy: Review TC"
Nếu chưa auto       → "Chạy: Implement automation" hoặc "Chạy test"
Nếu chưa execute    → "Chạy: Chạy test automation"
Nếu tất cả done     → "Chạy: Tạo báo cáo test"
```

---

## Mode UPDATE — Chi tiết

```
1. Đọc test plan hiện tại
2. Xác định thay đổi:
   - Thêm module → add row §2.1
   - Bỏ module → move sang §2.2
   - Đổi schedule → update §6.2
   - Thêm risk → update §7
   - Đổi criteria → update §4
3. Increment version: 1.0 → 1.1
4. Append §10 Revision History
5. Update CLAUDE.md (scope, criteria)
6. Cảnh báo downstream:
   "⚠️ Scope thay đổi ảnh hưởng [N] scenarios đã analyze.
    Cần chạy analyze-requirements mode UPDATE nếu applicable."
```

---

## Traceability: Test Plan → Downstream

```
§2 Scope       → CLAUDE.md → analyze-req (filter modules)
§3 Approach    → CLAUDE.md → implement-auto (auto module scope)
§4 Exit Criteria → CLAUDE.md → test-report (GO/NO-GO gates)
§6 Schedule    → CLAUDE.md → test-report (actual vs planned)
§7 Risks       → risk_assessment.md (merge + detail)
```

---

## Ngôn ngữ Output

**Viết tiếng Việt** cho toàn bộ nội dung test plan: headings, mô tả, mục đích, giả định, rủi ro, ghi chú.

**Giữ tiếng Anh** cho:
- Thuật ngữ kỹ thuật: Test Plan, Test Case, Smoke Test, Regression, UAT, API, UI/UX, Page Object Model, Selenium, TestNG, Maven, automation, framework, locator, proxy, browser, deploy, release, sprint, bug, blocker
- Tên tool: Claude Code, Playwright MCP, Chrome, openpyxl, Java, Python
- Status values: Draft, Approved, Pass, Fail, Blocked, Skipped, Open, Closed, In Progress
- Priority: P1, P2, P3, High, Medium, Low
- Tên module/feature nếu là tên riêng hệ thống (FILTER, KPI, FUNNEL, TAB1-4, NODATA, REFRESH, UE, UEDIST, API)
- Column headers trong bảng có thể giữ tiếng Anh nếu là convention (Status, Impact, Likelihood)
- Metrics: pass rate, coverage, score

---

## Quy tắc quan trọng

### Về scope
- **KHÔNG deep analyze docs** — chỉ scan names + headings
- **User quyết định** — skill suggest, user confirm
- **Out-of-scope phải có lý do**

### Về exit criteria
- **Phải measurable** — số cụ thể, không generic
- **Truyền sang test-report** — exit criteria = Quality Gates
- **User custom** — defaults cung cấp, user adjust

### Về versioning
- **Mỗi update = version mới** — 1.0 → 1.1 → 1.2
- **Revision history bắt buộc**
- **Draft until user confirms Approved**

### Về folder ownership
- **GHI:** `01_test-plans/`
- **APPEND:** `CLAUDE.md`
- **ĐỌC (RETRO):** `02_`, `03_`, `10_`, `11_`, `05_`, `07_`, `09_`
- **KHÔNG TOUCH:** downstream files (chỉ đọc trong RETRO)

---

## Checklist trước khi hoàn thành

### All modes
- [ ] Test plan file tạo trong 01_test-plans/
- [ ] Scope In/Out clearly defined
- [ ] Entry/Exit criteria measurable
- [ ] Risk register có mitigation
- [ ] CLAUDE.md đã append scope + criteria + approach
- [ ] Exit criteria → Quality Gates mapping documented
- [ ] User đã review (Draft hoặc Approved)

### CREATE only
- [ ] 00_input/ đã scan
- [ ] Q1-Q9 collected (hoặc skip với defaults)
- [ ] Schedule đầy đủ milestones
- [ ] Handoff → analyze-requirements

### RETRO only
- [ ] Existing MEMORY.md đã đọc + extracted
- [ ] Progress detection chính xác
- [ ] §8.1 Current Progress section present
- [ ] Questions reduced (~50% skip)
- [ ] Past dates = actual timestamps
- [ ] Handoff → correct next incomplete phase