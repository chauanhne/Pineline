# ECOM — Manual Testing Project

## Giới thiệu
Dự án kiểm thử manual cho hệ thống ECOM trên môi trường STG.

## Môi trường
| Môi trường | URL |
|-----------|-----|
| STG | https://staging.tongdaiwifi.vn/ |

## Cấu trúc thư mục
```
ECOM/
├── 00_input/                # Tài liệu đầu vào: URD, SRS, specs
├── 03_test-cases/
│   └── functional/          # File Excel test case
├── CLAUDE.md                # Conventions cho AI assistants
└── README.md                # File này
```

## Workflow
1. Đặt tài liệu URD/SRS vào `00_input/`
2. Chạy skill `generate-manual-tc` → xuất file Excel TC vào `03_test-cases/functional/`
3. Chạy skill `vibe-test` → Playwright thực thi TC, ghi Pass/Fail vào cột H
4. Chạy skill `log-bug` → tạo bug report `.xlsx` cho các TC Fail

## Naming Conventions
- Test case file: `AI_ClaudeCode_<TênChứcNăng>.xlsx`
- Bug report: `TC_XX - Tên sheet - Tên chức năng.xlsx`
- Evidence: `08_test-runs/[YYYY-MM-DD]/evidence/`

## Ngôn ngữ
Tiếng Việt — giữ tiếng Anh cho thuật ngữ kỹ thuật (button, dropdown, API, URL...)
