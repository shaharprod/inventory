# סקריפט לעצירת מערכת ניהול מלאי ב-Docker
# ============================================

Write-Host "`n🛑 " -NoNewline -ForegroundColor Red
Write-Host "עוצר את מערכת ניהול המלאי..." -ForegroundColor White
Write-Host ""

# בדיקה אם הקונטיינר רץ
$running = docker ps --filter "name=inventory_system" --format "{{.Names}}"

if ($running -eq "inventory_system") {
    Write-Host "🔍 קונטיינר פעיל - עוצר..." -ForegroundColor Yellow
    Write-Host ""

    docker-compose down

    Write-Host ""
    Write-Host "✅ הקונטיינר נעצר בהצלחה!" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 הנתונים נשמרו ב:" -ForegroundColor Cyan
    Write-Host "   • db.sqlite3" -ForegroundColor Gray
    Write-Host "   • media/" -ForegroundColor Gray
    Write-Host "   • logs/" -ForegroundColor Gray
    Write-Host "   • backups/" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "ℹ️  הקונטיינר לא פעיל" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ("="*75) -ForegroundColor Cyan
Write-Host ""

