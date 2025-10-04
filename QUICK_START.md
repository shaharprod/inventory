# 🚀 מדריך התחלה מהירה - מערכת ניהול מלאי

## 📋 תוכן עניינים
- [התקנה ראשונית](#התקנה-ראשונית)
- [הפעלת המערכת](#הפעלת-המערכת)
- [פרטי התחברות](#פרטי-התחברות)
- [נתוני דמו](#נתוני-דמו)
- [פתרון בעיות](#פתרון-בעיות)

---

## 🔧 התקנה ראשונית

### דרישות מקדימות
- Python 3.8 ומעלה
- pip (מנהל החבילות של Python)
- Windows 10/11

### צעדי התקנה

1. **התקנת חבילות Python:**
```bash
pip install -r requirements.txt
```

2. **יצירת בסיס נתונים:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **יצירת משתמש מנהל:**
```bash
python manage.py createsuperuser
```

4. **יצירת נתוני דמו (אופציונלי):**
```bash
python create_demo_data.py
```

---

## 🚀 הפעלת המערכת

### אפשרות 1: הפעלה פשוטה (מומלץ)
**לחץ כפול על הקובץ:** `start.bat`

### אפשרות 2: PowerShell
```powershell
.\start_server.ps1
```

### אפשרות 3: הפעלה ידנית
```bash
# הפעל את ה-virtual environment
.\venv\Scripts\Activate.ps1

# הרץ את השרת
python manage.py runserver
```

השרת יעלה על: **http://127.0.0.1:8000**

---

## 🔑 פרטי התחברות

### משתמש מנהל (Admin)
- **שם משתמש:** `admin`
- **סיסמה:** `admin123`

### לוח ניהול Django
- **כתובת:** http://127.0.0.1:8000/admin

---

## 📊 נתוני דמו

המערכת מגיעה עם נתוני דמו מוכנים:

### מוצרים (10)
- **אלקטרוניקה:** מחשב נייד Dell, עכבר אלחוטי
- **ביגוד:** חולצת פולו, ג'ינס כחול
- **מזון:** בקבוק מים, חטיף בריאות
- **ריהוט:** כיסא משרדי, שולחן כתיבה
- **ספרים:** ספר בדיון, מגזין טכנולוגיה

### מיקומים (2)
- **מחסן ראשי** - אזור תעשייה, פתח תקווה (70% מהמלאי)
- **חנות ראשית** - דיזנגוף 123, תל אביב (30% מהמלאי)

### לקוחות (4)
- דוד כהן (פרטי, הנחה 5%)
- שרה לוי (פרטי, הנחה 10%)
- חברת הטכנולוגיה בע"מ (עסקי, הנחה 15%)
- מסעדת הבשר (עסקי, הנחה 8%)

### קטגוריות (5)
אלקטרוניקה • ביגוד • מזון • ריהוט • ספרים

### ספקים (3)
ספק אלקטרוניקה • ספק ביגוד • ספק מזון

---

## 🎯 דפים עיקריים

| דף | כתובת URL | תיאור |
|---|---|---|
| דשבורד | `/` | מבט כללי על המערכת |
| מוצרים | `/products/` | רשימת מוצרים + חיפוש וסינון |
| מכירות | `/sales/add/` | ממשק קופה להוספת מכירות |
| חשבוניות | `/sales/` | רשימת חשבוניות מס |
| לקוחות | `/crm/customers/` | ניהול לקוחות CRM |
| דוחות | `/reports/` | דוחות ואנליטיקה |
| קטגוריות | `/categories/` | ניהול קטגוריות |
| ספקים | `/suppliers/` | ניהול ספקים |
| העברות | `/transfers/` | העברות מלאי בין מיקומים |
| מנהל | `/admin/` | לוח ניהול Django |

---

## 🛠️ פתרון בעיות

### שגיאה: "No module named 'django'"
**פתרון:**
```bash
# ודא ש-virtual environment מופעל
.\venv\Scripts\Activate.ps1

# או התקן מחדש
pip install -r requirements.txt
```

### שגיאה: "Table doesn't exist"
**פתרון:**
```bash
# הרץ migrations מחדש
python manage.py migrate
```

### איפוס מלא של בסיס הנתונים
**אזהרה: פעולה זו תמחק את כל הנתונים!**

```bash
# הפעל virtual environment
.\venv\Scripts\Activate.ps1

# מחק את בסיס הנתונים
Remove-Item db.sqlite3 -Force

# מחק migrations ישנים
Get-ChildItem -Path inventory\migrations\ -Filter "*.py" | Where-Object {$_.Name -ne "__init__.py"} | Remove-Item -Force

# צור מחדש
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python create_demo_data.py
```

### השרת לא עולה
1. בדוק שאין תהליך אחר שמשתמש בפורט 8000
2. נסה פורט אחר:
```bash
python manage.py runserver 8080
```

### בעיות עם Virtual Environment
```bash
# צור virtual environment מחדש
python -m venv venv

# הפעל אותו
.\venv\Scripts\Activate.ps1

# התקן חבילות
pip install -r requirements.txt
```

---

## 📞 תמיכה נוספת

לתיעוד מלא, ראה:
- **מדריך משתמש:** `docs/USER_MANUAL.md`
- **תיעוד טכני:** `docs/TECHNICAL_DOCUMENTATION.md`
- **מדריך התקנה:** `docs/INSTALLATION_GUIDE.md`

---

## ✅ בדיקות אחרי התקנה

- [ ] השרת עולה בהצלחה
- [ ] ניתן להתחבר עם משתמש admin
- [ ] דף מוצרים מציג 10 מוצרים
- [ ] דף מכירות עובד (יש מוצרים ולקוחות)
- [ ] דף דוחות מציג נתונים
- [ ] ניתן ליצור מכירה חדשה
- [ ] חשבונית מס נוצרת אוטומטית

---

**גרסה:** 2.0
**תאריך עדכון:** אוקטובר 2025
**מפתח:** מערכת ניהול מלאי מתקדמת
