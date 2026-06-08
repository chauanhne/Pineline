import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import openpyxl

path = 'C:\\Users\\ASUS\\Documents\\Pineline\\ECOM\\00_input\\Thông tin chung.xlsx'
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb.worksheets[0]

tcs = []
for row in ws.iter_rows(min_row=1, values_only=True):
    tc_id = row[1]
    if tc_id and str(tc_id).startswith('TC_'):
        tcs.append({
            'id': tc_id,
            'priority': row[2],
            'title': str(row[3])[:70] if row[3] else '',
            'precond': str(row[4])[:80] if row[4] else '',
            'steps': str(row[5])[:80] if row[5] else '',
        })

print(f'Tổng TC: {len(tcs)}')
high = [t for t in tcs if t['priority'] == 'High']
medium = [t for t in tcs if t['priority'] == 'Medium']
low = [t for t in tcs if t['priority'] == 'Low']
print(f'High: {len(high)} | Medium: {len(medium)} | Low: {len(low)}')
print()
for t in tcs:
    print(f"  {t['id']} | {t['priority']} | {t['title']}")
