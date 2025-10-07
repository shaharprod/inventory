# 🏪 מערכת ניהול מלאי מתקדמת

מערכת ניהול מלאי מלאה ומודרנית עם ממשק משתמש עברי, דוחות מתקדמים, ומערכת גיבויים אוטומטית.

## ✨ תכונות עיקריות

### 📦 ניהול מלאי
- **ניהול מוצרים** - הוספה, עריכה, מחיקה עם תמונות
- **קטגוריות וספקים** - ארגון מוצרים לפי קטגוריות
- **מעקב מלאי** - התראות אוטומטיות על מלאי נמוך
- **ברקודים** - יצירה וסריקה של ברקודים

### 💰 מכירות וחשבוניות
- **רישום מכירות** - ממשק פשוט וידידותי
- **חשבוניות PDF** - יצירה אוטומטית של חשבוניות
- **מעקב לקוחות** - CRM מובנה
- **תשלומים** - מעקב שיטות תשלום

### 📊 דוחות ומעקב
- **דוחות מלאי** - סטטיסטיקות מפורטות
- **דוחות מכירות** - ניתוח ביצועים
- **ייצוא Excel/CSV** - ייצוא נתונים
- **דוחות יומיים** - שליחה אוטומטית במייל

### 🔒 אבטחה וגיבויים
- **מערכת משתמשים** - הרשאות מתקדמות
- **גיבויים אוטומטיים** - שמירה יומית
- **שחזור נתונים** - שחזור מהיר מגיבויים
- **אבטחת נתונים** - הצפנה והגנה

## 🚀 התקנה מהירה

### Windows
```bash
# הורדה והתקנה אוטומטית
git clone https://github.com/shaharprod/inventory.git
cd inventory
install.bat
```

### Linux/Mac
```bash
# הורדה והתקנה אוטומטית
git clone https://github.com/shaharprod/inventory.git
cd inventory
chmod +x install.sh
./install.sh
```

### Docker
```bash
# התקנה עם Docker
git clone https://github.com/shaharprod/inventory.git
cd inventory
docker-compose up -d
```

## 📋 דרישות מערכת

- **Python 3.10+** (מומלץ 3.11)
- **RAM**: 4GB (מומלץ 8GB)
- **אחסון**: 2GB פנוי
- **דפדפן מודרני** (Chrome, Firefox, Edge)

## 🛠️ התקנה ידנית

### 1. הורדת הפרויקט
```bash
git clone https://github.com/shaharprod/inventory.git
cd inventory
```

### 2. יצירת סביבה וירטואלית
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. התקנת חבילות
```bash
pip install -r requirements.txt
```

### 4. הגדרת מסד נתונים
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. הפעלת השרת
```bash
python manage.py runserver
```

**פתח דפדפן:** http://127.0.0.1:8000

## 📁 מבנה הפרויקט

```
inventory/
├── inventory/              # אפליקציית Django
│   ├── models.py          # מודלי מסד הנתונים
│   ├── views.py           # לוגיקת העסק
│   ├── forms.py           # טפסים
│   └── templates/         # תבניות HTML
├── inventory_project/      # הגדרות Django
├── media/                  # קבצי מדיה
├── static/                 # קבצים סטטיים
├── backups/                # גיבויים
├── requirements.txt        # חבילות Python
├── install.bat            # התקנה Windows
├── install.sh             # התקנה Linux/Mac
├── Dockerfile             # Docker
└── docker-compose.yml     # Docker Compose
```

## 🎯 שימוש ראשוני

### 1. התחברות למערכת
- פתח: http://127.0.0.1:8000
- התחבר כמנהל: http://127.0.0.1:8000/admin

### 2. הגדרות ראשוניות
- היכנס ל-**הגדרות מערכת** (Settings)
- הגדר שם החברה ופרטי יצירת קשר
- הגדר הגדרות דוחות ומייל

### 3. הוספת נתונים
- **קטגוריות** - הוסף קטגוריות מוצרים
- **ספקים** - הוסף ספקים
- **מוצרים** - הוסף מוצרים עם תמונות
- **לקוחות** - הוסף לקוחות

### 4. התחלת עבודה
- **מכירות** - רשום מכירות חדשות
- **מלאי** - עקוב אחר רמות מלאי
- **דוחות** - צפה בדוחות וסטטיסטיקות

## 🔧 הגדרות מתקדמות

### הגדרות ייצור
```python
# ב-settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = 'your-secret-key'
```

### גיבויים אוטומטיים
```bash
# Windows Task Scheduler
python manage.py backup_database

# Linux Cron
0 2 * * * /path/to/python /path/to/manage.py backup_database
```

### שרת ייצור
```bash
# התקנת Gunicorn
pip install gunicorn

# הפעלת שרת ייצור
gunicorn inventory_project.wsgi:application --bind 0.0.0.0:8000
```

## 🚨 פתרון בעיות

### שגיאות נפוצות:
- **"ModuleNotFoundError"** - ודא שהסביבה הוירטואלית פעילה
- **"Database is locked"** - עצור את השרת והפעל `python manage.py migrate`
- **"Port already in use"** - שנה פורט: `python manage.py runserver 8001`

### לוגים וניפוי שגיאות:
```bash
# הפעלה עם לוגים מפורטים
python manage.py runserver --verbosity=2

# בדיקת שגיאות
python manage.py check --deploy
```

## 📚 תיעוד נוסף

- **[מדריך התקנה מפורט](SETUP_INSTALL.md)** - הוראות התקנה מפורטות
- **[מדריך משתמש](docs/USER_GUIDE.md)** - הוראות שימוש
- **[API Documentation](docs/API.md)** - תיעוד API
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - פתרון בעיות

## 🤝 תרומה לפרויקט

1. Fork את הפרויקט
2. צור branch חדש (`git checkout -b feature/amazing-feature`)
3. Commit השינויים (`git commit -m 'Add amazing feature'`)
4. Push ל-branch (`git push origin feature/amazing-feature`)
5. פתח Pull Request

## 📄 רישיון

פרויקט זה מופץ תחת רישיון MIT. ראה קובץ [LICENSE](LICENSE) לפרטים.

## 📞 תמיכה

- **GitHub Issues** - דיווח על באגים ובקשות תכונות
- **Email** - support@example.com
- **Documentation** - [docs/](docs/)

## 🏆 תכונות עתידיות

- [ ] אפליקציה למובייל
- [ ] אינטגרציה עם מערכות POS
- [ ] בינה מלאכותית לחיזוי מלאי
- [ ] API מלא לרובוטים
- [ ] מערכת הזמנות אוטומטית

---

**נבנה עם ❤️ בישראל**

*מערכת ניהול מלאי מתקדמת לבתי עסק קטנים ובינוניים*
