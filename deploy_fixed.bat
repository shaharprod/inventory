@echo off
echo ========================================
echo DEPLOYING FIXED VERSION
echo ========================================

echo.
echo 1. Stopping old versions...
gcloud app versions stop 20251007t221034 --quiet

echo.
echo 2. Deploying new version...
gcloud app deploy app.yaml --quiet

echo.
echo 3. Checking deployment status...
gcloud app versions list

echo.
echo 4. Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo DEPLOYMENT COMPLETED
echo ========================================
pause
