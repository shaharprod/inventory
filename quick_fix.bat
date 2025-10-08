@echo off
echo ========================================
echo QUICK FIX - DEPLOYING NEW VERSION
echo ========================================

echo.
echo Step 1: Deploying new version...
gcloud app deploy app.yaml --quiet

echo.
echo Step 2: Checking status...
gcloud app versions list

echo.
echo Step 3: Testing website...
curl -I https://my-claude-drive.uc.r.appspot.com

echo.
echo ========================================
echo QUICK FIX COMPLETED
echo ========================================
echo.
echo If still not working, try:
echo 1. Wait 2-3 minutes
echo 2. Refresh browser
echo 3. Clear browser cache
echo 4. Try incognito mode
echo.
pause
