# סקריפט ליצירת משימה מתוזמנת לשליחת דוח יומי בשעה 19:30
# הרץ כמנהל: Right-click -> Run as Administrator

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  📧 תזמון דוח יומי אוטומטי" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# הגדרות
$TaskName = "InventoryDailyReport"
$ScriptPath = "$PSScriptRoot\run_daily_report.ps1"
$TriggerTime = "19:30"
$Description = "שולח דוח יומי ממערכת ניהול המלאי בשעה 19:30"

# בדיקה אם המשימה כבר קיימת
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "⚠️  משימה קיימת '$TaskName' נמצאה" -ForegroundColor Yellow
    $Response = Read-Host "האם למחוק ולהחליף? (y/n)"
    if ($Response -eq 'y') {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ משימה ישנה נמחקה" -ForegroundColor Green
    } else {
        Write-Host "❌ ביטול" -ForegroundColor Red
        exit
    }
}

# יצירת המשימה המתוזמנת
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""
$Trigger = New-ScheduledTaskTrigger -Daily -At $TriggerTime
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# רישום המשימה
try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description $Description -Force
    Write-Host "`n✅ המשימה נוצרה בהצלחה!" -ForegroundColor Green
    Write-Host "📅 המשימה תרוץ כל יום בשעה $TriggerTime" -ForegroundColor Cyan
    Write-Host "`n🔍 לצפייה במשימה:" -ForegroundColor Yellow
    Write-Host "   Task Scheduler -> Task Scheduler Library -> $TaskName`n" -ForegroundColor Gray

    # הצגת פרטי המשימה
    Write-Host "`n📋 פרטי המשימה:" -ForegroundColor Cyan
    Write-Host "   שם: $TaskName"
    Write-Host "   זמן: $TriggerTime"
    Write-Host "   סקריפט: $ScriptPath"
    Write-Host "   תיאור: $Description`n"

    # שאלה אם להריץ עכשיו לבדיקה
    $RunNow = Read-Host "האם להריץ את הדוח עכשיו לבדיקה? (y/n)"
    if ($RunNow -eq 'y') {
        Write-Host "`n🚀 מריץ דוח...`n" -ForegroundColor Cyan
        & $ScriptPath
    }

} catch {
    Write-Host "`n❌ שגיאה ביצירת המשימה: $_" -ForegroundColor Red
    Write-Host "💡 ודא שהרצת את הסקריפט כמנהל (Run as Administrator)" -ForegroundColor Yellow
}

Write-Host "`n📝 הערות חשובות:" -ForegroundColor Yellow
Write-Host "   1. ודא שהגדרת את פרטי ה-SMTP ב-settings.py"
Write-Host "   2. שנה את EMAIL_HOST_USER ו-EMAIL_HOST_PASSWORD"
Write-Host "   3. שנה את DAILY_REPORT_EMAIL לכתובת המייל שלך"
Write-Host "   4. עבור Gmail, צור App Password במקום סיסמה רגילה`n"

Read-Host "לחץ Enter ליציאה"

