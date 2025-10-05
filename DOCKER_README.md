# 🐳 Docker - מערכת ניהול מלאי

## 📖 סקירה כללית

מערכת מלאה לניהול מלאי, מכירות ולקוחות, ארוזה בתמונת Docker מוכנה לשימוש.

### ✨ מה כלול בתמונה?
- ✅ Django 5.2+ Framework
- ✅ Python 3.10 סביבת ריצה
- ✅ SQLite מסד נתונים
- ✅ Pillow לעיבוד תמונות
- ✅ ReportLab ליצירת PDF
- ✅ OpenPyXL לקבצי Excel
- ✅ מערכת Email מלאה
- ✅ גיבוי ושחזור אוטומטי
- ✅ לוגים מתקדמים
- ✅ תמיכה בעברית

---

## 🚀 התחלה מהירה

### שלב 1: התקן Docker
```powershell
# Windows
winget install Docker.DockerDesktop
```

### שלב 2: הפעל את המערכת
```powershell
# הפעלה מהירה
.\docker-quick-start.ps1
```

**זהו! המערכת פועלת ב: http://localhost:8000**

---

## 📦 מבנה הפרויקט

```
inventory/
├── 🐳 Dockerfile                    # הגדרת תמונת Docker
├── 🐳 docker-compose.yml            # תצורת שירותים
├── 📄 .dockerignore                 # קבצים להתעלם
├── ⚙️  env.example                   # דוגמה להגדרות
├── 📝 DOCKER_DEPLOYMENT.md          # מדריך מלא
├── 🚀 docker-quick-start.ps1        # הפעלה מהירה
├── 🏗️  docker-build.ps1              # בניית תמונה
├── 📊 manage.py                     # Django ניהול
├── 📋 requirements.txt              # תלויות Python
├── 🗄️  inventory/                    # אפליקציית Django
├── ⚙️  inventory_project/           # הגדרות פרויקט
├── 📁 media/                        # קבצים שהועלו
├── 📁 static/                       # קבצים סטטיים
├── 📁 logs/                         # קבצי לוג
└── 📁 backups/                      # גיבויים
```

---

## 🔧 פקודות בסיסיות

### הפעלה ועצירה
```bash
# הפעלה
docker-compose up -d

# עצירה
docker-compose stop

# עצירה והסרה
docker-compose down
```

### צפייה בלוגים
```bash
# כל הלוגים
docker-compose logs -f

# 100 שורות אחרונות
docker-compose logs --tail=100

# רק שגיאות
docker-compose logs | grep ERROR
```

### בדיקת סטטוס
```bash
# סטטוס קונטיינרים
docker-compose ps

# שימוש במשאבים
docker stats inventory_system
```

---

## 🛠️ פקודות מתקדמות

### כניסה לקונטיינר
```bash
# כניסה לשורת פקודה
docker-compose exec inventory sh

# הרצת Django shell
docker-compose exec inventory python manage.py shell
```

### ניהול נתונים
```bash
# הרצת migrations
docker-compose exec inventory python manage.py migrate

# יצירת superuser
docker-compose exec inventory python manage.py createsuperuser

# יצירת נתוני דמו
docker-compose exec inventory python create_demo_data.py
```

### גיבוי ושחזור
```bash
# יצירת גיבוי
docker-compose exec inventory python manage.py backup_data

# רשימת גיבויים
docker-compose exec inventory python manage.py list_backups

# שחזור גיבוי
docker-compose exec inventory python manage.py restore_data <backup_name>
```

---

## 📊 Volumes - שמירת נתונים

הנתונים נשמרים ב-Docker Volumes ולא יאבדו בעת הפסקת הקונטיינר:

| Volume | תיאור | נתיב |
|--------|-------|------|
| `db_data` | מסד נתונים SQLite | `/app/db.sqlite3` |
| `media_data` | תמונות ובר-קודים | `/app/media/` |
| `logs_data` | קבצי לוג | `/app/logs/` |
| `backups_data` | גיבויים | `/app/backups/` |
| `static_data` | קבצים סטטיים | `/app/static/` |

### ניהול Volumes
```bash
# רשימת volumes
docker volume ls

# מידע על volume
docker volume inspect inventory_db_data

# גיבוי volume
docker run --rm -v inventory_db_data:/data -v $(pwd):/backup alpine tar czf /backup/db_backup.tar.gz /data

# שחזור volume
docker run --rm -v inventory_db_data:/data -v $(pwd):/backup alpine tar xzf /backup/db_backup.tar.gz -C /
```

---

## 🌐 גישה למערכת

### רשת מקומית (LAN)
1. **מצא את ה-IP המקומי שלך:**
   ```powershell
   ipconfig | findstr IPv4
   ```

2. **פתח פורט בחומת אש:**
   ```powershell
   netsh advfirewall firewall add rule name="Django" dir=in action=allow protocol=TCP localport=8000
   ```

3. **גש מכל מכשיר ברשת:**
   ```
   http://<YOUR-IP>:8000
   ```

### אינטרנט (דרך ngrok)
```bash
# התקן ngrok
winget install ngrok

# הפעל tunnel
ngrok http 8000

# השתמש ב-URL שניתן
```

---

## ⚙️ הגדרות מתקדמות

### משתני סביבה

צור קובץ `.env`:
```bash
cp env.example .env
```

ערוך את ההגדרות:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

טען מחדש:
```bash
docker-compose down
docker-compose up -d
```

### הוספת Nginx
הסר # מהשירות nginx ב-`docker-compose.yml` והפעל:
```bash
docker-compose up -d nginx
```

---

## 🔐 אבטחה

### המלצות לפרודקשן:
- ✅ `DEBUG=False`
- ✅ `SECRET_KEY` ייחודי וחזק
- ✅ `ALLOWED_HOSTS` מוגדר נכון
- ✅ שימוש ב-HTTPS (SSL/TLS)
- ✅ גיבויים אוטומטיים
- ✅ עדכונים שוטפים
- ✅ מעקב אחר לוגים

### יצירת SECRET_KEY חדש:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📈 ביצועים וניטור

### מעקב אחר שימוש במשאבים
```bash
# בזמן אמת
docker stats inventory_system

# שימוש בדיסק
docker system df
```

### אופטימיזציה
```yaml
# הוסף ל-docker-compose.yml:
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
    reservations:
      cpus: '1'
      memory: 512M
```

### ניקוי מערכת
```bash
# קונטיינרים ישנים
docker container prune -f

# תמונות ישנות
docker image prune -a -f

# volumes לא בשימוש
docker volume prune -f

# ניקוי כולל
docker system prune -a --volumes -f
```

---

## 🐛 פתרון בעיות

### הקונטיינר לא עולה
```bash
# בדוק לוגים
docker-compose logs --tail=100 inventory

# בדוק אם הפורט תפוס
netstat -ano | findstr :8000

# בנה מחדש
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### שגיאות migrations
```bash
# בדוק migrations
docker-compose exec inventory python manage.py showmigrations

# הרץ migrations
docker-compose exec inventory python manage.py migrate --fake-initial
```

### קבצים סטטיים לא נטענים
```bash
# אסוף קבצים
docker-compose exec inventory python manage.py collectstatic --noinput --clear
```

### אין גישה למערכת
```bash
# בדוק שהשרת פועל
docker-compose ps

# בדוק health
docker-compose exec inventory python manage.py check

# בדוק רשת
docker network inspect inventory_inventory_network
```

---

## 📦 ייצוא ושיתוף

### שמירת תמונה לקובץ
```bash
# שמור
docker save inventory_management:latest | gzip > inventory_image.tar.gz

# טען
gunzip -c inventory_image.tar.gz | docker load
```

### העלאה ל-Docker Hub
```bash
# התחבר
docker login

# תייג
docker tag inventory_management:latest yourusername/inventory:latest

# העלה
docker push yourusername/inventory:latest
```

### שיתוף עם Docker Hub
```bash
# על מכשיר אחר:
docker pull yourusername/inventory:latest
docker-compose up -d
```

---

## 🔄 עדכון המערכת

### עדכון לגרסה חדשה
```bash
# משוך שינויים
git pull

# בנה מחדש
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# הרץ migrations
docker-compose exec inventory python manage.py migrate
docker-compose exec inventory python manage.py collectstatic --noinput
```

---

## 📋 רשימת בדיקה לפרודקשן

לפני הפעלה בפרודקשן, ודא:

- [ ] ✅ DEBUG=False
- [ ] ✅ SECRET_KEY ייחודי וחזק
- [ ] ✅ ALLOWED_HOSTS מוגדר
- [ ] ✅ הגדרות Email פועלות
- [ ] ✅ גיבוי אוטומטי מופעל
- [ ] ✅ HTTPS/SSL מוגדר
- [ ] ✅ Firewall מוגדר
- [ ] ✅ Monitoring פועל
- [ ] ✅ כל התכונות נבדקו
- [ ] ✅ יש תוכנית שחזור אסון

---

## 📞 תמיכה וקישורים

### קישורים שימושיים:
- 📚 [מדריך Docker המלא](DOCKER_DEPLOYMENT.md)
- 📖 [תיעוד טכני](docs/TECHNICAL_DOCUMENTATION.md)
- 📘 [מדריך משתמש](docs/USER_MANUAL.md)
- 🚀 [הפעלה מהירה](QUICK_START.md)

### עזרה נוספת:
- Docker Docs: https://docs.docker.com
- Django Docs: https://docs.djangoproject.com
- GitHub Issues: פתח issue במאגר

---

## 📊 מידע טכני

### דרישות מערכת:
- **מעבד:** 2 ליבות (מומלץ 4)
- **זיכרון:** 2GB RAM (מומלץ 4GB)
- **דיסק:** 5GB פנויים (מומלץ 20GB)
- **מערכת הפעלה:** Windows 10/11, Linux, macOS

### גרסאות:
- Python: 3.10
- Django: 5.2+
- Docker: 20.10+
- Docker Compose: 2.0+

---

## 🎉 סיכום

**המערכת מוכנה לשימוש מיידי!**

1. הרץ: `.\docker-quick-start.ps1`
2. גש ל: http://localhost:8000
3. התחבר והתחל לעבוד!

**בהצלחה! 🚀**

