# תסריט גיבוי אוטומטי למערכת ניהול מלאי
# ניתן להפעיל דרך Windows Task Scheduler

# הגדרות
$ProjectPath = "C:\Users\User\Downloads\inventory"
$VenvPath = "$ProjectPath\venv\Scripts\python.exe"
$ManagePy = "$ProjectPath\manage.py"
$LogFile = "$ProjectPath\logs\backup_log.txt"

# יצירת תיקיית לוגים אם לא קיימת
$LogDir = "$ProjectPath\logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# כתיבת לוג
function Write-Log {
    param($Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp - $Message" | Add-Content -Path $LogFile
    Write-Host $Message
}

Write-Log "========================================="
Write-Log "מתחיל גיבוי אוטומטי"
Write-Log "========================================="

# מעבר לתיקיית הפרויקט
Set-Location $ProjectPath

try {
    # הרצת פקודת גיבוי
    Write-Log "מבצע גיבוי..."
    & $VenvPath $ManagePy backup_database --output-dir backups

    if ($LASTEXITCODE -eq 0) {
        Write-Log "✅ הגיבוי הושלם בהצלחה"
    } else {
        Write-Log "❌ הגיבוי נכשל עם קוד שגיאה: $LASTEXITCODE"
        exit 1
    }

    # בדיקת מספר הגיבויים
    $BackupCount = (Get-ChildItem -Path "$ProjectPath\backups" -Directory -Filter "backup_*").Count
    Write-Log "📦 סה`"כ גיבויים: $BackupCount"

} catch {
    Write-Log "❌ שגיאה: $($_.Exception.Message)"
    exit 1
}

Write-Log "========================================="
Write-Log "הגיבוי הושלם"
Write-Log "========================================="

