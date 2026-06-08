# Templates Reference

All starter templates for the manual testing project scaffold.

## Table of Contents
1. [Test Plan](#test-plan)
2. [Test Case](#test-case)
3. [Bug Report](#bug-report)
4. [Smoke Checklist](#smoke-checklist)
5. [Release Checklist](#release-checklist)
6. [Environments](#environments)
7. [Test Run Log](#test-run-log)
8. [Summary Report](#summary-report)
9. [README](#readme)
10. [CLAUDE.md](#claudemd)

---

## Test Plan

File: `01_test-plans/template-test-plan.md`

```markdown
# Test Plan: [Feature / Release Name]

## Mục tiêu (Objective)
Mô tả những gì đang được kiểm thử và lý do.

## Phạm vi (Scope)
### Trong phạm vi (In Scope)
-

### Ngoài phạm vi (Out of Scope)
-

## Loại kiểm thử (Test Types)
- [ ] Functional
- [ ] Regression
- [ ] Smoke
- [ ] UAT
- [ ] Exploratory
- [ ] Performance

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
```

### Team mode additions
Add after Resources:
```markdown
## Phân công (Assignments)
| Thành viên | Vai trò | Module phụ trách |
|------------|---------|-----------------|
|            |         |                 |
```

---

## Test Case

File: `03_test-cases/functional/TC-001-template.md`

```markdown
# TC-001: [Tên Test Case]

| Field        | Value                        |
|--------------|------------------------------|
| Module       |                              |
| Priority     | P1 / P2 / P3                 |
| Type         | Positive / Negative / Edge   |
| Tạo bởi     |                              |
| Cập nhật lần cuối |                         |

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
```

### Team mode additions
Add to the metadata table:
```markdown
| Assigned to  |                              |
| Reviewed by  |                              |
```

---

## Bug Report

File: `05_bug-reports/template-bug-report.md`

```markdown
# BUG-XXX: [Mô tả ngắn]

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
```

---

## Smoke Checklist

File: `06_checklists/smoke-checklist.md`

```markdown
# Smoke Test Checklist — [Tên sản phẩm]

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
```

---

## Release Checklist

File: `06_checklists/release-checklist.md`

```markdown
# Release Checklist — [Version]

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
```

---

## Environments

File: `07_environments/environments.md`

```markdown
# Test Environments

## DEV
| Field    | Value |
|----------|-------|
| URL      | {dev_url} |
| API URL  |       |
| Database |       |
| Ghi chú | Không ổn định, chỉ dành cho developer testing |

## STG (Staging)
| Field    | Value |
|----------|-------|
| URL      | {stg_url} |
| API URL  |       |
| Database |       |
| Ghi chú | Dữ liệu mirror từ production (đã ẩn danh) |

## UAT
| Field    | Value |
|----------|-------|
| URL      | {uat_url} |
| API URL  |       |
| Database |       |
| Ghi chú | Môi trường cho User Acceptance Testing |

## PRODUCTION
| Field    | Value |
|----------|-------|
| URL      | {prod_url} |
| Ghi chú | Chỉ chạy smoke test read-only |

## Tài khoản kiểm thử (Test Accounts)
> Không lưu mật khẩu thực ở đây. Sử dụng password manager của team.

| Vai trò | Username | Ghi chú |
|---------|----------|---------|
| Admin   |          |         |
| User    |          |         |
```

---

## Test Run Log

File: `08_test-runs/template-test-run.md`

```markdown
# Test Run — [Sprint / Release] — [Ngày]

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
```

---

## Summary Report

File: `09_reports/template-summary-report.md`

```markdown
# Báo cáo Tổng kết Kiểm thử — [Release / Sprint]

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
```

---

## README

File: `README.md`

```markdown
# {project_name} — Manual Testing Project

## Mục đích (Purpose)
Dự án kiểm thử thủ công cho {project_name}.

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
| `10_memory-project/` | Context chia sẻ cho AI/team |

## Quy tắc đặt tên (Naming Conventions)
- Test cases: `TC-[MODULE]-[NNN]-[short-title].md`
- Bug reports: `BUG-[NNN]-[short-title].md`
- Test runs: `TR-[SPRINT]-[YYYY-MM-DD].md`

## Môi trường mặc định (Default Environment)
{default_environment}

## Ngôn ngữ (Language)
- Nội dung test case: Tiếng Việt
- Thuật ngữ kỹ thuật và keywords: Tiếng Anh

## Liên hệ (Contacts)
- QA Lead:
- Dev Lead:
- PM:
```

---

## CLAUDE.md

File: `CLAUDE.md`

```markdown
# {project_name} — Project Context

## Thông tin dự án (Project Info)
- **Tên dự án:** {project_name}
- **Loại kiểm thử:** {test_types}
- **Môi trường:** {environments}
- **URL:** {urls}

## Quy trình làm việc (Workflow)
1. Đặt tài liệu đầu vào (URD, SRS, specs) vào `00_input/`
2. Phân tích yêu cầu → kết quả vào `02_analyze-requirements/`
3. Viết test case → `03_test-cases/[loại]/`
4. Chuẩn bị test data → `04_test-data/`
5. Thực hiện test → log vào `08_test-runs/`
6. Ghi nhận bug → `05_bug-reports/`
7. Tổng hợp báo cáo → `09_reports/`

## Quy ước (Conventions)
- Tên file test case: `TC-[MODULE]-[NNN]-[short-title].md`
- Tên file bug: `BUG-[NNN]-[short-title].md`
- Nội dung: Tiếng Việt, thuật ngữ kỹ thuật giữ nguyên tiếng Anh
- Status values: Pass, Fail, Blocked, Skipped (tiếng Anh)

## Tools
- Manual testing project scaffolded by `init-manual-project` skill
- Created on: {date}
```
