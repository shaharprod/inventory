#!/bin/bash
# סקריפט ניטור מערכת המלאי
# System Monitoring Script for Inventory System

echo "📊 ניטור מערכת המלאי"
echo "========================"

# בדיקת סטטוס קונטיינר
echo "🐳 סטטוס קונטיינר:"
if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q "inventory-system"; then
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "inventory-system"
    echo "✅ קונטיינר פועל"
else
    echo "❌ קונטיינר לא פועל"
    exit 1
fi

echo ""

# בדיקת נגישות
echo "🌐 בדיקת נגישות:"
if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ המערכת נגישה"
    echo "🔗 כתובת: http://localhost:8000"
else
    echo "❌ המערכת לא נגישה"
fi

echo ""

# בדיקת לוגים אחרונים
echo "📋 לוגים אחרונים:"
docker logs --tail 10 inventory-system

echo ""

# בדיקת שימוש במשאבים
echo "💻 שימוש במשאבים:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" inventory-system

echo ""

# בדיקת בריאות המערכת
echo "🏥 בדיקת בריאות:"
if docker exec inventory-system python manage.py check > /dev/null 2>&1; then
    echo "✅ המערכת תקינה"
else
    echo "❌ בעיות במערכת"
    echo "📋 פרטים:"
    docker exec inventory-system python manage.py check
fi

echo ""

# בדיקת מסד נתונים
echo "🗄️ בדיקת מסד נתונים:"
if docker exec inventory-system python manage.py dbshell -c "SELECT COUNT(*) FROM inventory_product;" > /dev/null 2>&1; then
    PRODUCT_COUNT=$(docker exec inventory-system python manage.py shell -c "from inventory.models import Product; print(Product.objects.count())")
    echo "✅ מסד נתונים תקין"
    echo "📦 מספר מוצרים: $PRODUCT_COUNT"
else
    echo "❌ בעיות במסד נתונים"
fi

echo ""

# בדיקת קבצי media
echo "🖼️ בדיקת קבצי media:"
MEDIA_COUNT=$(docker exec inventory-system find /app/media -type f | wc -l)
echo "📁 מספר קבצים: $MEDIA_COUNT"

echo ""

# בדיקת גיבויים
echo "💾 בדיקת גיבויים:"
BACKUP_COUNT=$(docker exec inventory-system find /app/backups -type d -name "backup_*" | wc -l)
echo "📦 מספר גיבויים: $BACKUP_COUNT"

echo ""

# סיכום
echo "📊 סיכום ניטור:"
echo "========================"
echo "🐳 קונטיינר: $(docker ps --format '{{.Status}}' --filter name=inventory-system)"
echo "🌐 נגישות: $(curl -s http://localhost:8000 > /dev/null && echo '✅' || echo '❌')"
echo "🏥 בריאות: $(docker exec inventory-system python manage.py check > /dev/null 2>&1 && echo '✅' || echo '❌')"
echo "📦 מוצרים: $PRODUCT_COUNT"
echo "🖼️ קבצים: $MEDIA_COUNT"
echo "💾 גיבויים: $BACKUP_COUNT"

echo ""
echo "🎯 המערכת מוכנה לשימוש!"
