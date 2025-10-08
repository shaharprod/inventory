@echo off
echo ========================================
echo ULTRA MINIMAL DEPLOYMENT
echo ========================================

echo.
echo Step 1: Copying minimal Dockerfile...
copy Dockerfile.minimal Dockerfile

echo.
echo Step 2: Stopping all versions...
gcloud app versions stop 20251008t223116 --quiet
gcloud app versions stop 20251007t221343 --quiet
gcloud app versions stop 20251007t221034 --quiet

echo.
echo Step 3: Waiting 60 seconds...
timeout /t 60

echo.
echo Step 4: Deploying ultra minimal version...
gcloud app deploy app_minimal.yaml --quiet

echo.
echo Step 5: Checking status...
gcloud app versions list

echo.
echo Step 6: Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo ULTRA MINIMAL DEPLOYMENT COMPLETED
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
echo 5. Try from different network
echo.
pause
