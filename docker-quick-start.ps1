# 🚀 הפעלה מהירה של מערכת המלאי ב-Docker

Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║    🚀 הפעלה מהירה - מערכת ניהול מלאי        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# בדיקת Docker
Write-Host "🔍 בודק Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "✅ Docker פועל" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker לא פועל! אנא הפעל את Docker Desktop" -ForegroundColor Red
    exit 1
}

Write-Host ""

# בדיקה אם יש תמונה קיימת
Write-Host "🔍 בודק תמונות קיימות..." -ForegroundColor Yellow
$imageExists = docker images | Select-String "inventory_management"

if (-not $imageExists) {
    Write-Host "⚠️  התמונה לא קיימת. בונה תמונה חדשה..." -ForegroundColor Yellow
    Write-Host ""
    docker-compose build

    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ הבניה נכשלה!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ התמונה קיימת" -ForegroundColor Green
}

Write-Host ""

# עצירת קונטיינרים ישנים
Write-Host "🧹 מנקה קונטיינרים ישנים..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null

Write-Host ""

# הפעלת המערכת
Write-Host "🚀 מפעיל את המערכת..." -ForegroundColor Cyan
Write-Host ""

docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ ההפעלה נכשלה!" -ForegroundColor Red
    Write-Host "🔍 בדוק לוגים עם: docker-compose logs" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "⏳ ממתין שהמערכת תהיה מוכנה..." -ForegroundColor Yellow

# המתן שהשרת יעלה
$maxWait = 30
$waited = 0
$ready = $false

while ($waited -lt $maxWait -and -not $ready) {
    Start-Sleep -Seconds 2
    $waited += 2

    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
        }
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host ""

if ($ready) {
    Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║         ✅ המערכת פועלת בהצלחה!              ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
} else {
    Write-Host "⚠️  המערכת עדיין עולה... זה יכול לקחת עוד כמה רגעים" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 כתובת המערכת: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 לוגים:          docker-compose logs -f" -ForegroundColor White
Write-Host "⏹️  עצירה:          docker-compose stop" -ForegroundColor White
Write-Host ""

# בדיקת סטטוס
Write-Host "📊 סטטוס קונטיינרים:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""

# הצע לפתוח בדפדפן
$openBrowser = Read-Host "האם לפתוח את המערכת בדפדפן? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y" -or $openBrowser -eq "") {
    Write-Host "🌐 פותח דפדפן..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
    Start-Process "http://localhost:8000"
}

Write-Host ""
Write-Host "🎉 המערכת מוכנה לשימוש!" -ForegroundColor Green
Write-Host ""

# הצע להציג לוגים
$showLogs = Read-Host "האם להציג לוגים בזמן אמת? (y/n)"
if ($showLogs -eq "y" -or $showLogs -eq "Y") {
    Write-Host ""
    Write-Host "📜 לוגים (לחץ Ctrl+C לעצירה):" -ForegroundColor Yellow
    Write-Host ""
    docker-compose logs -f
}

