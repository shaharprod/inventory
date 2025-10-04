# סקריפט להפעלת שרת Django עם virtual environment

Write-Host "`n🚀 מפעיל את מערכת ניהול המלאי..." -ForegroundColor Cyan
Write-Host ("="*70) -ForegroundColor Gray

# הפעלת virtual environment
Write-Host "`n📦 מפעיל virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment הופעל בהצלחה" -ForegroundColor Green
} catch {
    Write-Host "❌ שגיאה בהפעלת virtual environment" -ForegroundColor Red
    Write-Host "פתרון: הרץ את הפקודה: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# בדיקת מערכת
Write-Host "`n🔍 בודק את המערכת..." -ForegroundColor Yellow
python manage.py check
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ יש בעיות במערכת. אנא תקן אותן לפני הפעלת השרת." -ForegroundColor Red
    exit 1
}
Write-Host "✅ המערכת תקינה" -ForegroundColor Green

# הצגת מידע
Write-Host "`n" -NoNewline
Write-Host ("="*70) -ForegroundColor Gray
Write-Host "`n📊 מידע על המערכת:" -ForegroundColor Cyan
Write-Host "   • שרת Django יופעל על: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   • לוח ניהול: http://127.0.0.1:8000/admin" -ForegroundColor White
Write-Host "   • למצב debug: DEBUG=True ב-settings.py" -ForegroundColor White
Write-Host "`n💡 טיפים:" -ForegroundColor Yellow
Write-Host "   • לעצירת השרת: לחץ Ctrl+C" -ForegroundColor White
Write-Host "   • לפתיחת דפדפן: Start-Process 'http://127.0.0.1:8000'" -ForegroundColor White
Write-Host "   • לצפייה בלוגים: הודעות יופיעו מטה" -ForegroundColor White
Write-Host "`n" -NoNewline
Write-Host ("="*70) -ForegroundColor Gray

# הפעלת השרת
Write-Host "`n🌐 מפעיל את השרת Django..." -ForegroundColor Green
Write-Host "⏳ השרת עובד... (Ctrl+C לעצירה)`n" -ForegroundColor Cyan

python manage.py runserver

