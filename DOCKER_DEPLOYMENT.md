# 🐳 מדריך Docker - מערכת ניהול מלאי

## 📋 תוכן עניינים
1. [דרישות מקדימות](#דרישות-מקדימות)
2. [התקנה מהירה](#התקנה-מהירה)
3. [בניית תמונת Docker](#בניית-תמונת-docker)
4. [הפעלת המערכת](#הפעלת-המערכת)
5. [ניהול מתקדם](#ניהול-מתקדם)
6. [גיבוי ושחזור](#גיבוי-ושחזור)
7. [פתרון בעיות](#פתרון-בעיות)

---

## 🔧 דרישות מקדימות

### Windows
```powershell
# התקן Docker Desktop
winget install Docker.DockerDesktop
# או הורד מ: https://www.docker.com/products/docker-desktop/

# אמת התקנה
docker --version
docker-compose --version
```

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# אמת התקנה
docker --version
docker-compose --version
```

---

## ⚡ התקנה מהירה

### שלב 1: הורד את הקוד
```bash
git clone <repository-url>
cd inventory
```

### שלב 2: בנה והפעל
```bash
# בנייה והפעלה ראשונית
docker-compose up -d --build

# המתן שהמערכת תעלה (כ-30 שניות)
docker-compose logs -f inventory
```

### שלב 3: גש למערכת
פתח דפדפן: http://localhost:8000

---

## 🏗️ בניית תמונת Docker

### בנייה בסיסית
```bash
# בניית תמונה
docker build -t inventory_management:latest .

# הצגת תמונות
docker images | grep inventory
```

### בנייה עם פרמטרים
```bash
# בנייה ללא שימוש ב-cache
docker build --no-cache -t inventory_management:latest .

# בנייה עם platform ספציפי
docker build --platform linux/amd64 -t inventory_management:latest .
```

### בנייה דרך docker-compose
```bash
# בנייה
docker-compose build

# בנייה ללא cache
docker-compose build --no-cache
```

---

## 🚀 הפעלת המערכת

### הפעלה בסיסית
```bash
# הפעלה ברקע
docker-compose up -d

# הפעלה עם לוגים
docker-compose up

# הפעלה של שירות ספציפי
docker-compose up inventory
```

### בדיקת סטטוס
```bash
# בדיקת קונטיינרים
docker-compose ps

# בדיקת לוגים
docker-compose logs -f

# בדיקת שירות ספציפי
docker-compose logs -f inventory
```

### עצירה והסרה
```bash
# עצירה
docker-compose stop

# עצירה והסרה (שומר volumes)
docker-compose down

# עצירה והסרה (מוחק גם volumes)
docker-compose down -v
```

---

## 🔧 ניהול מתקדם

### כניסה לקונטיינר
```bash
# כניסה לשורת פקודה
docker-compose exec inventory sh

# הרצת פקודת Django
docker-compose exec inventory python manage.py shell

# הרצת migrations
docker-compose exec inventory python manage.py migrate

# יצירת superuser
docker-compose exec inventory python manage.py createsuperuser
```

### הרצת פקודות ניהול
```bash
# יצירת נתוני דמו
docker-compose exec inventory python manage.py loaddata demo_data.json

# ייצוא נתונים
docker-compose exec inventory python manage.py dumpdata > backup.json

# ניקוי לוגים
docker-compose exec inventory python manage.py cleanup_logs

# יצירת גיבוי
docker-compose exec inventory python manage.py backup_data
```

### צפייה בלוגים
```bash
# כל הלוגים
docker-compose logs -f

# 100 שורות אחרונות
docker-compose logs --tail=100

# לוגים מהשעה האחרונה
docker-compose logs --since 1h

# לוגים של שירות ספציפי
docker-compose logs -f inventory
```

### ניטור משאבים
```bash
# סטטיסטיקות בזמן אמת
docker stats inventory_system

# שימוש בדיסק
docker system df

# ניקוי קבצים ישנים
docker system prune -a
```

---

## 💾 גיבוי ושחזור

### גיבוי אוטומטי

#### 1. גיבוי נתונים דרך המערכת
```bash
# כניסה למערכת בדפדפן
http://localhost:8000/dashboard/

# לחץ על "Create Backup Now"
```

#### 2. גיבוי ידני של Volumes
```bash
# גיבוי DB
docker-compose exec inventory python manage.py dumpdata > backup_$(date +%Y%m%d).json

# גיבוי כל ה-volumes
docker run --rm \
  -v inventory_db_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/db_backup_$(date +%Y%m%d).tar.gz /data
```

#### 3. גיבוי מלא של המערכת
```bash
# עצור את המערכת
docker-compose down

# גבה את כל התיקיות
tar czf inventory_full_backup_$(date +%Y%m%d).tar.gz \
  db.sqlite3 media/ logs/ backups/

# הפעל מחדש
docker-compose up -d
```

### שחזור נתונים

#### 1. שחזור דרך המערכת
```bash
# כניסה למערכת בדפדפן
http://localhost:8000/dashboard/

# לחץ על "Restore Backup"
# בחר את הגיבוי הרצוי
```

#### 2. שחזור ידני
```bash
# עצור את המערכת
docker-compose down

# שחזר את הקבצים
tar xzf inventory_full_backup_YYYYMMDD.tar.gz

# הפעל מחדש
docker-compose up -d
```

---

## 🔐 אבטחה והגדרות

### הגדרת משתני סביבה
```bash
# העתק את קובץ הדוגמה
cp env.example .env

# ערוך את הקובץ
nano .env
```

### הגדרות חשובות:
```env
DEBUG=False
SECRET_KEY=your-unique-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

### הרצת collectstatic
```bash
docker-compose exec inventory python manage.py collectstatic --noinput
```

---

## 🌐 פרסום לאינטרנט

### 1. שימוש ב-Nginx (מומלץ)
```yaml
# הסר # מהשירות nginx ב-docker-compose.yml

# צור nginx.conf:
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream django {
        server inventory:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location /static/ {
            alias /app/static/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

# הפעל מחדש
docker-compose up -d
```

### 2. פתיחת פורטים ברשת מקומית
```bash
# Windows Firewall
netsh advfirewall firewall add rule name="Django Inventory" dir=in action=allow protocol=TCP localport=8000

# גש מכל מכשיר ברשת
http://<YOUR-LOCAL-IP>:8000
```

### 3. שימוש ב-ngrok (זמני)
```bash
# התקן ngrok
winget install ngrok

# הפעל tunnel
ngrok http 8000
```

---

## 📊 ניטור וביצועים

### Health Check
```bash
# בדוק בריאות המערכת
docker-compose exec inventory python manage.py check --deploy

# בדוק migrations
docker-compose exec inventory python manage.py showmigrations
```

### מעקב אחר ביצועים
```bash
# שימוש במשאבים
docker stats inventory_system

# כמות בקשות
docker-compose logs inventory | grep "GET\|POST" | wc -l
```

---

## ❌ פתרון בעיות

### הקונטיינר לא עולה
```bash
# בדוק לוגים מפורטים
docker-compose logs --tail=100 inventory

# בדוק אם הפורט תפוס
netstat -ano | findstr :8000

# נסה לבנות מחדש
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### שגיאות בסיס נתונים
```bash
# בדוק migrations
docker-compose exec inventory python manage.py showmigrations

# הרץ migrations
docker-compose exec inventory python manage.py migrate

# אפס DB (זהירות!)
docker-compose down -v
docker-compose up -d
docker-compose exec inventory python manage.py migrate
docker-compose exec inventory python manage.py createsuperuser
```

### בעיות עם קבצים סטטיים
```bash
# אסוף קבצים סטטיים
docker-compose exec inventory python manage.py collectstatic --noinput --clear

# בדוק הרשאות
docker-compose exec inventory ls -la /app/static
```

### בעיות זיכרון
```bash
# הגדל זיכרון לקונטיינר
# הוסף ל-docker-compose.yml תחת inventory:
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 512M
```

### ניקוי מערכת
```bash
# נקה containers ישנים
docker container prune -f

# נקה images ישנים
docker image prune -a -f

# נקה volumes לא בשימוש
docker volume prune -f

# נקה הכל
docker system prune -a --volumes -f
```

---

## 📦 ייצוא ושיתוף תמונה

### שמירת תמונה לקובץ
```bash
# שמור תמונה
docker save inventory_management:latest -o inventory_image.tar

# או דחוס
docker save inventory_management:latest | gzip > inventory_image.tar.gz
```

### טעינת תמונה ממכשיר אחר
```bash
# טען תמונה
docker load -i inventory_image.tar

# או מקובץ דחוס
gunzip -c inventory_image.tar.gz | docker load

# הפעל
docker-compose up -d
```

### העלאה ל-Docker Hub (אופציונלי)
```bash
# התחבר
docker login

# תייג את התמונה
docker tag inventory_management:latest yourusername/inventory:latest

# העלה
docker push yourusername/inventory:latest
```

---

## 🔄 עדכון המערכת

### עדכון גרסה חדשה
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

## 📞 תמיכה

### מידע שימושי לאיתור תקלות
```bash
# גרסאות
docker --version
docker-compose --version
python --version

# מידע על התמונה
docker inspect inventory_management:latest

# מידע על הקונטיינר
docker inspect inventory_system

# לוגים מלאים
docker-compose logs > full_logs.txt
```

---

## ✅ רשימת בדיקות (Checklist)

לפני הפעלה בפרודקשן:
- [ ] DEBUG=False ב-.env
- [ ] SECRET_KEY ייחודי
- [ ] ALLOWED_HOSTS מוגדר נכון
- [ ] הגדרות Email פועלות
- [ ] גיבוי אוטומטי מוגדר
- [ ] SSL/HTTPS מוגדר (nginx)
- [ ] Firewall מוגדר
- [ ] Monitoring מופעל
- [ ] נבדקו כל התכונות

---

**🎉 המערכת מוכנה לשימוש!**

לשאלות ותמיכה: פתח issue ב-GitHub או צור קשר עם המפתח.

