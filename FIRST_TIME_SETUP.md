# 🎯 הפעלה ראשונית - מדריך צעד אחר צעד

## 👋 ברוך הבא למערכת ניהול המלאי!

מדריך זה ילווה אותך בהפעלה ראשונית של המערכת.

---

## 📋 דרישות מקדימות

### 1️⃣ **Windows 10/11**
- מערכת הפעלה מעודכנת
- מנהל (Administrator) גישה

### 2️⃣ **Docker Desktop**
```powershell
# התקנה אוטומטית:
winget install Docker.DockerDesktop

# או הורד ידנית מ:
# https://www.docker.com/products/docker-desktop/
```

### 3️⃣ **Git (אופציונלי)**
```powershell
winget install Git.Git
```

---

## 🚀 הפעלה ראשונית - 5 דקות

### שלב 1: הורד את המערכת
```powershell
# אם יש Git:
git clone <repository-url>
cd inventory

# או:
# פתח את התיקייה שהורדת
```

### שלב 2: פתח PowerShell בתיקייה
```
לחץ ימני בתיקייה -> Open in Terminal
או:
Shift + לחץ ימני -> פתח חלון PowerShell כאן
```

### שלב 3: הפעל את המערכת
```powershell
# הפעלה אוטומטית מלאה:
.\docker-quick-start.ps1
```

**זהו!** המערכת תעלה אוטומטית.

### שלב 4: פתח דפדפן
```
http://localhost:8000
```

---

## 👤 יצירת משתמש ראשון

### דרך 1: ממשק ניהול Django
1. גש ל: **http://localhost:8000/admin/**
2. ליצור משתמש ראשי, הרץ בטרמינל:
```powershell
docker-compose exec inventory python manage.py createsuperuser
```
3. עקוב אחרי ההוראות

### דרך 2: מהקונסול
```powershell
# כניסה לקונטיינר:
docker-compose exec inventory sh

# יצירת superuser:
python manage.py createsuperuser

# הזן:
# - שם משתמש
# - אימייל (אופציונלי)
# - סיסמה (פעמיים)

# יציאה:
exit
```

---

## 📊 נתוני דמו (אופציונלי)

רוצה לראות איך המערכת נראית עם נתונים?

```powershell
# יצירת נתוני דמו:
docker-compose exec inventory python create_demo_data.py
```

זה יוסיף:
- ✅ 50+ מוצרים לדוגמה
- ✅ 20 לקוחות
- ✅ 10 ספקים
- ✅ קטגוריות
- ✅ מכירות דמו
- ✅ התראות

**הערה:** זה למטרת הדגמה בלבד!

---

## ⚙️ הגדרות ראשוניות

### 1. הגדרת Email (לדוחות)
1. גש ל: **http://localhost:8000/settings/**
2. מלא:
   - **Email Host:** smtp.gmail.com
   - **Port:** 587
   - **Use TLS:** ✅ כן
   - **Username:** your-email@gmail.com
   - **Password:** your-16-char-app-password

**חשוב:** צריך App Password של Gmail, לא הסיסמה הרגילה!

#### איך ליצור Gmail App Password:
1. גש ל: https://myaccount.google.com/security
2. **2-Step Verification** → הפעל (אם לא מופעל)
3. **App passwords** → צור חדש
4. בחר **Mail** ו-**Windows Computer**
5. העתק את הסיסמה בת 16 תווים
6. השתמש בה במערכת

### 2. בדיקת Email
לחץ על **"Test Email Settings"** בעמוד ההגדרות.

### 3. הגדרת דוח יומי (אופציונלי)
1. גש להגדרות
2. סמן **"Enable Daily Report"**
3. בחר שעה (למשל: 19:30)
4. הזן אימייל למשלוח
5. שמור

---

## 🎨 התאמה אישית

### שינוי שם העסק
ערוך את `inventory_project/settings.py`:
```python
SITE_NAME = "שם העסק שלך"
```

### שינוי Logo
החלף את הקובץ:
```
media/logo.png
```

### ערכת צבעים
ערוך:
```
inventory/static/inventory/css/dark-theme.css
```

---

## 🔐 אבטחה

### המלצות חשובות:
1. **שנה SECRET_KEY** ב-`settings.py`
2. **הגדר ALLOWED_HOSTS** נכון
3. **DEBUG=False** לפרודקשן
4. **השתמש בסיסמאות חזקות**
5. **עשה גיבויים קבועים**

### יצירת SECRET_KEY חדש:
```powershell
docker-compose exec inventory python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📍 גישה מרשת מקומית

רוצה לגשת למערכת מהנייד או ממחשב אחר?

### שלב 1: מצא IP
```powershell
ipconfig | findstr IPv4
# דוגמה: 192.168.1.100
```

### שלב 2: פתח פורט
```powershell
# הרץ כמנהל (Run as Administrator):
netsh advfirewall firewall add rule name="Django Inventory" dir=in action=allow protocol=TCP localport=8000
```

### שלב 3: גש מכל מכשיר
```
http://192.168.1.100:8000
```

---

## 💾 גיבוי ראשון

מומלץ לעשות גיבוי מיד!

### מהדשבורד:
1. גש ל: **http://localhost:8000/dashboard/**
2. לחץ **"Create Backup Now"**

### מהטרמינל:
```powershell
docker-compose exec inventory python manage.py backup_data
```

הגיבוי נשמר ב: `backups/`

---

## 🎓 למידה ושימוש

### מדריכים:
1. **DOCKER_QUICK_GUIDE.md** - מדריך מהיר
2. **docs/USER_MANUAL.md** - מדריך משתמש מלא
3. **SYSTEM_SUMMARY.md** - סיכום המערכת

### תהליך עבודה מומלץ:
1. ✅ הוסף קטגוריות
2. ✅ הוסף ספקים
3. ✅ הוסף מוצרים
4. ✅ הוסף לקוחות
5. ✅ צור מכירה ראשונה
6. ✅ צפה בדוחות

---

## 🐛 פתרון בעיות

### Docker לא פועל?
```powershell
# פתח Docker Desktop או:
Start-Service Docker
```

### הפורט 8000 תפוס?
```powershell
# בדוק מי משתמש בפורט:
netstat -ano | findstr :8000

# עצור את התהליך או שנה פורט ב:
# docker-compose.yml (ports: "8001:8000")
```

### המערכת לא עולה?
```powershell
# בדוק לוגים:
docker-compose logs --tail=100 inventory

# נסה לבנות מחדש:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### שכחת סיסמה?
```powershell
# איפוס סיסמת משתמש:
docker-compose exec inventory python manage.py changepassword username
```

---

## 📊 בדיקת תקינות

### ✅ רשימת בדיקה:
- [ ] Docker Desktop פועל
- [ ] המערכת עלתה: `docker-compose ps`
- [ ] נכנסתי ל: http://localhost:8000
- [ ] יצרתי superuser
- [ ] נכנסתי לאדמין: /admin/
- [ ] הגדרתי Email (אם צריך)
- [ ] יצרתי גיבוי ראשון
- [ ] הוספתי מוצר ראשון
- [ ] יצרתי מכירה ראשונה
- [ ] צפיתי בדוחות

---

## 📞 עזרה נוספת

### קבלת תמיכה:
- 📚 קרא את המדריכים המפורטים
- 🔍 בדוק את הלוגים
- 💬 צור issue ב-GitHub
- 📧 שלח מייל לתמיכה

### משאבים:
- [Django Documentation](https://docs.djangoproject.com)
- [Docker Documentation](https://docs.docker.com)
- [Bootstrap Documentation](https://getbootstrap.com)

---

## 🎯 הצעדים הבאים

אחרי ההפעלה הראשונית:

1. **למד את המערכת** - עבור על כל העמודים
2. **התאם אישית** - שנה צבעים, לוגו, שם
3. **הוסף נתונים** - התחל להזין את המידע שלך
4. **הגדר גיבוי אוטומטי** - הפעל גיבוי יומי
5. **הגדר דוחות** - הפעל דוחות במייל
6. **אמן צוות** - הדרך את המשתמשים
7. **עקוב** - בדוק לוגים ודוחות

---

## 🎉 סיימת!

**ברכות! המערכת שלך מוכנה לשימוש! 🚀**

### מידע מהיר:
- 🌐 **כתובת:** http://localhost:8000
- 👤 **אדמין:** http://localhost:8000/admin/
- ⚙️ **הגדרות:** http://localhost:8000/settings/
- 📊 **דוחות:** http://localhost:8000/reports/

### פקודות שימושיות:
```powershell
# הפעלה:
docker-compose up -d

# עצירה:
docker-compose stop

# לוגים:
docker-compose logs -f

# סטטוס:
docker-compose ps
```

---

**📅 מוכן לעבוד! בהצלחה! 🎊**


