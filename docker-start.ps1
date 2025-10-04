# סקריפט להפעלת מערכת ניהול מלאי ב-Docker
# ==============================================

Write-Host "`n🐳 " -NoNewline -ForegroundColor Cyan
Write-Host "מפעיל את מערכת ניהול המלאי ב-Docker..." -ForegroundColor White
Write-Host ""

# בדיקה אם Docker Desktop רץ
Write-Host "🔍 בודק אם Docker פעיל..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "   ✅ Docker פעיל!" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Docker לא פעיל!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   פתח את Docker Desktop ונסה שוב." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host ""

# בדיקה אם הקונטיינר כבר רץ
Write-Host "🔍 בודק סטטוס קונטיינר..." -ForegroundColor Yellow
$running = docker ps --filter "name=inventory_system" --format "{{.Names}}"

if ($running -eq "inventory_system") {
    Write-Host "   ℹ️  הקונטיינר כבר רץ!" -ForegroundColor Cyan
    Write-Host ""

    $choice = Read-Host "האם להפעיל מחדש? (y/n)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        Write-Host ""
        Write-Host "🔄 מפעיל מחדש..." -ForegroundColor Yellow
        docker-compose restart
    }
} else {
    Write-Host "   ▶️  מפעיל את הקונטיינר..." -ForegroundColor Green
    docker-compose up -d
}

Write-Host ""
Write-Host ("="*75) -ForegroundColor Cyan
Write-Host ""

# המתן שהשרת יהיה מוכן
Write-Host "⏳ ממתין שהשרת יהיה מוכן..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# בדיקת סטטוס סופית
$status = docker-compose ps --format json | ConvertFrom-Json
if ($status.State -eq "running") {
    Write-Host "   ✅ השרת רץ בהצלחה!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 גישה למערכת:" -ForegroundColor Yellow
    Write-Host "   http://localhost:8000" -ForegroundColor Cyan -BackgroundColor Blue
    Write-Host ""

    # שאלה אם לפתוח בדפדפן
    $open = Read-Host "האם לפתוח את הדפדפן? (y/n)"
    if ($open -eq "y" -or $open -eq "Y") {
        Start-Process "http://localhost:8000"
    }

    Write-Host ""
    Write-Host "📝 פקודות שימושיות:" -ForegroundColor Yellow
    Write-Host "   צפה בלוגים:       docker-compose logs -f" -ForegroundColor Cyan
    Write-Host "   עצור:             docker-compose down" -ForegroundColor Cyan
    Write-Host "   הפעל מחדש:       docker-compose restart" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "   ⚠️  בעיה בהפעלת השרת" -ForegroundColor Red
    Write-Host ""
    Write-Host "   צפה בלוגים לבדיקת שגיאות:" -ForegroundColor Yellow
    Write-Host "   docker-compose logs" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ("="*75) -ForegroundColor Cyan
Write-Host ""

