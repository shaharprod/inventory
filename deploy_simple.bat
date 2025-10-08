@echo off
echo ========================================
echo DEPLOYING SIMPLE VERSION
echo ========================================

echo.
echo Step 1: Deploying with simple config...
gcloud app deploy app_simple.yaml --quiet

echo.
echo Step 2: Checking deployment...
gcloud app versions list

echo.
echo Step 3: Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo SIMPLE DEPLOYMENT COMPLETED
echo ========================================
echo.
echo Website: https://my-claude-drive.uc.r.appspot.com
echo Login: admin / admin123
echo.
pause
