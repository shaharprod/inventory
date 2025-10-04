# 🚀 התחלה מהירה - 5 דקות

## להפעלת המערכת במהירות:

### 1️⃣ הפעלה ראשונה (חד פעמי)

```powershell
# פתח PowerShell בתיקיית המערכת והרץ:
.\start.ps1
```

הסקריפט יטפל בכל ההתקנה אוטומטית!

---

### 2️⃣ הפעלה רגילה (כל פעם)

```powershell
# הפעל את הסקריפט:
.\start.ps1

# או ידנית:
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

### 3️⃣ כניסה למערכת

פתח דפדפן וגש ל:
```
http://127.0.0.1:8000/
```

---

## 📦 פקודות שימושיות

### גיבוי:
```bash
python manage.py backup_database
```

### צפייה בגיבויים:
```bash
python manage.py list_backups
```

### שחזור:
```bash
python manage.py restore_database backup_20250104_120000
```

### צפייה בשגיאות:
```bash
python manage.py view_logs --type errors
```

---

## 🎯 מסכים ראשיים

| מסך | כתובת |
|-----|--------|
| דשבורד | http://127.0.0.1:8000/ |
| מוצרים | http://127.0.0.1:8000/products/ |
| לקוחות | http://127.0.0.1:8000/crm/customers/ |
| מכירות | http://127.0.0.1:8000/sales/ |
| דוחות | http://127.0.0.1:8000/reports/ |
| מנהל | http://127.0.0.1:8000/admin/ |

---

## ❓ בעיות נפוצות

### "אין אפשרות להתחבר"
→ ודא שהשרת פועל, הרץ `.\start.ps1`

### "Python לא מזוהה"
→ התקן Python מ: https://www.python.org/downloads/

### "Module not found"
→ הרץ: `pip install -r requirements.txt`

---

## 📚 תיעוד מלא

- [מדריך משתמש](docs/USER_MANUAL.md)
- [מדריך התקנה](docs/INSTALLATION.md)
- [README](README.md)

---

**צריך עזרה?** פנה למנהל המערכת

