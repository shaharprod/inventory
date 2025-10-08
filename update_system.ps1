# סקריפט אוטומטי לעדכון מערכת המלאי - PowerShell
# Inventory System Auto-Update Script for PowerShell

Write-Host "🚀 מתחיל תהליך אוטומטי לעדכון מערכת המלאי..." -ForegroundColor Green

# בדיקת Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker מותקן" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker לא מותקן! אנא התקן Docker Desktop תחילה." -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

# בדיקת קונטיינר קיים
$containerExists = docker ps -a --format "table {{.Names}}" | Select-String "inventory-system"
if (-not $containerExists) {
    Write-Host "❌ קונטיינר inventory-system לא קיים!" -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "📦 גיבוי הגדרות מערכת..." -ForegroundColor Yellow
try {
    docker exec inventory-system python manage.py dumpdata inventory.SystemSettings > settings_backup.json
    Write-Host "✅ הגדרות נשמרו בהצלחה!" -ForegroundColor Green
} catch {
    Write-Host "❌ שגיאה בגיבוי הגדרות!" -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "🏗️ יצירת תמונה חדשה..." -ForegroundColor Yellow
try {
    docker build -t inventory-system-v4:latest .
    Write-Host "✅ תמונה חדשה נוצרה בהצלחה!" -ForegroundColor Green
} catch {
    Write-Host "❌ שגיאה ביצירת תמונה!" -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "🛑 עצירת קונטיינר ישן..." -ForegroundColor Yellow
docker stop inventory-system
docker rm inventory-system
Write-Host "✅ קונטיינר ישן נעצר!" -ForegroundColor Green

Write-Host "🚀 הפעלת תמונה חדשה..." -ForegroundColor Yellow
try {
    docker run -d -p 8000:8000 --name inventory-system inventory-system-v4:latest
    Write-Host "✅ קונטיינר חדש הופעל בהצלחה!" -ForegroundColor Green
} catch {
    Write-Host "❌ שגיאה בהפעלת קונטיינר חדש!" -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "🔄 שחזור הגדרות..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
try {
    docker exec inventory-system python manage.py loaddata settings_backup.json
    Write-Host "✅ הגדרות שוחזרו בהצלחה!" -ForegroundColor Green
} catch {
    Write-Host "❌ שגיאה בשחזור הגדרות!" -ForegroundColor Red
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "✅ בדיקת המערכת..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ המערכת עובדת בהצלחה!" -ForegroundColor Green
    } else {
        throw "Status code: $($response.StatusCode)"
    }
} catch {
    Write-Host "❌ המערכת לא עובדת!" -ForegroundColor Red
    Write-Host "📋 בדוק את הלוגים: docker logs inventory-system" -ForegroundColor Yellow
    Read-Host "לחץ Enter כדי לצאת"
    exit 1
}

Write-Host "🎉 המערכת עודכנה בהצלחה!" -ForegroundColor Green
Write-Host "📊 דשבורד: http://localhost:8000" -ForegroundColor Cyan
Write-Host "⚙️ הגדרות: http://localhost:8000/settings" -ForegroundColor Cyan
Write-Host "👥 Admin: http://localhost:8000/admin" -ForegroundColor Cyan
Read-Host "לחץ Enter כדי לצאת"
