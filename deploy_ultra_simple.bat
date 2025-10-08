@echo off
echo ========================================
echo ULTRA SIMPLE DEPLOYMENT
echo ========================================

echo.
echo Step 1: Copying simple Dockerfile...
copy Dockerfile.simple Dockerfile

echo.
echo Step 2: Deploying ultra simple version...
gcloud app deploy app_simple.yaml --quiet

echo.
echo Step 3: Checking status...
gcloud app versions list

echo.
echo Step 4: Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo ULTRA SIMPLE DEPLOYMENT COMPLETED
echo ========================================
echo.
echo Website: https://my-claude-drive.uc.r.appspot.com
echo Login: admin / admin123
echo.
echo If still not working:
echo 1. Wait 5 minutes
echo 2. Try different browser
echo 3. Clear cache
echo.
pause
