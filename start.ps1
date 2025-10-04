# תסריט הפעלת מערכת ניהול מלאי ו-CRM
# הפעל קובץ זה כדי להפעיל את המערכת

Write-Host "
╔════════════════════════════════════════════════════════╗
║     מערכת ניהול מלאי ו-CRM - מפעיל את המערכת...      ║
╚════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# בדיקת Python
Write-Host "🔍 בודק התקנת Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python לא מותקן! הורד מ: https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "לחץ Enter לסגירה"
    exit 1
}

# בדיקת סביבה וירטואלית
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ סביבה וירטואלית לא נמצאה!" -ForegroundColor Red
    Write-Host "🔧 יוצר סביבה וירטואלית..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ סביבה וירטואלית נוצרה" -ForegroundColor Green
}

# הפעלת סביבה וירטואלית
Write-Host "🔧 מפעיל סביבה וירטואלית..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# בדיקת Django
Write-Host "🔍 בודק התקנת Django..." -ForegroundColor Yellow
$djangoInstalled = pip list | Select-String "Django"
if (-not $djangoInstalled) {
    Write-Host "❌ Django לא מותקן!" -ForegroundColor Red
    Write-Host "📦 מתקין תלויות..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ תלויות הותקנו" -ForegroundColor Green
} else {
    Write-Host "✅ Django מותקן" -ForegroundColor Green
}

# בדיקת מסד נתונים
if (-not (Test-Path "db.sqlite3")) {
    Write-Host "⚠️  מסד נתונים לא קיים, יוצר..." -ForegroundColor Yellow
    python manage.py migrate
    Write-Host "✅ מסד נתונים נוצר" -ForegroundColor Green

    Write-Host "
📝 האם ברצונך ליצור משתמש מנהל? (Y/N)" -ForegroundColor Cyan
    $createAdmin = Read-Host
    if ($createAdmin -eq "Y" -or $createAdmin -eq "y") {
        python manage.py createsuperuser
    }
}

# הפעלת שרת
Write-Host "
╔════════════════════════════════════════════════════════╗
║          🚀 מפעיל את השרת...                          ║
║                                                        ║
║  השרת יהיה זמין בכתובת: http://127.0.0.1:8000/       ║
║                                                        ║
║  לעצירת השרת: Ctrl+C                                  ║
╚════════════════════════════════════════════════════════╝
" -ForegroundColor Green

Start-Sleep -Seconds 2

# הרצת שרת
python manage.py runserver

# אם השרת נסגר
Write-Host "
השרת נסגר. להפעלה מחדש, הרץ שוב את start.ps1
" -ForegroundColor Yellow

