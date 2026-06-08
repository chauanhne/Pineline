#!/usr/bin/env python3
"""
Scaffold a manual testing project with folder structure and starter templates.
Usage:
    python3 scaffold.py \
        --project-name "my-project" \
        --environments "DEV,STG" \
        --urls "https://dev.example.com,https://stg.example.com" \
        --test-types "Functional,Regression,Smoke" \
        --team-size "solo" \
        --output-dir "/mnt/user-data/outputs"
"""

import argparse
import os
from datetime import date


def parse_args():
    parser = argparse.ArgumentParser(description="Scaffold a manual testing project")
    parser.add_argument("--project-name", required=True, help="Project name (kebab-case)")
    parser.add_argument("--environments", required=True, help="Comma-separated: DEV,STG,UAT,PROD")
    parser.add_argument("--urls", default="", help="Comma-separated URLs matching environments")
    parser.add_argument("--test-types", required=True,
                        help="Comma-separated: Functional,Regression,Smoke,UAT,Exploratory,Performance")
    parser.add_argument("--team-size", default="solo", choices=["solo", "team"],
                        help="solo or team")
    parser.add_argument("--automation", default="",
                        help="Automation framework, e.g. 'Java+Selenium+TestNG' or empty for no automation")
    parser.add_argument("--output-dir", default=".", help="Parent directory for the project")
    return parser.parse_args()


def mkdir(path):
    os.makedirs(path, exist_ok=True)


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_team_fields_tc():
    return """| Assigned to  |                              |
| Reviewed by  |                              |
"""


def build_team_fields_plan():
    return """
## Phân công (Assignments)
| Thành viên | Vai trò | Module phụ trách |
|------------|---------|-----------------|
|            |         |                 |
"""


def template_test_plan(project_name, test_types, team_size):
    checks = ""
    for tt in ["Functional", "Regression", "Smoke", "UAT", "Exploratory", "Performance"]:
        mark = "x" if tt in test_types else " "
        checks += f"- [{mark}] {tt}\n"

    team_section = build_team_fields_plan() if team_size == "team" else ""

    return f"""# Test Plan: [Feature / Release Name]

## Mục tiêu (Objective)
Mô tả những gì đang được kiểm thử và lý do.

## Phạm vi (Scope)
### Trong phạm vi (In Scope)
-

### Ngoài phạm vi (Out of Scope)
-

## Loại kiểm thử (Test Types)
{checks}
## Điều kiện bắt đầu (Entry Criteria)
- Build đã deploy lên [environment]
- Test data đã chuẩn bị xong

## Điều kiện kết thúc (Exit Criteria)
- Tất cả test case Critical/High đã pass
- Không còn bug P1/P2 đang mở

## Rủi ro & Biện pháp (Risks & Mitigations)
| Rủi ro | Mức ảnh hưởng | Biện pháp |
|--------|---------------|-----------|
|        |               |           |

## Lịch trình (Schedule)
| Giai đoạn | Bắt đầu | Kết thúc |
|-----------|---------|----------|
|           |         |          |

## Nguồn lực (Resources)
- Tester(s):
- Environment:
- Test data owner:
{team_section}"""


def template_test_case(team_size):
    team_rows = build_team_fields_tc() if team_size == "team" else ""
    return f"""# TC-001: [Tên Test Case]

| Field        | Value                        |
|--------------|------------------------------|
| Module       |                              |
| Priority     | P1 / P2 / P3                 |
| Type         | Positive / Negative / Edge   |
| Tạo bởi     |                              |
| Cập nhật lần cuối |                         |
{team_rows}
## Điều kiện tiên quyết (Preconditions)
- Người dùng đã đăng nhập
-

## Dữ liệu kiểm thử (Test Data)
| Field    | Value |
|----------|-------|
|          |       |

## Các bước thực hiện (Steps)
| # | Hành động | Kết quả mong đợi | Kết quả thực tế | Status |
|---|-----------|-------------------|------------------|--------|
| 1 |           |                   |                  | ⬜     |
| 2 |           |                   |                  | ⬜     |

## Hậu điều kiện (Post-conditions)
-

## Ghi chú (Notes)
-
"""


def template_bug_report():
    return """# BUG-XXX: [Mô tả ngắn]

| Field         | Value                              |
|---------------|------------------------------------|
| Severity      | Critical / High / Medium / Low     |
| Priority      | P1 / P2 / P3 / P4                 |
| Status        | New / In Progress / Fixed / Closed |
| Environment   |                                    |
| Build/Version |                                    |
| Reported by   |                                    |
| Reported on   |                                    |
| Assigned to   |                                    |

## Tóm tắt (Summary)
Mô tả ngắn gọn về bug trong một dòng.

## Các bước tái hiện (Steps to Reproduce)
1.
2.
3.

## Kết quả mong đợi (Expected Result)
Mô tả điều gì lẽ ra phải xảy ra.

## Kết quả thực tế (Actual Result)
Mô tả điều gì thực sự xảy ra.

## Đính kèm (Attachments)
- [ ] Screenshot
- [ ] Video
- [ ] Log file

## Ghi chú (Notes)
-
"""


def template_smoke_checklist(project_name):
    return f"""# Smoke Test Checklist — {project_name}

> Chạy trước mỗi chu kỳ kiểm thử. Nếu bất kỳ mục nào fail, chặn testing và thông báo cho dev.

## Xác thực (Authentication)
- [ ] Người dùng có thể đăng nhập với thông tin hợp lệ
- [ ] Người dùng không thể đăng nhập với thông tin không hợp lệ
- [ ] Luồng quên mật khẩu hoạt động

## Luồng chính (Core Flows)
- [ ] [Luồng quan trọng 1]
- [ ] [Luồng quan trọng 2]
- [ ] [Luồng quan trọng 3]

## Hạ tầng (Infrastructure)
- [ ] Ứng dụng load không có lỗi console
- [ ] API endpoints phản hồi (kiểm tra network tab)
- [ ] Không có hình ảnh bị hỏng hoặc tài nguyên bị thiếu

---
Kiểm thử bởi: ___________  Ngày: ___________  Build: ___________
"""


def template_release_checklist():
    return """# Release Checklist — [Version]

## Trước Release (Pre-Release)
- [ ] Tất cả bug P1/P2 đã được giải quyết
- [ ] Bộ test Regression đã pass
- [ ] UAT đã được sign-off
- [ ] Release notes đã soạn xong
- [ ] Kế hoạch rollback đã được ghi nhận

## Ngày Release (Release Day)
- [ ] Smoke test trên production sau khi deploy
- [ ] Theo dõi error logs trong 30 phút
- [ ] Thông báo cho các stakeholders

## Sau Release (Post-Release)
- [ ] Đóng các bug đã resolved trong tracker
- [ ] Lưu trữ kết quả test run
- [ ] Ghi nhận retrospective notes
"""


def template_environments(envs, urls):
    env_url_map = {}
    for i, env in enumerate(envs):
        env_url_map[env.strip().upper()] = urls[i].strip() if i < len(urls) else ""

    sections = ""
    env_configs = {
        "DEV": ("Không ổn định, chỉ dành cho developer testing", True),
        "STG": ("Dữ liệu mirror từ production (đã ẩn danh)", True),
        "UAT": ("Môi trường cho User Acceptance Testing", True),
        "PROD": ("Chỉ chạy smoke test read-only", False),
    }

    for env in envs:
        env_key = env.strip().upper()
        note, full = env_configs.get(env_key, ("", True))
        url = env_url_map.get(env_key, "")
        if full:
            sections += f"""
## {env_key}
| Field    | Value |
|----------|-------|
| URL      | {url} |
| API URL  |       |
| Database |       |
| Ghi chú | {note} |
"""
        else:
            sections += f"""
## {env_key}
| Field    | Value |
|----------|-------|
| URL      | {url} |
| Ghi chú | {note} |
"""

    return f"""# Test Environments
{sections}
## Tài khoản kiểm thử (Test Accounts)
> Không lưu mật khẩu thực ở đây. Sử dụng password manager của team.

| Vai trò | Username | Ghi chú |
|---------|----------|---------|
| Admin   |          |         |
| User    |          |         |
"""


def template_test_run():
    return """# Test Run — [Sprint / Release] — [Ngày]

| Field       | Value |
|-------------|-------|
| Environment |       |
| Build       |       |
| Tester(s)   |       |
| Ngày bắt đầu |     |
| Ngày kết thúc |     |

## Tổng kết (Summary)
| Tổng | Passed | Failed | Blocked | Skipped |
|------|--------|--------|---------|---------|
|      |        |        |         |         |

## Test Case bị Fail
| TC ID | Tiêu đề | Bug ID | Ghi chú |
|-------|---------|--------|---------|
|       |         |        |         |

## Mục bị Block
| TC ID | Lý do | Người phụ trách |
|-------|-------|-----------------|
|       |       |                 |

## Ghi chú (Notes)
-
"""


def template_summary_report():
    return """# Báo cáo Tổng kết Kiểm thử — [Release / Sprint]

## Tổng quan (Overview)
| Chỉ số            | Giá trị |
|--------------------|---------|
| Thời gian kiểm thử |        |
| Environment        |         |
| Build đã test      |         |
| Tổng TC đã chạy   |         |
| Tỷ lệ Pass        |         |
| Bug đã tạo        |         |
| Bug đã resolved    |         |
| Bug P1/P2 còn mở  |         |

## Đánh giá chất lượng (Quality Assessment)
Chất lượng tổng thể: **GO / NO-GO / CONDITIONAL GO**

Lý do:

## Rủi ro còn mở (Open Risks)
-

## Khuyến nghị (Recommendation)
- [ ] Chấp nhận release
- [ ] Release với known issues (liệt kê bên dưới)
- [ ] Chặn release
"""


def template_readme(project_name, test_types, envs, default_env):
    tt_str = ", ".join(test_types)
    return f"""# {project_name} — Manual Testing Project

## Mục đích (Purpose)
Dự án kiểm thử thủ công cho **{project_name}**.

## Loại kiểm thử (Test Types)
{tt_str}

## Cấu trúc thư mục (Folder Structure)
| Thư mục | Mục đích |
|---------|----------|
| `00_input/` | Tài liệu đầu vào: URD, SRS, specs |
| `01_test-plans/` | Kế hoạch kiểm thử theo release/feature |
| `02_analyze-requirements/` | Kết quả phân tích yêu cầu |
| `03_test-cases/` | Test case chi tiết theo loại |
| `04_test-data/` | Dữ liệu kiểm thử (valid/invalid) |
| `05_bug-reports/` | Báo cáo lỗi |
| `06_checklists/` | Checklist smoke test & release |
| `07_environments/` | Cấu hình môi trường |
| `08_test-runs/` | Log kết quả chạy test theo sprint |
| `09_reports/` | Báo cáo tổng kết cho stakeholders |
| `10_source-code/` | Automation source code + MEMORY tracking |

## Quy tắc đặt tên (Naming Conventions)
- Test cases: `TC-[MODULE]-[NNN]-[short-title].md`
  - Ví dụ: `TC-LOGIN-001-valid-credentials.md`
- Bug reports: `BUG-[NNN]-[short-title].md`
  - Ví dụ: `BUG-001-login-button-unresponsive.md`
- Test runs: `TR-[SPRINT]-[YYYY-MM-DD].md`
  - Ví dụ: `TR-S05-2026-04-06.md`

## Môi trường mặc định (Default Environment)
**{default_env}**

## Ngôn ngữ (Language)
- Nội dung test case, mô tả, bước thực hiện: **Tiếng Việt**
- Thuật ngữ kỹ thuật, keywords, status: **Tiếng Anh**

## Liên hệ (Contacts)
- QA Lead:
- Dev Lead:
- PM:
"""


def template_claude_md(project_name, test_types, envs, urls, automation=""):
    tt_str = ", ".join(test_types)
    env_str = ", ".join(envs)
    url_str = ", ".join(urls) if urls else "N/A"
    today = date.today().isoformat()

    auto_section = ""
    if automation:
        auto_section = f"""
## Automation Context
- **Framework:** {automation}
- **Source code:** `10_source-code/`
- **MEMORY (source-code):** `10_source-code/MEMORY.md`
- **Skills:** analyze-requirements → generate-tc → implement-automation
"""

    workflow_extra = ""
    if automation:
        workflow_extra = """8. Implement automation → `10_source-code/` (dùng skill implement-automation)
"""

    return f"""# {project_name} — Project Context

## Thông tin dự án (Project Info)
- **Tên dự án:** {project_name}
- **Loại kiểm thử:** {tt_str}
- **Môi trường:** {env_str}
- **URL:** {url_str}

## Quy trình làm việc (Workflow)
1. Đặt tài liệu đầu vào (URD, SRS, specs) vào `00_input/`
2. Phân tích yêu cầu → kết quả vào `02_analyze-requirements/` (skill: analyze-requirements)
3. Viết test case → `03_test-cases/[loại]/` (skill: generate-tc)
4. Chuẩn bị test data → `04_test-data/`
5. Thực hiện test → log vào `08_test-runs/`
6. Ghi nhận bug → `05_bug-reports/`
7. Tổng hợp báo cáo → `09_reports/`
{workflow_extra}
## MEMORY Files
- **Analyze MEMORY:** `02_analyze-requirements/MEMORY.md` — scenarios, test data, clarifications
- **Source-code MEMORY:** `10_source-code/MEMORY.md` — locators, page classes, implementation log (chỉ khi có automation)

## Quy ước (Conventions)
- Tên file test case: `TC-[MODULE]-[NNN]-[short-title].md`
- Tên file bug: `BUG-[NNN]-[short-title].md`
- Nội dung: Tiếng Việt, thuật ngữ kỹ thuật giữ nguyên tiếng Anh
- Status values: Pass, Fail, Blocked, Skipped (tiếng Anh)
{auto_section}
## Tools
- Manual testing project scaffolded by `init-manual-project` skill
- Created on: {today}
"""


def template_source_code_memory(project_name, automation):
    today = date.today().isoformat()
    return f"""# MEMORY — Source Code Context

> File này tracking cấu trúc source code automation.
> Tách biệt với 02_analyze-requirements/MEMORY.md (tracking requirement analysis).
> Cập nhật lần cuối: {today}

## 1. Project Structure
> Chạy skill implement-automation (Mode SCAN) để tự động điền section này.

```
10_source-code/
├── (chưa có source code — copy hoặc clone source code vào đây)
└── MEMORY.md
```

## 2. Tech Stack
| Component | Version | Ghi chú |
|-----------|---------|---------|
| Framework | {automation} | |

> Chạy Mode SCAN để extract versions từ pom.xml/build.gradle.

## 3. Conventions
> Sẽ được extract tự động từ source code hiện có khi chạy Mode SCAN.

## 4. Page Classes Registry
| Page Class | File Path | Elements | Methods | Scenarios Cover | Last Updated |
|------------|-----------|----------|---------|-----------------|-------------|

## 5. Test Classes Registry
| Test Class | File Path | Test Methods | Scenarios Cover | Status |
|------------|-----------|-------------|-----------------|--------|

## 6. Locator Registry
> Sử dụng MCP Playwright để lấy locator từ web thực.

## 7. Implementation Log
| Ngày | Mode | Scope | Files created/updated | Ghi chú |
|------|------|-------|----------------------|---------|

## 8. Locator Issues
| Element | Page | Issue | Status | Ngày phát hiện |
|---------|------|-------|--------|---------------|
"""


def main():
    args = parse_args()

    project = args.project_name
    envs = [e.strip() for e in args.environments.split(",") if e.strip()]
    urls = [u.strip() for u in args.urls.split(",") if u.strip()] if args.urls else []
    test_types = [t.strip() for t in args.test_types.split(",") if t.strip()]
    team = args.team_size
    root = os.path.join(args.output_dir, project)

    # Create folder structure
    mkdir(os.path.join(root, "00_input"))
    mkdir(os.path.join(root, "01_test-plans"))
    mkdir(os.path.join(root, "02_analyze-requirements"))

    # Only create test-case subfolders for selected types
    type_folder_map = {
        "Functional": "functional",
        "Regression": "regression",
        "Smoke": "smoke",
        "UAT": "uat",
        "Exploratory": "exploratory",
        "Performance": "performance",
    }
    for tt in test_types:
        folder = type_folder_map.get(tt)
        if folder:
            mkdir(os.path.join(root, "03_test-cases", folder))

    mkdir(os.path.join(root, "04_test-data", "valid"))
    mkdir(os.path.join(root, "04_test-data", "invalid"))
    mkdir(os.path.join(root, "05_bug-reports"))
    mkdir(os.path.join(root, "06_checklists"))
    mkdir(os.path.join(root, "07_environments"))
    mkdir(os.path.join(root, "08_test-runs"))
    mkdir(os.path.join(root, "09_reports"))

    # Create 10_source-code if automation is specified
    automation = args.automation.strip() if args.automation else ""
    if automation:
        mkdir(os.path.join(root, "10_source-code"))
        write(os.path.join(root, "10_source-code", "MEMORY.md"),
              template_source_code_memory(project, automation))

    # Write template files
    write(os.path.join(root, "01_test-plans", "template-test-plan.md"),
          template_test_plan(project, test_types, team))

    # Write TC template to first available test type folder
    first_type = type_folder_map.get(test_types[0], "functional") if test_types else "functional"
    tc_dir = os.path.join(root, "03_test-cases", first_type)
    mkdir(tc_dir)
    write(os.path.join(tc_dir, "TC-001-template.md"), template_test_case(team))

    write(os.path.join(root, "05_bug-reports", "template-bug-report.md"), template_bug_report())
    write(os.path.join(root, "06_checklists", "smoke-checklist.md"), template_smoke_checklist(project))
    write(os.path.join(root, "06_checklists", "release-checklist.md"), template_release_checklist())
    write(os.path.join(root, "07_environments", "environments.md"), template_environments(envs, urls))
    write(os.path.join(root, "08_test-runs", "template-test-run.md"), template_test_run())
    write(os.path.join(root, "09_reports", "template-summary-report.md"), template_summary_report())

    default_env = envs[0] if envs else "DEV"
    write(os.path.join(root, "README.md"), template_readme(project, test_types, envs, default_env))
    write(os.path.join(root, "CLAUDE.md"), template_claude_md(project, test_types, envs, urls, automation))

    # Add .gitkeep to empty dirs
    for empty_dir in ["00_input", "02_analyze-requirements"]:
        gitkeep = os.path.join(root, empty_dir, ".gitkeep")
        if not os.listdir(os.path.join(root, empty_dir)):
            write(gitkeep, "")

    print(f"✅ Project scaffolded successfully: {root}")
    print(f"   Environments: {', '.join(envs)}")
    print(f"   Test types: {', '.join(test_types)}")
    print(f"   Team mode: {team}")
    if automation:
        print(f"   Automation: {automation}")
        print(f"   Source-code MEMORY: 10_source-code/MEMORY.md")
    print(f"\n📁 Folder structure:")
    for dirpath, dirnames, filenames in sorted(os.walk(root)):
        level = dirpath.replace(root, "").count(os.sep)
        indent = "│   " * level
        basename = os.path.basename(dirpath)
        if level == 0:
            print(f"   {project}/")
        else:
            print(f"   {indent}├── {basename}/")
        subindent = "│   " * (level + 1)
        for f in sorted(filenames):
            print(f"   {subindent}├── {f}")


if __name__ == "__main__":
    main()
