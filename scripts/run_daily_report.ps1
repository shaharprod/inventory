# סקריפט להרצת הדוח היומי
# קובץ זה ייקרא על ידי Task Scheduler

# מעבר לתיקיית הפרויקט
$ProjectPath = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectPath

# כתיבה ללוג
$LogFile = Join-Path $ProjectPath "logs\daily_report.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"[$Timestamp] Starting daily report..." | Out-File -Append $LogFile

try {
    # הפעלת הסביבה הווירטואלית
    $VenvPath = Join-Path $ProjectPath "venv\Scripts\Activate.ps1"

    if (Test-Path $VenvPath) {
        & $VenvPath
        "[$Timestamp] Virtual environment activated" | Out-File -Append $LogFile
    } else {
        "[$Timestamp] ERROR: Virtual environment not found at $VenvPath" | Out-File -Append $LogFile
        exit 1
    }

    # הרצת פקודת Django
    $Output = & python manage.py send_daily_report 2>&1
    "[$Timestamp] Command output: $Output" | Out-File -Append $LogFile

    if ($LASTEXITCODE -eq 0) {
        "[$Timestamp] Daily report sent successfully" | Out-File -Append $LogFile
    } else {
        "[$Timestamp] ERROR: Command failed with exit code $LASTEXITCODE" | Out-File -Append $LogFile
    }

} catch {
    "[$Timestamp] ERROR: $_" | Out-File -Append $LogFile
    exit 1
}

"[$Timestamp] Daily report task completed" | Out-File -Append $LogFile

