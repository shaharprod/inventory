#!/usr/bin/env python
"""
תיקון הזחה בפונקציה send_instant_report
"""

# קרא את הקובץ
with open('inventory/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines, start=1):
    # תקן הזחה בשורות 2625-3060 (הפונקציה send_instant_report)
    if i >= 2625 and i <= 3060:
        # אם מוזז ב-12 רווחים, הפוך ל-8
        if line.startswith('            ') and not line.startswith('             '):
            line = line[4:]  # הסר 4 רווחים
    new_lines.append(line)

# שמור
with open('inventory/views.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ הזחה תוקנה!")

