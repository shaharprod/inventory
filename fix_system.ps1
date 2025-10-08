Write-Host "🔧 מתחיל תיקון המערכת..." -ForegroundColor Green

Write-Host "📋 בדיקת gcloud..." -ForegroundColor Yellow
gcloud --version

Write-Host "📋 בדיקת פרויקט..." -ForegroundColor Yellow
gcloud config get-value project

Write-Host "📋 בדיקת סטטוס App Engine..." -ForegroundColor Yellow
gcloud app services list

Write-Host "📋 בדיקת גרסאות..." -ForegroundColor Yellow
gcloud app versions list

Write-Host "📋 בדיקת לוגים..." -ForegroundColor Yellow
gcloud app logs read --service=default --limit=10

Write-Host "📋 בדיקת נגישות..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://my-claude-drive.uc.r.appspot.com" -Method Head

Write-Host "✅ סיום בדיקות" -ForegroundColor Green
