# CLAUDE.md — ECOM

## Project Info
- **Tên dự án:** ECOM
- **Mô tả:** Dự án kiểm thử hệ thống ECOM
- **Môi trường:** STG — URL: https://staging.tongdaiwifi.vn/
- **Test types:** Functional
- **Team:** Solo
- **Ngôn ngữ:** Tiếng Việt (giữ tiếng Anh cho thuật ngữ kỹ thuật)

## Automation
- **Framework:** Playwright (Vibe Test)
- **Source code:** `10_source-code/` (nếu cần)

## Naming Conventions
- Test cases: `AI_ClaudeCode_<TênChứcNăng>.xlsx`
- Bug reports: `TC_XX - Tên sheet - Tên chức năng/Block.xlsx`
- Test runs: `08_test-runs/[YYYY-MM-DD]/`

## Workflow
```
00_input/ (tài liệu gốc: URD, SRS, specs)
  → 03_test-cases/functional/ (viết TC bằng generate-manual-tc skill)
    → vibe-test (chạy Playwright, ghi Pass/Fail vào cột H)
      → 05_bug-reports/ (log bug bằng log-bug skill)
```

## Folder Reference
| Folder | Mục đích | Skill liên quan |
|--------|----------|----------------|
| 00_input/ | Tài liệu đầu vào: URD, SRS, specs | generate-manual-tc (đọc) |
| 03_test-cases/functional/ | File Excel test case | generate-manual-tc (ghi), vibe-test (đọc) |
| CLAUDE.md | Project conventions cho AI | Tất cả skills đọc |
