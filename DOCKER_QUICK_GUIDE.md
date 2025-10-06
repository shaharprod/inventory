# 🐳 מדריך מהיר - Docker

## 📦 מה יש כאן?

תמונת Docker מלאה של **מערכת ניהול מלאי וCRM** - מוכנה להפעלה מיידית!

---

## ⚡ התחלה מהירה (3 שלבים)

### 1️⃣ **הורד והתקן Docker**
```powershell
winget install Docker.DockerDesktop
```

### 2️⃣ **הפעל את המערכת**
```powershell
.\docker-quick-start.ps1
```

### 3️⃣ **גש למערכת**
פתח דפדפן: **http://localhost:8000**

**🎉 זהו! המערכת פועלת!**

---

## 📋 פקודות בסיסיות

```powershell
# הפעלה
docker-compose up -d

# עצירה
docker-compose stop

# לוגים
docker-compose logs -f

# סטטוס
docker-compose ps

# כניסה לקונטיינר
docker-compose exec inventory sh
```

---

## 🎯 מה כלול במערכת?

### ✅ **תכונות עיקריות:**
- 📦 ניהול מלאי מתקדם
- 🛒 מערכת מכירות
- 👥 ניהול לקוחות (CRM)
- 📊 דוחות ותרשימים
- 📧 שליחת מיילים אוטומטית
- 📈 ייצוא ל-Excel, CSV, PDF
- 🔐 מערכת משתמשים
- 📍 ניהול מיקומים
- 🏷️ ברקודים
- 💾 גיבוי ושחזור

### 🛠️ **טכנולוגיות:**
- Python 3.10
- Django 5.2+
- SQLite (מובנה)
- Bootstrap 5
- תמיכה מלאה בעברית

---

## 📂 קבצים חשובים

| קובץ | תיאור |
|------|-------|
| `docker-quick-start.ps1` | 🚀 הפעלה מהירה |
| `docker-build.ps1` | 🏗️ בניית תמונה |
| `DOCKER_DEPLOYMENT.md` | 📚 מדריך מלא |
| `DOCKER_README.md` | 📖 תיעוד מפורט |
| `docker-compose.yml` | ⚙️ הגדרות |
| `env.example` | 🔧 דוגמת הגדרות |

---

## 🌐 גישה מרשת מקומית

### שלב 1: מצא את ה-IP שלך
```powershell
ipconfig | findstr IPv4
```

### שלב 2: פתח פורט בחומת אש
```powershell
netsh advfirewall firewall add rule name="Django" dir=in action=allow protocol=TCP localport=8000
```

### שלב 3: גש מכל מכשיר
```
http://<YOUR-IP>:8000
```

---

## 💾 גיבוי ושחזור

### דרך הממשק:
1. גש ל-Dashboard
2. לחץ על "Create Backup Now"
3. לחץ על "Restore Backup" לשחזור

### דרך Terminal:
```powershell
# גיבוי
docker-compose exec inventory python manage.py backup_data

# רשימת גיבויים
docker-compose exec inventory python manage.py list_backups

# שחזור
docker-compose exec inventory python manage.py restore_data <backup_name>
```

---

## 🔧 פתרון בעיות

### הקונטיינר לא עולה?
```powershell
docker-compose logs --tail=100
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### הפורט תפוס?
```powershell
netstat -ano | findstr :8000
# עצור תהליך או שנה פורט ב-docker-compose.yml
```

### Docker לא פועל?
```powershell
# פתח Docker Desktop או הפעל:
Start-Service Docker
```

---

## 📊 מידע טכני

| פרט | ערך |
|-----|-----|
| **גודל תמונה** | ~710MB |
| **זמן בניה** | ~45 שניות |
| **פורט** | 8000 |
| **Python** | 3.10 |
| **Django** | 5.2+ |
| **מסד נתונים** | SQLite |

---

## 🎓 למידע נוסף

- 📚 [מדריך מלא](DOCKER_DEPLOYMENT.md) - כל הפקודות והתכונות
- 📖 [תיעוד](DOCKER_README.md) - מידע מפורט
- 🚀 [התחלה מהירה](QUICK_START.md) - בלי Docker
- 📘 [מדריך משתמש](docs/USER_MANUAL.md) - איך להשתמש במערכת

---

## 📦 שיתוף התמונה

### שמירה לקובץ:
```powershell
docker save inventory_management:latest -o inventory_image.tar
```

### טעינה במכשיר אחר:
```powershell
docker load -i inventory_image.tar
docker-compose up -d
```

**גודל קובץ: ~164MB** (דחוס)

---

## 🎉 סיכום

### ✅ **יתרונות Docker:**
- 📦 הכל בקופסה אחת
- 🚀 הפעלה מהירה
- 🔄 נייד בין מחשבים
- 🛡️ מבודד ובטוח
- 🔧 קל לניהול
- 📊 ניטור פשוט

### 🎯 **למי זה מתאים?**
- חנויות ובתי עסק
- מחסנים
- חברות סחר
- סטארטאפים
- עסקים קטנים ובינוניים

---

## 📞 תמיכה

**שאלות? בעיות?**
- צור issue ב-GitHub
- קרא את המדריכים המפורטים
- בדוק את הלוגים: `docker-compose logs -f`

---

**🎊 בהצלחה עם המערכת החדשה! 🚀**


