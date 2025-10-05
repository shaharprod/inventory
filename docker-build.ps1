# 🐳 סקריפט בניית Docker Image
# מערכת ניהול מלאי

Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🐳 בונה תמונת Docker - מערכת מלאי       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# בדיקת Docker
Write-Host "🔍 בודק התקנת Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker מותקן: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker לא מותקן! אנא התקן Docker Desktop" -ForegroundColor Red
    Write-Host "הורד מ: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose מותקן: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose לא מותקן!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# בחירת סוג בנייה
Write-Host "📋 בחר סוג בנייה:" -ForegroundColor Cyan
Write-Host "1. בנייה רגילה (מהירה)" -ForegroundColor White
Write-Host "2. בנייה מלאה ללא cache (איטית יותר, אבל מעודכנת)" -ForegroundColor White
Write-Host "3. בנייה והפעלה מיידית" -ForegroundColor White
Write-Host ""

$choice = Read-Host "הזן מספר (1-3)"

Write-Host ""
Write-Host "🏗️  מתחיל בניית התמונה..." -ForegroundColor Yellow
Write-Host ""

switch ($choice) {
    "1" {
        Write-Host "⚙️  בונה עם cache..." -ForegroundColor Cyan
        docker-compose build
    }
    "2" {
        Write-Host "⚙️  בונה ללא cache (ייקח יותר זמן)..." -ForegroundColor Cyan
        docker-compose build --no-cache
    }
    "3" {
        Write-Host "⚙️  בונה והופעל..." -ForegroundColor Cyan
        docker-compose up -d --build
    }
    default {
        Write-Host "❌ בחירה לא תקינה!" -ForegroundColor Red
        exit 1
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ הבניה נכשלה! בדוק את השגיאות למעלה." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║         ✅ הבניה הושלמה בהצלחה!              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# הצגת מידע על התמונה
Write-Host "📊 מידע על התמונה:" -ForegroundColor Cyan
docker images | Select-String "inventory"

Write-Host ""
Write-Host "📝 פקודות שימושיות:" -ForegroundColor Yellow
Write-Host "  הפעלה:          docker-compose up -d" -ForegroundColor White
Write-Host "  עצירה:          docker-compose down" -ForegroundColor White
Write-Host "  לוגים:          docker-compose logs -f" -ForegroundColor White
Write-Host "  סטטוס:          docker-compose ps" -ForegroundColor White
Write-Host ""

if ($choice -eq "3") {
    Write-Host "⏳ ממתין שהמערכת תעלה..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    Write-Host ""
    Write-Host "✅ המערכת פועלת!" -ForegroundColor Green
    Write-Host "🌐 גש לכתובת: http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""

    # שאל אם לפתוח בדפדפן
    $openBrowser = Read-Host "האם לפתוח בדפדפן? (y/n)"
    if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
        Start-Process "http://localhost:8000"
    }
} else {
    Write-Host "💡 להפעלת המערכת הרץ:" -ForegroundColor Cyan
    Write-Host "   docker-compose up -d" -ForegroundColor White
    Write-Host ""
}

Write-Host "🎉 סיימנו!" -ForegroundColor Green

