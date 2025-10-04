# 🌐 מדריך הכנה לרשת מקומית (LAN)
## זמן משוער: 30 דקות

---

## 📋 מה צריך לעשות?

כדי שהמערכת תעבוד על **רשת מקומית** (LAN) עם מספר משתמשים, צריך לתקן **4 דברים בלבד**:

---

## 🔧 שינוי 1: DEBUG=False (5 דקות)

### למה זה חשוב?
- `DEBUG=True` חושף מידע רגיש (סיסמאות, קוד, מסלולים)
- ברשת מקומית, משתמשים אחרים יכולים לראות את זה!

### איך לתקן?

**קובץ:** `inventory_project/settings.py`

**שורה 23 בערך:**
```python
# לפני:
DEBUG = True

# אחרי:
DEBUG = False
```

### ⚠️ חשוב!
אחרי השינוי הזה, צריך להריץ:
```bash
python manage.py collectstatic --noinput
```

---

## 🔧 שינוי 2: ALLOWED_HOSTS (5 דקות)

### למה זה חשוב?
- Django חוסם גישה מכתובות IP לא מורשות
- צריך להוסיף את כתובת ה-IP של השרת ברשת המקומית

### איך למצוא את ה-IP שלך?

**Windows:**
```powershell
ipconfig
```
חפש את השורה: `IPv4 Address` (למשל: `192.168.1.100`)

**Linux/Mac:**
```bash
ifconfig
# או
ip addr show
```

### איך לתקן?

**קובץ:** `inventory_project/settings.py`

**שורה 28 בערך:**
```python
# לפני:
ALLOWED_HOSTS = []

# אחרי (דוגמה):
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.100',  # ה-IP שלך ברשת
    '192.168.1.*',    # או כל המחשבים ברשת (פחות בטוח)
]
```

### 💡 טיפ:
אם ה-IP משתנה (DHCP), אפשר:
1. להגדיר IP סטטי לשרת
2. או להשתמש ב-`'*'` (לא מומלץ!)

---

## 🔧 שינוי 3: SECRET_KEY חזק (10 דקות)

### למה זה חשוב?
- SECRET_KEY משמש להצפנת סשנים, cookies, CSRF tokens
- המפתח הנוכחי קצר וחלש

### איך ליצור מפתח חזק?

**אופציה 1 - Python:**
```python
# הרץ בטרמינל Python
import secrets
print(secrets.token_urlsafe(50))
```

**אופציה 2 - אונליין:**
- גוגל: "django secret key generator"
- או: https://djecrety.ir/

### איך לתקן?

**קובץ:** `inventory_project/settings.py`

**שורה 23 בערך:**
```python
# לפני:
SECRET_KEY = 'django-insecure-...'

# אחרי (דוגמה):
SECRET_KEY = 'Xt7hR_9mK2pQ8vL4nB6wZ3fY1sC5dE0jG7iH2aF4kT9uN8mO1qP6rV3xW5zA7bY2c'
```

### 🔒 חשוב!
- **אל תשתף** את המפתח הזה עם אף אחד!
- אל תעלה אותו ל-Git
- אם הוא דלף - צור מפתח חדש!

---

## 🔧 שינוי 4: הוסף קובץ .env (10 דקות)

### למה זה חשוב?
- הפרדה בין קוד להגדרות
- אפשר לשנות הגדרות בלי לגעת בקוד
- יותר בטוח

### איך לעשות?

#### שלב 1: התקן python-decouple
```bash
pip install python-decouple
echo python-decouple==3.8 >> requirements.txt
```

#### שלב 2: צור קובץ .env
**קובץ חדש:** `.env` (בתיקיית הפרויקט)

```env
# הגדרות אבטחה
DEBUG=False
SECRET_KEY=Xt7hR_9mK2pQ8vL4nB6wZ3fY1sC5dE0jG7iH2aF4kT9uN8mO1qP6rV3xW5zA7bY2c
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100

# בסיס נתונים
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### שלב 3: עדכן settings.py
**קובץ:** `inventory_project/settings.py`

**בתחילת הקובץ (שורה 12 בערך):**
```python
from pathlib import Path
from decouple import config, Csv  # 👈 הוסף את זה

# ...

# שנה את השורות הבאות:
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

### ⚠️ חשוב!
הוסף לקובץ `.gitignore`:
```
.env
```

---

## ✅ סיימת! איך לבדוק?

### 1. הרץ את השרת ברשת
```bash
# במקום localhost:
python manage.py runserver 0.0.0.0:8000
```

### 2. גש ממחשב אחר ברשת
פתח בדפדפן:
```
http://192.168.1.100:8000
```
(החלף ב-IP שלך)

### 3. בדוק שאין שגיאות
- הדף צריך להיטען בלי שגיאות
- אין הודעות DEBUG
- אין חשיפת מידע רגיש

---

## 🔒 אבטחה נוספת (אופציונלי)

### הוסף מערכת התחברות בסיסית

#### שלב 1: הוסף login required
**קובץ:** `inventory/views.py`

בתחילת כל view:
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # ...
```

#### שלב 2: הגדר URL להתחברות
**קובץ:** `inventory_project/settings.py`

```python
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'
```

#### שלב 3: צור משתמשים
```bash
python manage.py createsuperuser
```

---

## 📊 השוואה: לפני ואחרי

| תכונה | לפני (מקומי) | אחרי (רשת) |
|-------|-------------|-----------|
| **DEBUG** | ✅ True | ❌ False |
| **ALLOWED_HOSTS** | ❌ ריק | ✅ עם IPs |
| **SECRET_KEY** | ⚠️ חלש | ✅ חזק |
| **גישה** | רק מחשב זה | כל הרשת |
| **אבטחה** | בסיסית | טובה |
| **משתמשים** | 1 | מספר |

---

## ⚡ טיפים חשובים

### 1. גיבוי לפני השינויים!
```bash
# גבה את כל התיקייה
cp -r inventory inventory_backup
```

### 2. בדוק אחד אחד
אחרי כל שינוי, הרץ:
```bash
python manage.py check
```

### 3. תיעוד השינויים
כתוב את כל ה-IPs שהוספת ל-ALLOWED_HOSTS

### 4. בעיות נפוצות

**בעיה:** הדף לא נטען אחרי DEBUG=False
**פתרון:** הרץ `collectstatic`

**בעיה:** "Invalid HTTP_HOST header"
**פתרון:** הוסף את ה-IP ל-ALLOWED_HOSTS

**בעיה:** CSS לא עובד
**פתרון:** וודא ש-STATIC_URL מוגדר ו-collectstatic רץ

---

## 🎯 סיכום: מה עשינו?

✅ **DEBUG=False** - אין חשיפת מידע רגיש
✅ **ALLOWED_HOSTS** - רק משתמשים מורשים
✅ **SECRET_KEY חזק** - הצפנה חזקה
✅ **קובץ .env** - ניהול הגדרות נוח ובטוח

**זמן כולל:** ~30 דקות
**רמת קושי:** בינוני
**תוצאה:** מערכת מאובטחת לרשת מקומית! 🎉

---

## 🚨 מה עדיין חסר (לענן)?

אם בעתיד תרצה לעלות לאינטרנט, תצטרך גם:
- ✅ HTTPS (SSL/TLS)
- ✅ PostgreSQL (במקום SQLite)
- ✅ Gunicorn + Nginx
- ✅ SESSION_COOKIE_SECURE=True
- ✅ CSRF_COOKIE_SECURE=True
- ✅ SECURE_HSTS_SECONDS=31536000

**אבל לרשת מקומית - זה מספיק!** ✅

---

## 💰 מחיר מומלץ

עם השינויים האלה, אפשר למכור ב:
- **רשת קטנה (2-5 משתמשים):** 2,000-3,000 ₪
- **רשת בינונית (5-10 משתמשים):** 3,000-5,000 ₪
- **כולל התקנה ותמיכה:** +1,000 ₪

---

**✅ בהצלחה! השינויים פשוטים והמערכת תהיה מאובטחת לרשת מקומית.**

