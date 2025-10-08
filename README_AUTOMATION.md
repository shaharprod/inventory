# 🤖 אוטומציה מלאה למערכת המלאי
# Full Automation for Inventory System

## 📋 תוכן עניינים
- [הקדמה](#הקדמה)
- [קבצי אוטומציה](#קבצי-אוטומציה)
- [הפעלה](#הפעלה)
- [פתרון בעיות](#פתרון-בעיות)
- [תכונות מתקדמות](#תכונות-מתקדמות)

## 🚀 הקדמה

מערכת אוטומציה מלאה לעדכון מערכת המלאי עם Docker. המערכת כוללת:
- ✅ גיבוי אוטומטי של הגדרות
- ✅ יצירת תמונה חדשה
- ✅ שחזור הגדרות
- ✅ בדיקת תקינות המערכת

## 📁 קבצי אוטומציה

### 1. Linux/Mac (Bash)
```bash
./update_system.sh
```
- **קובץ:** `update_system.sh`
- **פלטפורמה:** Linux, macOS, WSL
- **תכונות:** בדיקות שגיאות, הודעות צבעוניות

### 2. Windows (Batch)
```cmd
update_system.bat
```
- **קובץ:** `update_system.bat`
- **פלטפורמה:** Windows Command Prompt
- **תכונות:** הודעות בעברית, בדיקות שגיאות

### 3. Windows (PowerShell)
```powershell
.\update_system.ps1
```
- **קובץ:** `update_system.ps1`
- **פלטפורמה:** Windows PowerShell
- **תכונות:** צבעים, בדיקות מתקדמות

### 4. Docker Compose
```bash
docker-compose up -d
```
- **קובץ:** `docker-compose.yml`
- **פלטפורמה:** כל הפלטפורמות
- **תכונות:** Redis, Health Checks, Volumes

## 🎯 הפעלה

### Linux/Mac
```bash
# הרשאות הרצה
chmod +x update_system.sh

# הפעלה
./update_system.sh
```

### Windows Command Prompt
```cmd
# הפעלה ישירה
update_system.bat
```

### Windows PowerShell
```powershell
# הפעלה
.\update_system.ps1

# אם יש בעיית הרשאות
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Compose
```bash
# הפעלה
docker-compose up -d

# עצירה
docker-compose down

# לוגים
docker-compose logs -f
```

## 🔧 פתרון בעיות

### שגיאה: Docker לא מותקן
```bash
# התקנת Docker Desktop
# Windows: הורד מ-https://www.docker.com/products/docker-desktop
# Linux: sudo apt install docker.io
# Mac: brew install docker
```

### שגיאה: קונטיינר לא קיים
```bash
# יצירת קונטיינר ראשוני
docker run -d -p 8000:8000 --name inventory-system inventory-system-v3:latest
```

### שגיאה: פורט תפוס
```bash
# בדיקת פורטים תפוסים
netstat -an | findstr :8000

# עצירת תהליכים
docker stop inventory-system
```

### שגיאה: הרשאות PowerShell
```powershell
# פתרון בעיית הרשאות
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## ⚡ תכונות מתקדמות

### 1. גיבוי אוטומטי
```bash
# גיבוי הגדרות
docker exec inventory-system python manage.py dumpdata inventory.SystemSettings > settings_backup.json

# גיבוי מלא
docker exec inventory-system python manage.py dumpdata > full_backup.json
```

### 2. שחזור הגדרות
```bash
# שחזור הגדרות
docker exec inventory-system python manage.py loaddata settings_backup.json
```

### 3. בדיקת תקינות
```bash
# בדיקת המערכת
curl http://localhost:8000

# בדיקת לוגים
docker logs inventory-system
```

### 4. ניטור
```bash
# סטטוס קונטיינרים
docker ps

# שימוש במשאבים
docker stats inventory-system
```

## 📊 מעקב ביצועים

### 1. לוגים
```bash
# לוגים בזמן אמת
docker logs -f inventory-system

# לוגים אחרונים
docker logs --tail 100 inventory-system
```

### 2. סטטיסטיקות
```bash
# שימוש במשאבים
docker stats inventory-system

# מידע מפורט
docker inspect inventory-system
```

### 3. בריאות המערכת
```bash
# בדיקת בריאות
docker exec inventory-system python manage.py check

# בדיקת מסד נתונים
docker exec inventory-system python manage.py dbshell
```

## 🔄 עדכונים

### 1. עדכון קוד
```bash
# משיכת עדכונים
git pull origin main

# הפעלת אוטומציה
./update_system.sh
```

### 2. עדכון תמונה
```bash
# בניית תמונה חדשה
docker build -t inventory-system-v5:latest .

# עדכון docker-compose
# שנה את התמונה ב-docker-compose.yml
```

## 🛡️ אבטחה

### 1. משתני סביבה
```bash
# יצירת .env
echo "SECRET_KEY=your-secret-key" > .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
```

### 2. הרשאות
```bash
# הרשאות קבצים
chmod 600 .env
chmod 755 update_system.sh
```

### 3. גיבויים
```bash
# גיבוי יומי
0 2 * * * /path/to/backup_script.sh
```

## 📞 תמיכה

### 1. לוגים
```bash
# לוגים מפורטים
docker logs inventory-system 2>&1 | tee system.log
```

### 2. דיבוג
```bash
# כניסה לקונטיינר
docker exec -it inventory-system bash

# בדיקת קבצים
docker exec inventory-system ls -la /app
```

### 3. שחזור
```bash
# שחזור מגיבוי
docker exec inventory-system python manage.py loaddata full_backup.json
```

## 🎉 סיכום

מערכת האוטומציה מספקת:
- ✅ **עדכון אוטומטי** - ללא התערבות ידנית
- ✅ **גיבוי בטוח** - שמירת הגדרות
- ✅ **בדיקות אוטומטיות** - וידוא תקינות
- ✅ **תמיכה רב-פלטפורמת** - Windows, Linux, Mac
- ✅ **תיעוד מלא** - הוראות מפורטות

**המערכת מוכנה לשימוש!** 🚀
