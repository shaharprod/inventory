# 🐳 מדריך Docker למערכת ניהול מלאי

## 📦 מה זה עושה?

הקונטיינר של Docker שומר את המערכת **בדיוק כפי שהיא** - עם כל הקוד, התלויות והגדרות.
זה כמו "תמונה" של התוכנה שאפשר להריץ על כל מחשב עם Docker.

---

## 🚀 הרצה מהירה

### 1. התקן Docker Desktop
- הורד מ: https://www.docker.com/products/docker-desktop
- התקן והפעל את Docker Desktop
- **חשוב:** וודא ש-Docker Desktop פעיל לפני המשך!

### 2. בנה והרץ את הקונטיינר

#### אופציה 1: שימוש בסקריפטים (קל ומהיר!)

**Windows:**
```powershell
# הפעלה
.\docker-start.ps1

# עצירה
.\docker-stop.ps1
```

הסקריפט יבדוק הכל אוטומטית ויציע לפתוח את הדפדפן!

#### אופציה 2: פקודות ידניות

```bash
# בנה את הקונטיינר (פעם ראשונה בלבד)
docker-compose build

# הרץ את המערכת בפס רקע
docker-compose up -d

# או הרץ עם לוגים (בלי פס רקע)
docker-compose up
```

### 3. גש למערכת
פתח בדפדפן: http://localhost:8000

**אם לא עובד, נסה:**
- http://127.0.0.1:8000
- בדוק שהפורט 8000 לא תפוס: `netstat -ano | findstr :8000`

---

## 📝 פקודות שימושיות

### הפעלה ועצירה
```bash
# הפעל את המערכת
docker-compose up -d

# עצור את המערכת
docker-compose down

# הפעל מחדש
docker-compose restart

# צפה בלוגים
docker-compose logs -f
```

### ניהול
```bash
# צור משתמש admin
docker-compose exec inventory python manage.py createsuperuser

# הרץ גיבוי
docker-compose exec inventory python manage.py backup_database

# הצג סטטוס
docker-compose ps
```

### עדכון ובנייה מחדש
```bash
# בנה מחדש אחרי שינויים בקוד
docker-compose build --no-cache

# הפעל מחדש עם הגרסה החדשה
docker-compose up -d --build
```

---

## 📁 מבנה הקבצים

```
inventory/
├── Dockerfile              # הגדרת הקונטיינר
├── docker-compose.yml      # הגדרות הרצה
├── .dockerignore          # קבצים שלא להעתיק
├── db.sqlite3             # בסיס נתונים (נשמר מחוץ לקונטיינר)
├── media/                 # תמונות וקבצים (נשמר מחוץ לקונטיינר)
├── logs/                  # לוגים (נשמר מחוץ לקונטיינר)
└── backups/               # גיבויים (נשמר מחוץ לקונטיינר)
```

---

## 🔒 נתונים נשמרים

הקבצים הבאים **נשמרים מחוץ לקונטיינר** (volumes):
- ✅ `db.sqlite3` - בסיס הנתונים
- ✅ `media/` - תמונות מוצרים וברקודים
- ✅ `logs/` - קבצי לוג
- ✅ `backups/` - גיבויים

**כלומר:** גם אם תמחק את הקונטיינר, הנתונים נשמרים!

---

## 🎯 יתרונות

### ✅ ניידות
- הרץ את התוכנה על כל מחשב עם Docker
- אותה סביבה בכל מקום

### ✅ בידוד
- התוכנה רצה בסביבה מבודדת
- לא משפיע על המחשב

### ✅ גיבוי פשוט
```bash
# גבה את כל המערכת
docker save inventory_system:latest -o inventory_backup.tar

# שחזר מגיבוי
docker load -i inventory_backup.tar
```

---

## 📤 ייצוא והעברה למחשב אחר

### שלב 1: ייצוא הקונטיינר
```bash
# ייצא את הקונטיינר לקובץ
docker save inventory_system:latest -o inventory_image.tar

# או דחוס:
docker save inventory_system:latest | gzip > inventory_image.tar.gz
```

### שלב 2: העתק קבצים
העבר למחשב החדש:
1. `inventory_image.tar.gz` - התמונה
2. `docker-compose.yml` - קובץ ההגדרות
3. `db.sqlite3` - בסיס הנתונים
4. `media/` - תמונות
5. `backups/` - גיבויים (אופציונלי)

### שלב 3: טען במחשב החדש
```bash
# טען את התמונה
docker load -i inventory_image.tar.gz

# הרץ
docker-compose up -d
```

---

## 🆘 פתרון בעיות

### הקונטיינר לא עולה?
```bash
# בדוק לוגים
docker-compose logs

# בדוק סטטוס Docker
docker ps -a
```

### פורט תפוס?
```bash
# שנה פורט ב-docker-compose.yml
ports:
  - "8001:8000"  # במקום 8000
```

### רוצה למחוק הכל והתחלה מחדש?
```bash
# מחק קונטיינר
docker-compose down

# מחק גם volumes (זהירות! מוחק נתונים!)
docker-compose down -v

# בנה מחדש
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 גרסה זו (Development)

⚠️ **שים לב:** זו גרסת פיתוח עם:
- `DEBUG=True`
- SQLite
- `runserver` של Django

✅ **מתאים ל:**
- שימוש מקומי
- פיתוח
- בדיקות

❌ **לא מתאים ל:**
- פרודקשן באינטרנט
- רשת מקומית גדולה

---

## 🔄 עדכונים עתידיים

כשתהיה גרסת Production מוכנה:
```bash
# מחק את הקונטיינר הישן
docker-compose down

# בנה גרסה חדשה
docker-compose build --no-cache

# הפעל
docker-compose up -d
```

---

## 💡 טיפים

1. **גיבוי אוטומטי:** הקונטיינר כולל את מערכת הגיבוי המובנית
2. **נתונים בטוחים:** כל הנתונים ב-volumes מחוץ לקונטיינר
3. **קל לשחזר:** פשוט תעתיק את הקבצים למחשב אחר

---

**✅ הקונטיינר מוכן! המערכת גבויה כפי שהיא.**

