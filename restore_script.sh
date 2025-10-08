#!/bin/bash
# סקריפט שחזור מערכת המלאי
# Restore Script for Inventory System

if [ $# -eq 0 ]; then
    echo "❌ שימוש: $0 <backup_file.tar.gz>"
    echo "📋 דוגמה: $0 backup_20250107_193000.tar.gz"
    exit 1
fi

BACKUP_FILE="$1"
BACKUP_DIR="./backups"
TEMP_DIR="./temp_restore"

if [ ! -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    echo "❌ קובץ גיבוי לא נמצא: ${BACKUP_DIR}/${BACKUP_FILE}"
    exit 1
fi

echo "🔄 מתחיל שחזור מערכת המלאי..."

# עצירת קונטיינר נוכחי
echo "🛑 עצירת קונטיינר נוכחי..."
docker stop inventory-system 2>/dev/null || true
docker rm inventory-system 2>/dev/null || true

# יצירת תיקייה זמנית
echo "📁 יצירת תיקייה זמנית..."
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

# חילוץ ארכיון
echo "📦 חילוץ ארכיון..."
tar -xzf "../${BACKUP_DIR}/${BACKUP_FILE}"

# הפעלת קונטיינר חדש
echo "🚀 הפעלת קונטיינר חדש..."
cd ..
docker run -d -p 8000:8000 --name inventory-system inventory-system-v4:latest

# המתן שהמערכת תעלה
echo "⏳ ממתין למערכת לעלות..."
sleep 15

# שחזור הגדרות
echo "⚙️ שחזור הגדרות..."
if [ -f "${TEMP_DIR}/settings_"*.json ]; then
    docker cp "${TEMP_DIR}/settings_"*.json inventory-system:/app/settings_restore.json
    docker exec inventory-system python manage.py loaddata settings_restore.json
    echo "✅ הגדרות שוחזרו!"
else
    echo "⚠️ קובץ הגדרות לא נמצא"
fi

# שחזור מסד נתונים
echo "🗄️ שחזור מסד נתונים..."
if [ -f "${TEMP_DIR}/database_"*.json ]; then
    docker cp "${TEMP_DIR}/database_"*.json inventory-system:/app/database_restore.json
    docker exec inventory-system python manage.py loaddata database_restore.json
    echo "✅ מסד נתונים שוחזר!"
else
    echo "⚠️ קובץ מסד נתונים לא נמצא"
fi

# שחזור קבצי media
echo "🖼️ שחזור קבצי media..."
if [ -d "${TEMP_DIR}/media_"* ]; then
    docker cp "${TEMP_DIR}/media_"*/. inventory-system:/app/media/
    echo "✅ קבצי media שוחזרו!"
else
    echo "⚠️ תיקיית media לא נמצאה"
fi

# שחזור קבצי גיבוי
echo "💾 שחזור קבצי גיבוי..."
if [ -d "${TEMP_DIR}/backups_"* ]; then
    docker cp "${TEMP_DIR}/backups_"*/. inventory-system:/app/backups/
    echo "✅ קבצי גיבוי שוחזרו!"
else
    echo "⚠️ תיקיית גיבויים לא נמצאה"
fi

# ניקוי קבצים זמניים
echo "🧹 ניקוי קבצים זמניים..."
rm -rf "$TEMP_DIR"

# בדיקת המערכת
echo "✅ בדיקת המערכת..."
sleep 5
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ המערכת עובדת בהצלחה!"
    echo "🌐 גש ל: http://localhost:8000"
else
    echo "❌ המערכת לא עובדת!"
    echo "📋 בדוק את הלוגים: docker logs inventory-system"
fi

echo "🎉 שחזור הושלם!"
