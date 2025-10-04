# מדריך התקנה ותחזוקה - מערכת ניהול מלאי ו-CRM

## 📋 תוכן עניינים

1. [דרישות מערכת](#דרישות-מערכת)
2. [התקנה](#התקנה)
3. [הגדרות ראשוניות](#הגדרות-ראשוניות)
4. [הפעלת המערכת](#הפעלת-המערכת)
5. [תחזוקה שוטפת](#תחזוקה-שוטפת)
6. [גיבוי ושחזור](#גיבוי-ושחזור)
7. [שדרוג מערכת](#שדרוג-מערכת)
8. [פתרון תקלות](#פתרון-תקלות)

---

## 💻 דרישות מערכת

### חומרה מינימלית:
- **מעבד:** Intel Core i3 או שווה ערך
- **זיכרון:** 4GB RAM
- **שטח דיסק:** 10GB פנויים
- **חיבור אינטרנט:** לא נדרש (למעט התקנה)

### חומרה מומלצת:
- **מעבד:** Intel Core i5 ומעלה
- **זיכרון:** 8GB RAM ומעלה
- **שטח דיסק:** 50GB פנויים (SSD מומלץ)
- **חיבור אינטרנט:** לעדכונים ושירותי ענן

### תוכנה נדרשת:
- **מערכת הפעלה:** Windows 10/11, Linux, macOS
- **Python:** גרסה 3.10 ומעלה
- **דפדפן:** Chrome, Firefox, Edge (גרסה עדכנית)

---

## 🚀 התקנה

### שלב 1: התקנת Python

#### Windows:
1. הורד Python מ: https://www.python.org/downloads/
2. הרץ את קובץ ההתקנה
3. **חשוב:** סמן "Add Python to PATH"
4. לחץ על "Install Now"
5. אמת התקנה:
```powershell
python --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

#### macOS:
```bash
brew install python3
```

### שלב 2: הורדת המערכת

```bash
# הורד או העתק את תיקיית המערכת
cd C:\Users\User\Downloads\inventory
# או
git clone https://your-repository.git
cd inventory
```

### שלב 3: יצירת סביבה וירטואלית

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### שלב 4: התקנת תלויות

```bash
pip install -r requirements.txt
```

אם `requirements.txt` לא קיים, התקן ידנית:
```bash
pip install django pillow reportlab
```

### שלב 5: הגדרת מסד נתונים

```bash
# יצירת טבלאות
python manage.py makemigrations
python manage.py migrate
```

### שלב 6: יצירת משתמש מנהל

```bash
python manage.py createsuperuser
```
מלא:
- שם משתמש
- אימייל (אופציונלי)
- סיסמה (לפחות 8 תווים)

---

## ⚙️ הגדרות ראשוניות

### 1. הגדרת SECRET_KEY (חשוב לאבטחה!)

ערוך `inventory_project/settings.py`:

```python
# במקום:
SECRET_KEY = 'django-insecure-...'

# השתמש במשתנה סביבה:
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'temporary-key-change-me')
```

צור SECRET_KEY חדש:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. הגדרת DEBUG (סביבת ייצור)

```python
# פיתוח (development)
DEBUG = True
ALLOWED_HOSTS = []

# ייצור (production)
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1']
```

### 3. הגדרת קבצים סטטיים (ל-production)

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

אסוף קבצים סטטיים:
```bash
python manage.py collectstatic
```

### 4. הגדרת לוגים

הלוגים כבר מוגדרים ב-`settings.py`. תיקיית `logs/` תיווצר אוטומטית.

---

## ▶️ הפעלת המערכת

### פיתוח (Development):

```bash
# Windows
.\venv\Scripts\Activate.ps1
python manage.py runserver

# Linux/macOS
source venv/bin/activate
python manage.py runserver
```

גש ל: http://127.0.0.1:8000/

### ייצור (Production) - Windows:

1. **התקן Waitress:**
```bash
pip install waitress
```

2. **צור תסריט הפעלה** (`start_server.ps1`):
```powershell
$env:DJANGO_SECRET_KEY = "your-secret-key-here"
cd C:\Users\User\Downloads\inventory
.\venv\Scripts\Activate.ps1
waitress-serve --host=0.0.0.0 --port=8000 inventory_project.wsgi:application
```

3. **הרץ:**
```bash
.\start_server.ps1
```

### ייצור (Production) - Linux:

1. **התקן Gunicorn:**
```bash
pip install gunicorn
```

2. **הרץ:**
```bash
gunicorn --bind 0.0.0.0:8000 inventory_project.wsgi:application
```

### הפעלה אוטומטית בהפעלת Windows:

1. פתח Task Scheduler
2. צור Task חדש:
   - **Trigger:** At system startup
   - **Action:** Start a program
   - **Program:** `powershell.exe`
   - **Arguments:** `-File C:\path\to\start_server.ps1`

---

## 🔧 תחזוקה שוטפת

### גיבויים יומיים אוטומטיים

#### הגדרת גיבוי אוטומטי ב-Windows:

1. **צור Task ב-Task Scheduler:**
   - שם: "Inventory Daily Backup"
   - Trigger: Daily בשעה 02:00
   - Action: `powershell.exe`
   - Arguments: `-File C:\Users\User\Downloads\inventory\scripts\auto_backup.ps1`

2. **בדוק שהתסריט עובד:**
```powershell
.\scripts\auto_backup.ps1
```

#### ניהול גיבויים ידני:

```bash
# יצירת גיבוי
python manage.py backup_database

# רשימת גיבויים
python manage.py list_backups

# שחזור מגיבוי
python manage.py restore_database backup_20250104_120000
```

### ניקוי לוגים

```bash
# מחיקת לוגים ישנים (30 ימים)
python manage.py cleanup_logs --days 30

# דחיסה במקום מחיקה
python manage.py cleanup_logs --days 30 --compress
```

### צפייה בלוגים

```bash
# לוג כללי (50 שורות אחרונות)
python manage.py view_logs --type general --lines 50

# לוג שגיאות
python manage.py view_logs --type errors

# חיפוש בלוגים
python manage.py view_logs --search "error" --type all
```

### עדכון מסד נתונים (אחרי שינויים)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 💾 גיבוי ושחזור

### אסטרטגיית גיבוי מומלצת:

1. **גיבוי יומי אוטומטי** - בשעות הלילה
2. **גיבוי שבועי ידני** - לשמירה חיצונית
3. **גיבוי חודשי** - ארכיון ארוך טווח

### מיקומי גיבוי:

```
backups/
├── backup_20250104_020000/  # גיבוי אוטומטי יומי
│   ├── db.sqlite3
│   ├── media/
│   └── metadata.json
├── backup_20250103_020000/
└── ...
```

### שחזור במקרה חירום:

1. **זיהוי הגיבוי האחרון:**
```bash
python manage.py list_backups
```

2. **שחזור:**
```bash
python manage.py restore_database backup_20250104_020000
```

3. **אימות:**
```bash
python manage.py check
python manage.py runserver
```

### גיבוי חיצוני (מומלץ מאוד):

העתק את תיקיית `backups/` ל:
- דיסק חיצוני
- שירות ענן (Google Drive, Dropbox)
- שרת גיבוי מרוחק

---

## 🔄 שדרוג מערכת

### שדרוג Django ותלויות:

```bash
# גיבוי לפני שדרוג!
python manage.py backup_database

# עדכון תלויות
pip install --upgrade django
pip install --upgrade -r requirements.txt

# בדיקת תאימות
python manage.py check

# עדכון מסד נתונים
python manage.py migrate
```

### שדרוג גרסת Python:

1. גבה את המערכת
2. התקן Python חדש
3. צור venv חדש
4. התקן תלויות
5. בדוק תקינות

---

## 🐛 פתרון תקלות

### בעיה: "ModuleNotFoundError: No module named 'django'"

**פתרון:**
```bash
# ודא שסביבה וירטואלית מופעלת
.\venv\Scripts\Activate.ps1
pip install django
```

### בעיה: "port 8000 is already in use"

**פתרון:**
```bash
# השתמש בפורט אחר
python manage.py runserver 8080

# או סגור את התהליך הקיים (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### בעיה: קבצים סטטיים לא נטענים

**פתרון:**
```bash
python manage.py collectstatic --clear
```

### בעיה: שגיאות בלוגים

**בדיקה:**
```bash
# צפייה בלוג שגיאות
python manage.py view_logs --type errors --lines 100
```

### בעיה: מסד נתונים פגום

**פתרון:**
```bash
# שחזור מגיבוי אחרון
python manage.py list_backups
python manage.py restore_database backup_YYYYMMDD_HHMMSS
```

---

## 📊 ניטור ביצועים

### בדיקת תקינות:

```bash
python manage.py check
python manage.py check --deploy  # בדיקות אבטחה
```

### מעקב אחר שימוש בדיסק:

```bash
# גודל מסד נתונים
dir db.sqlite3  # Windows
ls -lh db.sqlite3  # Linux

# גודל גיבויים
du -sh backups/  # Linux
```

---

## 🔒 אבטחה

### רשימת בדיקה לאבטחה:

- [ ] DEBUG = False בייצור
- [ ] SECRET_KEY ייחודי ובטוח
- [ ] ALLOWED_HOSTS מוגדר
- [ ] גיבויים תקופתיים
- [ ] עדכוני אבטחה של Django
- [ ] HTTPS מופעל (בייצור)
- [ ] הרשאות קבצים מוגבלות
- [ ] לוגים מנוטרים

---

## 📞 תמיכה טכנית

### לוגים חשובים:

- `logs/general.log` - לוג כללי
- `logs/errors.log` - שגיאות
- `logs/security.log` - אבטחה
- `logs/database.log` - שאילתות DB

### מידע לתמיכה:

כשפונים לתמיכה, ספק:
1. גרסת Python: `python --version`
2. גרסת Django: `python -m django --version`
3. מערכת הפעלה
4. הודעת שגיאה מלאה
5. לוגים רלוונטיים

---

**גרסה:** 1.0
**עודכן לאחרונה:** 04/10/2025
**זכויות יוצרים:** כל הזכויות שמורות

