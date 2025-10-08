#!/bin/bash
# סקריפט גיבוי אוטומטי למערכת המלאי
# Automated Backup Script for Inventory System

BACKUP_DIR="./backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_${DATE}"

echo "📦 מתחיל גיבוי מערכת המלאי..."

# יצירת תיקיית גיבוי
mkdir -p "$BACKUP_DIR"

# גיבוי הגדרות
echo "📋 גיבוי הגדרות מערכת..."
docker exec inventory-system python manage.py dumpdata inventory.SystemSettings > "${BACKUP_DIR}/settings_${DATE}.json"

# גיבוי מסד נתונים
echo "🗄️ גיבוי מסד נתונים..."
docker exec inventory-system python manage.py dumpdata > "${BACKUP_DIR}/database_${DATE}.json"

# גיבוי קבצי media
echo "🖼️ גיבוי קבצי media..."
docker cp inventory-system:/app/media "${BACKUP_DIR}/media_${DATE}"

# גיבוי קבצי גיבוי
echo "💾 גיבוי קבצי גיבוי..."
docker cp inventory-system:/app/backups "${BACKUP_DIR}/backups_${DATE}"

# יצירת ארכיון
echo "📦 יצירת ארכיון..."
cd "$BACKUP_DIR"
tar -czf "${BACKUP_NAME}.tar.gz" "settings_${DATE}.json" "database_${DATE}.json" "media_${DATE}" "backups_${DATE}"
cd ..

# ניקוי קבצים זמניים
echo "🧹 ניקוי קבצים זמניים..."
rm -rf "${BACKUP_DIR}/settings_${DATE}.json"
rm -rf "${BACKUP_DIR}/database_${DATE}.json"
rm -rf "${BACKUP_DIR}/media_${DATE}"
rm -rf "${BACKUP_DIR}/backups_${DATE}"

# מחיקת גיבויים ישנים (יותר מ-7 ימים)
echo "🗑️ מחיקת גיבויים ישנים..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

echo "✅ גיבוי הושלם בהצלחה!"
echo "📁 מיקום: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo "📊 גודל: $(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)"
