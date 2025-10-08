#!/bin/bash
# סקריפט אוטומטי לעדכון מערכת המלאי
# Inventory System Auto-Update Script

echo "🚀 מתחיל תהליך אוטומטי לעדכון מערכת המלאי..."

# בדיקת Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker לא מותקן! אנא התקן Docker תחילה."
    exit 1
fi

# בדיקת קונטיינר קיים
if ! docker ps -a --format "table {{.Names}}" | grep -q "inventory-system"; then
    echo "❌ קונטיינר inventory-system לא קיים!"
    exit 1
fi

echo "📦 גיבוי הגדרות מערכת..."
if docker exec inventory-system python manage.py dumpdata inventory.SystemSettings > settings_backup.json; then
    echo "✅ הגדרות נשמרו בהצלחה!"
else
    echo "❌ שגיאה בגיבוי הגדרות!"
    exit 1
fi

echo "🏗️ יצירת תמונה חדשה..."
if docker build -t inventory-system-v4:latest .; then
    echo "✅ תמונה חדשה נוצרה בהצלחה!"
else
    echo "❌ שגיאה ביצירת תמונה!"
    exit 1
fi

echo "🛑 עצירת קונטיינר ישן..."
docker stop inventory-system
docker rm inventory-system
echo "✅ קונטיינר ישן נעצר!"

echo "🚀 הפעלת תמונה חדשה..."
if docker run -d -p 8000:8000 --name inventory-system inventory-system-v4:latest; then
    echo "✅ קונטיינר חדש הופעל בהצלחה!"
else
    echo "❌ שגיאה בהפעלת קונטיינר חדש!"
    exit 1
fi

echo "🔄 שחזור הגדרות..."
sleep 10  # המתן שהמערכת תעלה
if docker exec inventory-system python manage.py loaddata settings_backup.json; then
    echo "✅ הגדרות שוחזרו בהצלחה!"
else
    echo "❌ שגיאה בשחזור הגדרות!"
    exit 1
fi

echo "✅ בדיקת המערכת..."
sleep 5
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ המערכת עובדת בהצלחה!"
    echo "🌐 גש ל: http://localhost:8000"
else
    echo "❌ המערכת לא עובדת!"
    echo "📋 בדוק את הלוגים: docker logs inventory-system"
    exit 1
fi

echo "🎉 המערכת עודכנה בהצלחה!"
echo "📊 דשבורד: http://localhost:8000"
echo "⚙️ הגדרות: http://localhost:8000/settings"
echo "👥 Admin: http://localhost:8000/admin"
