@echo off
echo ========================================
echo DEPLOYING MINIMAL VERSION
echo ========================================

echo.
echo Step 1: Stopping all versions...
gcloud app versions stop 20251008t223116 --quiet
gcloud app versions stop 20251007t221343 --quiet
gcloud app versions stop 20251007t221034 --quiet

echo.
echo Step 2: Waiting 60 seconds...
timeout /t 60

echo.
echo Step 3: Deploying minimal version...
gcloud app deploy app_minimal.yaml --quiet

echo.
echo Step 4: Checking status...
gcloud app versions list

echo.
echo Step 5: Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo MINIMAL DEPLOYMENT COMPLETED
echo ========================================
echo.
echo Website: https://my-claude-drive.uc.r.appspot.com
echo Login: admin / admin123
echo.
echo If still not working:
echo 1. Wait 10 minutes
echo 2. Try different browser
echo 3. Clear cache
echo 4. Try incognito mode
echo.
pause
