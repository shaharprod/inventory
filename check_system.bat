@echo off
echo ========================================
echo SYSTEM DIAGNOSTICS
echo ========================================

echo.
echo 1. Checking gcloud version...
gcloud --version

echo.
echo 2. Checking current project...
gcloud config get-value project

echo.
echo 3. Checking App Engine services...
gcloud app services list

echo.
echo 4. Checking App Engine versions...
gcloud app versions list

echo.
echo 5. Checking recent logs...
gcloud app logs read --service=default --limit=5

echo.
echo 6. Testing website accessibility...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo DIAGNOSTICS COMPLETED
echo ========================================
pause
