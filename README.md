# 📦 מערכת ניהול מלאי ו-CRM מקצועית

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2+-green.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

**מערכת מקיפה לניהול מלאי, CRM, מכירות וחשבוניות**

[תיעוד מלא](docs/USER_MANUAL.md) • [מדריך התקנה](docs/INSTALLATION.md) • [דרישות מערכת](#-דרישות-מערכת)

</div>

---

## 📖 אודות

מערכת ניהול מלאי ו-CRM היא פתרון עסקי מקצועי המיועד לעסקים קטנים ובינוניים. המערכת מספקת כלים מתקדמים לניהול:

- 📦 **ניהול מלאי** - מעקב אחר מוצרים במחסן ובחנות
- 👥 **CRM מתקדם** - ניהול לקוחות וקשרי עסקיים
- 💰 **מכירות וחשבוניות** - מערכת מכירה מלאה עם הפקת חשבוניות PDF
- 🚚 **העברות מלאי** - ניהול העברות בין מיקומים
- 🔔 **התראות חכמות** - התראות אוטומטיות על מלאי נמוך
- 📊 **דוחות מפורטים** - ניתוחים עסקיים ודוחות סטטיסטיים
- 💾 **גיבוי אוטומטי** - מערכת גיבוי ושחזור מובנית
- 📝 **לוגים מקצועיים** - מעקב אחר כל פעולה במערכת

---

## ✨ תכונות עיקריות

### 📦 ניהול מלאי מתקדם
- מעקב אחר כמויות במחסן ובחנות בנפרד
- ברקודים למוצרים
- תמונות מוצר
- קטגוריות וספקים
- התראות על מלאי נמוך ואפסי
- מחירי קנייה ומכירה
- ניהול הנחות

### 👥 CRM מקצועי
- מאגר לקוחות מפורט
- סיווג לקוחות (VIP, רגיל, פוטנציאלי)
- היסטוריית רכישות
- הערות ותזכורות
- מעקב אחר חובות ואשראי
- דוחות לקוחות מתקדמים

### 💰 מכירות וחשבוניות
- רישום מכירות מהיר
- הפקת חשבוניות PDF מעוצבות
- חישוב מע"מ אוטומטי
- הנחות ומבצעים
- קישור אוטומטי ללקוח
- עדכון מלאי אוטומטי

### 🚚 ניהול העברות
- העברות בין מחסן לחנות
- מעקב אחר סטטוס העברה
- אישור קבלת סחורה
- היסטוריה מלאה

### 📊 דוחות ואנליטיקס
- דוחות מכירות מפורטים
- ניתוח רווחיות
- דוחות לקוחות
- דוחות מלאי
- גרפים אינטראקטיביים

### 🔒 אבטחה וגיבוי
- מערכת גיבוי אוטומטי יומי
- שחזור מהיר מגיבוי
- לוגים מפורטים
- הרשאות משתמשים (בפיתוח)

---

## 🚀 התחלה מהירה

### 🌐 גרסה מקוונת (GitHub Pages)

האפליקציה זמינה כעת ב-GitHub Pages:
- **URL:** https://shaharprod.github.io/inventory
- **לא דורש התקנה** - פשוט פתח בדפדפן
- **כולל את כל הנתונים** מהמערכת המקומית

### 🖥️ גרסה מקומית (Django)

### דרישות מקדימות

- Python 3.10 ומעלה
- pip (מותקן עם Python)
- 4GB RAM (מינימום)
- 10GB שטח דיסק פנוי

### התקנה

```bash
# 1. שיבוט הפרויקט
cd C:\Users\User\Downloads\inventory

# 2. יצירת סביבה וירטואלית
python -m venv venv

# 3. הפעלת הסביבה
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 4. התקנת תלויות
pip install django pillow reportlab

# 5. הגדרת מסד נתונים
python manage.py makemigrations
python manage.py migrate

# 6. יצירת משתמש מנהל
python manage.py createsuperuser

# 7. הרצת השרת
python manage.py runserver
```

גש ל: **http://127.0.0.1:8000/**

---

## 📚 תיעוד

### מדריכים מפורטים:

- 📖 [מדריך משתמש מלא](docs/USER_MANUAL.md)
- 🔧 [מדריך התקנה ותחזוקה](docs/INSTALLATION.md)
- 🐛 [פתרון בעיות נפוצות](docs/INSTALLATION.md#-פתרון-תקלות)

### פקודות ניהול שימושיות:

```bash
# גיבוי
python manage.py backup_database

# רשימת גיבויים
python manage.py list_backups

# שחזור
python manage.py restore_database backup_20250104_120000

# צפייה בלוגים
python manage.py view_logs --type errors

# ניקוי לוגים
python manage.py cleanup_logs --days 30
```

---

## 🖥️ צילומי מסך

### דשבורד ראשי
> מסך ראשי עם סטטיסטיקות בזמן אמת, התראות ונתונים חשובים

### ניהול מוצרים
> רשימת מוצרים עם חיפוש, סינון ועריכה מהירה

### CRM ולקוחות
> מערכת CRM מלאה עם מעקב אחר היסטוריה וקשרים

### הפקת חשבוניות
> חשבוניות PDF מעוצבות עם לוגו ופרטים מלאים

---

## 🛠️ טכנולוגיות

### Backend:
- **Django 5.2** - Framework עוצמתי ובטוח
- **Python 3.10+** - שפת תכנות מודרנית
- **SQLite** - מסד נתונים מהיר ויעיל (ניתן לשדרג ל-PostgreSQL/MySQL)

### Frontend:
- **Bootstrap 5.1.3** - עיצוב רספונסיבי ומודרני
- **Font Awesome 6.0** - אייקונים מקצועיים
- **Chart.js** - גרפים אינטראקטיביים
- **Dark Theme** - עיצוב כהה נעים לעין

### כלי פיתוח:
- **Django Admin** - ממשק ניהול מובנה
- **Django ORM** - גישה למסד נתונים
- **ReportLab** - יצירת PDF
- **Pillow** - עיבוד תמונות

---

## 📂 מבנה הפרויקט

```
inventory/
├── inventory/                  # אפליקציית ראשית
│   ├── models.py              # מודלים (טבלאות DB)
│   ├── views.py               # לוגיקת עסקית
│   ├── forms.py               # טפסים
│   ├── urls.py                # ניתוב
│   ├── admin.py               # ממשק ניהול
│   ├── templates/             # תבניות HTML
│   │   └── inventory/
│   ├── static/                # קבצים סטטיים
│   │   └── inventory/
│   │       └── css/
│   │           └── dark-theme.css
│   └── management/            # פקודות ניהול
│       └── commands/
│           ├── backup_database.py
│           ├── restore_database.py
│           ├── list_backups.py
│           ├── view_logs.py
│           └── cleanup_logs.py
├── inventory_project/         # הגדרות פרויקט
│   ├── settings.py            # הגדרות ראשיות
│   ├── urls.py                # ניתוב ראשי
│   └── wsgi.py                # WSGI
├── scripts/                   # תסריטים
│   └── auto_backup.ps1        # גיבוי אוטומטי Windows
├── docs/                      # תיעוד
│   ├── USER_MANUAL.md
│   └── INSTALLATION.md
├── backups/                   # גיבויים (נוצר אוטומטית)
├── logs/                      # לוגים (נוצר אוטומטית)
│   ├── general.log
│   ├── errors.log
│   ├── security.log
│   └── database.log
├── media/                     # קבצים שהועלו
├── db.sqlite3                 # מסד נתונים
├── manage.py                  # סקריפט ניהול Django
├── requirements.txt           # תלויות Python
└── README.md                  # קובץ זה
```

---

## 🔐 אבטחה

המערכת כוללת שכבות אבטחה מרובות:

- ✅ **CSRF Protection** - הגנה מפני התקפות CSRF
- ✅ **SQL Injection Protection** - Django ORM מונע SQL Injection
- ✅ **XSS Protection** - ניקוי אוטומטי של קלט משתמש
- ✅ **Password Hashing** - סיסמאות מוצפנות (בדרך)
- ✅ **Secure Cookies** - עוגיות מאובטחות
- ✅ **Logging System** - מעקב אחר כל פעולה
- ✅ **Backup System** - גיבוי אוטומטי יומי

### הגדרות אבטחה לייצור:

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🔄 עדכונים ותחזוקה

### גיבוי אוטומטי יומי:

המערכת כוללת תסריט גיבוי אוטומטי עם Windows Task Scheduler:

1. פתח Task Scheduler
2. צור Task חדש:
   - **שם:** "Inventory Daily Backup"
   - **Trigger:** Daily בשעה 02:00
   - **Action:** `powershell.exe`
   - **Arguments:** `-File C:\Users\User\Downloads\inventory\scripts\auto_backup.ps1`

### תחזוקה שוטפת:

```bash
# גיבוי ידני
python manage.py backup_database

# ניקוי לוגים (כל 30 ימים)
python manage.py cleanup_logs --days 30

# בדיקת תקינות
python manage.py check

# עדכון תלויות
pip install --upgrade -r requirements.txt
```

---

## 📊 סטטיסטיקות פרויקט

- **שורות קוד:** ~5,000+
- **מודלים:** 15+
- **תצוגות (Views):** 50+
- **תבניות (Templates):** 30+
- **פקודות ניהול:** 5
- **זמן פיתוח:** 40+ שעות

---

## 🐛 דיווח על באגים

אם נתקלת בבעיה:

1. בדוק את [פתרון בעיות](docs/INSTALLATION.md#-פתרון-תקלות)
2. צפה בלוג שגיאות: `python manage.py view_logs --type errors`
3. צור issue עם:
   - תיאור הבעיה
   - צילום מסך
   - לוג רלוונטי
   - גרסת Python ו-Django

---

## 🗺️ תוכנית פיתוח עתידי

### גרסה 1.1 (מתוכנן):
- [ ] מערכת התחברות והרשאות משתמשים
- [ ] API REST לאינטגרציות
- [ ] אפליקציית מובייל
- [ ] דוחות Excel מתקדמים
- [ ] אינטגרציה עם מדפסות קופה

### גרסה 1.2 (רעיונות):
- [ ] תמיכה במספר שפות
- [ ] מערכת הזמנות אוטומטית
- [ ] אינטגרציה עם חשבשבת
- [ ] מערכת שכר ונוכחות
- [ ] ניהול ספקים מתקדם

---

## 📄 רישיון

כל הזכויות שמורות. מערכת זו היא קניינית ומיועדת למכירה ללקוחות.

**אין להעתיק, לשנות או להפיץ ללא אישור מפורש.**

---

## 👨‍💻 פיתוח

פותח על ידי מערכת בינה מלאכותית מתקדמת עבור לקוח פרטי.

---

## 📞 יצירת קשר ותמיכה

לתמיכה טכנית, פנה למנהל המערכת עם:
- גרסת Python: `python --version`
- גרסת Django: `python -m django --version`
- תיאור הבעיה
- קבצי לוג רלוונטיים

---

<div align="center">

**עשוי באהבה ❤️ עם Django + Python**

⭐ אם המערכת עזרה לך, אל תשכח לדרג!

</div>

