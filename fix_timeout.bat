@echo off
echo ========================================
echo FIXING TIMEOUT ISSUE
echo ========================================

echo.
echo Step 1: Stopping all old versions...
gcloud app versions stop 20251008t223116 --quiet
gcloud app versions stop 20251007t221343 --quiet
gcloud app versions stop 20251007t221034 --quiet

echo.
echo Step 2: Waiting 30 seconds...
timeout /t 30

echo.
echo Step 3: Deploying with minimal resources...
gcloud app deploy app_simple.yaml --quiet

echo.
echo Step 4: Checking status...
gcloud app versions list

echo.
echo ========================================
echo TIMEOUT FIX COMPLETED
echo ========================================
echo.
echo If still not working, try:
echo 1. Wait 5 minutes
echo 2. Try different browser
echo 3. Clear cache
echo.
pause
