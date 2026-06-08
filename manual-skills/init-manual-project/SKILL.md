---
name: init-manual-project
description: Initialize a new manual testing project with a complete folder structure, starter document templates (test plans, test cases, bug reports, checklists, environment configs, test run logs, summary reports), and a README. Use this skill whenever the user wants to set up, scaffold, bootstrap, or create a new manual QA testing project, a new test project structure, or asks about organizing manual test documentation. Also trigger when the user mentions "init project", "new test project", "manual testing setup", "QA project scaffold", or "test folder structure". This skill supports functional, regression, smoke, UAT, exploratory, and performance testing types.
---

# Init Manual Project

Scaffold a complete manual testing project with best-practice folder structure and starter templates.

---

## Vị trí trong Pipeline

```
★ init-project ★ → create-test-plan → analyze-req → generate-tc → review-tc
     (00_)              (01_)           (02_)         (03_)        (11_)
                                                        ↓
                                         scan-source → implement-auto
                                            (10_)        (10_)
                                                           ↓
                                                     execute-maintain → log-bug
                                                        (10_§15)      (05_)
```

| Hướng | Skill | Đọc / Ghi |
|-------|-------|-----------|
| **Upstream** | (không có — bước đầu tiên) | — |
| **Downstream** | create-test-plan | Đọc cấu trúc thư mục đã tạo |
| **Downstream** | analyze-req | Đọc tài liệu từ 00_input/ |

---

## Workflow

### Step 1: Gather Project Info

Collect project info by asking **one question at a time**. Wait for the user's answer before asking the next question. Skip any question whose answer is already clear from conversation context.

**Question 1 — Project name**
Ask: "Tên dự án (project name) là gì? (Ví dụ: ecommerce-web, hrm-system, mobile-banking)"
→ Used as root folder name. Convert to kebab-case if needed.

**Question 2 — Environment**
Ask: "Dự án sẽ test trên môi trường nào? (Có thể chọn nhiều)"
→ Options: DEV, STG, UAT, PROD

**Question 3 — URL**
Ask: "URL cho từng môi trường đã chọn là gì?"
→ Collect one URL per environment. If the user doesn't have URLs yet, accept blank and move on.

**Question 4 — Test types in scope**
Ask: "Những loại kiểm thử nào nằm trong phạm vi? (Có thể chọn nhiều)"
→ Options: Functional, Regression, Smoke, UAT, Exploratory, Performance

**Question 5 — Team size**
Ask: "Dự án test solo hay theo team? (Solo sẽ bỏ bớt các field phân công)"
→ Options: Solo, Team

**Question 6 — Language preference**
Ask: "Ngôn ngữ viết test case: Tiếng Việt (mặc định, giữ tiếng Anh cho thuật ngữ kỹ thuật) hay ngôn ngữ khác?"
→ Default: Vietnamese. Only ask if uncertain; skip if user already indicated Vietnamese.

**Question 7 — Automation scope**
Ask: "Dự án có automation test không? Nếu có, framework gì? (Ví dụ: Java + Selenium, hoặc 'Không có')"
→ Nếu CÓ: tạo thêm `10_source-code/` với `MEMORY.md` starter. Ghi automation context vào CLAUDE.md.
→ Nếu KHÔNG: bỏ qua `10_source-code/`, chỉ scaffold manual project.
→ Nếu user đã có source code sẵn: ghi nhận path và note vào CLAUDE.md.

After collecting all answers, confirm the summary with the user before proceeding to Step 2.

### Step 2: Xác nhận danh sách thư mục với User

Dựa trên thông tin đã thu thập, **trình bày danh sách thư mục đề xuất** và hỏi user xác nhận trước khi tạo bất kỳ file/folder nào.

Trình bày theo dạng:

```
📁 Dưới đây là cấu trúc thư mục tôi sẽ tạo cho dự án "[project-name]":

<project-name>/
├── 00_input/                    # Tài liệu đầu vào: URD, SRS, specs
├── 01_test-plans/               # Test plan theo release/feature
├── 02_analyze-requirements/     # Kết quả phân tích requirement
├── 03_test-cases/               # Test case documents
│   ├── functional/              (✅ đã chọn)
│   ├── regression/              (✅ đã chọn)
│   └── smoke/                   (✅ đã chọn)
├── 04_test-data/                # Dữ liệu test
│   ├── valid/
│   └── invalid/
├── 05_bug-reports/              # Bug/defect records
├── 06_checklists/               # Smoke & release checklists
├── 07_environments/             # Cấu hình môi trường
├── 08_test-runs/                # Log chạy test theo sprint
├── 09_reports/                  # Báo cáo tổng hợp
├── 10_source-code/              # (✅ có automation: Java + Selenium)
├── 11_tc-review/                # TC quality review
├── CLAUDE.md
└── README.md

Bạn có muốn:
(a) Tạo tất cả các thư mục như trên
(b) Bỏ một số thư mục không cần thiết (gõ số thứ tự cần bỏ, ví dụ: "bỏ 06, 08")
(c) Thêm thư mục tuỳ chỉnh
```

**Quy tắc:**
- **KHÔNG tạo bất kỳ folder/file nào** cho đến khi user xác nhận hoặc điều chỉnh xong
- Nếu user bỏ folder nào → ghi nhận, **không tạo** folder đó
- Nếu user thêm folder tuỳ chỉnh → thêm vào danh sách và xác nhận lại lần cuối
- Sau khi user xác nhận → trình bày lại danh sách cuối cùng và hỏi: **"Xác nhận tạo cấu trúc này?"** trước khi chạy script

### Step 3: Run the Scaffold Script

Execute the scaffolding script to create all folders and files:

```bash
python3 /path/to/skill/scripts/scaffold.py \
  --project-name "<project-name>" \
  --environments "DEV,STG" \
  --urls "https://dev.example.com,https://stg.example.com" \
  --test-types "Functional,Regression,Smoke" \
  --team-size "solo" \
  --automation "Java 21 + Selenium 4 + TestNG 7" \
  --output-dir "/mnt/user-data/outputs"
```

Nếu không có automation, bỏ `--automation` hoặc để trống: `--automation ""`

**Important:** Copy the script to `/home/claude/` first since the skill directory is read-only:
```bash
cp /mnt/skills/user/init-manual-project/scripts/scaffold.py /home/claude/scaffold.py
python3 /home/claude/scaffold.py [args...]
```

### Step 4: Post-Scaffold Customization

After the script runs:

1. **Review generated files** with the user — walk through the folder tree
2. **Suggest naming conventions:**
   - Test cases: `TC-[MODULE]-[NNN]-[short-title].md` (e.g., `TC-LOGIN-001-valid-credentials.md`)
   - Bug reports: `BUG-[NNN]-[short-title].md` (e.g., `BUG-001-login-button-unresponsive.md`)
   - Test runs: `TR-[SPRINT]-[DATE].md` (e.g., `TR-S05-2026-04-06.md`)
3. **Generate CLAUDE.md** at project root with:
   - Project name, test scope, environments
   - Naming conventions
   - Workflow: input docs in `00_input/` → analyze → write test cases → review → execute → report
   - Vietnamese language rule for content (English for technical terms)
4. **Present the output** to the user for download

### Folder Structure

The script creates this structure (only folders matching selected test types get created under `03_test-cases/`):

```
<project-name>/
├── 00_input/                    # Input documents: URD, SRS, specs
├── 01_test-plans/               # High-level test plans per release/feature
│   └── template-test-plan.md
├── 02_analyze-requirements/     # Requirement analysis output
│   └── .gitkeep
├── 03_test-cases/               # Detailed test case documents
│   ├── functional/              # (if in scope)
│   ├── regression/              # (if in scope)
│   ├── smoke/                   # (if in scope)
│   ├── uat/                     # (if in scope)
│   ├── exploratory/             # (if in scope)
│   └── performance/             # (if in scope)
├── 04_test-data/                # Test input data
│   ├── valid/
│   └── invalid/
├── 05_bug-reports/              # Bug/defect records
│   └── template-bug-report.md
├── 06_checklists/               # Smoke & release checklists
│   ├── smoke-checklist.md
│   └── release-checklist.md
├── 07_environments/             # Environment configs, setup steps
│   └── environments.md
├── 08_test-runs/                # Execution logs per sprint/release
│   └── template-test-run.md
├── 09_reports/                  # Summary reports for stakeholders
│   └── template-summary-report.md
├── 10_source-code/              # Automation source code (if automation = yes)
│   └── MEMORY.md               # Source code context tracking
├── 11_tc-review/                # TC quality review reports
│   └── .gitkeep
├── CLAUDE.md                    # Project conventions for AI assistants
└── README.md                    # Project overview and usage guide
```

> **Folder numbering rationale (workflow order):**
> `00` input → `01` plan → `02` analyze → `03` write TC → `04` test data → `05` bugs
> → `06` checklists → `07` env → `08` execute → `09` report → `10` automation code → `11` TC review

### Folder Creation Rules

| Folder | Always created? | Condition |
|--------|----------------|-----------|
| `00_input/` — `09_reports/` | Yes | Always part of manual testing scaffold |
| `10_source-code/` | Conditional | Only if Question 7 answer ≠ "Không có" |
| `11_tc-review/` | Yes | Always created (review-tc skill output goes here) |

When `10_source-code/` is **NOT** created (no automation):
- Folder is omitted entirely from the tree
- `11_tc-review/` still keeps its number (no renumbering)
- CLAUDE.md notes: "Automation: Không có. Folder 10_source-code/ không được tạo."

When `10_source-code/` **IS** created:
- Contains `MEMORY.md` starter (empty template for scan-source-code skill)
- If user provides existing source code path → note in CLAUDE.md, user copies code in manually
- CLAUDE.md notes automation framework info for downstream skills

## Template Reference

All templates are in `references/templates.md`. Read that file to get the exact content for each generated file. The scaffold script already embeds these templates, but if you need to manually create or customize any template, consult that reference.

Key templates included:
- **Test Plan** — objective, scope, entry/exit criteria, risks, schedule
- **Test Case (TC-001)** — preconditions, test data, steps table with expected/actual/status
- **Bug Report** — severity, priority, steps to reproduce, expected vs actual
- **Smoke Checklist** — authentication, core flows, infrastructure checks
- **Release Checklist** — pre-release, release day, post-release items
- **Environments** — URL/API/DB config per environment, test accounts
- **Test Run Log** — pass/fail summary, failed/blocked items
- **Summary Report** — metrics, quality assessment, GO/NO-GO recommendation
- **README** — project purpose, folder guide, naming conventions, contacts

## Team vs Solo Mode

When team size is **Team**, templates include these extra fields:
- Test cases: `Assigned to`, `Reviewed by` columns
- Bug reports: `Assigned to` field (always present)
- Test runs: `Tester(s)` supports multiple names
- Test plans: `Resources` section lists team members and roles

When **Solo**, these fields are simplified or removed to reduce noise.

## Language Rule

All test case content, descriptions, steps, and expected results should be written in **Vietnamese**. Keep these in English:
- Technical terms (API, URL, database, login, etc.)
- Status values (Pass, Fail, Blocked, Skipped)
- Priority/severity labels (P1, P2, Critical, High, etc.)
- Template field names and headers
- File names and folder names

## Downstream Skill Integration

This scaffold is designed so that downstream skills know exactly where to read/write:

| Skill | Reads from | Writes to |
|-------|-----------|-----------|
| `analyze-requirements` | `00_input/`, `CLAUDE.md` | `02_analyze-requirements/` |
| `generate-tc` | `02_analyze-requirements/` | `03_test-cases/` |
| `review-tc` | `03_test-cases/`, `02_analyze-requirements/` | `11_tc-review/` |
| `scan-source-code` | `10_source-code/`, `CLAUDE.md` | `10_source-code/MEMORY.md` |
| `implement-automation` | `10_source-code/MEMORY.md`, `02_analyze-requirements/` | `10_source-code/*.java` |

The scaffold creates `.gitkeep` in empty folders so git tracks the structure. Downstream skills replace `.gitkeep` content with real files.

## CLAUDE.md Template

The generated `CLAUDE.md` should include:

```markdown
# CLAUDE.md — [Project Name]

## Project Info
- **Tên dự án:** [name]
- **Mô tả:** [từ user hoặc để trống]
- **Môi trường:** [ENV1] — URL: [url1] | [ENV2] — URL: [url2]
- **Test types:** [Functional, Regression, Smoke, ...]
- **Team:** [Solo / Team]
- **Ngôn ngữ:** Tiếng Việt (giữ tiếng Anh cho thuật ngữ kỹ thuật)

## Automation
- **Framework:** [Java 21 + Selenium 4 + TestNG 7 / Không có]
- **Source code:** `10_source-code/` [hoặc "Không có automation"]

## Naming Conventions
- Test cases: `TC-[MODULE]-[NNN]-[short-title].md`
- Bug reports: `BUG-[NNN]-[short-title].md`
- Test runs: `TR-[SPRINT]-[DATE].md`
- Scenarios: `SC-[MODULE]-[NNN]`
- Requirements: `REQ-[MODULE]-[NNN]`

## Workflow
```
00_input/ (tài liệu gốc)
  → 02_analyze-requirements/ (phân tích bằng analyze-requirements skill)
    → 03_test-cases/ (viết TC bằng generate-tc skill)
      → 11_tc-review/ (review TC bằng review-tc skill)
        → 08_test-runs/ (execute test)
          → 05_bug-reports/ (log bugs)
            → 09_reports/ (summary report)

Nếu có automation:
  → 10_source-code/ (scan bằng scan-source-code → implement bằng implement-automation)
```

## Folder Reference
| # | Folder | Mục đích | Skill liên quan |
|---|--------|----------|----------------|
| 00 | input | Tài liệu đầu vào: URD, SRS, specs | analyze-requirements (đọc) |
| 01 | test-plans | Test plan tổng thể | — |
| 02 | analyze-requirements | Kết quả phân tích + MEMORY.md | analyze-requirements (ghi) |
| 03 | test-cases | Test case Excel files | generate-tc (ghi), review-tc (đọc) |
| 04 | test-data | Dữ liệu test (valid/invalid) | — |
| 05 | bug-reports | Báo cáo lỗi | — |
| 06 | checklists | Smoke + release checklists | — |
| 07 | environments | Config môi trường | — |
| 08 | test-runs | Logs chạy test theo sprint | — |
| 09 | reports | Báo cáo tổng hợp cho stakeholders | — |
| 10 | source-code | Code automation + MEMORY.md | scan-source-code, implement-automation |
| 11 | tc-review | Review report (.md + .xlsx) | review-tc (ghi) |
```

## README.md Template

The generated `README.md` should include:
- Project name and purpose
- Folder structure with descriptions (matching the tree above)
- Naming conventions
- How to use with Claude Code / AI skills
- Environment info
- Contact/team info (if Team mode)
```