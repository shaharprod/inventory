@echo off
REM סקריפט אוטומטי לעדכון מערכת המלאי - Windows Batch
REM Inventory System Auto-Update Script for Windows

echo 🚀 מתחיל תהליך אוטומטי לעדכון מערכת המלאי...

REM בדיקת Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker לא מותקן! אנא התקן Docker Desktop תחילה.
    pause
    exit /b 1
)

REM בדיקת קונטיינר קיים
docker ps -a --format "table {{.Names}}" | findstr "inventory-system" >nul
if %errorlevel% neq 0 (
    echo ❌ קונטיינר inventory-system לא קיים!
    pause
    exit /b 1
)

echo 📦 גיבוי הגדרות מערכת...
docker exec inventory-system python manage.py dumpdata inventory.SystemSettings > settings_backup.json
if %errorlevel% neq 0 (
    echo ❌ שגיאה בגיבוי הגדרות!
    pause
    exit /b 1
)
echo ✅ הגדרות נשמרו בהצלחה!

echo 🏗️ יצירת תמונה חדשה...
docker build -t inventory-system-v4:latest .
if %errorlevel% neq 0 (
    echo ❌ שגיאה ביצירת תמונה!
    pause
    exit /b 1
)
echo ✅ תמונה חדשה נוצרה בהצלחה!

echo 🛑 עצירת קונטיינר ישן...
docker stop inventory-system
docker rm inventory-system
echo ✅ קונטיינר ישן נעצר!

echo 🚀 הפעלת תמונה חדשה...
docker run -d -p 8000:8000 --name inventory-system inventory-system-v4:latest
if %errorlevel% neq 0 (
    echo ❌ שגיאה בהפעלת קונטיינר חדש!
    pause
    exit /b 1
)
echo ✅ קונטיינר חדש הופעל בהצלחה!

echo 🔄 שחזור הגדרות...
timeout /t 10 /nobreak >nul
docker exec inventory-system python manage.py loaddata settings_backup.json
if %errorlevel% neq 0 (
    echo ❌ שגיאה בשחזור הגדרות!
    pause
    exit /b 1
)
echo ✅ הגדרות שוחזרו בהצלחה!

echo ✅ בדיקת המערכת...
timeout /t 5 /nobreak >nul
curl -s http://localhost:8000 >nul
if %errorlevel% neq 0 (
    echo ❌ המערכת לא עובדת!
    echo 📋 בדוק את הלוגים: docker logs inventory-system
    pause
    exit /b 1
)
echo ✅ המערכת עובדת בהצלחה!

echo 🎉 המערכת עודכנה בהצלחה!
echo 📊 דשבורד: http://localhost:8000
echo ⚙️ הגדרות: http://localhost:8000/settings
echo 👥 Admin: http://localhost:8000/admin
pause
